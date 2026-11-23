# DRSMS22-002 — SystemMonitoringService V2.2: Device/Service-Verwechslung im ServiceStatus-Text

**Review am 2026-11-23.** Vorhandene eingefrorene Finding-ID `DRSMS22-002`, keine neue Identität. `primary_surface=cross_artifact`, `primary_issue_kind=semantic_contradiction`, `defect_assessment=confirmed_pdf_defect`; `validation_effect=documentation_only,pdf_can_mislead_implementation,no_runtime_effect`; `sdk_behavior=no_runtime_diagnostic`. Keine XSD-/SDK-Runtime-Korrektur.

## 1. Exakte Originalquelle und sichtbare PDF-Stellen

Offizielle **VDV-Schrift 301-2-18 SystemMonitoringService V2.2 (08/2019)**: https://www.vdv.de/301-2-18-sdes-v2-2-systemmonitoringservice.pdfx. Originalpin `SMS_V2.2`, SHA-256 `996f639a81cb91ad20a8e78b6213e7c85d41ff0ec42caba4208d6c4652b140f4`, **847416 Bytes** (`audit_registry/pdf_source_pins_v0.1.json`).

Die sichtbare offizielle Original-PDF hat **drei textliche Fehlzuordnungen an zwei tatsächlich gedruckten Stellen**:

1. **Druckseite 10, §2.5 „Data Structure of Operation GetSystemStatus“, §2.5.2 „Response“, Tabelle 4 „Description of SystemMonitoringService.GetServiceStatusResponse“**, Tabellenkopfzeile `SystemMonitoringService.GetServiceStatusResponse`: **„Response structure with the service state of all devices in the system“**. Für den Service-Zustand werden fälschlich **devices** als Zielobjekte genannt.
2. **Druckseite 10, dieselbe §2.5.2/Tabelle 4**, Datensatz a `SystemMonitoringService.GetServiceStatusResponseData`: **„Detailed response structure with the device state of all services in the system (cf. table below)“**. Fälschlich **device state** statt service state.
3. **Druckseite 11, fortgesetzte §2.5.2 „Response“, Tabelle 5 „Description of SystemMonitoringService.GetServiceStatusResponseData“**, Kopfzeile `SystemMonitoringService.GetServiceStatusResponseData`: **„Detailed response structure with the device state of all services in the system“**, erneut falsches **device state**.

Der **sichtbare Gegenkontext** ist entscheidend: Druckseite 9 **§2.1/Tabelle 1** benennt `GetServiceStatus` und `SystemMonitoringService.GetServiceStatusResponseStructure` ausdrücklich; Druckseite 10 **§2.2.2 Tabellen 2–3** verwendet Device-Begriffe korrekt für `GetDeviceStatus`. Die konkrete Mitgliedszeile **`ServiceIdentificationWithStateList`** ist auf der sichtbaren **Druckseite 11 Tabelle 5** vorhanden. Die Beschreibungen ändern nicht die technischen Tabellenmember.

Die offizielle Live-PDF-Screenshot-Ansicht meldete **Cache miss**, deshalb nach verbindlichem Renderfallback das bereits für die exakt gepinnte Quelle erzeugte **EV-146**-Originalartefakt verwendet und **direkt visuell geprüft**: [EV-146 PASS, run 34026822637](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026822637), Artefakt **9987318510**, original `drsms22-ev146` ZIP SHA-256 **`181ff01b16dae43ec2826299e6f14717aef1668d66491b6051ae07661ee607f6`**, am 2026-11-23 neu berechnet. In der ZIP enthaltene ursprüngliche 180-dpi-Bilder (SHA-256 jeweils neu berechnet und tatsächlich visuell betrachtet):

| Original-Druckseite | PNG SHA-256 | Kontext |
| --- | --- | --- |
| 9 | `6f813ae55fd3acc28e99f055978c504b9759e03b1cfb52a133adaf696a2f3b79` | §2.1 / Tabelle 1, offizielle Operationstrennung |
| 10 | `97bf0974fa9a1ef98fed84d6c7c844afa804a7091d29061affbe5359205cc563` | §2.2.2/Tabelle 2–3 und §2.5.2/Tabelle 4 |
| 11 | `02b26dddd0fa57785ee5e35757a03dc6f1b1a595ae006cdb5ffe66481b4a2b7f` | §2.5.2/Tabelle 5 |

`page_text/page-10-layout.txt` und `page_text/page-11-layout.txt` aus EV-146 stimmen mit dem sichtbaren Layout überein, sind aber **nicht** alleinige Belegautorität. **Keine neue Original-PDF-Rohbytes-Beschaffung oder PDF-SHA-Neuberechnung** behauptet: PDF-Pin historisch, gepinnte Render-ZIP und tatsächliche Seiten-PNGs neu geprüft.

## 2. Exakte XSD-Autorität und Semantik

Offizielle **`VDVde/VDV301@VDV-301-2.2`**-Tag-Dateien am 2026-11-23 neu abgefragt, Git-Blob-Identität mit `dev/schema-integration` bestätigt:

| Datei | Git-Blob |
| --- | --- |
| `IBIS-IP_SystemMonitoringService_V2.2.xsd` | `d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c` |
| `IBIS-IP_common_V2.2.xsd` | `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` |
| `IBIS-IP_Enumerations_V2.2.xsd` | `2a23b512379b18e8f122ac1272cef8229fb86283` |

Die Service-XSD inkludiert Common V2.2 und Enumerations V2.2 explizit **Zeilen 5/6**. **Service-XSD Zeilen 30–41**: `GetServiceStatusResponseStructure` enthält die Wahl `GetServiceStatusResponseData` oder `OperationErrorMessage`; im Datenzweig **Zeile 40** ist `ServiceIdentificationWithStateList` vom Typ `ServiceIdentificationWithStateListStructure`. Der getrennte echte Device-Zweig hat **Zeile 26** `DeviceSpecificationWithStateList` für `GetDeviceStatusResponseData`.

**Common V2.2 Zeilen 490–499**: `ServiceIdentificationWithStateStructure` ist eine Sequenz aus **`ServiceIdentification` + `ServiceState`** (Zeilen 492/493), Liste aus `ServiceIdentificationWithState` (Zeile 498); **kein `DeviceState`** in dieser Struktur. Zum Kontrast hat **Common V2.2 Zeilen 267–275** die separate `DeviceSpecificationWithStateStructure` mit `DeviceSpecification` + `DeviceState`. Damit sind Device- und Service-Semantik im selben exakten offiziellen Profil klar getrennt; eine andere Common-Version oder sprachliche Interpretation ist nicht nötig.

## 3. Unabhängige Versionsgrenzen und Sprache

Die aktuelle **[offizielle VDV-IP-KOM-ÖV-Publikationsübersicht](https://www.vdv.de/ip-kom-oev.aspx)** wurde am **2026-11-23** erneut geprüft: als **eigenständige 301-2-18 SystemMonitoringService-Publikation** ist nur **V2.2** gelistet. Keine ältere eigenständige SMS-Ausgabe und kein späterer korrigierter offizieller Nachfolger wurden bestätigt. Frühere allgemeine Base Services sind nicht automatisch eigene SMS-Versionen. Ein **bilinguales offizielles PDF** (DE/EN Vorwort, technische Operationen auf Englisch) ist keine nachgewiesene getrennte Sprachversionslinie. **Erste/letzte belegte betroffene Version V2.2; keine erfundene Vorgänger-/Korrekturgrenze.**

## 4. Aktive Widerlegung, historische Tests und Abgrenzung

- **Hypothese „DeviceState ist im GetServiceStatus eine korrekte alternative Semantik“:** widerlegt durch dieselbe exakte Common V2.2 `ServiceIdentificationWithStateStructure` mit `ServiceState`, ohne `DeviceState`, und durch eindeutig getrennte Device- und Service-Datenzweige.
- **Hypothese „die OCR-/Layoutdarstellung hat Device-Verweise erzeugt“:** widerlegt durch die drei tatsächlich sichtbaren Originaltabellen-Zeilen auf Druckseiten 10/11.
- **Hypothese „eine neuere XSD oder andere Version korrigiert das Verhalten“:** hier nicht zulässig; die offizielle gepinnte V2.2-Schemafamilie ist eindeutig, kein `latest wins`.
- **Abgrenzung:** Der auf PDF-Druckseite 10 sichtbar irreführende §2.5-Titel **`GetSystemStatus`** ist **nicht** Gegenstand dieser ID; er gehört zum separaten vorhandenen SMS-Befund **`SMS-002`** (GetServiceStatus/GetSystemStatus). Ebenso sind `DRSMS22-001` (PDF-Textmarke), `DRSMS22-003` und `DRSMS22-004` getrennt. `a/b -1:1` bezeichnet XML-Choice, nicht eine negative Kardinalität.

Historische [EV-146 run34026822637 PASS](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026822637), [Closure 34026992744 SUCCESS](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026992744), [EV-116 run33269006407 SUCCESS](https://github.com/MarcLeinenDE/VDV301/actions/runs/33269006407) erneut bestätigt; EV146 belegt den visuellen Nachweis und die Common-Semantik, EV116 das bestehende exakte XML-Schema-Verhalten. **Keine frische eigenständige XML-Positiv-/Negativ-Instanzprüfung** im aktuellen Auditzyklus. Der Befund ist eine **semantische PDF-Copy/Paste-Verwechslung** mit potenziell irreführender Implementierungsdokumentation, aber **keiner neuen XML-Validierungsregel**. XSD normativ; keine SDK-Änderung, Alias oder Matcher.

## 5. Handoff und Gate-Anforderung

Ein eigenes `gate_pending`-Arbeitscommit aktualisiert den Source-Locator-, Original-Body- und Versionsgrenzen-Registereintrag, `sdk_manifest/manifest_v0.1.json` und `00_START_HERE/CURRENT_STATE.json` auf **112/192** (112/112 Body, 112/112 Boundary; **80** verbleibend). Nach **beiden substantiellen GitHub-Gates** folgt ein **separater `terminal_clean`-Statuscommit** und anschließend die Erfolgskontrolle **beider** finalen HEAD-Gates. Noch nicht begonnen: nächstes eingefrorenes Finding **`DRSMS22-003`**. Erst nach finaler CI eine geprüfte ai-mem-PR; keine automatische Hintergrundsynchronisierung.
