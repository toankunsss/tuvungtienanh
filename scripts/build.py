#!/usr/bin/env python3
"""Build combined outputs from data/grade-XX.json.

Outputs:
    dist/all.json        – all grades in one file
    dist/flat.json       – one record per word (grade, unit, unit_title, ...)
    dist/csv/grade-XX.csv
    dist/stats.json      – word counts per grade / unit
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DIST = ROOT / "dist"
FIELDS = ["grade", "unit", "unit_title", "status", "word", "pos", "ipa_uk", "ipa_us",
          "audio_uk", "audio_us", "meaning", "example"]


def main() -> None:
    grades = [json.loads(p.read_text(encoding="utf-8"))
              for p in sorted(DATA.glob("grade-*.json"))]
    (DIST / "csv").mkdir(parents=True, exist_ok=True)

    flat, stats = [], {"total_words": 0, "grades": []}
    for g in grades:
        rows = []
        gstat = {"grade": g["grade"], "words": 0, "units": []}
        for u in g["units"]:
            for w in u["words"]:
                rows.append({
                    "grade": g["grade"], "unit": u["unit"], "unit_title": u["title"],
                    "status": u["status"],
                    "word": w["word"], "pos": w["pos"],
                    "ipa_uk": w["ipa_uk"], "ipa_us": w["ipa_us"],
                    "audio_uk": w.get("audio_uk", ""), "audio_us": w.get("audio_us", ""),
                    "meaning": w["meaning"], "example": w.get("example", ""),
                })
            gstat["units"].append({"unit": u["unit"], "title": u["title"],
                                   "status": u["status"], "words": len(u["words"])})
            gstat["words"] += len(u["words"])
        stats["grades"].append(gstat)
        stats["total_words"] += gstat["words"]
        flat += rows
        with open(DIST / "csv" / f"grade-{g['grade']:02d}.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    def dump(name: str, obj) -> None:
        (DIST / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    dump("all.json", {"series": "Global Success", "grades": grades})
    dump("flat.json", flat)
    dump("stats.json", stats)
    print(f"Built {len(grades)} grades, {stats['total_words']} words -> {DIST.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
