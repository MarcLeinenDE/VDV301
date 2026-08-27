#!/usr/bin/env python3
"""Export XSD simpleType enumeration values to CSV and Markdown.

Purpose:
  Support the VDV301 PDF/XSD semantic audit by creating a reproducible
  inventory of all xs:simpleType definitions that contain xs:enumeration values.

Usage examples:
  python tools/export_xsd_enumerations.py IBIS-IP_Enumerations_V2.4.xsd \
    --out-csv docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv \
    --out-md docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.md

  python tools/export_xsd_enumerations.py IBIS-IP_Enumerations_V2.1.xsd IBIS-IP_Enumerations_V2.2.xsd

Notes:
  - This exporter uses only the Python standard library.
  - It preserves XSD document order.
  - It is intentionally limited to simpleType enumeration inventories.
    It does not decide whether PDF/XSD differences are schema defects or
    documentation defects.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


SIMPLE_TYPE_RE = re.compile(r"<(?P<prefix>\w+:)?simpleType\s+[^>]*name=\"(?P<name>[^\"]+)\"[^>]*>")
RESTRICTION_RE = re.compile(r"<(?P<prefix>\w+:)?restriction\s+[^>]*base=\"(?P<base>[^\"]+)\"[^>]*>")
ENUM_RE = re.compile(r"<(?P<prefix>\w+:)?enumeration\s+[^>]*value=\"(?P<value>[^\"]+)\"[^>]*/?>")
END_SIMPLE_TYPE_RE = re.compile(r"</(?P<prefix>\w+:)?simpleType>")


@dataclass(frozen=True)
class EnumValue:
    source_file: str
    simple_type: str
    restriction_base: str
    value_index: int
    value: str
    line: int


def extract_enumerations(path: Path) -> List[EnumValue]:
    """Extract enumeration values from one XSD file using a line-based parser."""
    rows: List[EnumValue] = []
    current_type: Optional[str] = None
    current_base: str = ""
    current_index = 0

    lines = path.read_text(encoding="utf-8-sig").splitlines()
    for lineno, line in enumerate(lines, start=1):
        start_match = SIMPLE_TYPE_RE.search(line)
        if start_match:
            current_type = start_match.group("name")
            current_base = ""
            current_index = 0

        if current_type is not None:
            restriction_match = RESTRICTION_RE.search(line)
            if restriction_match:
                current_base = restriction_match.group("base")

            enum_match = ENUM_RE.search(line)
            if enum_match:
                current_index += 1
                rows.append(
                    EnumValue(
                        source_file=path.name,
                        simple_type=current_type,
                        restriction_base=current_base,
                        value_index=current_index,
                        value=enum_match.group("value"),
                        line=lineno,
                    )
                )

            if END_SIMPLE_TYPE_RE.search(line):
                current_type = None
                current_base = ""
                current_index = 0

    return rows


def write_csv(rows: Iterable[EnumValue], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["source_file", "simple_type", "restriction_base", "value_index", "value", "line"])
        for row in rows:
            writer.writerow([
                row.source_file,
                row.simple_type,
                row.restriction_base,
                row.value_index,
                row.value,
                row.line,
            ])


def write_markdown(rows: List[EnumValue], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    grouped: dict[tuple[str, str], List[EnumValue]] = {}
    for row in rows:
        grouped.setdefault((row.source_file, row.simple_type), []).append(row)

    lines: List[str] = []
    lines.append("# XSD enumeration inventory")
    lines.append("")
    lines.append("Generated from XSD simpleType enumeration declarations.")
    lines.append("")
    lines.append("| Source file | Simple type | Restriction base | Count | Values |")
    lines.append("|---|---|---|---:|---|")
    for (source_file, simple_type), values in grouped.items():
        base = values[0].restriction_base
        joined_values = "<br>".join(f"`{value.value}`" for value in values)
        lines.append(f"| `{source_file}` | `{simple_type}` | `{base}` | {len(values)} | {joined_values} |")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export XSD simpleType enumeration values.")
    parser.add_argument("xsd", nargs="+", type=Path, help="XSD file(s) to inspect")
    parser.add_argument("--out-csv", type=Path, default=None, help="Optional CSV output path")
    parser.add_argument("--out-md", type=Path, default=None, help="Optional Markdown output path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows: List[EnumValue] = []
    for xsd_path in args.xsd:
        if not xsd_path.exists():
            raise FileNotFoundError(f"XSD file not found: {xsd_path}")
        rows.extend(extract_enumerations(xsd_path))

    if args.out_csv:
        write_csv(rows, args.out_csv)
    if args.out_md:
        write_markdown(rows, args.out_md)
    if not args.out_csv and not args.out_md:
        writer = csv.writer(__import__("sys").stdout)
        writer.writerow(["source_file", "simple_type", "restriction_base", "value_index", "value", "line"])
        for row in rows:
            writer.writerow([
                row.source_file,
                row.simple_type,
                row.restriction_base,
                row.value_index,
                row.value,
                row.line,
            ])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
