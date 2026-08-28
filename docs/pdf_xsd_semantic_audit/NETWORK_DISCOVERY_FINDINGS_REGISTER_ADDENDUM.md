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

VDV 301-2 General Conventions V2.2 fresh Deep Read:
  German materially changes to 'no specification for IP-address allocation';
  only consistency between participants is required, with fixed IP/DHCP as best practice.
  English still retains ZeroConf wording, RFC 2927 and 169.254.x.x requirements.
  Bibliography lists RFC 3927.

Historical V2.3 and V2.4 first-pass observations follow the later German/English conflict pattern.
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
VDV 301-2 General Conventions V2.2 removes the ZeroConf prescription from German,
while English continues to cite RFC 2927 and 169.254.x.x; bibliography still lists RFC 3927.
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

Fresh V1.0, V2.0, V2.1 and V2.2 reads retain wording equivalent to preferring the lower SRV weight at equal priority. RFC 2782 instead defines proportional weighted selection, where larger positive weights receive correspondingly higher probability.

This evidence is tracked in `DR3012-002` and its later-document extensions rather than being duplicated as a separate DISC finding.

## General-Conventions V2.2 documentation findings

The V2.2 Deep Read additionally records:

```text
DR3012GC22-001
  repeated unresolved Word cross-reference placeholders across device-class, system-start and XML/table-reference sections.

DR3012GC22-002
  German DNS-SD TXT subsection is incorrectly numbered 3.3.1 like SRV;
  English correctly uses 3.3.2 for TXT.
```

These are documentation findings, not runtime/XSD rules.
