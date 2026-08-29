# HTMLDisplayService V2.1 — Deep Read Pass 2

Status: independent fresh read and targeted visible review complete; historical reconciliation intentionally pending.

## Source authority

- Official publication: VDV-Schrift 301-2-17, HtmlDisplayService V2.1, 07/2018.
- Official URL: https://www.vdv.de/301-2-17-sds-v2-1-htmldisplayservice.pdfx
- Pinned SHA-256: `c8aa91626bf60c8e74200200d63d44d497aeb3ab240c47039333b2c922a0e495`
- Pinned size: `734901` bytes.
- Source pin run: `33265498869`.
- Interactive screenshot path returned cache miss; exact pinned-byte fallback render used.
- Render run: `33265541783`, job `99134831905`, artifact `9718526667`.
- Visibly reviewed pages: 7, 8, 9, 10.

## Authority boundary

The checked official `VDV-301-2.1` tag and `dev/schema-integration` contain no dedicated HtmlDisplayService XSD. The publication itself states that HtmlDisplayService defines no own protocol. Therefore this document is treated as a **non-XSD DNS-SD/HTTP profile**. Supporting DeviceManagementService/Common structures do not create an HDS XML contract.

## Independent fresh-read observations

1. HtmlDisplayService is presented as comparable to TimeService in the sense that it does not define its own service protocol.
2. Service discovery uses DNS-SD with service name `HtmlDisplayService` and transport `_http._tcp`.
3. The SRV record supplies target host and port. TXT records use `content` and `path`.
4. The browser target is formed as `http://host:port/path`; the `path` value may contain query and/or fragment components.
5. `content` identifies the displayed content but is project-specific and explicitly not standardized by the publication. Multiple offered URLs are represented as separate DNS-SD entries.
6. The publication intentionally avoids prescribing stable requirements for the actual HTTP content/browser implementation, because those requirements would age quickly. Browser/content compatibility is left to the involved suppliers.
7. Device integration is performed through DeviceManagementService using `DeviceClass = MultiFunctionalDisplay`; devices are distinguished by `DeviceID`. No separate DeviceManagementService is introduced for HDS.

## Falsification / boundary checks

- Searched the official `VDV-301-2.1` release inventory for a dedicated HDS schema: none found.
- Searched the integration root pool for a dedicated HDS schema: none found.
- The visible German and English pages both support the non-XSD protocol-profile interpretation.
- No XML/XSD finding is created from this document.
- No requirement is inferred for MIME type or HTML feature support beyond what the publication explicitly states.

## Fresh finding result

No new finding ID is promoted from the independent fresh read. This is not a claim that historical HDS findings are valid or invalid; they have deliberately not been opened yet.

## Next gate

Only after this freeze may the historical HDS audit files and finding register be opened. Each historical item must then be revalidated against this pinned source and the protocol authority boundary under `FINDING_EVIDENCE_GATE.md`.
