# Runtime-mapping review — TimeService V1.0 DRTIME10-002 — 2026-09-21

Status: **review decision complete / not yet persisted into semantic registry at report creation**.

## Finding assessment

`DRTIME10-002` remains a **confirmed PDF/documentation defect**.

The exact byte-pinned VDV 301-2-10 TimeService V1.0 publication shows on physical page 6 that the German text explicitly excludes additional cyclic transmission of the current time while the adjacent English service description omits that sentence. EV-147 visually confirmed the omission from the exact pinned PDF.

This is a bilingual normative-text omission, not evidence for a second English runtime profile and not permission to synthesize a generic cyclic UDP time-broadcast mechanism.

## Runtime-mapping decision

Decision: `not_designed -> not_applicable`.

Reason:

- TimeService V1.0 intentionally has no XSD semantic authority in this audit.
- The finding is not tied to a discrete XML validation result or another uniquely matchable runtime message.
- The operational consequence is an architecture/profile guard: synchronization remains the SNTP path selected by the publication.
- Creating a standalone Known-Issues matcher would invent a runtime event that the finding itself does not define.

The finding and its bilingual diagnostic remain part of the semantic knowledge base and may be used for explanatory/profile documentation. Only the runtime matcher classification becomes terminal `not_applicable`.

## Authority and guards

- official source: VDV 301-2-10 TimeService V1.0, 02/2018;
- pinned SHA-256: `d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3`;
- decisive visible locator: physical PDF page 6;
- external protocol selected by VDV: RFC 4330 / SNTP;
- EV-147: run `34028395412`, closure `34028583953`;
- no XSD is authoritative for TimeService V1.0;
- no XSD mutation or alias is involved;
- no generic cyclic UDP time-broadcast behavior may be inferred.

## Expected mapping inventory after persistence

```text
reviewed        61
candidate       17
not_designed     0
not_applicable 114
implemented      0
```

No executable Known-Issues matcher is added.
