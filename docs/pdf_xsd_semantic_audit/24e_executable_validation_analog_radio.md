# EV-105 - executable validation of AnalogRadio ARA-003

Status: completed for the explicitly selected candidate/integration profile.

## Evidence run

```text
GitHub Actions run: 33111831627
head tested: 86e3592968f24cfa59e05ace625f64886ca3ae89
job: 98656347989
environment: Ubuntu 24.04 / Python 3.12.14 / lxml 6.1.2
EV-105 status: 0 / PASS
```

Harness:

```text
tools/validate_analog_radio_ev105.py
```

Authority boundary:

```text
IBIS-IP_AnalogRadioService_V2.4.xsd is candidate/integration material from open upstream PR #27.
The result below applies only when that candidate profile is explicitly selected.
It is not promoted to an official release schema by this test.
```

## ARA-003 - Transmitter cardinality

Candidate schema declaration:

```text
AnalogRadioService.RadioTelegramStructure
  Transmitter type=TransmitterStructure minOccurs=0 maxOccurs=1
```

Executable results:

```text
PASS: candidate AnalogRadioService V2.4 XSD compiles
PASS: Transmitter declaration is 0:1
PASS: otherwise complete SendTelegram without Transmitter validates
PASS: otherwise complete SendTelegram with Transmitter validates
```

Conclusion:

```text
ARA-003 = executable-confirmed for the candidate/integration profile.
The XSD permits omission of Transmitter, while the checked PDF table states 1:1.
```

No XSD was changed.

## Phase result

With EV-105, the planned XSD executable-evidence sequence is complete:

```text
EV-001/EV-002 baseline compile and legacy roots
EV-101 PCS-001
EV-102 CE-018
EV-103 video compositor findings
EV-104 TrainSet modelling/context
EV-105 AnalogRadio cardinality
```

Next phase:

```text
runtime/protocol validation profiles
- HTTP/XML transport and Content-Type
- DNS-SD/service discovery
- TimeService/SNTP
- Video RTSP/RTP boundary
```
