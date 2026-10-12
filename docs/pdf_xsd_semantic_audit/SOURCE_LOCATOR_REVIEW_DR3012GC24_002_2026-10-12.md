# DR3012GC24-002 — German §2.1.1 duplicate heading, official V2.2–V2.4

Date: 2026-10-12. Existing semantic finding ID retained; affected official PDF scope expanded V2.4 → **V2.2, V2.3, V2.4** after independent adjacent historical release review.

## Primary finding

Under visible original **§2.1 Adressierung** the German sections **§2.1.1 IP-Adressen** and **§2.1.1 Subnetzmasken/Gateways** reuse the same number in GC V2.2, V2.3 and V2.4. Independent English document bodies correctly label **§2.1.1 IP Addresses** and **§2.1.2 Subnet Masks/Gateways**. This is a **PDF editorial navigation defect, documentation-only**, not an XML/XSD or functional conformance rule.

## Original PDF body and version-scope boundary

| Official pinned publication | Printed original page(s), body result | Status |
|---|---|---|
| VDV-Schrift 301-2 V1.0 (Deutsch) | de p20: 2.1.1 IP-Adressen / 2.1.2 Subnetzmasken/Gateways | historical_unaffected_control |
| VDV-Schrift 301-2 Basic Services V2.0 | de/en p21: 2.1.1 IP-Adressen / 2.1.2 Subnetzmasken/Gateways; separate English prose controls same heading meanings | historical_unaffected_control |
| VDV-Schrift 301-2 Basic Services V2.1 | de/en p22: 2.1.1 IP-Adressen / 2.1.2 Subnetzmasken/Gateways, English inline translated counterpart | last_nonaffected_predecessor |
| VDV-Schrift 301-2 General Conventions V2.2 | de p17: 2.1.1 IP-Adressen / 2.1.1 Subnetzmasken/Gateways (duplicated German number); en p20: 2.1.1 IP Addresses / 2.1.2 Subnet Masks/Gateways (correct independent English) | first_affected |
| VDV-Schrift 301-2 General Conventions V2.3 | de p17: 2.1.1 IP-Adressen / 2.1.1 Subnetzmasken/Gateways (duplicated German number); en p20: 2.1.1 IP Addresses / 2.1.2 Subnet Masks/Gateways (correct independent English) | intermediate_affected |
| VDV-Schrift 301-2 General Conventions V2.4 | de p20: 2.1.1 IP-Adressen / 2.1.1 Subnetzmasken/Gateways (duplicated German number); en p23: 2.1.1 IP Addresses / 2.1.2 Subnet Masks/Gateways (correct independent English) | last_checked_affected_no_corrected_successor |

**First affected** GC V2.2 (August 2019). **Last independently verified unaffected predecessor** Basic Services V2.1 (July 2018). **Persisting affected** GC V2.3 and GC V2.4, the latest checked edition. No available corrected successor documented; no inferred fix.

## Byte-pinned source/visible-body evidence

- **VDV301-2_V1.0_DE**, SHA-256 `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`, run38235045280 artifact11740188048. Actual printed p20 (de), §2.1; PNG SHA-256 `bc7edd969f0fe42f0fb8579fd316626f9b2e69a98e9f543e3675fb62d52ecd34`.
- **VDV301-2_BASE_V2.0**, SHA-256 `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`, run38234839369 artifact11740437015. Actual printed p21 (de/en), §2.1; PNG SHA-256 `b330a4b676bb763cd120a4e79fbf9e91bc4b8190f4c9fff7c7d8aa6c63565c24`.
- **VDV301-2_BASE_V2.1**, SHA-256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`, run38241336859 artifact11742178834. Actual printed p22 (de/en), §2.1; PNG SHA-256 `efe838ac40ab7f6f5ad68c08f7e3d4fa8e4fc42da721caf9c91ea3db77810010`.
- **VDV301-2_GC_V2.2**, SHA-256 `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051`, run38241136892 artifact11742114523. Actual printed p17 (de), §2.1; PNG SHA-256 `02dbb8a9233ba2477d541e7a903d138a3485fbcd3b65a1011a899fe94ebe87cb`; Actual printed p20 (en), §2.1; PNG SHA-256 `1daa0a654816510463e8644cc48c94cb6802189fb4af68c6641066d178cbd46c`.
- **VDV301-2_GC_V2.3**, SHA-256 `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603`, DE run38234454263 artifact11739882271; EN run38241642951 artifact11742209098. Actual printed p17 (de), §2.1; PNG SHA-256 `bc66bac6d590d5415925bb1669546e2bbce92ba50ba86f54137a69bf46014508`; Actual printed p20 (en), §2.1; PNG SHA-256 `c0c0c3a36b2d8a04a2198d81e3af3c1fced21e97f0dccbeb3c678000936f06cf`.
- **VDV301-2_GC_V2.4**, SHA-256 `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d`, EV-134 run33843888080 artifact9925822375. Actual printed p20 (de), §2.1; PNG SHA-256 `08813005a3db7005eeff725c5988c0a3f85d9ec0b98f67df7248445fca1c6e35`; Actual printed p23 (en), §2.1; PNG SHA-256 `0d676a9e8935148f8cb467f6dc934f936e147fbf244d95ab43e6fdb4356b9906`.

All PDFs are original official publications from `audit_registry/pdf_source_registry_v0.1.json` and pinned in `audit_registry/pdf_source_pins_v0.1.json`. The actual body (not TOC/history/inferred heading sequence) was inspected page by page. The V1.0 official source is German-only in the audited source inventory; do not invent an English V1.0 PDF control. Basic V2.0/V2.1 use bilingual headings and prose on shared pages.

## Disproof and conformance treatment

Strongest alternative considered: the second German `2.1.1` could be a meaningful second classification instead of a typo. The independent English editions V2.2–V2.4 label the second subsection `2.1.2`; the entire earlier official line V1.0 DE and Basic V2.0/V2.1 also numbers the identical two subjects `2.1.1/2.1.2`. Thus the duplication in the three GC German bodies is a confirmed editorial copy/numbering defect. No relevant XSD component or executable XML validation difference exists.

**SDK:** `normative_authority=contextual_only`, `validation_effect=documentation_only/no_runtime_effect`, `sdk_behavior=no_runtime_diagnostic`, `runtime_match=not_applicable`. No runtime matcher, provider FAIL, alias, XSD edit or PR is authorized here. Recommend reporting the long-lived publication correction to VDV as an editorial correction with each historical document explicitly scoped.

**Progress:** locator, body verified and scope boundary 77 → **78/192**; 114 remaining. All six official PDF publications and the exact affected DE/EN pages recorded. Gate-pending after substantive commit; complete full schema gate before terminal-clean separate status commit. **Next: DR3012GC24-003**.
