# Visible-body source-locator revalidation — CE-007 / CE-008

Date: 2026-10-05

## CE-007

Visible PDF body was checked for all affected publication lanes. V1.0/V2.0/V2.1 used the exact-byte pinned render artifacts after live-render cache misses; V2.2/V2.3/V2.4 were checked in the live renderer.

The PDFs use the lexemes `Other`, `Valid` and `Air`. The exact selected XSDs use `other`, `valid` and `air`.

No semantic change: CE-007 remains a confirmed case-sensitive cross-artifact mismatch. PDF spellings are not XSD aliases.

## CE-008

Visible body checks confirm the Funicular/Taxi tables at:

- V2.2 p.46, Tables 103/104
- V2.3 p.47, Tables 103/104
- V2.4 p.50, Tables 102/103

The PDFs use `Unknown`, `Undefined` and `minicab`; the selected XSDs use `unknown`, `undefined` and `miniCab`.

No semantic change: CE-008 remains a high-confidence documentation-side casing mismatch. Validation follows the exact selected XSD.

## Evidence

Fallback artifacts:

- V1.0 run 33275626001 / artifact 9721397514
- V2.0 run 33279811315 / artifact 9722644456
- V2.1 run 33393002497 / artifact 9758203545

## Accounting

- current-standard verified: 25/40
- pending: 15
- structural count remains frozen at 40
- next pending finding: CE-009

## Gate

- GitHub Actions run: **37295002908**
- result: **SUCCESS**
- validated manifest commit: `ffba6e0024c34b6c362a4cecac0804c3011e6264`
- structural locators: **40**
- current-standard verified: **25**
- pending current-standard revalidation: **15**
- next pending finding: **CE-009**

The gate validated the current locator manifest/body-registry synchronization and the existing audit regression suite.
