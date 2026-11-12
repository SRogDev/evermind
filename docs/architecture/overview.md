# Architecture Overview

**Status:** Conceptual only. No architecture has been selected,
implemented, or validated. This document maps the pieces and their
responsibilities so candidate designs can be compared on common ground.

## Conceptual data flow

```text
External application / event producer
              |
              v
       Evermind Python SDK          (future; integration ergonomics)
              |
      persistent connection
              |
              v
       Evermind runtime             (future; connections, isolation,
              |                      scheduling, state persistence)
     isolated model session
              |
              v
  Continuous Intelligence model    (the research object)
  - pretrained backbone (SmolLM3-3B-Base, initial candidate)
  - internal persistent state
  - incremental state update
  - learned signal / silence behavior
              |
              v
     structured signal output
              |
              v
External application / Harness / workflow engine
              (decides what to do with the signal)
```

## Responsibilities — and their boundaries

| Piece | Owns | Must not become |
|---|---|---|
| **Model** | Understanding the stream, updating internal state, deciding silence vs. signal | A formatter for a rules engine; a chatbot answering per-event prompts |
| **Internal state** | Carried-forward representation of what matters from past events | An ever-growing token history; an external database pretending to be memory |
| **Runtime** | Connections, authentication, per-connection isolation, scheduling/batching, checkpointing actual model state, metrics/health | An external context summarizer that re-prompts a conventional LLM |
| **SDK** | Establishing/maintaining a connection, configuring persistent signal preferences, publishing events, consuming signals, reconnection semantics | A mandatory proxy in the application's normal request path; intelligence |
| **Downstream application / Harness** | Deciding what to do with a signal (act, notify, trigger a workflow) | Part of the model — detection and action stay separate |

## What is deliberately unresolved

- **The state mechanism.** Bounded KV cache, recurrent/fixed-size
  state, hybrid designs — all candidates; see
  [`candidate-architectures.md`](candidate-architectures.md). No winner
  is declared here.
- **Event encoding.** Text, structured fields, or a combination.
- **Signal-configuration conditioning.** How persistent configuration
  influences the model without per-event prompting.
- **Session engineering.** How a persistent logical session is realized
  (it is not assumed to be one permanently open autoregressive call),
  and how computation pauses between events while continuity is
  preserved.
- **Serving.** Shared weights with isolated per-connection state is the
  intended pattern; batching, state isolation, and resource allocation
  designs remain open.

## Relation to the other architecture documents

- `internal-state-and-continuity.md` — the persistent session and why
  state must live inside the model.
- `kv-cache-research.md` — the KV-cache growth problem and the
  compression/eviction research space.
- `candidate-architectures.md` — comparison of at least three
  architecture families.
- `runtime-and-sdk-boundary.md` — future runtime/SDK responsibilities
  and multi-tenant boundaries (not built in this phase).
