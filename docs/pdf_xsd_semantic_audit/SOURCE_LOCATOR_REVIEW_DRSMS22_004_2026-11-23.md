# DRSMS22-004 — SystemMonitoringService V2.2: fehlende Req./Resp.-Labels bei UnsubscribeServiceStatus

**Review 2026-11-23.** Bestehender eingefrorener Finding `DRSMS22-004` (keine neue ID), `primary_surface=pdf`, `primary_issue_kind=editorial_residue`, `defect_assessment=confirmed_pdf_defect`; `validation_effect=documentation_only,pdf_can_mislead_implementation,no_runtime_effect`, `sdk_behavior=no_runtime_diagnostic`. Der Fehler betrifft ausschließlich die fehlenden **Tabellenspalten-Bezeichnungen**, nicht die Strukturen, nicht eine fehlende XML-Operation und nicht den SDK-Validator.

## 1. Offizielles Original-PDF: tatsächlich sichtbare Tabelle statt TOC-Inferenz

Offizielle [VDV-Schrift 301-2-18 SystemMonitoringService V2.2, 08/2019](https://www.vdv.de/301-2-18-sdes-v2-2-systemmonitoringservice.pdfx); kanonischer ursprünglicher `SMS_V2.2`-PDF-Pin **SHA-256 `996f639a81cb91ad20a8e78b6213e7c85d41ff0ec42caba4208d6c4652b140f4`**, **847416 Bytes**.

**Gedruckte Originalseite 9, sichtbarer Body §2 „Operations of the SystemMonitoringService“ → §2.1 „Operationen SystemMonitoringService“, „Tabelle 1 Beschreibung von Operationen des SystemMonitoringService / Description of Operations at the SystemMonitoringService“.** Die Spaltenüberschriften lauten `Operation`, `Request/Response`, `Verwendeter Datentyp, Datenstruktur / Used data types, Data structures`.

In der **letzten Operation `UnsubscribeServiceStatus`** enthält Tabelle 1 die **beiden vollständigen typnamengebenden Datenstruktur-Zeilen**:

- Erste Strukturzeile: **`UnsubscribeRequestStructure`**; die dazugehörige mittlere Zelle ist sichtbar **leer** statt **`Req.`**.
- Zweite Strukturzeile: **`UnsubscribeResponseStructure`**; die dazugehörige mittlere Zelle ist sichtbar **leer** statt **`Resp.`**.

Das sind **zwei fehlende Tabellen-Labels**, **keine fehlenden Anforderungs-/Antwortdatenstrukturen**. Die angrenzenden `SubscribeServiceStatus`-Zeilen sowie die davorstehenden `UnsubscribeDeviceStatus`-Zeilen enthalten in derselben mittleren Spalte die erwarteten Labels `Req.` und `Resp.`. Das isolierte Layoutmuster weist auf einen Tabellen-Redaktions-/Satzfehler hin.

Die offizielle Live-Screenshot-PDF-Ansicht konnte Druckseite 9 wegen **Cache-Miss** nicht anzeigen. Gemäß `AUDIT_WORKFLOW_CONTRACT.md` wurde daher das historisch exakt quellengepinnte original gerenderte **EV-146**-Fallback-Artefakt verwendet und die **tatsächliche gedruckte Tabelle visuell gelesen**, nicht aus TOC, Historie, Sequenz oder Textextraktion erschlossen:

- [EV-146 Original-Run 34026822637 – SUCCESS](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026822637), Artifact **9987318510** `drsms22-ev146`, ZIP-Datei `drsms22-ev146-drsm003.zip` neu aus diesem unveränderten Artifact geladen, am 23.11.2026 **SHA-256 `181ff01b16dae43ec2826299e6f14717aef1668d66491b6051ae07661ee607f6`** frisch verifiziert (994106 Bytes).
- `renders/page-09.png` (180 dpi) **SHA-256 `6f813ae55fd3acc28e99f055978c504b9759e03b1cfb52a133adaf696a2f3b79`**, **166033 Bytes**, exakt zu `ev146_results.json:fresh_render_hashes[9]` und am 23.11.2026 **direkt visuell geprüft**.
- `page_text/page-09-layout.txt`, SHA-256 `39ebc38e197d3813612a87d01260359f2418ac021d2438ea96e7f4179206479c`, und `unsubscribe_service_status_segment.txt`, SHA-256 `d96f260bea04867fedae83ab993dac7ca84fe7dd34fd5a65537475e35e42f5d0`, bestätigen den Unterschied nur **sekundär**; tatsächliche Belegautorität ist das sichtbare Originalbild.
- **Keine frische Roh-PDF-Herunterladung oder neue Roh-PDF-SHA-Prüfung** in diesem Block behauptet: Der PDF-Pin stammt aus der früheren Originalquellenprüfung. Das unveränderte EV-146 ZIP und die Originalseite wurden neu gehasht.

**Visuelle Kontextprobe Seite 11:** Die tatsächlich sichtbare Originalseite 11, **§2.7 „Data Structure of Operation UnsubscribeSystemStatus“**, verweist für das Abmelden von Abonnements explizit auf Strukturen aus **VDV 301-2-1** (allgemeine Strukturen). Seite 11 wurde über dasselbe EV146 Original-PNG `renders/page-11.png`, SHA-256 `02b26dddd0fa57785ee5e35757a03dc6f1b1a595ae006cdb5ffe66481b4a2b7f`, visuell betrachtet. **Wichtig:** Die gegenüber Tabelle 1 andere Titelbezeichnung `UnsubscribeSystemStatus` in §2.7 ist **nicht** Gegenstand dieser eingefrorenen Finding-ID und wird hier nicht automatisch als Synonym/Normvorgabe umgedeutet.

## 2. Exakte offizielle XSD-Autorität — generische Common-Strukturen vorhanden

Unabhängig am 23.11.2026 abgefragte `VDVde/VDV301@VDV-301-2.2` Original-Tag-Dateien, alle **Git-Blob-identisch** mit `MarcLeinenDE/VDV301@dev/schema-integration`:

| Original XSD | SHA-1 Git-Blob | Prüffunktion |
| --- | --- | --- |
| `IBIS-IP_SystemMonitoringService_V2.2.xsd` | `d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c` | ausgewählter offizieller Dienstprofileinstieg; direkte `xs:include` auf Common/Enumerations **Zeilen 5–6** |
| `IBIS-IP_common_V2.2.xsd` | `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` | normative allgemeine Unsubscribe-Strukturen, siehe genaue Zeilen unten |
| `IBIS-IP_Enumerations_V2.2.xsd` | `2a23b512379b18e8f122ac1272cef8229fb86283` | exakt ausgewählte historische Enum-Abhängigkeit, keine `latest wins` |

**Common V2.2 Zeilen 898–905:** Deklariert das globale Element `UnsubscribeRequest` als `UnsubscribeRequestStructure`. Der komplexe Typ **`UnsubscribeRequestStructure`** enthält `Client-IP-Address` (erforderlich), `ReplyPort` (optional), `ReplyPath` (optional). XPath-Komponente `/xs:schema/xs:complexType[@name='UnsubscribeRequestStructure']`.

**Common V2.2 Zeilen 906–912:** Deklariert das globale Element `UnsubscribeResponse` als `UnsubscribeResponseStructure`. Der komplexe Typ **`UnsubscribeResponseStructure`** enthält `Active` (erforderlich) und `OperationErrorMessage` (optional). XPath `/xs:schema/xs:complexType[@name='UnsubscribeResponseStructure']`.

Der **SMS-Service-XSD-Teil enthält bewusst nur die spezifischen GetDeviceStatus/GetServiceStatus-Response-Elemente** (Gruppe und Definitionen **Zeilen 7–42**) und nutzt generische Subscribe-/Unsubscribe-Datenstrukturen aus Common. Er muss **nicht** zusätzlich einen dienstspezifischen `UnsubscribeServiceStatusRequestStructure`-Typ definieren. Die PDF-Tabelle selbst identifiziert die zwei generischen Datentypen zutreffend. Eine fehlende Tabellenbeschriftung darf **nicht** in einen fehlenden XSD-Typ, eine fehlende Operation, eine falsche Kardinalität oder eine neue Runtime-Ausnahme umgedeutet werden.

## 3. Unabhängiger Versions-/Sprachenabgleich

Am **2026-11-23** wurde der [offizielle VDV-IP-KOM-ÖV-Katalog](https://www.vdv.de/ip-kom-oev.aspx) erneut abgefragt: Für die **eigenständige VDV 301-2-18 SystemMonitoringService** ist nur **V2.2** gelistet. Keine frühere eigenständige SMS-PDF-Ausgabe und kein korrigierter dedizierter späterer SMS-Nachfolger wurden unabhängig bestätigt. Allgemeine Common-V2.1/V2.3/V2.4 oder ältere Basisdienst-Dokumente sind **keine** eigenständigen SMS-Versionen und ändern die historische V2.2-Autorität nicht. **Erste und letzte belegte betroffene Ausgabe: SMS V2.2; kein erfundener Vorgänger-/Nachfolger-Grenzpunkt.**

Das offizielle Vorwort der SMS-V2.2-Publikation bezeichnet **eine bilinguale Veröffentlichung**, in der die technischen Operationsbeschreibungen **englischsprachig** sind. Der Fehler liegt **einmal in der einen gemeinsamen Tabelle 1**, keine separat belegte fehlerhafte DE- und EN-Technikversion. Der gewählte exakt versionsgepinnte offizielle XSD-Pfad bleibt alleinige XML-Normautorität.

## 4. Aktive Falsifikation, historische Tests, SDK-Entscheid

- **„Die Operation hat keine Request-Struktur“**: widerlegt durch sichtbar vorhandene `UnsubscribeRequestStructure` in Tabelle 1 und den expliziten Common-V2.2-Typ auf Zeilen 899–905.
- **„Die Antwortstruktur fehlt“**: widerlegt durch sichtbar vorhandene `UnsubscribeResponseStructure` in derselben Zeile und Common-V2.2-Typ auf Zeilen 907–912.
- **„Req./Resp. fehlt nur in OCR/Text-Extraktion“**: widerlegt durch tatsächlich visuell inspizierte **leere Zellen** beider Original-PDF-Tabellenzeilen, bei gefüllten Nachbarzellen.
- **„Ein dienstspezifisches XML-Element fehlt, weil die Service-XSD nur Get-Antworten enthält“**: widerlegt durch belegte generische Common-Abonnementstrukturen und die ausdrückliche PDF-Verweisung auf VDV 301-2-1; keine implizite Service-XSD-Pflicht.
- **„Die andere §2.7-Überschrift beweist ein alternatives gültiges Get-/Unsubscribe-Schema“**: unzulässig; diese Titelabweichung ist außerhalb der isolierten Tabellenlabel-ID. Ebenso sind die anderen eingefrorenen `DRSMS22-001/-002/-003`-Befunde getrennt. Die PDF-Notation `a/b -1:1` bleibt XML-Choice-Notation, nicht negative Kardinalität.

Historische **[EV-146 run 34026822637](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026822637)**, **[Closure run 34026992744](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026992744)**, **[EV-116 run 33269006407](https://github.com/MarcLeinenDE/VDV301/actions/runs/33269006407)** alle frühere **SUCCESS/PASS**-Belege, nicht als frisch ausgeführte XML-Instanztests bezeichnet. Im aktuellen Zyklus wurde **kein neuer XML-Positiv-/Negativtest** durchgeführt, weil reine Tabellenlayout-Labels weder Schema-Akzeptanz noch Laufzeitverhalten ändern. Weder offizielles XSD noch SDK-Validierungslogik verändert; die vorhandenen zweisprachigen diagnostischen Textbausteine bleiben erhalten, **`no_runtime_diagnostic`**.

## 5. Kanonischer Gate-/Handoff-Plan

Ein einziger substantieller `gate_pending`-Commit aktualisiert Source-Locator-, Original-PDF-Body- und Versionsgrenzenregister plus `sdk_manifest/manifest_v0.1.json` und `00_START_HERE/CURRENT_STATE.json` auf **114/192 vollständige eindeutige Source-Locators**, **114/114 tatsächlich sichtbar belegte Original-PDF-Bodys**, **114/114 unabhängig geprüfte Versionsgrenzen**, **78 verbleibende** Findings. Nach **beiden** erfolgreichen substantiellen GitHub-Gates folgt getrennt `terminal_clean` nur durch Status- und SDK-Metadaten-Commit. Beide **finalen HEAD-Gates** müssen dann erneut unabhängig erfolgreich sein. Nach Review und Merge geprüfte ai-mem-PR, keine automatische Hintergrundsync. **Nächster eindeutiger eingefrorener Finding: `DRTIME10-001`, nicht begonnen.**
