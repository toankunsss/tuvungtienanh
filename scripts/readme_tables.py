#!/usr/bin/env python3
"""Regenerate the status tables inside README.md (between the AUTO markers)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = {1: 16, 2: 16, 3: 20, 4: 20, 5: 20, 6: 12, 7: 12, 8: 12, 9: 12, 10: 10, 11: 10, 12: 10}


def main() -> None:
    grades = {}
    for p in sorted((ROOT / "data").glob("grade-*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        grades[d["grade"]] = d

    lines = [
        "| Lớp | Số unit | Số từ | Unit đã có nguồn (`sourced`) | Unit chưa xác minh (`unverified`) |",
        "|---:|---:|---:|---|---|",
    ]
    total = 0
    for g in range(1, 13):
        if g not in grades:
            lines.append(f"| {g} | {EXPECTED[g]} | – | _chưa có dữ liệu_ | |")
            continue
        units = grades[g]["units"]
        n = sum(len(u["words"]) for u in units)
        total += n
        ok = [u["unit"] for u in units if u["status"] == "sourced"]
        bad = [u["unit"] for u in units if u["status"] != "sourced"]
        lines.append(f"| {g} | {len(units)} | {n} | {fmt(ok)} | {fmt(bad)} |")
    lines.append(f"| **Tổng** | | **{total}** | | |")

    detail = []
    for g in sorted(grades):
        d = grades[g]
        detail.append(f"<details><summary><b>Lớp {g}</b> – {d['book_title']}</summary>\n")
        detail.append("| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |")
        detail.append("|---:|---|---|---:|---|")
        for u in d["units"]:
            st = "✅ sourced" if u["status"] == "sourced" else "⚠️ unverified"
            detail.append(f"| {u['unit']} | {u['title']} | {u['title_vi']} | {len(u['words'])} | {st} |")
        detail.append("\n</details>\n")

    block = "\n".join(lines) + "\n\n" + "\n".join(detail)
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = re.sub(r"(<!-- AUTO:START -->\n).*?(<!-- AUTO:END -->)",
                  lambda m: m.group(1) + block + m.group(2), text, flags=re.S)
    readme.write_text(text, encoding="utf-8")
    print("README tables updated")


def fmt(nums: list[int]) -> str:
    """[1,2,3,5] -> '1–3, 5'"""
    if not nums:
        return "–"
    out, start = [], nums[0]
    for a, b in zip(nums, nums[1:] + [None]):
        if b != a + 1:
            out.append(str(start) if start == a else f"{start}–{a}")
            start = b
    return ", ".join(out)


if __name__ == "__main__":
    main()
