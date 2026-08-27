# Official PR candidates addendum - VideoLiveService

Status: tracking only. No PR is opened or modified by this addendum.

## VLS PR candidate - LiveStreamData compositor

Linked finding:

```text
VLS-002
```

Current observation:

```text
IBIS-IP_VideoLiveService_V2.0.xsd defines VideoLiveService.LiveStreamData with xs:choice.
Both public VideoLiveService V1.0/V2.0 documents describe LiveStreamData as one record containing stream identification, camera data, rtspURI, video dimensions, codec, frame rate, bitrate, transforms and quality.
Current upstream master still contains the same xs:choice.
```

Initial assessment:

```text
Strong schema-structure candidate, but not safe for an immediate patch during audit.
Potential correction from xs:choice to an ordered/all-field compositor may be behavior-breaking for consumers built around the current XSD and must be validated locally first.
```

Required before any official-facing action:

```text
1. Compile the exact V2.0 family unchanged.
2. Demonstrate current one-field choice behavior with positive/negative samples.
3. Validate a complete PDF-intended LiveStreamData sample against the current XSD.
4. Check VideoDisplay/VideoRecording schemas for analogous compositor patterns and intended modelling conventions.
5. Search current upstream PR/issues again immediately before proposal.
6. Determine whether xs:sequence, xs:all or a different optional-field model matches the documented semantics and compatibility expectations.
7. Prepare only a minimal isolated patch if still justified.
8. Ask the user explicitly before opening or modifying any upstream PR.
```

Documentation-only VLS-003/VLS-004 are not XSD correction candidates in this addendum.
