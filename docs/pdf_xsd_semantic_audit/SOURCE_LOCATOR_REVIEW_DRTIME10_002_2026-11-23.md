# DRTIME10-002 — TimeService V1.0: englischer Ausschluss zyklischer Uhrzeitübertragung fehlt

**Review 2026-11-23; bestehende eingefrorene Finding-ID.** Dokument: [offizielle VDV-Schrift 301-2-10 TimeService V1.0 (02/2018)](https://www.vdv.de/301-2-10sds-v-1-01.pdfx), `TIME_V1.0`, historischer Original-Roh-PDF-Pin SHA256 `d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3`, 515920 Bytes (Pin-Run 33196758957).

## Sichtbarer Originalkörper: gedruckte Seite 6, §1

Originaldruckseite **6**, tatsächlicher Body **§1 „Dienst TimeService“** direkt gefolgt von **„Service TimeService“**, physischer PDF-Index 5, keine TOC-Inferenz.

Deutsch nach der SNTP-Synchronisationsbeschreibung: **„Ein zyklisches Versenden der aktuellen Uhrzeit ist darüber hinaus nicht vorgesehen.“** Im englischen Nachbarabschnitt folgt auf **„The actual form of time synchronization is then processed using the SNTP protocol.“** unmittelbar die Zeitzonen-TXT-Passage; **kein entsprechender no-cyclic-Satz**. Die deutschen und englischen Abschnitte nennen ausdrücklich SNTP/RFC 4330, DNS-SD, `sntp-server` und `_ibisip_udp._udp`. Fehlender englischer Satz ≠ englische Erlaubnis zu einem eigenen zyklischen Broadcast.

**Frische visuelle Prüfung:** Die originale, öffentlich ausgelieferte VDV-PDF-Seite 6 wurde am 2026-11-23 als Live-Screenshot tatsächlich sichtbar geprüft. Die Roh-PDF-Datei wurde in dieser Sitzung **nicht neu heruntergeladen oder SHA-verifiziert**, der aktuelle Screenshot wurde **nicht binär gehasht**. Unabhängiger historischer exact-byte-Beleg: [EV-147 run34028395412 PASS](https://github.com/MarcLeinenDE/VDV301/actions/runs/34028395412), Artifact 9987794844, gedruckte Originalseite 6 bei 180dpi PNG SHA256 `099a2198df048ef805ea37ac559fc1adec24e9b622fd2e7b421ac31d8bbb0cfd` (402182 Bytes), am 2026-09-06 ursprünglich visuell geprüft, Metadaten-ZIP-Digest `sha256:2fbb9272c55ebbe704ae4736f488af5758bc0cbbbc8902e77d1a46e19b1ffc92`. Kein neuer ZIP-Download behauptet.

## Versionsgrenzen, Sprachen und Gegenhypothesen

Offizieller [VDV IP-KOM-ÖV-Katalog](https://www.vdv.de/ip-kom-oev.aspx) am 2026-11-23: **nur dedizierte TimeService-V1.0-Publikation** (02/2018). Kein separat herausgegebener TimeService-Vorgänger und kein nachweislich korrigierter Nachfolger. Die 2016er allgemeine VDV-301-2-Basisschrift ist keine zweite selbständige TimeService-Ausgabe. DE und EN innerhalb derselben V1.0-PDF wurden **unabhängig** geprüft: DE ausdrücklich kein weiterer zyklischer Zeitversand, EN Satz **ausgelassen**, nicht gegenteilig ausgesagt. Keine Sprach- oder Versionsscope-Erfindung.

Aktive Falsifikation: Englischtext auf p6 vollständig neben Deutsch verglichen (Satz nicht an anderer Stelle innerhalb des Abschnitts); Original-Sichtkontrolle verhindert bloße OCR-Lücke; `_ibisip_udp._udp` ist im VDV-Text DNS-SD-Discovery-Typ, keine Broadcast-Payload-Definition; SNTP wird ausdrücklich als eigentliche Synchronisation genannt. Keine positive alternative Zeitübertragung im englischen Text, daher keine andere Normvorgabe.

## Authority, SDK und vorhandener RV-003

`TimeService@V1.0`: `protocol_discovery_profile` mit VDV-gewähltem **SNTP RFC4330** und DNS-SD; **kein TimeService-XML-XSD-Root**. `documentation_only`, `confirmed_pdf_defect`, `sdk_behavior=no_runtime_diagnostic` für dieses Finding. Keine neuen XML-Positiv-/Negativtests erforderlich, keine Mutation an XSDs oder SDK-Code, kein neuer DRTIME10-002-spezifischer Matcher.

**Präzise historisch korrigierter Teststand:** Das EV147-Dokument vom 2026-09-06 behauptet irrtümlich, ein RV-003-Prüfer bzw. `cyclic_time_broadcast_expected` existiere an seinem HEAD nicht. Unabhängige GitHub-Abfrage **desselben** originalen EV147-Commits `686ce92ede0f1391e04a4260bc7adf98b6ae3103` bestätigt hingegen `tools/validate_time_runtime_rv003.py` (Blob `ff6e3fcd35d4c2f6bff760b3e86f5adb0e72156c`) und `tools/runtime_time_profile.py` (Blob `acd28ca0bd6ac1917b3d2db29745555b7e17d8dd`) einschließlich `cyclic_time_broadcast_expected()==False`. Aktueller [Schema-Gate 45170321287](https://github.com/MarcLeinenDE/VDV301/actions/runs/45170321287) führte RV-003 **SUCCESS** aus, mit konkretem `OK TimeService does not expect cyclic transmission of current time`. Detaillierte Korrektur: [historischer Overlay](CORRECTION_RV003_HISTORICAL_EVIDENCE_DRTIME10_002_2026-11-23.md). Der vorhandene allgemeine deterministische RV003-Check ist **kein** neuer Finding-spezifischer Runtime-Trigger oder Live-Fahrzeugtest. Altes Evidenzregister/Altreport nicht heimlich überschrieben.

## Kanonischer Fortschritt und Handoff

Genau eine zusätzliche Finding-ID: **116/192 Source Locators vollständig**, **116/116 Originalbody-Evidenz**, **116/116 unabhängige Versionsgrenzen**, **76 offen**. Bereits existierende semantische Klassifikation in Wirkung/Scope unverändert, nur falscher historischer Testhinweis berichtigt und Semantic-Git-Blob-Pins synchronisiert.

Nach substanziellem `gate_pending`-Commit kompletten Schema-Audit-/Handoff-Gate beobachten, gesonderten `terminal_clean`-Commit nur nach SUCCESS schreiben und dessen finale Gates getrennt bestätigen. **Nächstes Finding `DRTIME10-003` noch nicht begonnen.**
