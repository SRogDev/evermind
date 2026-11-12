# KV-Cache Research

**Status:** Research framing. No method is selected; no technique is
claimed to work without evidence.

## The problem

Conventional autoregressive Transformer inference keeps a KV cache —
the keys and values of previous tokens — so they are not recomputed.
In a long-running session the cache grows with sequence length. Three
costs grow with it:

1. **Memory:** the cache itself, per active stream.
2. **Compute / memory traffic:** attention over a longer history each
   step.
3. **Money:** both of the above, multiplied by concurrent streams and
   by operating duration.

For a stream that never ends, an unbounded cache is not a viable
design. Evermind's question is what can replace or bound it without
destroying the information needed to detect patterns that only emerge
across many events.

## Grouped-Query Attention (GQA) — the starting point

SmolLM3-3B-Base uses Grouped-Query Attention: multiple query heads
share fewer key/value heads, so the KV cache is smaller than standard
multi-head attention by roughly the grouping factor.

- **Benefit:** real, immediate reduction in per-token cache size;
  already present in the chosen base model at no research cost.
- **Limitation:** it does not by itself bound cache growth. A smaller
  constant factor on linear growth is still linear growth. GQA is a
  starting advantage, not a solution.
- **Experiment needed:** measure cache size and per-event latency vs.
  stream length for the unmodified base model, to establish the growth
  curve every bounded method must beat.

## Sliding-window / bounded KV cache

Keep only the most recent *W* tokens (or a fixed token budget) in the
cache; older entries leave the window.

- **Benefits:** hard bound on state size; per-event cost becomes
  constant in stream length; simple to reason about and to implement as
  a baseline.
- **Failure modes:** any pattern whose evidence spans longer than the
  window is undetectable in principle. Delayed signals (an early event
  matters only when a later event arrives) are lost if the early event
  falls out of the window. Information loss is silent — the model
  cannot report what it no longer holds.
- **Compute implications:** constant per-event cost; the cheapest
  bounded option.
- **Experiments needed:** detection quality vs. window size on
  multi-event patterns; which pattern classes fail first as the window
  shrinks; whether a window plus a compact summary of evicted content
  recovers any of the loss (and whether that reintroduces the
  summarization the project forbids as the target architecture).

## Cache eviction and selective retention

Instead of a fixed window, evict cache entries by policy: least
recently attended, lowest attention mass, oldest, or a learned
importance score; retain entries judged important.

- **Benefits:** can preserve rare but decisive events that a sliding
  window would drop; adapts retention to content rather than position.
- **Failure modes:** importance is judged with present information —
  an entry that looks irrelevant now may be the key to a pattern later
  (the delayed-consequence case). Learned retention policies can
  overfit the training distribution and fail on rare events, which are
  precisely the events that matter most. Eviction decisions are
  irreversible.
- **Compute implications:** retention scoring adds per-event cost; the
  policy itself must be cheap or it defeats the purpose.
- **Experiments needed:** retention policy vs. sliding window at equal
  state budgets; failure analysis on delayed-signal patterns; stability
  of learned importance under distribution shift.

## KV quantization / compression

Store keys and values at lower precision (e.g. 8-bit, 4-bit) or in a
compressed representation, shrinking bytes per token without reducing
the number of retained tokens.

- **Benefits:** orthogonal to eviction — it multiplies the effective
  window at a fixed byte budget; preserves token coverage that eviction
  would lose.
- **Failure modes:** quantization error accumulates over long streams
  and can distort attention, especially for rare tokens or fine
  distinctions; it delays the growth problem rather than bounding it
  (bytes per token shrink, but token count still grows without a
  budget). Compression/decompression adds latency.
- **Compute implications:** modest per-event overhead; memory-bandwidth
  savings can outweigh it.
- **Experiments needed:** detection quality vs. quantization level over
  long sessions; error accumulation curves; combination with a bounded
  budget (quantization *inside* a bounded cache).

## Recurrent / fixed-size state

Replace (or augment) the growing cache with a compact state updated
per event: the state has fixed size by construction, so growth is
bounded by design rather than by policy.

- **Benefits:** the only family that bounds state structurally rather
  than by eviction; per-event cost constant; state can in principle
  encode abstractions (counts, trends, regime) rather than raw tokens.
- **Failure modes:** fixed capacity means irreversible information
  loss — the state must learn *what* to forget, and training must teach
  it; long-range exact recall (a specific token from long ago) is
  generally impossible; training a state-update mechanism through long
  sequences is harder than fine-tuning attention (gradient flow,
  stability, credit assignment over delays).
- **Compute implications:** cheapest per-event cost at scale, but the
  training cost to make the state useful may be the highest of any
  family.
- **Experiments needed:** what state size preserves which pattern
  classes; degradation curves over 24h+ simulated streams; whether a
  pretrained Transformer backbone can be adapted to a recurrent state
  without destroying its pretrained representations.

## Hybrid attention + recurrent state

Keep attention (and a bounded cache) for recent context and add a
recurrent/fixed-size state for long-range information — the two
mechanisms cover different timescales.

- **Benefits:** combines exact recent recall with compressed long-term
  memory; the most expressive family; lets the pretrained backbone keep
  doing what it is good at while the new component handles continuity.
- **Failure modes:** the most complex to train and to evaluate (two
  interacting mechanisms, credit assignment between them); risk that
  one mechanism does all the work and the other is dead weight; more
  parameters and design decisions, more ways to be wrong.
- **Compute implications:** per-event cost is the sum of both
  mechanisms; still bounded if both components are bounded.
- **Experiments needed:** ablation — hybrid vs. each component alone at
  equal state budgets; which timescale each component actually serves
  (measured, not assumed); training stability.

## Cross-cutting questions

- For every method: **what is lost, and does the loss matter?**
  Information-loss analysis is a first-class experiment, not an
  afterthought.
- **State size over time** is a metric for every candidate, reported
  alongside detection quality — a method that detects well while its
  state grows is not a success.
- **Fair budgets:** candidates are compared at equal state budgets
  (bytes per stream) and equal training budgets where feasible, not at
  each method's most flattering setting.
