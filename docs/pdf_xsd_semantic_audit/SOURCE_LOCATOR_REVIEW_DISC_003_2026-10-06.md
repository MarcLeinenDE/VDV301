# Source-locator review — DISC-003 — 2026-10-06

Status: **complete / visible-body verified / historical documentation correction**.

## Result

DISC-003 confirms a documentation omission in German V2.3 Table 3 and its explicit repair in V2.4. No XSD or runtime-validity rule is derived.

## Visible evidence

- V2.3 General Conventions, printed page 27, section 3.3.1, Table 3: visible rows end with `ver`, `path`, `multicast`, `sntp-server`. `coachnumber`, `deviceclass` and `deviceID` are absent.
- V2.4, printed page 30: Table 3 adds `coachnumber`.
- V2.4, printed page 31: Table 3 includes `deviceclass` and `deviceID`.
- V2.4, printed page 75, section 7.3.2: version history explicitly records that missing entries in the German version of Table 3 were added.

## Disproof

The added rows are not classified as a new V2.4 protocol feature. The official history itself labels the change as a correction of missing German table entries.

## Consequence

Historical documentation defect only. No XSD mutation, no runtime matcher, and no change to selected-XSD authority.
