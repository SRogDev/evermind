# Problem Definition

Formalizes the concepts Evermind research uses. These definitions are
the shared vocabulary for questions, hypotheses, baselines, and
evaluation. No application domain is chosen here.

## Event stream

An unbounded, ordered sequence of events arriving over time from one
external source (an application, a feed, a sensor network, a business
system). The stream has no known end; the model must operate as if it
never ends. Events arrive at irregular intervals, including long idle
gaps and bursts.

## Event

A single discrete unit of information in the stream: something that
happened, at a known time, in a known context. An event may be text, a
structured record (fields, identifiers, quantities), or a combination.
The research question of how events are encoded — text, structured
fields, or both — is open (see
`architecture/candidate-architectures.md`); the definition does not
presume text.

## Stream / connection

One logical connection between an event producer and one Evermind model
session. Each connection has exactly one persistent logical session
(see "session continuity"), one persistent signal configuration, and
isolated state: state, events, and configuration must not leak across
connections or organizations.

## Persistent organization-level signal configuration

The standing definition, established before or when a stream is
initialized, of what kinds of events or patterns should be surfaced for
that connection or organization. It is **configuration of the ongoing
system, not a prompt repeated for every event**. How it should influence
the model — learned adapters, initialization/configuration encoding, a
dedicated conditioning mechanism, or another method — is an open
research question. It must never be implemented by inserting a
natural-language instruction into every event.

## Internal model state

The model's own carried-forward representation of what it has seen and
what it currently considers relevant. It is updated incrementally as
events arrive and is the sole basis (together with the incoming event
and the persistent signal configuration) for deciding silence vs.
signal. It is **not** an external database, a retrieved summary, or a
reconstructed prompt. The central research objective is to keep this
state bounded while preserving useful information.

## State update

The operation performed when a new event arrives: the model consumes
the event and produces a new internal state (and possibly a signal).
State updates must be incremental — cost proportional to the new event,
not to the entire history — and must be learnable, so training can
shape what is retained and what is discarded.

## Signal

A structured, machine-readable output emitted when the model detects a
relevant pattern: what was detected, which evidence (events) supports
it, when it was detected, and a confidence/calibration if applicable.
A signal is the model's only output channel to the outside world.

## Silence

The deliberate absence of a signal for an event (or a stretch of
events). Silence is a first-class, intended outcome — not a missing
response, timeout, or error. A model that signals on every event has
failed the silence requirement, however accurate its signals are.
Silence must be represented and evaluated explicitly (false-alarm rate,
silence rate on noise stretches).

## Detection delay

The time — in wall-clock time, in number of events, or both — between
the moment a pattern becomes detectable in the stream and the moment
the model emits the corresponding signal. Some patterns are only
detectable after several events; delay is therefore a metric, not a
defect per se, but unbounded or unexplained delay is a failure.

## Session continuity

The property that a stream's logical model session persists across
events and across idle gaps: the internal state is carried forward, not
rebuilt from scratch per event. Logical continuity does **not** require
a continuously busy GPU, nor one permanently open autoregressive
generation call; the engineering mechanism is an open research question.
What matters is the behavior: the model at event *n+1* knows what it
learned from events *1..n*.

## Bounded state

The requirement that the active inference state (whatever its
representation — KV cache, recurrent state, hybrid) does not grow
without bound as the stream length grows. "Bounded" means controlled by
design (a fixed budget, a sublinear growth rule, or an eviction /
compression policy with understood information loss), not merely "small
so far". A model retaining all previous tokens in an ever-growing cache
does not satisfy this objective.

## Event-processing cost

The compute, memory traffic, latency, and (ultimately) money required
to process one event and update state — including idle cost when no
events arrive. The research target is cost low enough for sustained
high-volume use; cost per million events is the headline efficiency
metric (see `research/evaluation-plan.md`).

## Temporal patterns

Many signals of interest are not properties of a single event. They
only become detectable across multiple events, for example:

- **Accumulation:** a quantity crossing a threshold only after many
  small increments.
- **Sequence:** an ordered series of events whose combination — but no
  single member — is meaningful.
- **Change of regime:** behavior that was normal for a long stretch
  stops being normal, detectable only against retained history.
- **Delayed consequence:** an early event matters only when a later,
  apparently unrelated event arrives.
- **Absence:** something expected within a window does not happen.

These patterns are why per-event classification is an insufficient
baseline and why long-stream training and evaluation are central to
Evermind: a system can be perfect on isolated events and useless on
the patterns that matter.
