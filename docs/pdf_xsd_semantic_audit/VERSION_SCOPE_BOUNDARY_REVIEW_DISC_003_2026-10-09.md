# DISC-003: korrigierte Versionsgrenze (09.10.2026)

**Verifiziert nach materiellem Scope-Disproof:** betroffen sind **General Conventions V2.2 und V2.3 Deutsch**, korrigiert wurde der Dokumentationsfehler erstmals in **V2.4 Deutsch**.

**Sichtbarer Originalnachweis:** offizielles V2.2 PDF `https://www.vdv.de/301-2-sdes-v2-2-common-conventions.pdfx`, SHA-256 `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051`. Gedruckte Seite **27**, §3.3.1, deutsche **Tabelle 3** enthält nur Ver/Path/multicast/sntp-server; **coachnumber, deviceclass, deviceID** fehlen. Gedruckte Seite **33**, §3.3.2, englische **Table 3** derselben Veröffentlichung enthält dagegen **alle drei Einträge**; deviceclass und deviceID sind ausdrücklich ab IBIS-IP V2.2 mandatory. Beide Seiten am 09.10.2026 sichtbar geprüft.

**Negativer Vorgänger:** In Base V2.0/V2.1 stehen die drei späteren Attribute laut gepinntem Quelltext in beiden Sprachfassungen noch nicht, weshalb der spezifische DE/EN-Tabellenwiderspruch dort nicht vorliegt. Der Live-Screenshot für V2.1 pp36–37 lieferte Cache-Miss; eine neue **visuelle** Negativkontrolle wird ausdrücklich nicht behauptet.

**Weiterer Verlauf:** V2.3 Deutsch p27 omittiert die drei weiterhin, V2.4 Deutsch pp30–31 ergänzt sie; V2.4 Versionshistorie p75 bezeichnet die Einträge ausdrücklich als Korrektur. Historische `SOURCE_LOCATOR_REVIEW_DISC_003_2026-10-06.md` und der 2026-10-08-Widerlegungsbericht bleiben als Evidence, nicht als kanonische Scope-Autorität.

**Konformität:** Ein Finding, `DISC-003`; weiterhin `confirmed_pdf_defect`, `contextual_only`, `sdk_behavior=info`, `runtime_match=not_applicable`. **Keine XSD-Regel, kein Runtime-Matcher und kein Anbieter-FAIL** wegen der fehlenden deutschen Tabellenzeilen.

**Repo-Synchronisierung:** DISC-Semantikblock, aggregierte Semantik, Source-Locators, PDF-Body-Reg, Runtime-/Locator-Semantikblob-Pins, Boundary-Registry, Current State und SDK-Manifest. Nach erfolgreichem Gate: 49/70 verifiziert, 21 offen, nächstes DMS-001.
