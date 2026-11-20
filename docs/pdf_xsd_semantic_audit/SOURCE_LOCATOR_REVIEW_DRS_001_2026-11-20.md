# DRS-001 – Vollständiger Original-PDF-/XSD- und Versionsgrenzen-Nachweis (2026-11-20)

**Finding:** bereits existierendes `DRS-001` aus dem eingefrorenen 192er-Inventar; keine neue Finding-ID, keine doppelte Fortschrittszählung. **Bewertung:** `confirmed_pdf_defect`, `wrong_operation_reference`, `copy_paste_operation_name`; rein redaktionelle fehlerhafte Operationsübersicht, `no_runtime_diagnostic`/`not_applicable`.

## 1. Offizielle Originalquelle, visuelle Körperprüfung

- **VDV-Schrift 301-2-15, DoorStateService V2.1, Ausgabe 07/2018**; Quelle `DOOR_V2.1`, offizieller Download: https://www.vdv.de/301-2-15-sd-v2-1-doorstateservice.pdfx.
- Bereits offiziell byte-gepinnte Quelle **SHA-256 `7413c99f2910f125947213561658ae9c808952d5b57700d155b939c899de26e8`**, **851513 Byte**, 16 PDF-Seiten; Source-Pin-GitHub-Run **33241913638**.
- Der interaktive Web-PDF-Screenshot lieferte am 20.11.2026 einen Cache-Miss. Pflichtgemäß wurde der **bestehende, exakt an den Quell-Pin gebundene** deterministische Fallback `vdv-pdf-render-fallback`, GitHub-Run **43888781452**, Artefakt **14234584210**, erneut heruntergeladen. Der ZIP-Digest wurde selbst auf **SHA-256 `55af6a28af906e127df216116a080000677f25f24eb640190f339caa78e78da2`** geprüft (GitHub-Artefaktdigest identisch); `render_manifest.json` bestätigt Dokument-Hash, Dateigröße, 16 Seiten, 160 dpi und Einzelseiten-Hashes.
- **Tatsächlich visuell geprüft und anhand der Manifest-Hashes unabhängig verifiziert:** gedruckte **S.1** Umschlag bc059e744a0d8fbab47e94b2c20595bc66f1099f5bfeed4e308542563267f8a3, **S.9** Abschnitt **2 „Operations of the DoorStateService“ / Tabelle 1 „Description of Operations of DoorStateService“** 0aa5447c81474719a89816d6128f0e371e708f58d4c0be82fef327a3df58c9f6, **S.11** Abschnitte **2.5 und 2.6** 6655c4c27c55acf2dfd35f8a3f2ceb8aafb1f764a4e1e96a30f17a39f669fdb6.
- Die PDF-Rohdatei wurde in diesem Prüfzyklus **nicht neu heruntergeladen oder selbst SHA-gehasht**. Die unveränderte amtliche Byte-Identität ist über den früheren Repository-Quellpin und die erneut verifizierte Original-Renderkette belegt. Kein Vorwand einer frischen Roh-PDF-Byteprüfung.

## 2. Exakter Widerspruch im sichtbaren Dokumentkörper

Tabelle 1 auf der gedruckten S.9 listet für `DoorOpenStates` die Operationen `GetDoorOpenStates`, `SubscribeDoorOpenStates` und `UnsubscribeDoorOpenStates` korrekt. Unmittelbar nach **`GetDoorOperationStates`** wiederholt die Spalte **Operation** jedoch fälschlich **`SubscribeDoorOpenStates`** und **`UnsubscribeDoorOpenStates`** (jeweils Req./Resp.-Zeilen). Dort müssten die **OperationStates**-Namen stehen.

Die tatsächlichen sichtbaren Abschnittstitel **S.11 §2.5 „Data Structures of Operation SubscribeDoorOperationStates“** und **§2.6 „Data Structures of Operation UnsubscribeDoorOperationStates“** nennen die richtigen getrennten Operationen. Tabelle 6/7 auf S.11 behandeln `DoorOperationStates` bzw. `OperationState` ebenfalls getrennt. Der Locator verwendet die **sichtbare S.9 Tabelle 1**, nicht das Inhaltsverzeichnis oder eine erschlossene Tabellennummer.

**Aktive Gegenhypothese:** gemeinsame/generische Subscribe-Operationen für beide Türzustandsfamilien. **Widerlegt:** §2.5/§2.6 führen eigenständige OperationStates-Namen, und das offizielle XSD-Gruppenmodell deklariert jeweils eigene Req./Resp.-Member. Die generischen **Strukturtypen** `SubscribeRequestStructure`/`SubscribeResponseStructure` erklären lediglich den gemeinsamen Payload-Typ, nicht eine identische Operation.

## 3. Exakte offizielle XSD-Autorität und Original-Veröffentlichungsgrenzen

- Offizielles Upstream-Release **`VDVde/VDV301@VDV-301-2.1`**. `IBIS-IP_DoorStateService_V2.1.xsd`, Git-Blob **`abff0f3960e2ec7a9caaa9ddeb6efff8f4183805`**, stimmt byte-identisch zwischen Release-Tag und `dev/schema-integration` überein.
- **XSD `DoorStateServiceGroup`, Zeilen 10–23:** `DoorStateService.SubscribeDoorOpenStatesRequest/Response` (Zeilen 14–15), `DoorStateService.UnsubscribeDoorOpenStatesRequest/Response` (16–17), separat `DoorStateService.SubscribeDoorOperationStatesRequest/Response` (20–21) sowie `DoorStateService.UnsubscribeDoorOperationStatesRequest/Response` (22–23). **Lokale Gruppen-Member, keine erfundenen globalen XML-Dokumentroots.**
- **Absichtlich historische direkte Includes:** `IBIS-IP_common_V1.0.xsd` Git-Blob `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c` und `IBIS-IP_Enumerations_V1.0.xsd` Git-Blob `a9bea5bc73003ed91ded8519db06c32c4067831d`. Beide wurden für den aktuellen Prüflauf erneut gegen das offizielle Upstream-Tag verglichen, jeweils identisch. Kein `latest wins`.
- Offizieller VDV-Publikationsindex **https://www.vdv.de/ip-kom-oev.aspx**, am 20.11.2026 überprüft: als **eigenständige 301-2-15-DoorStateService-Schrift** ist nur **V2.1** nachgewiesen. Die älteren allgemeinen VDV-301-2-V1.0- oder V2.0-Veröffentlichungen sind **keine eigenständigen früheren Ausgaben dieser 301-2-15-Schrift**. Kein eigenständiger direkter Vorgänger, keine eigenständige spätere Korrekturausgabe und kein korrigierter Nachfolger unabhängig belegt.
- **Sprachgrenze:** Ein und dieselbe bilinguale V2.1-Schrift; Umschlag/Vorwort DE/EN, die technischen Operationen werden laut Vorwort nur auf Englisch beschrieben. Der Fehler steht in der gemeinsamen englischen Operationstabelle und ist nicht als zwei getrennte DE-/EN-Veröffentlichungen zu zählen. Keine eigenständige deutschsprachige Operationstabelle als unbetroffene Kontrolle behauptet.

## 4. SDK-Auswirkung, Identitätsabgrenzung und Abschluss

Der bereits semantisch bestätigte Finding-Eintrag mit vollständiger **DE-/EN-Diagnostik** und `sdk_behavior=no_runtime_diagnostic` bleibt unverändert. Auch das Runtime-Mapping ist `not_applicable`: **keine XSD-Änderung, kein Alias, keine automatische Umbenennung, keine neuen produktiven Matcher**. Die XML-Validität wird ausschließlich durch die exakte ausgewählte XSD-Familie bestimmt. Ein neuer XML-Instanztest wurde für diesen ausschließlich redaktionellen Tabellenfehler nicht ausgeführt; kein neues Runtime-PASS/FAIL behauptet.

**Getrennte historische IDs:** `DRDOOR21-001` betrifft die vier falschen/verkürzten RetrieveSpecific-Beschreibungen auf S.11/12, `DRDOOR21-002` die falsche OpenState-Semantik in Tabelle 9 auf S.12, `DRS-002` einen separaten XML-/PDF-Elementnamenkonflikt. Keine dieser Identitäten wird `DRS-001` zugeschlagen.

Historischer Evidenzpfad: `docs/pdf_xsd_semantic_audit/deep_read/DOOR_V2.1.md`, `docs/pdf_xsd_semantic_audit/DOOR_STATE_SERVICE_FINDINGS_REGISTER_ADDENDUM.md`, `docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_DRS_V21_2026-09-06.md`, **EV-145 / run 34026409256 / closure 34026674927**. Diese Befunde bleiben erhalten.

**Zählung nach genau einem neuen Locator:** 107/192 strukturell vollständige Source-Locators, 107/107 sichtbar geprüfte Originalseiten-Findings, 107/107 unabhängig geprüfte Versionsgrenzen, 85 offen. Kanonische Register und `CURRENT_STATE.json` werden in demselben absturzsicheren Commit aktualisiert. **Terminal erst nach vollständigem Schema-Gate, separatem `terminal_clean`-Commit sowie beiden GitHub-Gates auf dem finalen HEAD.** Nächstes eindeutiges Finding nach diesem Block: `DRS-002`.
