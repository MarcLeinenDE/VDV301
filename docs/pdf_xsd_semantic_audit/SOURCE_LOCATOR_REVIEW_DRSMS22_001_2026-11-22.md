# DRSMS22-001 — SystemMonitoringService V2.2: fehlerhafte Textmarke im Abbildungsverzeichnis

**Review 2026-11-22.** Fortführung derselben eingefrorenen Finding-ID `DRSMS22-001` ohne Doppelzählung. `primary_surface=pdf`, `primary_issue_kind=editorial_residue`, `defect_assessment=confirmed_pdf_defect`; `validation_effect=documentation_only,no_runtime_effect`; `sdk_behavior=no_runtime_diagnostic`. Keine XSD- oder SDK-Runtime-Korrektur.

## 1. Original-PDF und sichtbarer Body

Offizielle **VDV-Schrift 301-2-18, SystemMonitoringService V2.2 (08/2019)**, [originale VDV-Veröffentlichung](https://www.vdv.de/301-2-18-sdes-v2-2-systemmonitoringservice.pdfx). Original-Pin `SMS_V2.2`, SHA256 `996f639a81cb91ad20a8e78b6213e7c85d41ff0ec42caba4208d6c4652b140f4`, **847416 Bytes** gemäß `audit_registry/pdf_source_pins_v0.1.json`.

**Gedruckte Originalseite 5**, tatsächlich sichtbar mit Überschrift **„Inhaltsverzeichnis / Content“**, enthält den Eintrag **„Abbildungsverzeichnis / List of figures“** und direkt daran die Word-Fehlermeldung **„Fehler! Textmarke nicht definiert.“**. Für diesen Befund ist die **fehlerhafte Inhaltsverzeichniszeile selbst** die echte sichtbare Originalfundstelle: kein aus dem Inhaltsverzeichnis erschlossener Verweis auf einen anderen PDF-Body, keine Table-Nummer.

Live-Web-PDF-Screenshot meldete Cache miss. Gemäß obligatorischem Renderfallback wurde das **bereits original-byte-gepinnte historische EV-146-Renderartefakt** gelesen:
- [EV-146 SUCCESS](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026822637), Artefakt `9987318510`, ZIP `drsms22-ev146`; ZIP-SHA256 **neu berechnet** am 22.11.2026: `181ff01b16dae43ec2826299e6f14717aef1668d66491b6051ae07661ee607f6`.
- Original `renders/page-05.png` (180 dpi), SHA256 **neu berechnet**: `39091e889381a592ce7c294161af36c1bbd3c804b9becd786630aefd3b1b781a`, identisch zur EV-146-Ergebnisdatei. Diese gerenderte Originalseite wurde **tatsächlich visuell geprüft**.
- Original `page_text/page-05-layout.txt` und `page_text/page-05-raw.txt` enthalten dieselbe Zeichenfolge: zusätzliche Textextraktions-Kontrolle, nicht visuelle Locator-Autorität.

**Keine Scheinevidenz:** PDF-Rohbytes wurden im aktuellen Zyklus **nicht erneut heruntergeladen oder SHA-geprüft**; der bestehende exakte PDF-Originalpin bleibt die Autorität, die Render-ZIP- und Seitenbild-Hashes wurden jedoch frisch verifiziert. Die Seitenansicht zeigt den Fehler eindeutig, nicht nur extrahierten Text.

## 2. Exakte offizielle XSD-Autorität

Gegen offiziellen Release-Tag **`VDVde/VDV301@VDV-301-2.2`** und kanonisches `dev/schema-integration` abgeglichen; alle drei Git-Blobs **identisch**:

| XSD | exakter Git-Blob |
| --- | --- |
| `IBIS-IP_SystemMonitoringService_V2.2.xsd` | `d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c` |
| `IBIS-IP_common_V2.2.xsd` | `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` |
| `IBIS-IP_Enumerations_V2.2.xsd` | `2a23b512379b18e8f122ac1272cef8229fb86283` |

Originales SMS-Service-XSD inkludiert in Zeilen **5/6** die exakten Common-/Enumerations-Dateien V2.2; `SystemMonitoringServiceGroup` ab Zeile **8**. Der fehlerhafte gedruckte Word-Querverweis ist **keine** XSD-Deklaration, XML-Elementkarte oder Transportregel. Kein `latest wins`; keine Alias- oder XML-Fail-Ausnahme.

## 3. Unabhängige Versionsgrenzen

Die offizielle [VDV-Publikationsübersicht](https://www.vdv.de/ip-kom-oev.aspx) wurde am **22.11.2026** erneut geprüft und führt **nur die eigenständige VDV 301-2-18 SystemMonitoringService V2.2** (08/2019) auf. **Kein** eigenständiger SMS-Vorgänger und **kein** korrigierter späterer SMS-Nachfolger sind dort belegt. Allgemeine frühere Basisdienstveröffentlichungen gehören nicht automatisch zum selben SMS-Publikationsstamm.

Die Vorwortseiten der offiziellen PDF beschreiben **eine bilinguale Ausgabe**, deutsche und englische Erläuterungen, technische Operationsbeschreibungen nur in Englisch. Es gibt keinen Beleg für separat versionierte deutsche und englische SMS-V2.2-Quellen. **Erste/letzte unabhängig belegte betroffene Version: V2.2; Korrekturgrenze unbekannt, nicht erfinden.** Exakter offizieller Service/Common/Enum V2.2 Dependency-Pool bleibt der einzige gewählte XSD-Pfad.

## 4. Gegenhypothesen und Bewertung

- **Nur Textextraktion/OCR?** Widerlegt durch das echte sichtbare Original-PNG mit frisch geprüftem SHA-256.
- **Versteckter echter Verweis statt gedrucktem Word-Fehler?** Der Fehlertext steht tatsächlich sichtbar neben dem Abbildungsverzeichnis-Eintrag.
- **Anderer XML-Operationsname/Schemafeld?** Nicht belegt; das Fehlwort ist Dokumentgenerierung, kein XML-Wortschatz oder ausführbarer Typ.
- **Weitere betroffene Editionen?** Die offizielle Versions- und Sprachpublikationslage belegt nur die eine V2.2-Ausgabe, keine Ausweitung.
- **Doppelt mit anderen SMS-Findings?** Nein. `DRSMS22-002` (Service-Status-Prosa), `DRSMS22-003` (SystemManagementService-Schreibweise) und `DRSMS22-004` (Req/Resp-Labels) sind getrennte eingefrorene Sachverhalte.

Der historische [EV-146-Run 34026822637](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026822637) und die [Closure 34026992744](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026992744) wurden als **SUCCESS** erneut abgefragt. Revalidierungsquelle `docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_DRSMS22_2026-09-06.md`, Deep Read `docs/pdf_xsd_semantic_audit/deep_read/SMS_V2.2.md`. Dokumentationsfehler ohne XML-Verhaltensauswirkung: **kein neuer ausführbarer Positiv-/Negativ-XML-Test**, kein Runtime-Matcher, kein XSD-Patch.

## 5. Kanonischer Zwischenstand und Gates

Der einzelne `gate_pending`-Commit hält drei Belegregister, `sdk_manifest/manifest_v0.1.json` und `CURRENT_STATE.json` konsistent bei **111/192** vollständigen eindeutigen Source-Locators, **111/111** tatsächlich sichtbaren originalen PDF-Body-Verifikationen, **111/111** unabhängigen Versionsgrenzen, **81** offen.

**Noch ausstehend beim Schreiben dieses Reports:** beide substantiellen GitHub-Gates, danach separater `terminal_clean`-Commit und erneute Erfolgskontrolle **beider** Workflows auf finalem HEAD. Das nächste eingefrorene eindeutige Finding ist **`DRSMS22-002` noch nicht begonnen**. Keine XSD-/SDK-Runtime-Änderung.
