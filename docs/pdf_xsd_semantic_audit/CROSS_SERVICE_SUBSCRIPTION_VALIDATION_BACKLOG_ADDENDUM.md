# Cross-service subscription validation backlog addendum

Status: open technical tasks.

```text
SUB-VB-001 Compile representative CIS/SMS/DMS V2.2 pools and map valid generic subscription payload structures.
SUB-VB-002 Create positive SubscribeRequestStructure sample with Client-IP-Address and optional ReplyPort/ReplyPath.
SUB-VB-003 Create positive UnsubscribeRequestStructure sample and negative TerminateSubscribeRequestStructure alias test.
SUB-VB-004 Verify SubscribeResponseStructure Active/Heartbeat/OperationErrorMessage combinations against exact version pools.
SUB-VB-005 Build DMS V2.2 operation-group sample proving service-prefixed local member plus generic payload type behaviour.
SUB-VB-006 Build CIS/SMS tests proving operation support cannot be inferred solely from local operation-group membership.
SUB-VB-007 Build TSD V2.2 tests separating Subscribe operation acknowledgement from subsequent TripRef/TripInformation callback payloads if the root model permits that interpretation.
SUB-VB-008 Capture or synthesize a runtime subscription flow with callback endpoint and heartbeat monitoring; classify results separately from XSD validation.
SUB-VB-009 Add operation-manifest resolver regression test for mixed service versions.
```

No task is marked passed until actually executed.
