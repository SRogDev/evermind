# Continuous Intelligence Principles

These principles define Evermind. Do not weaken, reinterpret, or
silently replace them. (Source: Section 2 of
`docs/plans/repository-creation-plan.md`; this file is the durable
record inside the repository.)

## 1. Continuity lives inside the model

The primary research direction is **internal continuity**.

The model must maintain and update its own operational state as events
arrive. The runtime may manage connections, transport, scheduling,
isolation, and persistence of the model's actual inference state, but it
must not simulate intelligence by repeatedly summarizing history and
injecting that summary as a new prompt.

External storage may be useful for durability, recovery, or engineering
operations. It is not a substitute for the model's internal
continuous-processing mechanism.

The primary research direction is not an external-memory-first
architecture.

## 2. One persistent logical session

Each connected stream has a persistent logical model session.

- Events arrive over time.
- The model processes each new event incrementally.
- The internal state is carried forward and updated.
- The model does not restart a fresh conversational context for each
  event.
- The session can remain logically active for long periods.
- The system should not require a continuously busy GPU when no events
  are arriving. Logical continuity does not mean wasting compute on
  empty time.

Do not assume this must be implemented as one permanently open
autoregressive generation call. The engineering mechanism is an open
research question. The required behavior is persistent logical inference
with incremental state updates.

## 3. Zero Instruction during operation

Evermind does not receive a new instruction, conversational prompt, or
task description for each event.

The model learns its signal-detection behavior during training and
adaptation. At runtime it receives the event stream and updates its
state without per-event prompting.

An organization or user may establish a **persistent signal
configuration** before or when a stream is initialized. For example, a
business may define the kinds of events or patterns that should be
surfaced. This is configuration of the ongoing system, not a prompt
repeated for every event.

How this persistent configuration should influence the model — for
example through learned adapters, initialization/configuration encoding,
a dedicated conditioning mechanism, or another method — remains a
research and design question. Do not solve it by inserting a
natural-language instruction into every event.

## 4. Silence is a first-class output

The model must not produce a response for every event.

Its operational outcomes are:

- **Silence:** no signal is warranted.
- **Signal:** a relevant pattern has been detected and a structured
  signal is emitted.

Silence is not a missing response or an error. It is an intended model
behavior and must be represented and evaluated explicitly.

## 5. Evermind detects; other systems act

Evermind only emits structured signals. It does not call tools, browse
the internet, execute external actions, invoke APIs on its own, run
workflows, or modify external systems.

A separate application, Harness, or workflow engine decides what to do
with an emitted signal.

## 6. Continuous event-stream intelligence, not periodic summarization

Evermind is intended to process incoming events as a continuing stream,
updating its state incrementally.

It is not a system that polls an application every five or ten minutes,
summarizes recent activity with a large LLM, and then looks for
noteworthy changes.

Periodic processing may be used as a baseline in experiments, but it is
not the target architecture.

## 7. Bounded state and low operating cost

A central research objective is to support effectively unbounded
operating duration without an ever-growing inference state.

The system should investigate mechanisms that keep the active state
bounded or controlled while preserving useful information for future
detection.

The goal is not merely to make a model that can remain connected. It is
to make that continuous operation economically viable at high event
volumes.

---

## Invariants checklist (for reviews)

Any proposal — architecture, experiment, runtime design — must be
checked against these:

- [ ] No per-event instructions or prompts.
- [ ] Internal continuity is the primary direction (not external memory).
- [ ] One persistent logical session per stream.
- [ ] Incremental event processing.
- [ ] Silence is intentional and evaluated.
- [ ] Signals are structured outputs.
- [ ] Evermind does not execute actions.
- [ ] Bounded state and low cost are central objectives.
- [ ] No periodic LLM summarization as the target architecture.

A proposal failing any item is not an Evermind design, whatever its
other merits.
