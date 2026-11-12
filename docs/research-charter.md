# Evermind Research Charter

**Status:** Foundation — initial charter, version 0.1.0 (2026-11-11).
**Scope:** Research framing only. No architecture, model, dataset, or
runtime has been implemented or validated.

## Vision

A continuously operating intelligence: a model that stays logically
connected to an external information stream, processes events as they
arrive over hours, days, or longer, and surfaces only what deserves
attention — without being restarted per event, without a new instruction
per event, and without the state and cost of that operation growing
without bound.

The intelligence is the model itself, not a pipeline wrapped around a
chatbot. If the model is removed, nothing in the system should still be
able to "detect" — that is the test of whether the research succeeded.

## Research problem

Conventional autoregressive Transformer inference commonly uses a KV
cache to avoid recomputing keys and values for previous tokens. In a
long-running session, a conventional cache grows with sequence length,
and attention computation and memory traffic become increasingly
expensive as history grows. SmolLM3's Grouped-Query Attention reduces
KV-cache size relative to standard multi-head attention, but it does
not by itself solve unbounded cache growth.

The problem is therefore not "how long a context can we fit" but
"how can a model keep operating indefinitely, cheaply, on a stream it
never sees the end of, and still notice the patterns that only become
visible across many events?"

Evermind is not primarily optimizing for maximum context length,
perfect long-document recall, or general-purpose memory quality. The
target is continuous, low-cost inference with sufficient internal state
to detect meaningful patterns over time.

## Primary research question

> Can a pretrained approximately 3B-parameter language model be adapted
> into a continuously operating event-stream intelligence whose internal
> state remains bounded, whose state updates are incremental, and whose
> operating cost is low enough for sustained high-volume use — without
> per-event instructions?

## Supporting research questions

1. What information must the model retain across events to detect
   temporally distributed patterns?
2. Can a bounded internal state preserve useful information that a
   conventional growing KV cache would otherwise retain?
3. Which architectural changes provide the best trade-off between
   detection quality, state size, latency, throughput, and compute cost?
4. Can the model learn to remain silent on irrelevant events while
   reliably emitting structured signals for relevant patterns?
5. How should persistent organization-level signal configuration be
   represented without per-event prompting?
6. How does detection quality change over long sessions — for example,
   after 24 hours, several days, or simulated longer streams?
7. Can the system pause computation between events while preserving
   logical session continuity?
8. What is the cost per million events under realistic event
   distributions and signal rates?

Full detail: [`research/research-questions.md`](research/research-questions.md).

## Working hypotheses

Hypotheses, not established facts. Each is falsifiable; the evidence
that would support or weaken it is recorded in
[`research/hypotheses.md`](research/hypotheses.md).

- **H1.** A pretrained ~3B model can be adapted to detect useful
  event-stream signals without per-event instructions.
- **H2.** A learned internal state mechanism can preserve relevant
  temporal information with bounded state.
- **H3.** A bounded or recurrent state architecture can reduce
  long-session memory growth compared with an unbounded conventional KV
  cache.
- **H4.** Training on long event sequences improves detection of
  multi-event patterns compared with independent event classification.
- **H5.** A learned silence/signal mechanism can achieve useful recall
  while controlling false alarms.
- **H6.** An adapted architecture can achieve a lower cost per million
  events than a conventional large-LLM monitoring pipeline.

No numeric thresholds are asserted for any hypothesis; thresholds
require later approval and domain-specific evidence.

## Scope

**In scope for the research program:**

- Architectural adaptation of a pretrained small model for continuous
  event-stream operation.
- Internal-state mechanisms: bounded KV cache, recurrent/fixed-size
  state, hybrid attention/recurrent designs (as research candidates).
- Learned signal/silence behavior and its evaluation.
- Baselines and fair comparisons, including periodic-summarization and
  external-memory baselines *as comparisons only*.
- Explicit, inspectable training loops in PyTorch; Hugging Face
  libraries for loading/tokenization/interoperability.
- Long-stream evaluation: detection quality over time, state
  degradation, cost per million events.

**Out of scope (non-goals):**

- Downloading or modifying model weights during repository creation.
- Fine-tuning/training before a separately approved experimental phase.
- Selecting a final architecture in this foundation phase.
- Creating or downloading datasets; selecting an application domain
  without owner approval.
- Building a production runtime, SDK, broker, database, or multi-tenant
  serving system.
- Integrating LangGraph, Polygrow, JEV, or other systems.
- Browsing, tool use, agentic behavior, or external actions.
- Periodic summarization as the target architecture; per-event prompting.
- Any claim that continuous operation, bounded memory, or low cost has
  already been achieved.

## Initial model candidate

**SmolLM3-3B-Base** (`HuggingFaceTB/SmolLM3-3B-Base`), the Base
checkpoint — not instruction-tuned. ~3B parameters, decoder-only
Transformer with GQA and NoPE, pretrained on 11.2T tokens, 64k training
context with YaRN extrapolation to 128k. Open weights; Apache 2.0 model
license as stated by the upstream project (verify exact terms before
redistribution or commercial deployment). Technical report: Bakouch et
al. (2025), *SmolLM3: smol, multilingual, long-context reasoner*,
<https://huggingface.co/blog/smollm3>.

3B is an initial candidate, not a proven optimum. The base model stays
replaceable so later comparisons are possible; the initial scope is not
a large model survey.

## Core principles (summary)

The invariants from Section 2 of the creation plan, preserved exactly
(full text in
[`continuous-intelligence-principles.md`](continuous-intelligence-principles.md)):

1. Continuity lives inside the model.
2. One persistent logical session per stream.
3. Zero Instruction during operation.
4. Silence is a first-class output.
5. Evermind detects; other systems act.
6. Continuous event-stream intelligence, not periodic summarization.
7. Bounded state and low operating cost.

## Evaluation principles

- Success is not "the socket stayed open", "the cache was retained",
  or "isolated events were classified". See the evaluation philosophy in
  the repository README and
  [`research/evaluation-plan.md`](research/evaluation-plan.md).
- Report detection quality (precision/recall/F1, false alarms),
  temporal behavior (detection delay, degradation over long sessions),
  and efficiency (state size over time, latency, cost per million
  events, idle cost).
- Fair comparisons: equivalent data, event order, signal definitions,
  training budget where feasible, stated resource constraints.
- Negative results are valuable and are reported honestly.
- Benchmark definitions and numeric acceptance thresholds must be
  approved after the first domain and data strategy are selected.

## Unresolved decisions

These require owner approval before the experimental phase:

1. **Application domain** — undecided; no dataset work until chosen.
2. **Repository license** — pending; no `LICENSE` file until selected.
3. **Architecture-selection criteria** — which trade-offs decide between
   candidate families (Section 5 of the plan), and who judges them.
4. **Evaluation thresholds** — numeric acceptance criteria per metric,
   after domain and data strategy.
5. **Persistent signal-configuration mechanism** — learned adapters,
   initialization/configuration encoding, dedicated conditioning, or
   another method (research question, not a premature choice).
6. **Compute budget and GPU resources** for adaptation/training.
7. **Dataset provenance and licensing** for the first domain.
8. **State checkpointing/recovery semantics** — what "resume a session"
   must guarantee.

## Criteria for approving the first experimental phase

The experimental phase may begin only when:

1. The application domain is selected and approved by the owner.
2. A dataset strategy exists for that domain (provenance, licenses,
   train/validation/test separation by stream, entity, or time).
3. Architecture-selection criteria and evaluation thresholds are
   approved.
4. GPU compute for adaptation/training is available and budgeted.
5. The first experiment is registered using
   `experiments/templates/experiment.yaml`, with its research question
   and hypothesis stated before any training run.
6. The repository license decision is recorded (even if the decision is
   to defer it explicitly with a date).

Until then, this repository remains foundation and documentation only.
