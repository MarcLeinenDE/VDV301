# DRTIME10-003 – Originale englische `cd. 1`-Querverweis-Unstimmigkeit in der TimeService-Versionshistorie

**Datum:** 2026-11-24. **Eindeutige eingefrorene Finding-ID:** `DRTIME10-003` (kein neuer Finding-Typ). **Status:** Originaldruck visuell anhand erneut verifizierter source-pinned EV-147-Originalbilder kontrolliert; technische Folgerung rein dokumentarisch. CI-Gates nach nachfolgendem `gate_pending`-Commit ausstehend.

## 1. Exakt ausgewählte Quelle und Original-PDF-Body

Offizielle [VDV-Schrift 301-2-10 TimeService V1.0 (02/2018)](https://www.vdv.de/301-2-10sds-v-1-01.pdfx), Quellen-ID `TIME_V1.0`, originaler offizieller PDF-Rohbyte-Pin **SHA-256 `d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3`**, **515920 Bytes**, ursprünglicher Pin-Run `33196758957`. **Die Roh-PDF-Datei selbst wurde im aktuellen Zyklus nicht neu heruntergeladen/gehasht; der unveränderte historische Byte-Pin wird nicht als frisch überprüfte Original-PDF-Binärdatei ausgegeben.**

**Aktuell 2026-11-24 neu geprüfter exakter Renderbeweis:** GitHub [EV-147, Run 34028395412](https://github.com/MarcLeinenDE/VDV301/actions/runs/34028395412), Artifact **9987794844** `drtime10-ev147`, vollständig frisch heruntergeladene **ZIP 579380 Bytes**, SHA-256 **`2fbb9272c55ebbe704ae4736f488af5758bc0cbbbc8902e77d1a46e19b1ffc92`**. Dieser Wert stimmt exakt mit dem vorhandenen EV147-GitHub-Digest/ursprünglichem Evidenzregister überein.

Die Originalbilder wurden aus diesem ZIP **neu extrahiert, gegen die EV147-Original-Hashes erneut SHA-256-geprüft und direkt visuell angesehen**:

| Originaldruckseite | Originalbild | SHA-256 | Bytes |
|---|---|---|---:|
| **7**, Befund | `renders/page-07.png` | `daf92ecdb9370957c772a73e46a016835a1d8e7e171915deea88288f53d395fd` | 88405 |
| **6**, reales Querverweisziel | `renders/page-06.png` | `099a2198df048ef805ea37ac559fc1adec24e9b622fd2e7b421ac31d8bbb0cfd` | 402182 |

Die interaktive Live-PDF-Screenshot-Funktion lieferte am 2026-11-24 für Druckseite 7 einen **Cache miss**; die gemäß `AUDIT_WORKFLOW_CONTRACT` zulässige **verifizierte bestehende exakt quellengebundene EV147-Fallback-Bilddatei** wurde deshalb verwendet. Die Layoutabbildungen sind nicht aus PDF-Extraktion, TOC oder numerischer Reihenfolge rekonstruiert, sondern selbst visuell untersucht.

**Tatsächliche Überschriften auf Originaldruckseite 7:** `2 Versionshistorie` → `2.1 Version 1.0` → `2.1.2 Technische Ergänzungen/Korrekturen / Technical Upgrade/Corrections`. Unter derselben Bullet-Position sind unmittelbar benachbart:

- Deutsch: `Typ für Service-Discovery definiert:_ibisip_udp._udp (vgl. 1)`.
- Englisch: `define Type for Service-Discovery: _ibisip_udp._udp (cd. 1)`.

**Tatsächliches referenziertes Ziel:** Originaldruckseite **6**, sichtbare echte Überschrift `1 Dienst TimeService` und daneben `Service TimeService`, enthält ausdrücklich `_ibisip_udp._udp` als **Service-Discovery-Typ für DNS-SD**, während Uhrzeitabgleich über SNTP/RFC 4330 erfolgt. Diese geprüfte §1-Fundstelle ist eine **Referenzziel-Gegenprobe**, keine neue zweite Fehlstelle.

## 2. Aktive Widerlegung und genaue Zuschreibungsgrenze

- **Nur Text-/OCR-Fehler?** Nein. `cd. 1` ist im originalen 180dpi-PNG deutlich gedruckt und stimmt mit der sekundären Textversion überein.
- **Technisch alternativ gültiger Discovery-Typ?** Nein. Die beiden Historienzeilen enthalten **denselben** `_ibisip_udp._udp`-Token. Der eigentliche Diensttext §1 bestätigt genau diesen DNS-SD-Typ. `cd. 1` steht ausschließlich in Klammern als vermutlicher Querverweisrest und ist **kein Bestandteil des Service-Discovery-Namens**.
- **Tatsächliches Ziel fehlt?** Nein: gedruckte Seite 6 zeigt die eigene echte Überschrift §1 und denselben Typ.
- **Legitime abweichende englische Publikationsversion?** Nein: Deutsch und Englisch stehen unmittelbar nebeneinander in derselben official bilingual V1.0-Ausgabe.
- **Ist ein exakter Soll-Ersatztext bewiesen?** **Nein.** Deutsch `vgl. 1` legt einen Abschnittsvergleich nahe; welches konkrete englische Wort/Abkürzung anstelle `cd.` beabsichtigt wurde, wird nicht durch ein autoritatives VDV-Korrigendum belegt. Deshalb **keine** automatische Festsetzung etwa einer vermeintlichen englischen `cf. 1`-Korrektur. Die an sich plausibelste Interpretation wird von der normativen Ersatzautorität getrennt.

**Klassifikation:** `primary_issue_kind=editorial_residue`, `confirmed_pdf_defect`, `documentation_only` und `no_runtime_effect`. Bestehende semantische Klassifikation und vollständige DE-/EN-Diagnostik bleiben **unverändert**, auch im historischen Originalbefund `DRTIME10-003` war Ersatztext absichtlich `null`. Keine neuen Findings oder Alias-Tokens.

## 3. Unabhängige Versions- und Sprachgrenzen

[Offizieller VDV IP-KOM-ÖV-Publikationskatalog](https://www.vdv.de/ip-kom-oev.aspx) am **2026-11-24** geprüft: für die eigenständige **VDV 301-2-10 TimeService**-Dienstschrift nur **V1.0 (02/2018)**. Ein separat publizierter TimeService-Vorgänger beziehungsweise später korrigierter Nachfolger ist nicht belegt. Historische allgemeine VDV301-2-Basisdienst-Veröffentlichungen oder spätere Common-/Konventionseditionen sind **keine** selbstständigen neuen 301-2-10-TimeService-Publikationsversionen.

**DE-Spur:** derselbe p7-Historienblock mit `(vgl. 1)`, Abschnitt 1 existiert und ist technisch passend. **EN-Spur:** im direkt nachfolgenden Text derselben V1.0-Ausgabe `(cd. 1)` als inkonsistenter Querverweisrest. Kein belegter Versionseffekt jenseits dieser einzigen eigenständigen V1.0-Veröffentlichung und keine Behauptung einer später korrigierten Version.

## 4. XSD-/SDK-/Runtime-Folge und Testabgrenzung

`TimeService@1.0` ist ein **`protocol_discovery_profile`** (DNS-SD-Service-Discovery, SNTP nach explizit referenziertem **RFC4330**), **ohne TimeService-XML/XSD-Schema-Autorität**. Im exakt ausgewählten Protokolltext ist `_ibisip_udp._udp` unverändert. Für `DRTIME10-003` ist der vorhandene `runtime_match.state=not_applicable`, `sdk_behavior=no_runtime_diagnostic`; es wird **kein** Runtime-Matcher, kein SNTP/Discovery-Verhalten, kein Routing und keine XML-Gültigkeitsregel aus `cd. 1` erzeugt.

Der bereits existierende allgemeine RV-003-Deterministikcheck darf als **unabhängige bestehende Profilprüfung**, nicht als diesem redaktionellen Fehler neu zugeordnetes positives/negatives XML-Beweispaar bezeichnet werden. Keine neuen XSDs, kein SDK-Code, keine XML-Testinstanzen und kein Hardware-Live-Test in diesem Block.

## 5. Fortschritt und Gates

Exakt **eine** bereits eingefrorene Finding-ID wird source-locator-komplett: **117/192** eindeutige Locators, **117/117** gültige sichtbare Body-Belege und **117/117** unabhängig geprüfte Versionsgrenzen, **75** verbleibend. Originalbefunde und frühere 116/192-Meilensteine bleiben erhalten.

Der Block zählt erst nach `schema-audit-validation` und `handoff-integrity` auf dem sachlichen `gate_pending`-HEAD sowie anschließendem getrennten `terminal_clean`-Commit und beiden finalen Erfolgsnachweisen auf dem tatsächlichen finalen HEAD als abgeschlossen. **Nächstes eingefrorenes Finding nach erfolgreicher Schließung: `DRTRAINSET21-001`, nicht begonnen.**
