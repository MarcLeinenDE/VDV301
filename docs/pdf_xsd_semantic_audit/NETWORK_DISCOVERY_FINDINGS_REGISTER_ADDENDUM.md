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
German V2.2/V2.4: no specific IP-address allocation rule; address ranges must be consistent; fixed IP/DHCP best practice.
English V2.2/V2.4: retained ZeroConf wording, RFC 2927 reference and 169.254.x.x language.
Historical V2.3 observation follows the same pattern.
```

Handling:

```text
Do not enforce ZeroConf/169.254 as a hard VDV rule from the English text alone.
Do not silently choose one language version as corrected authority.
Expose the documentation conflict if relevant to diagnostics.
```

## DISC-002 - RFC 2927 reference is unrelated to IPv4 Link-Local addressing

Classification: `pdf_table_or_documentation_error_candidate`.

External corroboration:

```text
RFC 2927: MIME Directory Profile for LDAP Schema.
RFC 3927: Dynamic Configuration of IPv4 Link-Local Addresses, 169.254/16.
```

Handling: reference-number correction candidate only; does not override DISC-001.

## DISC-003 - V2.4 history records missing German DNS-SD table entries were added

Classification: `ok_with_note` / historical documentation correction.

Handling:

```text
Keep discovery semantics/version provenance separate from language-table completeness.
No schema correction.
```
