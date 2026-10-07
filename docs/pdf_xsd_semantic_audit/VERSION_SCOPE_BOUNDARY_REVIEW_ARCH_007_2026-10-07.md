# Version-scope boundary review — ARCH-007 — 2026-10-07

Status: **verified / scope unchanged / edition wording independently checked in English**.

## Finding
`ARCH-007` is a version-context non-defect. VDV 301-1 V1.0 describes SNTP and RTP as conceivable protocols that are not yet specified in **this edition/issue**. That is historical publication-state wording, not a permanent prohibition.

## Publication-lineage check
Current VDV publication surfaces expose only VDV 301-1 V1.0 in German plus its English translation. No later VDV 301-1 architecture version is published.

## Independent English-language control
The English V1.0 communication section independently states that other IP-based protocols could be used, giving SNTP for time synchronization and RTP for audio/video streaming as examples, followed by the statement that these are not yet specified in this issue.

This independently confirms the edition-specific nature of the statement.

The project source registry also contains later TimeService and VideoLiveService service publications. Those are separate Part-2 service authority lineages; they are not successor editions of VDV 301-1 and must be evaluated under their own selected-version authority.

## Boundary conclusion
- predecessor Part-1 publication: none available;
- first/last applicable Part-1 version: V1.0;
- successor Part-1 publication: none available;
- German: normative original;
- English: edition-specific wording independently confirmed.

Semantic scope remains `V1.0 / documentation_only`.

## Consequence
Never convert “not yet specified in this issue” into a permanent SNTP/RTP prohibition. Later selected service profiles remain authoritative for their own protocol requirements.
