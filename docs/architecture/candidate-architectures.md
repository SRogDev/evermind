# Candidate Architectures

**Status:** Conceptual comparison. No family is selected, and none is
claimed to work without evidence. At least three families are compared
here, plus external-memory approaches as baselines only.

Comparison dimensions used for every family: expected state size,
per-event compute, long-range temporal information, training
complexity, compatibility with pretrained weights, likely failure
modes, and evaluation needed.

## Family 1 — Conventional Transformer with bounded KV cache

The pretrained SmolLM3-3B-Base backbone, used with ordinary
finite-context inference, but with the KV cache held to a fixed budget
(sliding window, eviction, quantization, or a combination — see
[`kv-cache-research.md`](kv-cache-research.md)).

- **State size:** bounded by construction (the budget); bytes per
  stream are known in advance.
- **Per-event compute:** constant in stream length once the budget is
  reached; the cheapest family to run.
- **Long-range temporal information:** limited to the budget. Patterns
  spanning longer than the retained window are undetectable in
  principle; delayed signals are the known blind spot.
- **Training complexity:** lowest — fine-tuning for detection/silence
  behavior on top of an unchanged architecture; no new state mechanism
  to train.
- **Compatibility with pretrained weights:** highest — the architecture
  is unchanged; all pretrained representations are retained.
- **Likely failure modes:** silent information loss at the window edge;
  good short-stream scores that collapse on long streams; temptation to
  quietly grow the budget until the bound is meaningless.
- **Evaluation needed:** detection quality vs. window/budget size;
  degradation over 24h+ simulated streams; failure analysis by pattern
  class (which patterns die first as the budget shrinks).

This family is the **primary baseline** as well as a candidate: every
more novel family must beat it at equal state budget and training
budget, or the novelty is not justified.

## Family 2 — Pretrained Transformer augmented with recurrent or fixed-size internal state

The pretrained backbone is kept, and a recurrent or fixed-size state
mechanism is added: new events update a compact state rather than
requiring the complete token history. The state is learned — training
shapes what is retained and what is discarded.

- **State size:** fixed by design; the only family that bounds state
  structurally rather than by eviction policy.
- **Per-event compute:** constant and low at inference; the state
  update is a small operation per event.
- **Long-range temporal information:** in principle unbounded in time
  (the state can carry abstractions — counts, trends, regime — across
  arbitrary durations), but limited in fidelity: exact recall of a
  specific long-ago token is generally impossible, and capacity forces
  irreversible forgetting.
- **Training complexity:** highest — the state-update mechanism must be
  trained through long sequences (gradient flow, stability, credit
  assignment over delays), and the interaction with the frozen or
  fine-tuned backbone must be learned without destroying pretrained
  representations.
- **Compatibility with pretrained weights:** moderate — the backbone is
  retained, but the new component starts untrained and its interface to
  the backbone (where it reads from and writes to) is a design decision
  with no established answer.
- **Likely failure modes:** state collapse (the state learns to encode
  nothing useful); the backbone ignoring the state; training
  instability on long sequences; good performance on training pattern
  lengths that fails to generalize to longer streams.
- **Evaluation needed:** state-size vs. pattern-class coverage; 24h+
  degradation curves; ablation of state vs. no-state at equal budgets;
  whether the state actually carries information (probing) or the model
  is succeeding some other way.

## Family 3 — Hybrid Transformer / recurrent architecture

Attention layers (with a bounded cache for recent context) combined
with recurrent or compressed-state mechanisms for long-range
information — the two mechanisms cover different timescales. Possible
research families include recurrent memory mechanisms, state-space
approaches, gated delta-rule architectures, and hybrid
attention/recurrent designs. These are candidates for literature
review, not approved implementation choices.

- **State size:** bounded if both components are bounded; the sum of a
  bounded cache plus a fixed-size state.
- **Per-event compute:** the sum of both mechanisms; still constant in
  stream length, but the highest per-event cost of the three families.
- **Long-range temporal information:** the most expressive — exact
  recent recall from attention plus compressed long-term memory from
  the recurrent component.
- **Training complexity:** high — two interacting mechanisms, credit
  assignment between them, more design decisions, more ways to be
  wrong.
- **Compatibility with pretrained weights:** moderate — the attention
  backbone is retained, but integrating a recurrent component into
  pretrained layers (which layers, what interface) is unresolved.
- **Likely failure modes:** one mechanism does all the work and the
  other is dead weight; the hybrid is better than either component but
  not better than the sum of their costs; complexity that cannot be
  debugged when it fails.
- **Evaluation needed:** ablation — hybrid vs. each component alone at
  equal state budgets; measured (not assumed) timescale each component
  serves; training stability; cost per million events vs. Family 1.

## Comparison baseline — external memory / repeated context (not a research direction)

A conventional model supplied with bounded or summarized history on
each event: retrieve relevant past events, or summarize recent history,
and inject it as context. This is a **comparison baseline**, not the
target architecture, and not a candidate family.

It is included because it is the easiest way to get *something*
working, and therefore the result every candidate must beat to justify
its complexity. Its known properties: state lives outside the model
(violating Principle 1 if presented as the solution); cost grows with
retrieval/summarization frequency; the intelligence lives partly in
the retrieval/summarization prompt rather than in learned state. If a
candidate family cannot beat this baseline on detection quality at
equal or lower cost per million events, that is a result to report
honestly — see the evaluation philosophy in the repository README.

Periodic summarization (poll every few minutes, summarize with a large
LLM, look for changes) is a related baseline with the same status:
useful for comparison, not the target.

## What would decide between families

No selection is made in this foundation phase. Selection criteria
themselves are an unresolved decision (see
`research-charter.md#unresolved-decisions`); the intended basis is:

1. Detection quality on multi-event and delayed patterns, not only on
   isolated events.
2. State size over time (measured, bounded by design or by policy).
3. Cost per million events, including idle cost.
4. Degradation over long sessions (24h, multi-day simulations).
5. Training cost and stability to reach that quality.
6. Silence quality: false-alarm rate on long noise stretches.

Do not assume the most architecturally novel approach will win.
