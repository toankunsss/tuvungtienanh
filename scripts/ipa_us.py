#!/usr/bin/env python3
"""Derive American (US) IPA from the CMU Pronouncing Dictionary.

CMU ARPAbet transcriptions are converted to dictionary-style IPA in the
Cambridge Dictionary US convention (ɑː, ɝː, ɚ, oʊ, ...), with stress marks
placed before the stressed syllable (maximal-onset syllabification).
When a word has several CMU pronunciations, the one closest to the existing
UK IPA is chosen (e.g. 'present' n. vs v.).

Requires: pip install cmudict

Usage:
    python3 scripts/ipa_us.py                # fill/refresh ipa_us in data/*.json
    python3 scripts/ipa_us.py --report       # only list words not found in CMU
"""
import difflib
import json
import re
import sys
from pathlib import Path

import cmudict

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OVERRIDES = ROOT / "scripts" / "ipa_us_overrides.json"

CMU = cmudict.dict()

VOWELS = {
    "AA": "ɑː", "AE": "æ", "AH": "ʌ", "AO": "ɑː", "AW": "aʊ", "AY": "aɪ",
    "EH": "e", "ER": "ɝː", "EY": "eɪ", "IH": "ɪ", "IY": "iː", "OW": "oʊ",
    "OY": "ɔɪ", "UH": "ʊ", "UW": "uː",
}
CONS = {
    "B": "b", "CH": "tʃ", "D": "d", "DH": "ð", "F": "f", "G": "ɡ", "HH": "h",
    "JH": "dʒ", "K": "k", "L": "l", "M": "m", "N": "n", "NG": "ŋ", "P": "p",
    "R": "r", "S": "s", "SH": "ʃ", "T": "t", "TH": "θ", "V": "v", "W": "w",
    "Y": "j", "Z": "z", "ZH": "ʒ",
}
# Legal English syllable onsets (IPA), used for maximal-onset syllabification.
ONSETS = {
    "", *[c for c in CONS.values() if c != "ŋ"],
    "pl", "pr", "bl", "br", "tr", "dr", "kl", "kr", "ɡl", "ɡr", "fl", "fr",
    "θr", "ʃr", "sp", "st", "sk", "sm", "sn", "sl", "sw", "sf", "tw", "dw",
    "kw", "ɡw", "θw", "pj", "bj", "fj", "vj", "mj", "kj", "ɡj", "hj", "spl",
    "spr", "str", "skr", "skw", "spj", "skj",
}


def vowel_ipa(base: str, stress: str, nxt: str | None) -> str:
    if base == "AH":
        return "ʌ" if stress in "12" else "ə"
    if base == "ER":
        return "ɝː" if stress in "12" else "ɚ"
    if base == "IY":
        return "iː" if stress in "12" else "i"
    if base == "UW":
        return "u" if stress == "0" and nxt in VOWELS else "uː"
    if base == "AO" and nxt == "R":
        return "ɔː"
    if base == "IH" and stress == "0" and nxt is None:
        return "i"
    return VOWELS[base]


def arpabet_to_ipa(phones: list[str]) -> str:
    """Convert one CMU pronunciation to IPA with stress marks."""
    segs = []  # (ipa, is_vowel, stress)
    for i, ph in enumerate(phones):
        m = re.fullmatch(r"([A-Z]+)([012]?)", ph)
        base, stress = m.group(1), m.group(2)
        nxt = re.sub(r"\d", "", phones[i + 1]) if i + 1 < len(phones) else None
        nxt_stress = phones[i + 1][-1] if i + 1 < len(phones) else ""
        if base == "ER" and stress == "0" and nxt in VOWELS and nxt_stress in "12":
            segs.append(("ə", True, "0"))
            segs.append(("r", False, ""))
        elif base in VOWELS:
            segs.append((vowel_ipa(base, stress, nxt), True, stress))
        else:
            segs.append((CONS[base], False, ""))

    vowel_idx = [i for i, s in enumerate(segs) if s[1]]
    if not vowel_idx:
        return "".join(s[0] for s in segs)
    n_syll = len(vowel_idx)

    # syllable start positions (maximal onset)
    starts = [0]
    for a, b in zip(vowel_idx, vowel_idx[1:]):
        cluster = [segs[i][0] for i in range(a + 1, b)]
        split = len(cluster)
        for k in range(len(cluster) + 1):
            if "".join(cluster[k:]) in ONSETS:
                split = k
                break
        starts.append(a + 1 + split)

    out = []
    for syl, (st, v) in enumerate(zip(starts, vowel_idx)):
        end = starts[syl + 1] if syl + 1 < n_syll else len(segs)
        body = "".join(s[0] for s in segs[st:end])
        stress = segs[v][2]
        mark = ""
        if n_syll > 1:
            mark = "ˈ" if stress == "1" else "ˌ" if stress == "2" else ""
        out.append(mark + body)
    ipa = "".join(out)
    if "ˈ" in ipa:
        head, tail = ipa.split("ˈ", 1)
        ipa = head + "ˈ" + tail.replace("ˌ", "")
    # r-coloured vowels in Cambridge US style
    ipa = ipa.replace("ɝːr", "ɝː").replace("ɚr", "ɚ")
    return ipa


def normalise(ipa: str) -> str:
    """Rough accent-neutral form for comparing UK and US transcriptions."""
    s = ipa.strip("/").replace("(r)", "r").replace("ː", "").replace(".", "")
    s = re.sub(r"(?<=[tdnsθlz])ju", "u", s)
    for a, b in (("əʊ", "oʊ"), ("ɒ", "ɑ"), ("ɔ", "ɑ"), ("ɝ", "ɜr"), ("ɚ", "ər"),
                 ("ʌ", "ə"), ("eə", "er"), ("ɪə", "ɪr"), ("ʊə", "ʊr")):
        s = s.replace(a, b)
    return s


def word_ipa(token: str, uk_hint: str) -> str | None:
    prons = CMU.get(token.lower())
    if not prons:
        return None
    cands = [arpabet_to_ipa(p) for p in prons]
    target = normalise(uk_hint)
    best = max(cands, key=lambda c: difflib.SequenceMatcher(None, normalise(c), target).ratio())
    return single_primary(best, uk_hint)


def single_primary(ipa: str, uk_hint: str) -> str:
    """CMU sometimes gives two primary stresses (thirteen, baseball).
    Keep one, following the UK transcription: stress-initial words keep the
    first primary, others demote earlier primaries to secondary."""
    if ipa.count("ˈ") < 2:
        return ipa
    head, rest = ipa.split("ˈ", 1)
    if uk_hint.lstrip("/").startswith("ˈ"):
        return head + "ˈ" + rest.replace("ˈ", "")
    *firsts, last = ipa.split("ˈ")
    return "ˌ".join(firsts) + "ˈ" + last


def us_ipa(word: str, uk_ipa: str, overrides: dict) -> str | None:
    if word in overrides:
        return overrides[word]
    raw = [t for t in re.split(r"[\s\-–]+", word.replace("’", "'")) if t]
    words = [(t, t.strip("!?.,()")) for t in raw]
    real = [core for _, core in words if core]
    uk_tokens = [t for t in uk_ipa.strip("/").split() if t.strip(".")]
    aligned = len(uk_tokens) == len(real)
    parts, k = [], 0
    for tok, core in words:
        if not core:  # placeholder such as "..." in sentence patterns
            parts.append("...")
            continue
        hint = uk_tokens[k] if aligned else uk_ipa
        ipa = word_ipa(core, hint)
        if ipa is None:
            return None
        if len(real) > 1 and aligned:
            ipa = match_phrase_stress(ipa, uk_tokens[k])
        parts.append(ipa)
        k += 1
    return "/" + " ".join(parts) + "/"


def match_phrase_stress(us: str, uk: str) -> str:
    """Inside a phrase, give each word the same stress level as in the UK IPA."""
    bare = us.replace("ˈ", "").replace("ˌ", "")
    multi = us != bare or sum(us.count(v) for v in "aeiouæɑɒɔəɚɝɪʊʌ") > 1
    if "ˈ" in uk:
        return us if "ˈ" in us else "ˈ" + bare
    if "ˌ" in uk:
        return us.replace("ˈ", "ˌ") if us != bare else "ˌ" + bare
    # unstressed word in the UK phrase: weak vowel, no primary stress
    if not multi:
        return bare.replace("ʌ", "ə") if "ə" in uk and "ʌ" not in uk else bare
    return us.replace("ˈ", "ˌ")


def main() -> int:
    report_only = "--report" in sys.argv
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8")) if OVERRIDES.exists() else {}
    missing: dict[str, str] = {}
    for path in sorted(DATA.glob("grade-*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        for unit in doc["units"]:
            new_words = []
            for w in unit["words"]:
                uk = w.get("ipa_uk") or w.get("ipa")
                us = us_ipa(w["word"], uk, overrides)
                if us is None:
                    missing[w["word"]] = uk
                    us = w.get("ipa_us", "")
                # rebuild with a stable key order
                nw = {"word": w["word"], "pos": w["pos"], "ipa_uk": uk, "ipa_us": us}
                for k in ("audio_uk", "audio_us", "meaning", "example"):
                    if k in w:
                        nw[k] = w[k]
                new_words.append(nw)
            unit["words"] = new_words
        if not report_only:
            path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(missing)} words not in CMU dict and not in overrides:")
    for k, v in sorted(missing.items()):
        print(f"  {k!r}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
