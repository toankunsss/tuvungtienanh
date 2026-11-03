#!/usr/bin/env python3
"""Validate data/grade-XX.json files against the dataset schema.

Usage:
    python3 scripts/validate.py              # validate all grades present
    python3 scripts/validate.py 6 7          # validate only grades 6 and 7
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Number of units in each Global Success book (excluding Review units).
EXPECTED_UNITS = {
    1: 16, 2: 16,
    3: 20, 4: 20, 5: 20,
    6: 12, 7: 12, 8: 12, 9: 12,
    10: 10, 11: 10, 12: 10,
}

POS = {
    "n", "v", "adj", "adv", "prep", "conj", "pron", "det", "num",
    "exclam", "phr", "phr v", "idiom", "modal v", "aux v",
}

IPA_RE = re.compile(r"^/[^/]+/$")


def check_grade(grade: int) -> list[str]:
    errs: list[str] = []
    path = DATA / f"grade-{grade:02d}.json"
    if not path.exists():
        return [f"{path.name}: missing"]
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{path.name}: invalid JSON: {e}"]

    def err(msg: str) -> None:
        errs.append(f"{path.name}: {msg}")

    for key in ("grade", "series", "book_title", "publisher", "units"):
        if key not in doc:
            err(f"missing top-level key '{key}'")
    if doc.get("grade") != grade:
        err(f"grade field is {doc.get('grade')!r}, expected {grade}")

    units = doc.get("units", [])
    if len(units) != EXPECTED_UNITS[grade]:
        err(f"has {len(units)} units, expected {EXPECTED_UNITS[grade]}")

    for i, u in enumerate(units, start=1):
        tag = f"unit {u.get('unit', '?')}"
        if u.get("unit") != i:
            err(f"{tag}: unit number should be {i}")
        for key in ("title", "title_vi", "status", "words", "sources"):
            if key not in u:
                err(f"{tag}: missing '{key}'")
        if u.get("status") not in ("sourced", "unverified"):
            err(f"{tag}: status must be 'sourced' or 'unverified'")
        if u.get("status") == "sourced" and not u.get("sources"):
            err(f"{tag}: status 'sourced' but no sources")
        if not isinstance(u.get("sources", []), list):
            err(f"{tag}: 'sources' must be a list")
        words = u.get("words", [])
        if len(words) < 3:
            err(f"{tag}: only {len(words)} words")
        seen = set()
        for w in words:
            word = w.get("word", "")
            if not word or word != word.strip():
                err(f"{tag}: bad word {word!r}")
            key = (word.lower(), w.get("pos"))
            if key in seen:
                err(f"{tag}: duplicate word {word!r} ({w.get('pos')})")
            seen.add(key)
            if w.get("pos") not in POS:
                err(f"{tag}: {word!r} has unknown pos {w.get('pos')!r}")
            for key in ("ipa_uk", "ipa_us"):
                if not IPA_RE.match(w.get(key) or ""):
                    err(f"{tag}: {word!r} has bad {key} {w.get(key)!r}")
            for key in ("audio_uk", "audio_us"):
                if key in w and not (ROOT / w[key]).exists():
                    err(f"{tag}: {word!r} {key} file missing: {w[key]}")
            if not w.get("meaning", "").strip():
                err(f"{tag}: {word!r} has no meaning")
            if bool(w.get("example")) != bool(w.get("example_vi")):
                err(f"{tag}: {word!r} needs both example and example_vi")
            extra = set(w) - {"word", "pos", "ipa_uk", "ipa_us", "audio_uk", "audio_us",
                              "meaning", "example", "example_vi"}
            if extra:
                err(f"{tag}: {word!r} has unexpected keys {sorted(extra)}")
    return errs


def main() -> int:
    grades = [int(a) for a in sys.argv[1:]] or [
        g for g in EXPECTED_UNITS if (DATA / f"grade-{g:02d}.json").exists()
    ]
    all_errs: list[str] = []
    for g in grades:
        errs = check_grade(g)
        all_errs += errs
        status = "OK" if not errs else f"{len(errs)} error(s)"
        print(f"grade {g:>2}: {status}")
    for e in all_errs:
        print("  -", e)
    return 1 if all_errs else 0


if __name__ == "__main__":
    sys.exit(main())
