# DRS-004 — VDV DoorStateService V2.1: ausschließlich nicht ausführbare Schreibfehler in xs:documentation

**Review am 2026-11-20.** Bereits eingefrorene Identität `DRS-004` (keine neue ID). `primary_surface=xsd`; `primary_issue_kind=documentation_spelling`; `defect_assessment=confirmed_xsd_defect` **nur im Sinne eines redaktionellen Annotationsfehlers**, nicht eines ausführbaren Schemafehlers. `validation_effect=documentation_only,no_runtime_effect`; `sdk_behavior=no_runtime_diagnostic`. Dieser Review **ändert weder XSD noch SDK-Laufzeitlogik**.

## 1. Exakte offizielle XSD-Quelle und fehlerhafte Stellen

Quelle **`VDVde/VDV301@VDV-301-2.1`** Tag, Datei **`IBIS-IP_DoorStateService_V2.1.xsd`**, Git-Blob **`abff0f3960e2ec7a9caaa9ddeb6efff8f4183805`**. Upstream-Tag und ausgewählte Kopie auf `dev/schema-integration` erneut **blobidentisch** geprüft (20.11.2026).

| Original-XSD-Zeile | Position | Fehlerhafte Zeichenfolge (genau wie im Original) | Vergleich mit ausführbarer/normaler Schreibweise |
| --- | --- | --- | --- |
| **44** | `/xs:schema/xs:complexType[@name='DoorStateService.GetDoorOperationStatesResponseStructure']/xs:annotation/xs:documentation` | `DoorStateService.GetDoorOpeationStates` | `DoorStateService.GetDoorOperationStates` |
| **72** | `/xs:schema/xs:complexType[@name='DoorStateService.RetrieveSpecificDoorOperationStateRequestStructure']/xs:annotation/xs:documentation` | `DoorStateService.RetrieveSpecificDoorOperationnState` | `DoorStateService.RetrieveSpecificDoorOperationState` |
| **80** | `/xs:schema/xs:complexType[@name='DoorStateService.RetrieveSpecificDoorOperationStateResponseStructure']/xs:annotation/xs:documentation` | `DoorStateService.RetrieveSpecificDoorOperationnState` | `DoorStateService.RetrieveSpecificDoorOperationState` |
| **80** (zweite Stelle) | dieselbe `xs:documentation`-Annotation | `operationn state` | `operation state` |

**Aktive Widerlegung eines ausführbaren Effekts:** Das gesamte originale 127-Zeilen-DoorState-XSD wurde auf alle drei falschen Zeichenfolgen geprüft: exakt **vier Treffer, ausnahmslos innerhalb von `xs:documentation`**; **null** Treffer in `@name` oder `@type`. In den unmittelbar umgebenden ausführbaren Deklarationen stehen **Zeile 18/19** die GetDoorOperationStates-Elemente, **42** der korrekte GetDoorOperationStatesResponseStructure-Typ, **47** der GetDoorOperationStatesResponseData-Zweig, **26/27** die korrekt geschriebenen RetrieveSpecificDoorOperationState-Request-/Response-Elemente, **70/78** die korrekt geschriebenen Request-/Response-Typen, **75** `DoorID`, **83–84** `DoorOperationState` / `ErrorMessage`. `xs:annotation/xs:documentation` ist erklärender Text, keine ausführbare XSD-Namensdeklaration oder Typreferenz. Ein Tippfehler-Matcher oder Validator-Alias ist **nicht** gerechtfertigt.

Die exakte Historienroute bleibt **`IBIS-IP_DoorStateService_V2.1.xsd` + `IBIS-IP_common_V1.0.xsd` + `IBIS-IP_Enumerations_V1.0.xsd`**. Die direkten Include-Blobs `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c` und `a9bea5bc73003ed91ded8519db06c32c4067831d` wurden erneut gegen `VDV-301-2.1` byteidentisch nachgeprüft; **kein latest-wins**.

## 2. Originäres PDF als unabhängige Kontext- und Schreibweisenkontrolle

Official VDV-Schrift 301-2-15 DoorStateService V2.1 (07/2018), pinned source SHA256 7413c99f2910f125947213561658ae9c808952d5b57700d155b939c899de26e8, 851513 bytes / 16 pages; original EV145 run34026409256 artifact9987189102 ZIP SHA256 77d90917105e6a26cfd05660612ebd0ab2f37db6a1b5fc49b86bce95a8e179f9. Web PDF screenshot cache missed on 2026-11-20; existing exact-byte-pinned 180dpi original source renders were physically visually inspected with PNG SHA256 freshly rechecked. Full PDF raw bytes not re-downloaded/rehashed this cycle.

- **Gedruckte S. 10**, Original-Body **§2.4 „Data Structures of Operation GetDoorOperationStates“** und **§2.4.2 „Response“, Tabelle 5 „Description of DoorStateService.GetDoorOperationStatesResponse“**: sichtbarer Operationsname **`GetDoorOperationStates`**, nicht das XSD-Annotations-Typo `GetDoorOpeationStates`. Gerenderte Original-PNG SHA256 **`9973a258e9eac95c241aa0632c3239dd4d3b3f185559504376a7f1bb397421a0`**.
- **Gedruckte S. 12**, Original-Body **§2.8 „Data Structures of Operation RetrieveSpecificDoorOperationState“**, **§2.8.1 „Request“, Tabelle 10**, **§2.8.2 „Response“, Tabelle 11**: die **Überschrift** und die ausführbaren Strukturzeilen der Originaltabellen verwenden `RetrieveSpecificDoorOperationState`. Die beschreibende Operationszeile der Tabellen ist ihrerseits teils verkürzt bzw. falsch geschrieben (`RetrieveDoorOpereationState`) und gehört zur **getrennten** eingefrorenen ID **`DRDOOR21-001`**; sie darf nicht als XSD-Annotations-Typo von `DRS-004` doppelt gezählt werden. Original-PNG SHA256 **`e90660e9ec8ec21bb955f761aff0b73de01576f80f1c81555f6f446d927fcb5f`**.
- Technische Operationen der **einen bilingualen VDV-301-2-15-Ausgabe** sind laut **gedruckter S.4 Vorwort** auf Englisch beschrieben. Deshalb keine unabhängig existierende zweite deutsche technische PDF-Fassung behaupten.

Hier ist die amtliche PDF **nur eine belegte Kontext- und Orthografiekontrolle**; der Defekt sitzt **exklusiv** in `xs:documentation` der offiziellen XSD. Der PDF-Body wurde nicht als Quelle eines neuen PDF-Defekts gedeutet. Der Web-Viewer-Screenshot hatte einen Cache-Miss; der ordnungsgemäß gepinnte und per SHA kontrollierte **Originalrender-Fallback** wurde tatsächlich visuell gelesen.

## 3. Versionsgrenzen unabhängig geprüft

Die am **20.11.2026** frisch abgerufene offizielle [VDV-Publikationsübersicht](https://www.vdv.de/ip-kom-oev.aspx) listet als **eigenständige** **301-2-15 DoorStateService**-Ausgabe **nur V2.1**; das abgeglichene offizielle XSD-Release `VDV-301-2.1` trägt die Schreibfehler auf den exakten Zeilen 44/72/80. Frühere allgemeine `VDV301-2`-Basisdienstveröffentlichungen (V1.0 DE+EN und V2.0) sind keine früheren eigenständigen DoorStateService-`301-2-15`-Revisionen. **Kein früherer direkt vergleichbarer separater DoorStateService-Vorgänger oder später korrigierter offizieller Nachfolger** wurde unabhängig belegt; aus anderen XSD-Dateiversionen, `master` oder nicht offiziellen Kandidaten wird **keine** stille Korrektur- oder Authority-Grenze behauptet. Deutschsprachiges Vorwort + englischsprachige technische Abschnitte sind Bestandteile **derselben** V2.1-Publikation, keine eigenständigen Sprachtitel.

## 4. Vorhandene Validierung und Gegenhypothesen

Das eingefrorene Original-Finding `DRS-004` wurde im [DoorStateService-Deep-Read](deep_read/DOOR_V2.1.md) und im [EV145-Revalidierungsbericht](FINDING_REVALIDATION_DRS_V21_2026-09-06.md) mit `context_verified`/nicht ausführbarem Annotationstext protokolliert; der originale [EV-145-Run #34026409256](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026409256) und Closure [#34026674927](https://github.com/MarcLeinenDE/VDV301/actions/runs/34026674927) wurden erneut erfolgreich abgefragt. EV145 revalidierte alle 50 XSDs; **für DRS-004 ist kein eigenständiger Positiv-/Negativ-XML-Test erforderlich**, weil nur Dokumentationstext betroffen ist. Der jetzige Review kontrollierte XSD-Quelltext und Blob-Identität, PDF-Originallayout und existierende Run-Ergebnisse, **aber führte keinen neuen XML-Test aus**.

- Gegenhypothese „`GetDoorOpeationStates` wird als alternativer XML-Operationsname benötigt“: **falsch**, ausschließlich `xs:documentation`; echte Namen `GetDoorOperationStates` korrekt.
- Gegenhypothese „`RetrieveSpecificDoorOperationnState` benennt einen anderen Operationstyp“: **falsch**, 2-mal Annotation; die exakten ausführbaren Operationen/Strukturen haben nur **ein n** in `OperationState`.
- Gegenhypothese „das `operationn state` ändert das Element `DoorOperationState`“: **falsch**, `DoorOperationState` ist am ausführbaren Responsezweig Zeile 83 unverändert und korrekt.
- Gegenhypothese „PDF-Tabellenbeschreibung ist ebenfalls ein `DRS-004`-Defekt“: **verworfen**; getrennte ID `DRDOOR21-001` bewahrt den tatsächlich anderen PDF-Fehler.

## 5. Konsequenz für die kanonische Auditkette

`DRS-004` bleibt ein **bestätigter redaktioneller XSD-Dokumentationsfehler ohne Validator-/Runtime-Auswirkung** (`no_runtime_diagnostic`). Ein Schemafehler im Sinne ungültiger XSD-Namen oder XML-Instanzen ist **nicht** belegt. **Keine XSD-Änderung, kein SDK-Matcher, keine Aliasregel, keine Finding-ID-Neuanlage.**

Dieser Report begleitet genau **einen** vollständigen **`gate_pending`-Auditblock** mit Source-Locator-/sichtbarem Original-PDF-Body-/Versionsgrenzen-Registry plus SDK-Metadaten und `CURRENT_STATE.json`: **110/192** einzigartige Locators, **110/110** Body-Checks, **110/110** unabhängig bestätigte Versionsgrenzen, **82** weitere Findings. Danach zwei substanzielle GitHub-Gates, separater `terminal_clean`-Commit und **beide** Gates auf finalem HEAD, ai-mem-PR nur für geprüfte Fakten. **Nächstes eingefrorenes Finding: `DRSMS22-001` noch nicht begonnen.**
