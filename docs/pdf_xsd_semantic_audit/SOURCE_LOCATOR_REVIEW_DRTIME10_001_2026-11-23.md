# DRTIME10-001 — TimeService V1.0: falscher Dokumentverweis im englischen Vorwort

**Audit 2026-11-23; eingefrorene Finding-ID DRTIME10-001, keine Neuanlage.** Quelle: offizielle [VDV-Schrift 301-2-10 TimeService V1.0, 02/2018](https://www.vdv.de/301-2-10sds-v-1-01.pdfx), Source-ID `TIME_V1.0`, historischer Roh-PDF-Pin **SHA-256 d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3**, **515920 Bytes**, originaler Pin-Run **33196758957**. Dieser Zyklus lädt keine PDF-Rohbytes neu und gibt keine neue Roh-Hash-Prüfung aus.

## 1. Exakte Originalfundstelle und sichtbare Body-Autorität

**Original gedruckte Seite 4, Überschriften `Vorwort` und `Foreword`** unmittelbar hintereinander in *derselben* bilingualen Ausgabe (physische PDF-Seite 4 / 0-basierter PDF-Index 3, keine Inhaltsverzeichnis-Nummer als Locator). Deutscher Wortlaut identifiziert `VDV-Schrift 301-2-10` als TimeService. Englischer Wortlaut identifiziert statt dessen `VDV 301-2-1` als TimeService.

Gegenkontrolle: Das eigene Deckblatt trägt `VDV-Schrift 301-2-10`; die gedruckte Seite 8 `Regelwerke – Normen und Empfehlungen` ordnet `VDV 301-2-1` den **Gemeinsamen Datenstrukturen und Aufzählungstypen** zu. Der [offizielle VDV-Katalog](https://www.vdv.de/ip-kom-oev.aspx) listet `VDV 301-2-10 TimeService V1.0` sowie `VDV 301-2-1 Common Data Structures` getrennt. Diese Querverbindung widerlegt die Hypothese zweier legitimer TimeService-Dokumentnummern.

**Quellen- und Sichtprüfungsgrenze:** Das historische erfolgreiche [EV-147, Run 34028395412](https://github.com/MarcLeinenDE/VDV301/actions/runs/34028395412), Artifact **9987794844**, hat das exakt quellengepinnte ursprüngliche gedruckte Original-PDF-Body-Bild physische Seite 4 auf 180 dpi **tatsächlich visuell geprüft**, laut `audit_registry/drtime10_revalidation_evidence_2026-09-06.json`, Original-PNG SHA-256 **1614a270b77c37cd2abb51bbfb84f3626554ff7b60b385c45b3b02ee29d2ac06** (131551 Bytes). Das GitHub-Artefakt ist beim Abruf 2026-11-23 **nicht abgelaufen**, Metadaten `sha256:2fbb9272c55ebbe704ae4736f488af5758bc0cbbbc8902e77d1a46e19b1ffc92`, 579380 Bytes, Run und HEAD `686ce92ede0f1391e04a4260bc7adf98b6ae3103` stimmen mit dem gespeicherten EV147-Evidenzregister überein. Die **aktuellen offiziellen PDF-Texte** wurden unabhängig nachgelesen. Der **neue** Online-Screenshot lieferte **Cache-Miss**. **Keine aktuelle Sichtinspektion des ZIP/PNG-Bildes oder aktuelle Hash-Neuberechnung der Binärdatei** wird behauptet; die exakte originale EV147-Sichtprüfung ist eine wiederverwendete historische Evidenz.

## 2. Unabhängige Versions- und Sprachgrenzen

Am 23.11.2026: VDV-Publikationsindex hat genau **eine eigenständige TimeService-Schrift V1.0 (02/2018)**; eine ältere dedizierte TimeService-PDF und eine spätere korrigierte eigenständige TimeService-Version wurden **nicht** unabhängig festgestellt. Erste und letzte nachgewiesen betroffene dedizierte Ausgabe daher **TimeService V1.0**, kein imaginärer korrigierter Nachfolger.

**Deutsch (same publication):** Vorwort korrekt `301-2-10`, nicht von dieser Finding-ID betroffen. **Englisch:** direkt benachbartes Foreword fälschlich `301-2-1`, betroffen. Der Fehler ist **kein** Unterschied zwischen unabhängigen deutschen und englischen Publikationsversionen, sondern ein einzelner Satzfehler innerhalb eines bilingualen Dokuments.

Historische Kontrolle **VDV 301-2 V1.0, 07/2016**: eine dortige falsche TimeService-Verweisung `301-2-11` wird unter **separater bestehender Finding-ID `DR3012-006`** geführt. VDV-Mitteilung 3002 (10/2016) und die VLS-Schrift 301-2-11 von 05/2017 werden in dessen historischem Audit besprochen. Der Basisdienst ist **kein dedizierter Vorgängertext der hier falschen V1.0-Foreword-Stelle**. Identitäten nicht zusammenwerfen, Fehler nicht doppelt zählen.

## 3. Normative und SDK-Auswirkung

- **Quelle/Authority:** `documentation_only` hinsichtlich dieses Fehlers; realer Dienst ist `TimeService@1.0: protocol_discovery_profile`. Das offizielle TimeService-Dokument definiert **SNTP gemäß RFC 4330** und DNS-SD (`_ibisip_udp._udp`, TXT `sntp-server`), **keinen XML-/XSD-TimeService-Validierungsroot**. Keine XSD-Datei, kein Git-Blob und kein XSD-PASS/FAIL sind für diese Finding-ID relevant.
- **Klassifikation:** `confirmed_pdf_defect` / `document_identity_mismatch`, `documentation_only`, keine neue normative Last.
- **SDK:** bereits bestehende `no_runtime_diagnostic`; keine Änderung an Source-Schema, XML-Annahme, konkreter SNTP-Laufzeitprüfung, Resolver, SDK-Code, Diagnostiktexten oder bestehenden DE/EN-Templates. Der englische Satz darf **nicht** als Grundlage für eine Fehlrouting-Regel Richtung Common-Strukturen dienen.
- **Aktive Widerlegung:** `301-2-1` könnte TimeService als Teilkapitel enthalten? Nein, offizielle Veröffentlichungsidentität, same-page DE-Gegenstück und Common-Kapitelverweis p8 trennen die Dokumente. OCR-Zahlendreher? Historical EV147 sichtbare Originalseite belegt den Fehler; heutige Textextraktion allein ist keine neue visuelle Beweisaufnahme.
- **Tests:** bestehendes [EV147](https://github.com/MarcLeinenDE/VDV301/actions/runs/34028395412) historisch PASS; der neu zu beobachtende Voll-Gate prüft Registerinvarianten. Kein neuer XML-Positiv/Negativ-Test notwendig oder durchgeführt, da hier keine XML-Semantik.

## 4. Canonical source-locator handoff

Einzige neue vollständige kanonische Source-Locator-ID `DRTIME10-001`: **115/192**, Body-Evidenzregister **115/115**, separat geprüftes Versionsgrenzenregister **115/115**, **77** weitere eingefrorene Findings noch ohne vollständige Locator-Dokumentation. Alte 114/192-Meilensteine bleiben historische Snapshots, kein doppelter Fortschritt. Dieser Bericht ist Beleg und nicht eine neue `CURRENT_STATE`-Autorität.

**Gate-Abschluss erst nach verifiziertem `schema-audit-validation` SUCCESS auf dem substantiellen `gate_pending`-HEAD und anschließendem `terminal_clean` plus finalem Handoff-Integrity SUCCESS.** Bei Gateversagen bleibt der Block explizit offen. Nächste eingefrorene Finding-ID nach erfolgreichem Abschluss: **`DRTIME10-002`**, nicht zuvor begonnen.
