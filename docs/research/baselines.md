# Baselines

Documented candidate baselines. None is implemented now. Baselines
exist so that candidate architectures must earn their complexity: a
novel architecture that cannot beat the baselines at equal budgets has
not demonstrated value.

## Baseline families

### 1. Conventional pretrained model baseline

SmolLM3-3B-Base adapted for event classification/detection using
ordinary finite-context inference: each event (or a short window) is
classified independently, with no cross-event state beyond the context
window.

- **What it tests:** how far per-event classification alone goes.
- **Expected weakness:** multi-event and delayed patterns; anything
  requiring memory beyond the window.

### 2. External-memory / repeated-context baseline

A conventional model supplied with bounded or summarized history on
each event — retrieved past events, or a summary of recent history,
injected as context. This is a **comparison baseline, not the target
architecture**.

- **What it tests:** the strongest "easy" system, and the ceiling of
  external-memory approaches.
- **Expected weakness:** cost grows with retrieval/summarization;
  intelligence lives partly in the retrieval prompt; summary loss is
  uncontrolled. If a candidate cannot beat this on quality-per-cost,
  the candidate is not justified.

### 3. Bounded KV-cache baseline

A model using a limited cache or context window (sliding window,
eviction, quantization — see
`architecture/kv-cache-research.md`).

- **What it tests:** the cheapest bounded design; the bar every
  recurrent/hybrid candidate must clear.
- **Expected weakness:** patterns spanning longer than the budget.

### 4. Recurrent-state candidate

A model whose internal state is updated across events (fixed-size
state; see `architecture/candidate-architectures.md`, Family 2).

- **What it tests:** whether learned, bounded state preserves
  temporal information better than a bounded cache at the same budget.
- **Expected weakness:** training difficulty; irreversible forgetting.

### 5. Hybrid candidate

A combination of pretrained attention layers and recurrent or
compressed state mechanisms (Family 3).

- **What it tests:** whether two timescales beat one.
- **Expected weakness:** complexity, training stability, cost.

## Fair-comparison requirements

The final research design must define fair comparisons:

- **Equivalent data:** same event streams, same order, same splits.
- **Equivalent signal definitions:** same patterns count as signals
  for every candidate.
- **Equivalent training budget where feasible:** same data volume and
  comparable compute; where budgets cannot be equal, the difference is
  stated, not hidden.
- **Clearly stated resource constraints:** state budget (bytes per
  stream), latency budget, and cost budget are fixed before the
  comparison, not chosen after seeing results.
- **Same evaluation:** all candidates measured on the same metrics
  (`evaluation-plan.md`), including long-stream and noise-stretch
  behavior — not only short, favorable slices.

Do not assume the most architecturally novel approach will win. If the
bounded-cache baseline (3) performs as well as a novel recurrent
architecture at lower cost, that is the result, and it is reported
honestly.
