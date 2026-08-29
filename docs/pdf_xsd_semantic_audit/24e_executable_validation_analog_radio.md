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

## Current-route revalidation under the Deep Read Evidence Gate

The original EV-105 run remains provenance evidence, but its historical head still had the PR-30 candidate blob at the root path `IBIS-IP_common_V2.3.xsd`.

A later canonical full-suite run reran the same checker after the Common V2.3 authority split:

```text
run: 33228250613
job: 99036090357
head: 97a117a2b03fa2bc78f7fedb7eb2d31bd81ec419
AnalogRadioService V2.4: 48fb303b80936d2d762f0889ce0c359e04c16e5b
Common V2.3 official:     0d8926c4063c12de9a5e68b6f0addaab35a55dc1
Enumerations V2.2:       2a23b512379b18e8f122ac1272cef8229fb86283
result: PASS
```

The run explicitly compiled `IBIS-IP_AnalogRadioService_V2.4.xsd`, confirmed `Transmitter` 0:1, accepted SendTelegram both without and with Transmitter, and the same full suite compiled 50/50 repository root XSDs.

Therefore ARA-003 is executable-confirmed under the current Evidence Gate without allocating a new EV ID. The result is still candidate/integration behavior only and must not be described as official V2.4 release conformance.
