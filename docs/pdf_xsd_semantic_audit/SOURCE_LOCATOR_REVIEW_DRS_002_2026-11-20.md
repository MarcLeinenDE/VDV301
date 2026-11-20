# DRS-002 — originale RetrieveSpecific-Fehleralternative, offizielle XSD und Versionsgrenzen (2026-11-20)

**Vorhandene Finding-ID:** `DRS-002` (kein neues Finding). **Klassifikation:** `confirmed_pdf_defect` / `pdf_xsd_element_name_mismatch` / `wrong_response_choice_member`, `sdk_behavior=error_with_advisory`. Anders als rein redaktionelle Findings ist der dokumentierte XML-Elementname **nicht XSD-valid**. Das selected-XSD-Ergebnis ist normativ; ein erklärender Matcher ist **reviewed_not_implemented**.

## 1. Unabhängig sichtbarer Original-PDF-Body (nicht TOC/OCR)

Offizielle **VDV-Schrift 301-2-15, DoorStateService V2.1, 07/2018**, Source-ID `DOOR_V2.1`, URL https://www.vdv.de/301-2-15-sd-v2-1-doorstateservice.pdfx. Kanonischer PDF-Pin SHA-256 **`7413c99f2910f125947213561658ae9c808952d5b57700d155b939c899de26e8`**, **851513 Bytes**, 16 Seiten, Source-Pin-Run **33241913638**. Beim webbasierten Screenshot der Original-PDF am 20.11.2026: **Cache miss**. Gemäß Pflicht-Fallback wurde das bereits vorhandene, an den Original-Pin gebundene GitHub-Artefakt **EV-145 / Run 34026409256 / Artifact 9987189102** erneut heruntergeladen. **ZIP SHA256 `77d90917105e6a26cfd05660612ebd0ab2f37db6a1b5fc49b86bce95a8e179f9`** selbst neu berechnet und mit GitHub-Artefakt-Digest verglichen; Original-PNG-SHA256 aus `ev145_results.json` ebenfalls neu berechnet. Tatsächlich sichtbare Seiten wurden direkt angesehen:

- **Gedruckte Seite 9**, §2.1.2 `Response`, **Tabelle 2** `Description of DoorStateService.GetDoorOpenStatesResponse`: der `GetDoorOpenStatesResponse`-Fehlerzweig heißt **`OperationErrorMessage`**. Seiten-PNG 180dpi SHA `699fc2f28e1e901d8f0078004418e6e065d232756ab1cb3bf37ea16a3895d983`.
- **Gedruckte Seite 10**, §2.4.2 `Response`, **Tabelle 5** `Description of DoorStateService.GetDoorOperationStatesResponse`: auch `GetDoorOperationStatesResponse` verwendet legitimerweise **`OperationErrorMessage`**. PNG SHA `9973a258e9eac95c241aa0632c3239dd4d3b3f185559504376a7f1bb397421a0`.
- **Gedruckte Seite 12**, §2.7.2 `Response`, **Tabelle 9**, tatsächlicher Titel `Description of DoorStateService.RetrieveSpecificDoorOpenStateResponse`: Erfolgsalternative `DoorOpenState`, Fehleralternative in der Element-Spalte **`OperationErrorMessage`**, Wahlmarkierung `a/b -1:1`. Original-PNG SHA `e90660e9ec8ec21bb955f761aff0b73de01576f80f1c81555f6f446d927fcb5f`.
- **Dieselbe gedruckte Seite 12**, §2.8.2 `Response`, **Tabelle 11**, tatsächlicher Titel `Description of DoorStateService.RetrieveSpecificDoorOperationStateResponse`: Erfolgsalternative `DoorOperationState`, Fehleralternative erneut **`OperationErrorMessage`**. Dieselbe SHA-geprüfte PNG.

Die Seite-11-Kontrolle (§§2.7.1/2.7 und benachbarte Datenstruktur) wurde zusätzlich unter PNG SHA `96ef34798f2041af47ff943a36e37523e0acae45b866775b91f8523e2a73c570` geprüft; die Original-PDF-Rohbytes wurden **in diesem Zyklus nicht neu separat heruntergeladen oder selbst gehasht**. Die Originalautorität beruht auf dem unveränderten registrierten PDF-Quellpin und dem revalidierten Render-/Testartefakt. Textlayer der PDF ist nicht alleiniger Locatorbeleg (die Tabellen-Wörter werden dort durch Spaltenumbruch teilweise getrennt).

## 2. Exakte XSD-Autorität (nicht durch PDF-Namenskonvention ersetzen)

Offizielles Release `VDVde/VDV301@VDV-301-2.1`; `IBIS-IP_DoorStateService_V2.1.xsd`, exakter Service-Git-Blob **`abff0f3960e2ec7a9caaa9ddeb6efff8f4183805`**, auf dem aktuellen `dev/schema-integration` identisch. Die offiziellen historischen direkten `xs:include`-Abhängigkeiten **`IBIS-IP_common_V1.0.xsd` Blob `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`** sowie **`IBIS-IP_Enumerations_V1.0.xsd` Blob `a9bea5bc73003ed91ded8519db06c32c4067831d`** sind ebenfalls byte-identisch zu ihren entsprechenden Release-Tag-Originalen.

Die offizielle XSD trennt:
- **`DoorStateService.GetDoorOpenStatesResponseStructure`**, `xs:choice`, **Zeilen 32–39**: `GetDoorOpenStatesResponseData | OperationErrorMessage`.
- **`DoorStateService.GetDoorOperationStatesResponseStructure`**, `xs:choice`, **Zeilen 42–49**: `GetDoorOperationStatesResponseData | OperationErrorMessage`.
- **`DoorStateService.RetrieveSpecificDoorOpenStateResponseStructure`**, `xs:choice`, **Zeilen 60–67**: `DoorOpenState | ErrorMessage` (nicht `OperationErrorMessage`).
- **`DoorStateService.RetrieveSpecificDoorOperationStateResponseStructure`**, `xs:choice`, **Zeilen 78–85**: `DoorOperationState | ErrorMessage` (nicht `OperationErrorMessage`).
- Der ausgewählte `DoorStateServiceGroup` definiert die entsprechenden Operationen lokal in **Zeilen 24–27**, **keine Behauptung frei verwendbarer globaler XML-Roots**.

## 3. Aktive Widerlegung und ausführbare Belege

**Gegenhypothese A: `OperationErrorMessage` ist nur ein generisches Prosawort.** Widerlegt: Das Token steht sichtbar in beiden Tabellen **in der Spalte für XML-Strukturelemente**, unter dem `choice`-Compositor und mit Typ `IBIS-IP.string`; damit ist es nicht lediglich ein erläuterndes Etikett.

**Gegenhypothese B: beide Get-/RetrieveSpecific-Familien verwenden dieselbe Fehleralternative.** Widerlegt: PDF S.9/10 `Get` benutzt `OperationErrorMessage` tatsächlich korrekt; die offizielle XSD unterscheidet aber in den separaten `RetrieveSpecific`-Antworttypen ausdrücklich `ErrorMessage`. Der Copy/Paste-Verdacht ist daher anhand derselben Publikation und der offiziellen XSD gestützt. **Notation `a/b -1:1` steht für die VDV-Choice-Darstellung und ist kein negativer Mindestwert.**

**Bereits ausführbar getestet:** EV-111, erfolgreicher GitHub-Run **33242337308** (Job 99073684198), und **in EV-145 erneut ausgeführt**, GitHub-Run **34026409256**, Job 101468048441, `ev111_rerun.log` aus dem originalen EV145-ZIP selbst kontrolliert:
- `ProbeRetrieveOpenResponse`: `<ErrorMessage>` **valid**, `<OperationErrorMessage>` **invalid**.
- `ProbeRetrieveOperationResponse`: `<ErrorMessage>` **valid**, `<OperationErrorMessage>` **invalid**.
- Beide Prüfungen verwenden **Probe-Roots**, die gegen die exakten XSD-Typen kompiliert wurden; dies sind **keine** erfundenen globalen DoorStateService-Dokumentroots.
- **Keine neue lokale Testausführung in diesem Auditzyklus behauptet.** Verifizierte erfolgreiche Original-Runs/Protokolle reichen als bereits vorhandene ausführbare Evidenz für diese unveränderte XSD-Route aus.

## 4. Unabhängige Versions- und Sprachgrenze

Die offizielle VDV-Publikationsliste https://www.vdv.de/ip-kom-oev.aspx wurde **am 20.11.2026 erneut überprüft** und nennt nur die eigenständige **VDV 301-2-15 DoorStateService V2.1**. Für diese 07/2018-Ausgabe sind S.9/10-`Get` als Gegenkontrolle und S.12-`RetrieveSpecific` betroffen. Die allgemeine VDV-301-2-V1.0-DE/EN- bzw. V2.0-Basisdienstpublikation ist **keine direkte frühere Ausgabe des eigenständigen DoorStateService-Teils**. Kein vorheriger direkt vergleichbarer standalone Release, kein korrigierter standalone Nachfolger unabhängig bestätigt; keine erdachte Korrektur. Das Vorwort beschreibt **eine bilinguale Veröffentlichung**, technische Operationen und Datenstrukturen ausschließlich **in Englisch**. Diese Fehlerstelle ist daher ein einzelner betroffener englischer Tabellenkontext, nicht zwei getrennte DE/EN-Versionen.

## 5. Konsequenzen und Registry-Fortschritt

Bestehende semantische Klassifikation und vollständige deutsche/englische Diagnostik bleiben unverändert. Das Runtime-Manifest führt `DRS-002` bereits als **`error_with_advisory` / `xsd_invalid_advisory` / `reviewed_not_implemented`**. Für einen aufgrund des falschen XML-Elements tatsächlich XSD-invaliden `RetrieveSpecific`-Antwortzweig muss die spätere SDK-Diagnostik **den XSD-FAIL unverändert** belassen und darf den bekannten PDF-Fehler nur erklären. Kein `OperationErrorMessage`→`ErrorMessage`-Alias/Normalisierung, kein XSD-Edit, keine Änderung der Produktivmatcher in diesem Audit.

Die benachbarten bestehenden Finding-IDs `DRS-001`, `DRDOOR21-001`, `DRDOOR21-002` bleiben ausdrücklich getrennt. `DRS-003` (GetRequest-anyType) ist der nachfolgende eigene Block.

Nach genau einem neuen Source-Locator: **108/192** vollständige Locators, **108/108** sichtbare Original-Body-Prüfungen, **108/108** unabhängig geprüfte Versionsgrenzen, **84 offen**. Der kanonische `gate_pending`-Commit enthält den vollständigen Bericht, drei Register, SDK-Zählerspiegel und `CURRENT_STATE.json` gemeinsam. Erst **nach vollständigem GitHub-Schema-Gate**, separatem `terminal_clean`-Commit und **beiden grünen finalen HEAD-Gates** ist der Block terminal. Danach überprüfter Memory-PR und Cleanup nach ai-mem-Protokoll.
