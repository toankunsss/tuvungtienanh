#!/usr/bin/env python3
"""Regenerate the status tables inside README.md (between the AUTO markers)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = {1: 16, 2: 16, 3: 20, 4: 20, 5: 20, 6: 12, 7: 12, 8: 12, 9: 12, 10: 10, 11: 10, 12: 10}


SOURCE_NOTE = {
    1: "SBT + SGV Tiếng Anh 1",
    2: "Tài liệu tập huấn, giáo án, vở luyện từ",
    3: "Giáo án, mind map",
    4: "Đề cương ôn tập",
    5: "Word list theo bài (đối chiếu giáo án)",
    6: "Glossary SGK + trang bài học SGK",
    7: "Đối chiếu web (VietJack, VnDoc…)",
    8: "Bản chép Glossary (Luyện viết từ vựng 8)",
    9: "Bản chép Glossary (Wordlist TA9)",
    10: "Đối chiếu web",
    11: "Bản chép Glossary (Wordlist TA11)",
    12: "Bản chép Glossary (Wordlist TA12)",
}


def main() -> None:
    grades = {}
    for p in sorted((ROOT / "data").glob("grade-*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        grades[d["grade"]] = d

    lines = [
        "| Lớp | Số unit | Số từ | Theo SGK (`official`) | Có nguồn (`sourced`) | Chưa xác minh (`unverified`) | Nguồn chính |",
        "|---:|---:|---:|---|---|---|---|",
    ]
    total = 0
    for g in range(1, 13):
        if g not in grades:
            lines.append(f"| {g} | {EXPECTED[g]} | – | _chưa có dữ liệu_ | | | |")
            continue
        units = grades[g]["units"]
        n = sum(len(u["words"]) for u in units)
        total += n
        by = {st: [u["unit"] for u in units if u["status"] == st] for st in ("official", "sourced", "unverified")}
        lines.append(f"| {g} | {len(units)} | {n} | {fmt(by['official'])} | {fmt(by['sourced'])} | "
                     f"{fmt(by['unverified'])} | {SOURCE_NOTE.get(g, '')} |")
    lines.append(f"| **Tổng** | | **{total}** | | | | |")

    detail = []
    for g in sorted(grades):
        d = grades[g]
        detail.append(f"<details><summary><b>Lớp {g}</b> – {d['book_title']}</summary>\n")
        detail.append("| Unit | Tên unit | Nghĩa | Số từ | Trạng thái |")
        detail.append("|---:|---|---|---:|---|")
        for u in d["units"]:
            st = {"official": "📗 official", "sourced": "✅ sourced"}.get(u["status"], "⚠️ unverified")
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
