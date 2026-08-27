#!/usr/bin/env python3
"""Reusable HTTP/runtime profile helpers for the VDV301 audit and future SDK.

The module deliberately keeps source authority separate from severity:
- VDV profile rules (method / explicitly pinned HTTP version)
- external HTTP/XML media-type rules
- diagnostic inference

It does not perform network I/O.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


TOKEN_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    ok: bool
    severity: str
    authority: str
    message: str
    observed: str | None = None
    expected: str | None = None


@dataclass(frozen=True)
class MediaType:
    type: str
    subtype: str
    parameters: tuple[tuple[str, str], ...]

    @property
    def normalized(self) -> str:
        return f"{self.type}/{self.subtype}"

    @property
    def is_xml(self) -> bool:
        return self.normalized in {"application/xml", "text/xml"} or self.subtype.endswith("+xml")


def _split_semicolon_aware(value: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    quoted = False
    escaped = False
    for char in value:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if quoted and char == "\\":
            current.append(char)
            escaped = True
            continue
        if char == '"':
            quoted = not quoted
            current.append(char)
            continue
        if char == ";" and not quoted:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    if quoted or escaped:
        raise ValueError("unterminated quoted-string in Content-Type")
    parts.append("".join(current).strip())
    return parts


def _parse_parameter_value(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("empty media-type parameter value")
    if value.startswith('"'):
        if len(value) < 2 or not value.endswith('"'):
            raise ValueError("unterminated quoted media-type parameter")
        inner = value[1:-1]
        out: list[str] = []
        escaped = False
        for char in inner:
            if escaped:
                out.append(char)
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                raise ValueError("unescaped quote in media-type parameter")
            else:
                out.append(char)
        if escaped:
            raise ValueError("trailing escape in media-type parameter")
        return "".join(out)
    if not TOKEN_RE.fullmatch(value):
        raise ValueError("invalid token media-type parameter value")
    return value


def parse_content_type(raw: str) -> MediaType:
    """Parse the RFC 9110 media-type shape used by Content-Type.

    This is intentionally a focused parser for deterministic SDK classification,
    not a replacement for a complete HTTP field parser.
    """
    parts = _split_semicolon_aware(raw.strip())
    if not parts or not parts[0] or "/" not in parts[0]:
        raise ValueError("Content-Type does not contain type/subtype")
    type_part, subtype_part = (part.strip() for part in parts[0].split("/", 1))
    if not TOKEN_RE.fullmatch(type_part) or not TOKEN_RE.fullmatch(subtype_part):
        raise ValueError("invalid media type token")

    parameters: list[tuple[str, str]] = []
    seen: set[str] = set()
    for part in parts[1:]:
        if not part or "=" not in part:
            raise ValueError("invalid media-type parameter")
        name, value = (item.strip() for item in part.split("=", 1))
        if not TOKEN_RE.fullmatch(name):
            raise ValueError("invalid media-type parameter name")
        name_norm = name.lower()
        if name_norm in seen:
            raise ValueError(f"duplicate media-type parameter: {name}")
        seen.add(name_norm)
        parameters.append((name_norm, _parse_parameter_value(value)))

    return MediaType(type_part.lower(), subtype_part.lower(), tuple(parameters))


def check_content_type(
    raw: str | None,
    *,
    body_present: bool,
    expected_xml: bool,
) -> list[CheckResult]:
    """Classify Content-Type without inventing a VDV-specific media type.

    Missing Content-Type with content is an RFC 9110 SHOULD-level warning.
    For XSD-backed VDV operations, a declared non-XML type is a media/payload
    mismatch combining VDV payload semantics with external media-type semantics.
    """
    if raw is None or not raw.strip():
        if body_present:
            return [
                CheckResult(
                    "HTTP-X02",
                    False,
                    "warning",
                    "external_normative",
                    "Message has content but no Content-Type; RFC 9110 says the sender SHOULD generate it when the intended media type is known.",
                    observed=None,
                    expected="media type describing the representation",
                )
            ]
        return [
            CheckResult(
                "HTTP-X02",
                True,
                "not_applicable",
                "external_normative",
                "No message content; Content-Type presence is not required by this check.",
            )
        ]

    try:
        media = parse_content_type(raw)
    except ValueError as exc:
        return [
            CheckResult(
                "HTTP-X01",
                False,
                "error",
                "external_normative",
                f"Malformed Content-Type: {exc}",
                observed=raw,
                expected="RFC 9110 media-type syntax",
            )
        ]

    results = [
        CheckResult(
            "HTTP-X01",
            True,
            "pass",
            "external_normative",
            "Content-Type media-type syntax is parseable.",
            observed=media.normalized,
        )
    ]

    if not expected_xml:
        results.append(
            CheckResult(
                "HTTP-X-MEDIA",
                True,
                "informational",
                "profile_context",
                "This profile does not impose the XSD-backed XML media-type expectation.",
                observed=media.normalized,
            )
        )
        return results

    if media.normalized == "application/xml":
        results.append(
            CheckResult(
                "HTTP-X03",
                True,
                "pass",
                "external_normative",
                "application/xml is compatible with an XML document representation.",
                observed=media.normalized,
            )
        )
    elif media.normalized == "text/xml":
        results.append(
            CheckResult(
                "HTTP-X04",
                True,
                "pass_with_note",
                "external_normative",
                "text/xml is an XML media-type alias; RFC 7303 recommends application/xml for the generic application type.",
                observed=media.normalized,
            )
        )
    elif media.subtype.endswith("+xml"):
        results.append(
            CheckResult(
                "HTTP-X05",
                True,
                "pass_with_note",
                "external_normative",
                "The +xml structured-syntax suffix identifies an XML-based media type; the custom media type is not automatically a VDV-defined type.",
                observed=media.normalized,
            )
        )
    else:
        results.append(
            CheckResult(
                "HTTP-X06",
                False,
                "error",
                "combined_vdv_payload_and_external_media_semantics",
                "Selected operation expects an XML/XSD payload but Content-Type declares a non-XML media type.",
                observed=media.normalized,
                expected="application/xml, text/xml, or an explicitly justified XML-based +xml media type",
            )
        )
    return results


def check_vdv_http_method(actual_method: str, *, request_data_present: bool) -> CheckResult:
    expected = "POST" if request_data_present else "GET"
    actual = actual_method.upper()
    return CheckResult(
        "HTTP-V02" if request_data_present else "HTTP-V03",
        actual == expected,
        "pass" if actual == expected else "error",
        "vdv_normative",
        f"VDV operation method {'matches' if actual == expected else 'does not match'} the request-data convention.",
        observed=actual,
        expected=expected,
    )


def _version_tuple(version: str) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in version.split("."))
    except ValueError as exc:
        raise ValueError(f"invalid numeric VDV General-Conventions version: {version}") from exc


def check_vdv_http_version(actual_version: str, *, general_conventions_version: str) -> CheckResult:
    """Apply only the historically justified explicit VDV HTTP-version gate."""
    pinned = _version_tuple(general_conventions_version) >= (2, 3)
    observed = actual_version.strip().upper().replace("HTTP/", "")
    if not pinned:
        return CheckResult(
            "HTTP-V01",
            True,
            "not_applicable",
            "vdv_normative",
            "The audit does not retroactively apply the explicit V2.3+ HTTP/1.1 rule to this earlier General-Conventions profile.",
            observed=observed,
            expected=None,
        )
    return CheckResult(
        "HTTP-V01",
        observed == "1.1",
        "pass" if observed == "1.1" else "error",
        "vdv_normative",
        f"General Conventions {general_conventions_version} explicitly pins HTTP/1.1.",
        observed=observed,
        expected="1.1",
    )


def has_error(results: Iterable[CheckResult]) -> bool:
    return any((not result.ok) and result.severity == "error" for result in results)
