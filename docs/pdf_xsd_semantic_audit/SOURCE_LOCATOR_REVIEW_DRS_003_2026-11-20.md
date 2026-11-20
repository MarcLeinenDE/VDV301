# DRS-003 — originaler DoorStateService-Get-Request-Body, XSD-anyType und Versionsgrenze (2026-11-20)

**Bestehende Finding-ID:** `DRS-003`, keine neue Finding-Identität. **Bewertung:** `defect_assessment=undetermined`, `confidence=confirmed` nur für die *nachgewiesene XML-Schema-Semantik*, **nicht** für eine Ursache/Remediation. `sdk_behavior=valid_with_advisory`, Laufzeit-Zuordnung `reviewed_not_implemented`. Keine XSD-/SDK-Implementierungsänderung.

## 1. Exakte PDF-Quelle: sichtbare Originalseite und Body-Locator

Offizielle VDV-Schrift **301-2-15 DoorStateService V2.1, 07/2018**, Quelle `DOOR_V2.1`, https://www.vdv.de/301-2-15-sd-v2-1-doorstateservice.pdfx; PDF-Bytepin **SHA256 `7413c99f2910f125947213561658ae9c808952d5b57700d155b939c899de26e8`**, **851513 Bytes**, 16 Seiten; kanonische Pin-Registry und Source-Pin-Run **33241913638**.

Der Web-PDF-Screenshot des Originals lieferte am 20.11.2026 für die benötigten Seiten einen **Cache-Miss**. Gemäß dem verbindlichen Render-Fallback wurde das **bereits bestehende** originalgebundene GitHub-Renderartefakt **EV-145, Run 34026409256, Artifact 9987189102** wiederverwendet. ZIP-**SHA256 `77d90917105e6a26cfd05660612ebd0ab2f37db6a1b5fc49b86bce95a8e179f9`**, original p9/p10-PNG-Hashes und `ev145_results.json` wurden am 20.11.2026 unabhängig erneut berechnet und verglichen; die gerenderten Bilder wurden **selbst visuell gelesen**, nicht nur OCR/TOC:

- **Gedruckte Seite 9**, sichtbarer **§2.1 „Data Structures of Operation GetDoorOpenStates“ / §2.1.1 „Request“**. Der Text lautet **„Because of being a Get operation, there is no request structure for this operation.“**. Auf derselben Seite nennt die sichtbare **Tabelle 1 „Description of Operations of DoorStateService“** für `GetDoorOpenStates`, Zeile `Req.`, als verwendete Struktur **`-`**, aber `Resp.` den expliziten Typ `DoorStateService.GetDoorOpenStatesResponseStructure`. Original-PNG 180dpi SHA `699fc2f28e1e901d8f0078004418e6e065d232756ab1cb3bf37ea16a3895d983`.
- **Gedruckte Seite 10**, sichtbarer **§2.4 „Data Structures of Operation GetDoorOperationStates“ / §2.4.1 „Request“**; derselbe sichtbare Satz **„Because of being a Get operation, there is no request structure for this operation.“**. Die zugehörige **Tabelle 1 auf Seite 9** zeigt für `GetDoorOperationStates`, Zeile `Req.`, ebenfalls **`-`**, obwohl `Resp.` ausdrücklich `DoorStateService.GetDoorOperationStatesResponseStructure` hat. Original-PNG 180dpi SHA `9973a258e9eac95c241aa0632c3239dd4d3b3f185559504376a7f1bb397421a0`.
- Die sichtbaren **§2.1.2 auf S.9** und **§2.4.2 auf S.10** beschreiben durchaus echte **Response**-Strukturen (Tabelle 2 bzw. Tabelle 5); „no request structure“ betrifft nur die Get-Request-Seite.

**Transparente Rohdaten-Grenze:** Die amtlichen PDF-Rohbytes wurden in diesem Bearbeitungsblock **nicht erneut separat heruntergeladen oder selbst SHA256-gehasht**. Die Publikationsidentität stammt aus dem früheren geprüften Quellpin und der jetzt neu gehashten Original-Renderkette. Screenshots aus dem aktuellen Web-PDF-Reader waren wegen Cache-Miss nicht nutzbar, der geprüfte Fallback aber vollständig.

## 2. Exakte offizielle XSD-Route und W3C-Defaultsemantik

Offizielles Upstream-Release **`VDVde/VDV301@VDV-301-2.1`**, `IBIS-IP_DoorStateService_V2.1.xsd`, Git-Blob **`abff0f3960e2ec7a9caaa9ddeb6efff8f4183805`**: am 20.11.2026 gegen `dev/schema-integration` **byte-identisch** überprüft. Die direkten Includes **`IBIS-IP_common_V1.0.xsd`** Git-Blob **`194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`** sowie **`IBIS-IP_Enumerations_V1.0.xsd`** Git-Blob **`a9bea5bc73003ed91ded8519db06c32c4067831d`** sind in diesem offiziellen Release ebenfalls tagidentisch; historische V1.0-Abhängigkeiten werden **nicht** durch neuere Varianten ersetzt.

Im **lokalen** `xs:group[@name='DoorStateServiceGroup']/xs:sequence` stehen:
- **Zeile 12:** `<xs:element name="DoorStateService.GetDoorOpenStatesRequest"/>`.
- **Zeile 18:** `<xs:element name="DoorStateService.GetDoorOperationStatesRequest"/>`.

Beide lokalen Deklarationen besitzen weder `type`-Attribut noch untergeordnetes `xs:complexType`/`xs:simpleType`. Nach **W3C XML Schema Part 1 / Element Declaration** und **W3C XML Schema Primer §5.5** gilt in diesem Fall standardmäßig **`xs:anyType`**, also gerade **kein explizites Empty-Content-Modell**. Autoritäten: https://www.w3.org/TR/xmlschema-1/ und https://www.w3.org/TR/xmlschema-0/ .

**Unverzichtbare Grenze:** Die beiden genannten Deklarationen sind **lokale Mitglieder von `DoorStateServiceGroup`**, keine allein aus dieser XSD abgeleiteten frei verwendbaren **globalen XML-Dokumentroots**. Die XML-Schema-Defaultsemantik gilt für die genannten Deklarationen; daraus wird kein eigener HTTP-/SOAP- oder globaler Request-Root erfunden.

## 3. Bereits vorhandene ausführbare Verifikation und aktive Widerlegung

Bestehender **EV-111** erfolgreicher GitHub-Run **33242337308**, Job **99073684198**, Werkzeug `tools/validate_door_v21_ev111.py`; **EV-145** erfolgreicher Run **34026409256**, Job **101468048441** hat genau diesen EV111-Check erneut erfolgreich ausgeführt. Am 20.11.2026 wurden GitHub-Run-Metadaten, Quellskript und `ev111_rerun.log` direkt aus dem erneut SHA-geprüften Original-EV145-Artefakt geprüft; **kein neuer lokaler XML-Testlauf behauptet**.

Das EV111-Werkzeug prüft zuerst die exakten lokalen Deklarationen **per XPath** auf Abwesenheit von `type` und Inline-Typ, kompiliert die echte offizielle XSD und verwendet dann ausschließlich für die gezielte Defaultsemantik-Prüfung eine **nicht normative globale Probe-Deklaration derselben unveränderten Elementform**. Beide Probe-Requests:
- `DoorStateService.GetDoorOpenStatesRequest`: leer **valid**, `<UnexpectedPayload><Nested>…</Nested></UnexpectedPayload>` **valid**;
- `DoorStateService.GetDoorOperationStatesRequest`: leer **valid**, derselbe unerwartete verschachtelte Inhalt **valid**.

**Gegenhypothese A:** „No request structure“ aus der PDF erzwingt automatisch XML-leeren Elementinhalt. **Widerlegt** durch den fehlenden Typ in der ausgewählten XSD und die `xs:anyType`-Semantik. **Gegenhypothese B:** die leeren Probe-Root-Typen könnten als echte VDV-Request-Dokumentroots angesehen werden. **Ausgeschlossen**: das Testskript kennzeichnet die aus technischen Gründen globalen Probe-Elemente ausdrücklich als **nicht normativ**; reale Deklarationen bleiben lokal. **Gegenhypothese C:** die permissive XSD ist nachweislich ein VDV-Fehler. **Nicht belegt**: es ist unklar, ob das Modell absichtlich großzügig blieb. Daher `undetermined` statt spekulativer `confirmed_xsd_defect`.

## 4. Eigenständige Versions- und Sprachgrenzenprüfung

Die am 20.11.2026 erneut eingesehene offizielle [VDV-Publikationsliste](https://www.vdv.de/ip-kom-oev.aspx) weist als **eigenständige** `VDV 301-2-15 DoorStateService`-Veröffentlichung ausschließlich **V2.1** aus. Die allgemeinen früheren VDV-301-2-V1.0-DE/EN- und V2.0-Basisdienste sind **keine früheren Standalone-Revisionen** der eigens veröffentlichten `301-2-15`-Schrift. Ein eigenständiger direkter Vorgänger oder ein späterer korrigierter Nachfolger wurde **nicht unabhängig belegt**; keine Korrektur, Version oder XSD-Promote erfinden.

Eine physische **bilinguale Ausgabe**: Vorwort DE/EN, technische Operationen/Datenstrukturen **nur Englisch** (offizielle S.4). Die sichtbaren Request-Stellen sind daher in der englischen technischen Sprachspur derselben Ausgabe, nicht zwei getrennte DE/EN-Dokumente. Der Scope schließt nicht etwa den nachfolgenden `DRS-004`-Annotierungsfehler ein.

## 5. SDK- und Auditwirkung

Die vorhandene Klassifikation bleibt unverändert: `defect_assessment=undetermined` bei **bestätigter** permissiver XSD-Semantik, `sdk_behavior=valid_with_advisory`, `activation_class=xsd_valid_advisory`, `implementation_state=reviewed_not_implemented`, `required_precondition=xsd_result_valid`.

**Keine Negativvalidierung bei nichtleerem Get-Request, solange er nach der exakt ausgewählten XSD gültig ist.** Ein späterer SDK-Hinweis darf nur einen bereits **gültigen** XML-Befund erläutern und niemals zusätzliche XSD-Restriktionen oder XML-Autoreparaturen einschleusen. **Keine XSD-Datei, kein produktiver Matcher, keine eingefrorenen Finding-IDs oder EV-Proben verändert.**

Genau **eine bestehende** Finding-ID `DRS-003` wird nun Source-Locator-vollständig: **109/192**, sichtbar geprüfter Body **109/109**, unabhängig geprüfte Versionsgrenzen **109/109**, **83 offen**. Diese Register, das SDK-Metadatenmanifest und `CURRENT_STATE.json` werden **im selben substantiellen, absturzsicheren `gate_pending`-Commit** geschrieben. Nach **beiden GitHub-Gates** erfolgt ein **separater** `terminal_clean`-Commit, für den **beide** finalen Gates auf exakt diesem neuen HEAD ebenfalls erfolgreich sein müssen. Danach verifizierter ai-mem-PR; nächstes eindeutig eingefrorenes Finding **`DRS-004`**.
