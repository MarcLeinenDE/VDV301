# CIS PDF source-pin correction — 2026-09-14

Status: **evidence-backed registry correction**. This is not a new source pin and does not replace the original official-source evidence.

The original successful CIS pin run `33736316368`, job `100587592810`, artifact `9885887536` (digest `sha256:8a514d33d5c9f23408a14dd1302366845b319027e280773407a2188c27b23cfe`) contains PDF bytes, extracted full text, page renders and hash manifests. The values previously stored in `pdf_source_pins_v0.1.json` for the four CIS sources did not match that artifact. The artifact and the original run log agree with each other.

| Source | Prior registry PDF SHA / bytes | Correct evidence PDF SHA / bytes | Fulltext SHA / pages |
|---|---|---|---|
| `CIS_V1.1` | `89080a41da387270ecac5b228df6aa4903ccb123a0d37e9e73cd98396786931b` / `985025` | `f9d63dd1f2e417691913e57a9c7121c90b4e781cbcd1328be681695975f59739` / `809729` | `cb6d9c80f9869eb6a6ee76a357997dfdb2ea18379b99122f000a0d1916b79f50` / `25` |
| `CIS_V2.0` | `0e3041d6354c040d532767391947476238a8afcab7a8df4276da1e7cad0cfa2b` / `878454` | `d4a4a0ab89b1dfbf47a2d69e5bd73ec511bb515fff0c147794087ed0ebbecf3d` / `810529` | `e1266d67e4948ec30d53cdd6c00dabed24b7bed3819a68a18c956c51c429078c` / `25` |
| `CIS_V2.2` | `3fcd258cf21c60527c48bd438c4d09a2a139c7093c0ff6984185e7c81efb8802` / `831079` | `789abcd3ea9b42ef7393b09484bfd5257e20a069dbd7d1ca99409fc80a5e76f0` / `951233` | `c0bc1c8be902a9c60e7b51a96a9cc6e9dcd387906035f30bb2c2e5b424245c31` / `26` |
| `CIS_V2.3` | `3f427901177e372daf0fee974648240e38da267c30030a909ccb712686f71ab1` / `1035224` | `b9e057a96dfbd824e18b4ace0958a6f80f62cd853ad6360bc2c76ea5db837f87` / `480140` | `b8179881d2121cacfdd6ac173712e5f433aefd43eeca0afb6a0ae3c1969cedf4` / `27` |

Correction rule: existing source evidence is preserved; only the machine-readable registry values are reconciled to the exact immutable evidence artifact. No XSD, frozen finding inventory, finding terminal state or source PDF is modified.
