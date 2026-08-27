#!/usr/bin/env python3
"""Executable evidence for EV-103 video-service compositor findings.

This harness does not modify or reinterpret the VDV301 schemas. It validates
minimal XSD-shaped positive samples and PDF-shaped multi-field samples against
the exact selected V2.0 schemas. The VideoRecording V2.4 candidate is used only
as an explanatory control and remains candidate/integration authority.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Case:
    name: str
    xml: str
    expected_valid: bool


def compile_schema(filename: str) -> etree.XMLSchema:
    return etree.XMLSchema(etree.parse(str(ROOT / filename)))


def check(schema: etree.XMLSchema, case: Case) -> bool:
    doc = etree.fromstring(case.xml.encode("utf-8"))
    valid = bool(schema.validate(doc))
    if valid == case.expected_valid:
        expectation = "valid" if case.expected_valid else "invalid"
        print(f"OK  {case.name} (expected {expectation})")
        if not valid and schema.error_log.last_error is not None:
            print(f"    evidence: {schema.error_log.last_error}")
        return True

    expectation = "valid" if case.expected_valid else "invalid"
    print(f"ERR {case.name} (expected {expectation}, got {'valid' if valid else 'invalid'})")
    if schema.error_log.last_error is not None:
        print(f"    {schema.error_log.last_error}")
    return False


def live_cases() -> list[Case]:
    return [
        Case(
            "VLS-002 single StreamID allowed by xs:choice",
            """<VideoLiveService.ListAllLiveStreamsResponse>
  <ListAllLiveStreamsData>
    <StreamID><Value>1</Value></StreamID>
  </ListAllLiveStreamsData>
</VideoLiveService.ListAllLiveStreamsResponse>""",
            True,
        ),
        Case(
            "VLS-002 PDF-shaped StreamID+CameraName+rtspURI rejected",
            """<VideoLiveService.ListAllLiveStreamsResponse>
  <ListAllLiveStreamsData>
    <StreamID><Value>1</Value></StreamID>
    <CameraName><Value>Front camera</Value></CameraName>
    <rtspURI><Value>rtsp://192.0.2.10/live</Value></rtspURI>
  </ListAllLiveStreamsData>
</VideoLiveService.ListAllLiveStreamsResponse>""",
            False,
        ),
        Case(
            "VLS-002 complete PDF-shaped LiveStreamData rejected",
            """<VideoLiveService.ListAllLiveStreamsResponse>
  <ListAllLiveStreamsData>
    <StreamID><Value>1</Value></StreamID>
    <CameraName><Value>Front camera</Value></CameraName>
    <CameraType><Value>Interior</Value></CameraType>
    <CameraCurrentState>Connected</CameraCurrentState>
    <rtspURI><Value>rtsp://192.0.2.10/live</Value></rtspURI>
    <VideoWidth><Value>1920</Value></VideoWidth>
    <VideoHeight><Value>1080</Value></VideoHeight>
    <VideoCodec>H264</VideoCodec>
    <FramesPerSecond><Value>25</Value></FramesPerSecond>
    <Bitrate><Value>4000000</Value></Bitrate>
    <Mirrored><Value>false</Value></Mirrored>
    <Flipped><Value>false</Value></Flipped>
    <Rotation><Value>0</Value></Rotation>
    <Quality><Value>100</Value></Quality>
  </ListAllLiveStreamsData>
</VideoLiveService.ListAllLiveStreamsResponse>""",
            False,
        ),
    ]


def recording_v20_cases() -> list[Case]:
    return [
        Case(
            "VRS-003 V2.0 single State allowed by xs:choice",
            """<VideoRecordingService.GetVideoRecordingStateResponse>
  <State>RRM</State>
</VideoRecordingService.GetVideoRecordingStateResponse>""",
            True,
        ),
        Case(
            "VRS-003 V2.0 State+AlarmArchiveFillLevel rejected",
            """<VideoRecordingService.GetVideoRecordingStateResponse>
  <State>RRM</State>
  <AlarmArchiveFillLevel><Value>50</Value></AlarmArchiveFillLevel>
</VideoRecordingService.GetVideoRecordingStateResponse>""",
            False,
        ),
        Case(
            "VRS-003 V2.0 State+StartStopMode rejected",
            """<VideoRecordingService.GetVideoRecordingStateResponse>
  <State>RRM</State>
  <StartStopMode>IBIS-IP</StartStopMode>
</VideoRecordingService.GetVideoRecordingStateResponse>""",
            False,
        ),
    ]


def recording_v24_control_cases() -> list[Case]:
    return [
        Case(
            "VRS-003 V2.4 candidate control accepts grouped state fields",
            """<VideoRecordingService.GetVideoRecordingStateResponse>
  <VideoRecordingState>
    <State>RRM</State>
    <AlarmArchiveFillLevel><Value>50</Value></AlarmArchiveFillLevel>
    <StartStopMode>IBIS-IP</StartStopMode>
  </VideoRecordingState>
</VideoRecordingService.GetVideoRecordingStateResponse>""",
            True,
        ),
    ]


def display_cases() -> list[Case]:
    return [
        Case(
            "VDS-002 single ViewID allowed by xs:choice",
            """<VideoDisplayService.ListViewCapabilitiesResponse>
  <ViewID><Value>1</Value></ViewID>
</VideoDisplayService.ListViewCapabilitiesResponse>""",
            True,
        ),
        Case(
            "VDS-002 PDF-shaped ViewID+ViewName+ViewType rejected",
            """<VideoDisplayService.ListViewCapabilitiesResponse>
  <ViewID><Value>1</Value></ViewID>
  <ViewName><Value>Front</Value></ViewName>
  <ViewType>Single</ViewType>
</VideoDisplayService.ListViewCapabilitiesResponse>""",
            False,
        ),
        Case(
            "VDS-003 single ViewID request allowed by xs:choice",
            """<VideoDisplayService.SetVideoViewRequest>
  <ViewID><Value>1</Value></ViewID>
</VideoDisplayService.SetVideoViewRequest>""",
            True,
        ),
        Case(
            "VDS-003 PDF-required ViewID+Timeout rejected",
            """<VideoDisplayService.SetVideoViewRequest>
  <ViewID><Value>1</Value></ViewID>
  <Timeout><Value>PT5S</Value></Timeout>
</VideoDisplayService.SetVideoViewRequest>""",
            False,
        ),
        Case(
            "VDS-004 SetVideoViewResponse single State allowed",
            """<VideoDisplayService.SetVideoViewResponse>
  <State>On</State>
</VideoDisplayService.SetVideoViewResponse>""",
            True,
        ),
        Case(
            "VDS-004 SetVideoViewResponse State+CurrentViewID rejected",
            """<VideoDisplayService.SetVideoViewResponse>
  <State>On</State>
  <CurrentViewID><Value>1</Value></CurrentViewID>
</VideoDisplayService.SetVideoViewResponse>""",
            False,
        ),
        Case(
            "VDS-004 GetDisplayStateResponse single State allowed",
            """<VideoDisplayService.GetDisplayStateResponse>
  <State>On</State>
</VideoDisplayService.GetDisplayStateResponse>""",
            True,
        ),
        Case(
            "VDS-004 GetDisplayStateResponse State+CurrentViewID rejected",
            """<VideoDisplayService.GetDisplayStateResponse>
  <State>On</State>
  <CurrentViewID><Value>1</Value></CurrentViewID>
</VideoDisplayService.GetDisplayStateResponse>""",
            False,
        ),
        Case(
            "VDS-004 SetNextViewIndexResponse single State allowed",
            """<VideoDisplayService.SetNextViewIndexResponse>
  <State>On</State>
</VideoDisplayService.SetNextViewIndexResponse>""",
            True,
        ),
        Case(
            "VDS-004 SetNextViewIndexResponse State+OperationErrorMessage rejected",
            """<VideoDisplayService.SetNextViewIndexResponse>
  <State>On</State>
  <OperationErrorMessage><Value>example</Value></OperationErrorMessage>
</VideoDisplayService.SetNextViewIndexResponse>""",
            False,
        ),
    ]


def main() -> int:
    failures = 0

    pools = [
        (
            "VideoLiveService V2.0 official",
            "IBIS-IP_VideoLiveService_V2.0.xsd",
            live_cases(),
        ),
        (
            "VideoRecordingService V2.0 official",
            "IBIS-IP_VideoRecordingService_V2.0.xsd",
            recording_v20_cases(),
        ),
        (
            "VideoDisplayService V2.0 official",
            "IBIS-IP_VideoDisplayService_V2.0.xsd",
            display_cases(),
        ),
        (
            "VideoRecordingService V2.4 candidate explanatory control",
            "IBIS-IP_VideoRecordingService_V2.4.xsd",
            recording_v24_control_cases(),
        ),
    ]

    for label, filename, cases in pools:
        print(f"\n{label}")
        try:
            schema = compile_schema(filename)
            print(f"OK  compiled {filename}")
        except Exception as exc:  # noqa: BLE001 - evidence tool
            print(f"ERR compile {filename}: {exc}")
            failures += 1
            continue

        for case in cases:
            if not check(schema, case):
                failures += 1

    if failures:
        print(f"\nFAILED: {failures} EV-103 check(s) did not match expectation")
        return 1

    print("\nPASSED: EV-103 video compositor behaviour confirmed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
