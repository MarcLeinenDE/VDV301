# Network / discovery findings register addendum

## NET-001 - VDV 301-3 English scope says VDV 303-3

Classification: `pdf_label_or_heading_error_candidate`.

Impact: documentation only; no executable schema effect.

## NET-002 - English section number 2.3.5 vs German 2.3.4

Classification: `pdf_label_or_heading_error_candidate`.

Affected topic: cabling of end devices with switches.

Impact: documentation navigation only.

## NET-003 - fibre section prints IEE 802.3

Classification: `pdf_table_or_documentation_error_candidate`.

Likely intended reference: IEEE 802.3, consistent with the rest of VDV 301-3.

## DISC-001 - German/English IP-address allocation conflict

Classification: `pdf_table_or_documentation_error_candidate`.

Observed:

```text
VDV 301-2 Base Services V2.0 fresh Deep Read:
  German ZeroConf/link-local paragraph cites RFC 3927.
  English translation of the same passage still cites RFC 2927.
  Bibliography lists RFC 3927.

VDV 301-2 Base Services V2.1 fresh Deep Read:
  the same German RFC 3927 / English RFC 2927 split persists.

German V2.2/V2.4 first-pass observation:
  no specific IP-address allocation rule; address ranges must be consistent; fixed IP/DHCP best practice.

English V2.2/V2.4 first-pass observation:
  retained ZeroConf wording, RFC 2927 reference and 169.254.x.x language.

Historical V2.3 first-pass observation follows the later German/English conflict pattern.
```

Handling:

```text
Do not enforce ZeroConf/169.254 as a hard VDV rule from the English text alone.
Do not silently choose one language version as corrected authority.
Expose the documentation conflict if relevant to diagnostics.
Preserve version/language provenance when explaining the rule.
```

## DISC-002 - RFC 2927 reference is unrelated to IPv4 Link-Local addressing

Classification: `pdf_table_or_documentation_error_candidate`.

External corroboration:

```text
RFC 2927: MIME Directory Profile for LDAP Schema.
RFC 3927: Dynamic Configuration of IPv4 Link-Local Addresses, 169.254/16.
```

Deep Read history:

```text
VDV 301-2 V1.0 cites RFC 2927.
VDV 301-2 Base Services V2.0 corrects the German text to RFC 3927,
but the English translation still cites RFC 2927; the bibliography uses RFC 3927.
VDV 301-2 Base Services V2.1 retains the same bilingual split.
```

Handling: reference-number correction candidate only; does not override DISC-001.

## DISC-003 - V2.4 history records missing German DNS-SD table entries were added

Classification: `ok_with_note` / historical documentation correction.

Handling:

```text
Keep discovery semantics/version provenance separate from language-table completeness.
No schema correction.
```

## Discovery Deep Read note - SRV Weight semantics

Fresh V1.0, V2.0 and V2.1 Base-Service reads all retain wording equivalent to preferring the lower SRV weight at equal priority. RFC 2782 instead defines proportional weighted selection, where larger positive weights receive correspondingly higher probability.

This evidence is tracked in `DR3012-002` and its later-document extensions rather than being duplicated as a separate DISC finding.
