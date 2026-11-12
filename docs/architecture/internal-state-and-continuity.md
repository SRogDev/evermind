# Internal State and Continuity

**Status:** Conceptual research framing. Implementation mechanisms are
unresolved.

## The desired behavior

Each connected stream has one persistent logical session. Events arrive
over time; the model processes each new event incrementally; the
internal state is carried forward and updated; the model never restarts
a fresh conversational context for an event; the session can remain
logically active for hours, days, or longer.

The test is behavioral: the model at event *n+1* must know what it
learned from events *1..n* — without being re-told the history as a
prompt.

## Why state must live inside the model

The primary research direction is internal continuity (Principle 1).
The runtime may manage connections, transport, scheduling, isolation,
and persistence of the model's actual inference state, but it must not
simulate intelligence by repeatedly summarizing history and injecting
that summary as a new prompt. External storage may help durability or
recovery; it is not a substitute for the model's internal
continuous-processing mechanism.

The distinction matters because a summarizer-plus-prompt system can
pass short evaluations while failing exactly what Evermind is for:
the summary is lossy in ways no one controls, its cost grows with the
summary's size or frequency, and the "intelligence" lives in the
summarization prompt rather than in a learned state-update mechanism.
That design is a legitimate baseline for comparison — it is not the
target architecture.

## The conventional Transformer KV cache

Conventional autoregressive Transformer inference uses a KV cache to
avoid recomputing keys and values for previous tokens. In a long-running
session this cache grows with sequence length: memory grows, and
attention computation and memory traffic become increasingly expensive
as history grows. For a stream that never ends, an unbounded cache is
not a design — it is a slow failure (out-of-memory, latency growth,
cost growth).

SmolLM3's Grouped-Query Attention reduces KV-cache size relative to
standard multi-head attention, but it does not by itself bound cache
growth: a smaller constant factor on a linear growth is still linear
growth. See [`kv-cache-research.md`](kv-cache-research.md).

## Logical persistence vs. a permanently busy generation loop

Two things must not be confused:

- **Logical session persistence** — the required behavior: state carried
  forward, session identity maintained, no restart per event.
- **A permanently open autoregressive generation call** — one possible
  (and probably wrong) engineering mechanism.

The plan explicitly does not assume the session must be implemented as
one permanently open generation call. The engineering mechanism is an
open research question. Equally, logical continuity does not mean
wasting compute on empty time: the system should not require a
continuously busy GPU when no events are arriving. Pausing computation
between events while preserving logical continuity is itself a research
question (supporting question 7): state must be cheap to hold and cheap
to resume, or pausing is impossible.

## Event arrival and incremental state update

The intended processing model, per event:

1. An event arrives (with its timestamp / ordering).
2. The model consumes the event together with its current internal
   state.
3. The model produces an updated internal state — incrementally, at a
   cost proportional to the new event, not to the entire history.
4. The model emits either silence or a structured signal.

Step 3 is where the research lives: what the state representation is,
how it is updated, what is preserved and what is irreversibly lost, and
how gradients can train the update mechanism. A state update that
requires reprocessing the whole history is not incremental and fails
the cost objective, however good its detection quality.

## Checkpointing and recovery (engineering concern)

State checkpointing and recovery — saving the actual model state so a
session can survive a restart, and restoring it — is an engineering
concern of the future runtime, not a substitute for internal
continuity. Open questions, to be resolved in the experimental phase:

- What exactly is checkpointed (state tensors? cache? configuration?
  event position?) and how often?
- What are the recovery semantics: exact resume, best-effort resume,
  or declared loss?
- How is a session's state isolated per connection during checkpointing
  (no cross-tenant leakage)?
- How does detection quality degrade after a checkpoint/restart, and is
  that degradation measured (see `research/evaluation-plan.md`)?

Checkpointing answers "how do we survive a crash"; it does not answer
"how does the model remember". The two must not be conflated.

## The bounded-state objective

The active state must not grow without bound as the stream grows. The
mechanisms under investigation — bounded cache, eviction, compression,
recurrent/fixed-size state, hybrids — are compared in
[`candidate-architectures.md`](candidate-architectures.md) and
[`kv-cache-research.md`](kv-cache-research.md). What counts as
"bounded" must be defined per candidate (fixed budget, sublinear
growth rule, eviction policy with understood information loss) and
demonstrated by measurement: state size over time is an evaluation
metric, not an assertion.

## Unresolved

- State representation and update rule for each candidate family.
- Whether (and how) state can be reset, checkpointed, restored, or
  isolated per connection for each family.
- The pause/resume mechanism between events.
- What information is irreversibly lost under each bounded-state
  mechanism, and whether that loss matters for the target patterns.
