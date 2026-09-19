# AoE2 DE replay-viewing gRPC interface

LibreMatch documents an additional **local replay interface**, separate from hosted leaderboard and match-history APIs. Its [gRPC reference](https://github.com/librematch/wiki/tree/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/grpc) and [Delta Play Replay project](https://github.com/librematch/delta-play-replay/tree/9bc90f67f22aec47bb050cdea5b73a5fec0d629e) describe AoE2 DE replay playback and the CaptureAge-related state stream.

The linked [`cade_api.proto`](https://github.com/librematch/delta-play-replay/blob/9bc90f67f22aec47bb050cdea5b73a5fec0d629e/crates/uncage-client/proto/cade_api.proto) defines package `cade_api.rpc`, service `CadeRemote`, and these operations:

| RPC | Request fields | Result |
| --- | --- | --- |
| `Info` | Empty request | Game/API versions, base directory and enabled mod directories |
| `Pause` | `paused` | Whether replay pause control succeeded and changed state |
| `SetFogOfWar` | `fogOfWar` | Replay-view fog setting result |
| `SetPerspective` | `playerId` | Selected replay perspective |
| `Frames` | Desired resolution per category, command/particle filtering options | Server stream of `FrameSequence` messages |

`Frames` carries binary state patches, reverse patches when present, events, recorded commands and metrics. The protocol has an event/command data model; these records are output from playback, not five RPCs for issuing arbitrary unit orders. Parsing its binary patches requires the matching state model, not just generated protobuf bindings. [Delta format reference](https://github.com/librematch/wiki/blob/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/grpc/delta_format.md).

The adjacent atlas/file-metadata proto files describe rendering resources. They should not be counted as additional RPC services merely because they contain protobuf message definitions.

The project’s proposed `.dlpr` format aims to preserve replay state independently of repeatedly running the original simulation. That is a project goal, not a compatibility guarantee for every historical recording. Its README treats equivalent AoE4/AoE3/Mythology interfaces as possibilities, not established implementations.

**Verification:** the five RPC declarations were checked against the pinned `.proto` file. No game was launched, gRPC connection opened, replay converted, or local listener address/port verified. No working AoE4 equivalent is established by this source. One wiki data-source index incorrectly expands “CA:DE” as Command & Conquer; the dedicated gRPC pages and linked project identify AoE2 DE.
