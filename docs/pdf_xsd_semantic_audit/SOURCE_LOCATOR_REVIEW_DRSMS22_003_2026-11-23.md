# DRSMS22-003 — SystemMonitoringService V2.2: `SystemManagmentService` im PDF-Versionsverlauf

**Review 2026-11-23.** Bereits eingefrorene Finding-ID `DRSMS22-003`, keine neue Identität. `primary_surface=pdf`, `primary_issue_kind=documentation_spelling`, `defect_assessment=confirmed_pdf_defect`; `validation_effect=documentation_only,no_runtime_effect`, `sdk_behavior=no_runtime_diagnostic`. Keinerlei Änderung an offiziellen XSDs, XML-Konformität oder SDK-Runtime.

## 1. Gepinnter Original-PDF-Body — die eigentliche Fundstelle und die Gegenprobe

Offizielle [VDV-Schrift 301-2-18 SystemMonitoringService V2.2 (08/2019)](https://www.vdv.de/301-2-18-sdes-v2-2-systemmonitoringservice.pdfx), `SMS_V2.2`, ursprünglicher PDF-SHA256 **`996f639a81cb91ad20a8e78b6213e7c85d41ff0ec42caba4208d6c4652b140f4`**, **847416 Bytes** aus dem kanonischen Originalquellen-Pin.

- **Gedruckte Seite 12**: Original-Body **„3 Versionshistorie / Version History“**, **§3.1 „Version 2.2“**, **§3.1.1 „Funktionale Erweiterungen / Functional Upgrade“**. Im ersten Strichpunkt wird `SystemManagementService` exakt **zweimal** als **`SystemManagmentService`** gedruckt: einmal in der **deutschen**, einmal in der **englischen** Formulierung. Die beiden Vorkommen gehören **zur selben bilingualen Veröffentlichung**, nicht zu getrennten Sprachversionen.
- **Gedruckte Seite 13**: Tatsächlich sichtbarer Original-Body **„Regelwerke – Normen und Empfehlungen / References“**, **Referenz-Eintrag (3) „VDV 301-2-0“**. Die dort aufgeführten historischen **Basisdienste V2.0** benennen **`SystemManagementService` korrekt**, neben `DeviceManagementService` und `SystemDocumentationService`. Der unmittelbare Kontext dieser selben amtlichen Publikation widerspricht einem angeblich zulässigen technischen Alias.

Sowohl der sichtbare falsche Original-Drucktext auf Seite 12 als auch die tatsächlich sichtbare korrekte Referenz auf Seite 13 wurden am **2026-11-23** erneut manuell visuell gelesen. Die [interaktive Original-PDF-Screenshot-Abfrage](https://www.vdv.de/301-2-18-sdes-v2-2-systemmonitoringservice.pdfx) lieferte einen **Cache-Miss**, weshalb gemäß verbindlichem Fallback das **bereits exakt Original-PDF-gepinnte** alte Evidence-Renderartefakt wiederverwendet wurde:

- [EV-146 Original-GitHub-Run #34026822637 – SUCCESS](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026822637), Artefakt **9987318510**, ZIP `drsms22-ev146`, am 23.11.2026 **frisch berechnete ZIP SHA-256 `181ff01b16dae43ec2826299e6f14717aef1668d66491b6051ae07661ee607f6`**.
- **Druckseite 12** `renders/page-12.png`, 180 dpi, am 23.11.2026 frisch berechnete SHA-256 **`41515d4afc0455e0628128f47eecba3d88364858882c5551b2616af72528addf`**; exakt identisch mit `ev146_results.json:fresh_render_hashes[12]`.
- **Druckseite 13** `renders/page-13.png`, 180 dpi, am 23.11.2026 frisch berechnete SHA-256 **`d323b92c7b84c67bb4eeb5fcb2559b8d5fb94dd19635e210c4ed9106791b2ba2`**; exakt identisch mit `ev146_results.json:fresh_render_hashes[13]`.
- `page_text/page-12-layout.txt` und `page_text/page-13-layout.txt` bestätigen die jeweilige Zeichenfolge **als zusätzliche Extraktionsgegenprobe**. Textextraktion allein ist **nicht** visuelle Belegautorität.

**Präzise Evidenzgrenze:** Das historisch geprüfte PDF-Pin-Hash und die Rohgröße sind weiterhin registriert; die PDF-Rohbytes wurden in **diesem** Review nicht erneut heruntergeladen oder neu gehasht. ZIP, EV146-Manifest und beide tatsächlich geprüften Seiten-PNGs dagegen neu und erfolgreich SHA-verifiziert.

## 2. Versionierte XSD-/Upstream-Autorität ohne erfundene Typen

Drei Original-XSD-Blobs aus dem **offiziellen Upstream-Tag `VDVde/VDV301@VDV-301-2.2`** wurden am 23.11.2026 unabhängig mit dem aktuellen `dev/schema-integration` abgeglichen und **byteidentisch** bestätigt:

| Datei / Rolle | Original-Git-Blob |
| --- | --- |
| `IBIS-IP_SystemMonitoringService_V2.2.xsd` (ausgewähltes Service-XSD) | `d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c` |
| `IBIS-IP_common_V2.2.xsd` (historische direkte Abhängigkeit) | `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` |
| `IBIS-IP_Enumerations_V2.2.xsd` (historische direkte Abhängigkeit) | `2a23b512379b18e8f122ac1272cef8229fb86283` |

Die aktuelle SMS-XSD enthält auf **Zeilen 5–6** die exakt V2.2-versionierten `xs:include`-Anweisungen. Die Dienstgruppe ab **Zeile 8** deklariert `SystemMonitoringService.GetDeviceStatusResponse` und `SystemMonitoringService.GetServiceStatusResponse`, nicht `SystemManagmentService`. **Wichtig:** `SystemManagementService` wird hier **nicht** fälschlich als durch diese SMS-XSD definierter ausführbarer Service bezeichnet. Sein korrekt geschriebener historischer Referenzname wird aus dem **gedruckten PDF-Eintrag (3)** und aus der aktuellen offiziellen Basisdienst-Publikationsübersicht abgeleitet. Ein fehlerhaftes Wort im beschreibenden PDF-Versionsabschnitt ist weder ein `@name`-Attribut noch eine alternative ausführbare XSD-Regel.

## 3. Versions-, Sprachen- und Publikationsgrenze

Die aktuelle [offizielle VDV-Publikationsübersicht](https://www.vdv.de/ip-kom-oev.aspx) wurde **2026-11-23** geprüft: **eine eigenständige VDV 301-2-18 SystemMonitoringService V2.2**-Veröffentlichung; **kein** eigenständiger SMS-Vorgänger und **keine** später korrigierte eigenständige SMS-Ausgabe belegt. Die ältere offiziell gelistete **VDV 301-2 Basisdienste V2.0** ist ein **anderer Publikationstyp**, kein älteres eigenständiges SMS 301-2-18 PDF; sie unterstützt den richtigen historischen **SystemManagementService**-Namen, aber begründet **keine** zusätzlichen vom Schreibfehler betroffenen SMS-Versionen.

Der Vorworttext des SMS V2.2 ist ausdrücklich **bilingual**, technische Operationsabschnitte sind englischsprachig. Die falsche Zeichenfolge tritt im **deutschen und englischen Versionsverlauf derselben Veröffentlichung** auf. Keine separat versionierte deutsche oder englische SMS-Technik-PDF-Variante angenommen. **Einzige positiv nachgewiesene betroffene dedizierte Version: V2.2; frühere/sichere Korrekturgrenzen unbekannt, ausdrücklich nicht extrapoliert.**

## 4. Aktive Falsifikation, Abgrenzung und vorhandene CI-Belege

1. **„Die fehlerhafte Schreibweise ist gültiger technischer Alternativdienstname“**: verworfen. Die Originalreferenz (3) p13 benennt `SystemManagementService` korrekt, ebenso der amtliche Basisdienstkatalog, während p12 innerhalb einer erklärenden Versionsnotiz `SystemManagmentService` druckt; kein Alias-Nachweis.
2. **„Nur PDF-Textgewinnungs-/OCR-Artefakt“**: verworfen durch zwei hashgeprüfte, sichtbar betrachtete Original-Druckseiten; Layout-Text nur zusätzliche Absicherung.
3. **„Betroffen ist die aktuelle SMS-XSD-Operation“**: verworfen; deren ausführbare Response-Elemente heißen `SystemMonitoringService.*` und sind davon unberührt. Keine Umdeutung des älteren Basisdienstes als ein SMS-XSD-Element.
4. **„Das im selben Versionsabschnitt gedruckte `302-2` muss mitkorrigiert oder doppelt gezählt werden“**: verworfen, weil es sich um eine **andere historische PDF-Referenzabweichung** handelt (Deep Read `FR-SMS22-OBS-005`) und **nicht** Teil der eingefrorenen ID `DRSMS22-003` ist. `DRSMS22-001/-002/-004` bleiben eigenständige Findings.

[Historischer EV-146 run34026822637](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026822637) und [Closure run34026992744](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026992744) am 2026-11-23 erneut **SUCCESS**; [EV-116 run33269006407](https://github.com/MarcLeinenDE/VDV301/actions/runs/33269006407) ebenfalls **SUCCESS** auf der seinerzeit geprüften ausgewählten Schemafamilie. **Keine neue eigenständige XML-Positiv-/Negativ-Testmatrix** für den neuen Locator ausgeführt oder behauptet; für den reinen PDF-Schreibfehler gibt es keinen veränderten ausführbaren XML-Verhaltenstest. Bestehender Freeze: `docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_DRSMS22_2026-09-06.md`, `docs/pdf_xsd_semantic_audit/deep_read/SMS_V2.2.md`; keine XSD-/Runtime-Änderung und keine neue Finding-ID.

## 5. Kanonischer Gate- und Handoff-Zustand

Der **eine** substanzielle `gate_pending`-Commit synchronisiert die drei kanonischen Source-Locator-/sichtbarer Original-PDF-Body-/Versionsgrenzenregister mit `sdk_manifest/manifest_v0.1.json` und `00_START_HERE/CURRENT_STATE.json` auf **113/192 vollständige einzigartige Source-Locators, 113/113 originale Body-Prüfungen, 113/113 eigenständig verifizierte Versionsgrenzen, 79 offene Findings**. Nach **beiden** erfolgreichen substantiven GitHub-Gates folgt der **separate** `terminal_clean`-Status-Commit und beide finalen HEAD-Gates müssen separat erfolgreich verifiziert werden. Erst danach ai-mem-PR, keine automatische Synchronisierung. **Nächster noch unbegonnener Finding: `DRSMS22-004`.**
