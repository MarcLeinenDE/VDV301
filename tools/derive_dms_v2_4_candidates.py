#!/usr/bin/env python3
"""Derive conservative DMS V2.4 XSD candidate variants.

This helper is intentionally deterministic and fails if the expected V2.2
source patterns are not found exactly. It does not use public forks as a
normative source; fork files may be used later only for comparison.
"""

from __future__ import annotations

import argparse
import difflib
from dataclasses import dataclass
from pathlib import Path

SOURCE_FILE = "IBIS-IP_DeviceManagementService_V2.2.xsd"
TARGET_FILE = "IBIS-IP_DeviceManagementService_V2.4.xsd"


@dataclass(frozen=True)
class Variant:
    key: str
    title: str
    common_include: str
    enumerations_include: str


VARIANTS = [
    Variant(
        key="variant_a_existing_repository_dependencies",
        title="DMS V2.4 with existing repository dependencies",
        common_include="IBIS-IP_common_V2.3.xsd",
        enumerations_include="IBIS-IP_Enumerations_V2.2.xsd",
    ),
    Variant(
        key="variant_b_v24_schema_family_dependencies",
        title="DMS V2.4 with V2.4 schema-family dependencies",
        common_include="IBIS-IP_common_V2.4.xsd",
        enumerations_include="IBIS-IP_Enumerations_V2.4.xsd",
    ),
]


def replace_exact(text: str, old: str, new: str, expected_count: int = 1) -> str:
    count = text.count(old)
    if count != expected_count:
        raise RuntimeError(
            f"Expected {expected_count} occurrence(s), found {count}: {old!r}"
        )
    return text.replace(old, new, expected_count)


def replace_in_segment(text: str, start_marker: str, end_marker: str, replacements: list[tuple[str, str]]) -> str:
    start = text.find(start_marker)
    if start < 0:
        raise RuntimeError(f"Start marker not found: {start_marker!r}")
    end = text.find(end_marker, start)
    if end < 0:
        raise RuntimeError(f"End marker not found after {start_marker!r}: {end_marker!r}")
    end += len(end_marker)

    segment = text[start:end]
    for old, new in replacements:
        segment = replace_exact(segment, old, new, expected_count=1)
    return text[:start] + segment + text[end:]


def derive(source: str, variant: Variant) -> str:
    text = source

    # Dependency decision. The source DMS V2.2 file currently includes common V2.2
    # and enumerations V2.2. Variant A stays within files already present in the
    # official repository. Variant B uses the V2.4 schema-family dependency names.
    text = replace_exact(
        text,
        '<xs:include schemaLocation="IBIS-IP_common_V2.2.xsd"/>',
        f'<xs:include schemaLocation="{variant.common_include}"/>',
    )
    if variant.enumerations_include != "IBIS-IP_Enumerations_V2.2.xsd":
        text = replace_exact(
            text,
            '<xs:include schemaLocation="IBIS-IP_Enumerations_V2.2.xsd"/>',
            f'<xs:include schemaLocation="{variant.enumerations_include}"/>',
        )

    # DMS V2.4: error messages are optional (0:*), not mandatory 10:*.
    text = replace_exact(
        text,
        '<xs:element name="ErrorMessage" type="MessageStructure" minOccurs="10" maxOccurs="unbounded">',
        '<xs:element name="ErrorMessage" type="MessageStructure" minOccurs="0" maxOccurs="unbounded">',
        expected_count=2,
    )

    # DMS V2.4: DeviceStatusImpact and DeviceStatusPriority are optional.
    text = replace_exact(
        text,
        '<xs:element name="DeviceStatusImpact" type="DeviceStateEnumeration"> </xs:element>',
        '<xs:element name="DeviceStatusImpact" type="DeviceStateEnumeration" minOccurs="0"> </xs:element>',
    )
    text = replace_exact(
        text,
        '<xs:element name="DeviceStatusPriority" type="IBIS-IP.int"></xs:element>',
        '<xs:element name="DeviceStatusPriority" type="IBIS-IP.int" minOccurs="0"></xs:element>',
    )

    # DMS V2.4: InstallUpdateRequest fields are optional for pre-defined update
    # storage locations. Keep similarly named fields in update state/history
    # structures mandatory by applying replacements only inside this type.
    text = replace_in_segment(
        text,
        '<xs:complexType name="DeviceManagementService.InstallUpdateRequestStructure">',
        '</xs:complexType>',
        [
            (
                '<xs:element name="UpdateID" type="IBIS-IP.NMTOKEN">',
                '<xs:element name="UpdateID" type="IBIS-IP.NMTOKEN" minOccurs="0">',
            ),
            (
                '<xs:element name="UpdateTimestamp" type="IBIS-IP.dateTime">',
                '<xs:element name="UpdateTimestamp" type="IBIS-IP.dateTime" minOccurs="0">',
            ),
            (
                '<xs:element name="UpdateURL" type="IBIS-IP.anyURI">',
                '<xs:element name="UpdateURL" type="IBIS-IP.anyURI" minOccurs="0">',
            ),
        ],
    )

    return text


def write_diff(source: str, target: str, out_path: Path, fromfile: str, tofile: str) -> None:
    diff = difflib.unified_diff(
        source.splitlines(keepends=True),
        target.splitlines(keepends=True),
        fromfile=fromfile,
        tofile=tofile,
    )
    out_path.write_text("".join(diff), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root containing the official DMS V2.2 source XSD.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("generated/dms-v2.4-candidates"),
        help="Output directory relative to repo root unless absolute.",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    out_root = args.output if args.output.is_absolute() else repo_root / args.output
    source_path = repo_root / SOURCE_FILE
    source = source_path.read_text(encoding="utf-8")

    for variant in VARIANTS:
        variant_dir = out_root / variant.key
        variant_dir.mkdir(parents=True, exist_ok=True)
        target = derive(source, variant)
        target_path = variant_dir / TARGET_FILE
        target_path.write_text(target, encoding="utf-8")
        write_diff(
            source,
            target,
            variant_dir / "diff_against_official_dms_v2.2.patch",
            fromfile=SOURCE_FILE,
            tofile=f"{variant.key}/{TARGET_FILE}",
        )
        (variant_dir / "README.md").write_text(
            f"# {variant.title}\n\n"
            "Status: generated candidate for review, not an official VDV file.\n\n"
            f"Source: `{SOURCE_FILE}` from the official baseline.\n\n"
            f"Output: `{TARGET_FILE}`.\n\n"
            "Dependency choice:\n\n"
            f"- common include: `{variant.common_include}`\n"
            f"- enumerations include: `{variant.enumerations_include}`\n\n"
            "Run the full schema-pool validation before using this for an upstream PR.\n",
            encoding="utf-8",
        )

    print(f"Generated {len(VARIANTS)} DMS V2.4 candidate variants under {out_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
