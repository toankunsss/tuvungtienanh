#!/usr/bin/env python3
"""Generate US and UK pronunciation audio (MP3) for every word in data/.

TTS engine: Kokoro-82M (Apache-2.0) through `kokoro-onnx`.
    US voice: af_heart   UK voice: bf_emma

For each word the engine's own phonemisation is compared with the IPA stored
in the dataset. If they agree, the plain text is spoken (most natural). If
they disagree (heteronyms such as "live" v., acronyms, rare words), the
dataset IPA is converted to Kokoro phonemes and spoken instead, so the audio
always matches the transcription shown to learners.

Setup (once):
    pip install kokoro-onnx soundfile
    # model files from https://github.com/thewh1teagle/kokoro-onnx/releases (model-files-v1.0)
    #   kokoro-v1.0.onnx, voices-v1.0.bin
    # ffmpeg must be on PATH

Usage:
    python3 scripts/make_audio.py --model DIR [--force] [--only WORD ...] [--check]

    --check   only compare phonemes and print mismatches; no audio written
"""
import argparse
import difflib
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
AUDIO = ROOT / "audio"
VOICES = {"us": ("af_heart", "en-us"), "uk": ("bf_emma", "en-gb")}
SPEED = 0.9
VOWELS = set("aeiouæɑɒɔəɚɛɜɝɪʊʌᵻɐ")


def slugify(word: str) -> str:
    s = unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "word"


def spoken_text(word: str) -> str:
    text = word.replace("...", " ").replace("…", " ")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([?!.,])", r"\1", text)
    return text


def to_kokoro(ipa: str, accent: str, question: bool) -> str:
    """Dataset IPA (/.../) -> Kokoro phoneme string."""
    s = ipa.strip("/").replace("...", " ").replace(".", "")
    s = s.replace("(r)", "" if accent == "uk" else "r")
    if accent == "us":
        s = s.replace("ɝː", "ɜː").replace("ɝ", "ɜː")
    s = s.replace("r", "ɹ")
    s = re.sub(r"e(?![ɪə])", "ɛ", s)
    if accent == "uk":
        s = s.replace("æ", "a")
    tokens = s.split()
    out = []
    for tok in tokens:
        # Kokoro puts the stress mark right before the vowel, not the syllable
        chars, pending, res = list(tok), "", []
        for ch in chars:
            if ch in "ˈˌ":
                pending = ch
                continue
            if pending and ch in VOWELS:
                res.append(pending)
                pending = ""
            res.append(ch)
        tok = "".join(res)
        if len(tokens) == 1 and "ˈ" not in tok:
            i = next((i for i, c in enumerate(tok) if c in VOWELS), 0)
            tok = tok[:i] + "ˈ" + tok[i:]
        out.append(tok)
    return " ".join(out) + ("?" if question else "")


def skeleton(ph: str) -> str:
    s = ph.strip("/").replace("(r)", "").replace("...", "")
    for a, b in (("ˈ", ""), ("ˌ", ""), ("ː", ""), ("ɾ", "t"), ("ɹ", "r"), ("ᵻ", "ɪ"), ("ɐ", "ə"),
                 ("ɝ", "ɜr"), ("ɚ", "ər"), ("ɛ", "e"), ("aɪ", "AI"), ("aʊ", "AU"),
                 ("a", "æ"), ("AI", "aɪ"), ("AU", "aʊ"), ("ɔ", "ɑ"), ("ɒ", "ɑ"),
                 ("oʊ", "əʊ"), ("ʌ", "ə"), ("i", "ɪ"), ("u", "ʊ"), (" ", ""),
                 ("?", ""), ("ɜr", "ɜ")):
        s = s.replace(a, b)
    return s


def stressed_vowel_index(ph: str) -> int | None:
    """Index (among vowel letters) of the first primary-stressed vowel."""
    s = ph.strip("/")
    count, primed = 0, False
    for ch in s:
        if ch == "ˈ":
            primed = True
        elif ch in VOWELS:
            if primed:
                return count
            count += 1
    return None


def agrees(engine: str, ours: str, multiword: bool) -> bool:
    if difflib.SequenceMatcher(None, skeleton(engine), skeleton(ours)).ratio() < 0.86:
        return False
    if not multiword:
        a, b = stressed_vowel_index(engine), stressed_vowel_index(ours)
        n_syll = sum(c in VOWELS for c in skeleton(ours))
        if n_syll > 1 and a is not None and b is not None and a != b:
            return False
    return True


def collect() -> dict:
    """slug -> {word, ipa_uk, ipa_us}; the same word with a different IPA gets a pos suffix."""
    entries: dict[str, dict] = {}
    for path in sorted(DATA.glob("grade-*.json")):
        for unit in json.loads(path.read_text(encoding="utf-8"))["units"]:
            for w in unit["words"]:
                slug = slugify(w["word"])
                cur = entries.get(slug)
                if cur and (cur["ipa_uk"], cur["ipa_us"]) != (w["ipa_uk"], w["ipa_us"]) \
                        and cur["word"] == w["word"]:
                    slug = f"{slug}-{slugify(w['pos'])}"
                    cur = entries.get(slug)
                if cur is None:
                    entries[slug] = {"word": w["word"], "ipa_uk": w["ipa_uk"], "ipa_us": w["ipa_us"]}
    return entries


def slug_for(entries: dict, w: dict) -> str:
    base = slugify(w["word"])
    for slug in (base, f"{base}-{slugify(w['pos'])}"):
        e = entries.get(slug)
        if e and (e["ipa_uk"], e["ipa_us"]) == (w["ipa_uk"], w["ipa_us"]):
            return slug
    raise KeyError(w["word"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="folder with kokoro-v1.0.onnx and voices-v1.0.bin")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()

    from kokoro_onnx import Kokoro
    import soundfile as sf

    model = Path(args.model)
    kokoro = Kokoro(str(model / "kokoro-v1.0.onnx"), str(model / "voices-v1.0.bin"))
    entries = collect()
    manifest_path = AUDIO / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}

    todo = [s for s, e in entries.items() if not args.only or e["word"] in args.only]
    mismatches = []
    with tempfile.TemporaryDirectory() as tmp:
        for n, slug in enumerate(todo, 1):
            e = entries[slug]
            text = spoken_text(e["word"])
            multi = len(text.split()) > 1
            info = {"word": e["word"]}
            for accent, (voice, lang) in VOICES.items():
                ours = e[f"ipa_{accent}"]
                engine = kokoro.tokenizer.phonemize(text, lang)
                if agrees(engine, ours, multi):
                    mode, phonemes = "text", engine
                else:
                    mode, phonemes = "ipa", to_kokoro(ours, accent, text.endswith("?"))
                    mismatches.append((accent, e["word"], ours, engine, phonemes))
                info[accent] = {"mode": mode, "phonemes": phonemes, "file": f"{accent}/{slug}.mp3"}
                out = AUDIO / accent / f"{slug}.mp3"
                if args.check or (out.exists() and not args.force):
                    continue
                out.parent.mkdir(parents=True, exist_ok=True)
                samples, sr = kokoro.create(phonemes, voice=voice, speed=SPEED, lang=lang, is_phonemes=True)
                wav = Path(tmp) / "a.wav"
                sf.write(wav, samples, sr)
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-ac", "1",
                                "-ar", "24000", "-b:a", "48k", str(out)], check=True)
            manifest[slug] = info
            if n % 100 == 0:
                print(f"{n}/{len(todo)}", flush=True)

    for m in mismatches:
        print("MISMATCH %s %-24s data %-26s engine %-24s -> %s" % m)
    print(f"{len(mismatches)} mismatches (spoken from dataset IPA)")
    if args.check:
        return 0

    AUDIO.mkdir(exist_ok=True)
    manifest_path.write_text(json.dumps(dict(sorted(manifest.items())), ensure_ascii=False, indent=1) + "\n",
                             encoding="utf-8")
    # link audio files into the data
    for path in sorted(DATA.glob("grade-*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        for unit in doc["units"]:
            new = []
            for w in unit["words"]:
                slug = slug_for(entries, w)
                nw = {k: w[k] for k in ("word", "pos", "ipa_uk", "ipa_us")}
                nw["audio_uk"] = f"audio/uk/{slug}.mp3"
                nw["audio_us"] = f"audio/us/{slug}.mp3"
                nw["meaning"] = w["meaning"]
                for k in ("example", "example_vi"):
                    if k in w:
                        nw[k] = w[k]
                new.append(nw)
            unit["words"] = new
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("data/*.json updated with audio_uk / audio_us")
    return 0


if __name__ == "__main__":
    sys.exit(main())
