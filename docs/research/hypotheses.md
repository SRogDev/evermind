# Working Hypotheses

Hypotheses, not established facts. Each states what would support it
and what would falsify or weaken it. **No numeric thresholds are
invented here** — thresholds require later approval and
domain-specific evidence.

## H1 — Instruction-free detection is learnable

A pretrained ~3B model can be adapted to detect useful event-stream
signals without per-event instructions.

- **Supports:** a model trained with only the event stream and a
  persistent signal configuration detects target patterns at useful
  recall/precision, with no per-event prompt at inference.
- **Falsifies/weakens:** detection only works when a per-event
  instruction is present; or performance collapses to the level of
  per-event classification with no cross-event information.

## H2 — Bounded state can preserve temporal information

A learned internal state mechanism can preserve relevant temporal
information with bounded state.

- **Supports:** a fixed-size state model matches or approaches the
  detection quality of an unbounded-cache reference on multi-event and
  delayed patterns, at fixed state size.
- **Falsifies/weakens:** bounded-state models systematically fail
  exactly the patterns that require long-range retention, while the
  unbounded reference succeeds; or the required state size grows with
  stream length in practice.

## H3 — Bounded/recurrent state reduces long-session memory growth

A bounded or recurrent state architecture can reduce long-session
memory growth compared with an unbounded conventional KV cache.

- **Supports:** measured memory per active stream stays flat (or grows
  sublinearly) over 24h+ simulated streams, vs. linear growth for the
  unbounded baseline, at comparable detection quality.
- **Falsifies/weakens:** memory is flat only because detection quality
  collapsed; or the bounded architecture's memory is flat but its
  per-event compute is so high that cost per million events is worse.

## H4 — Long-sequence training beats independent classification

Training on long event sequences can improve detection of multi-event
patterns compared with independent event classification.

- **Supports:** a model trained on long sequences outperforms the same
  architecture trained on isolated events, specifically on multi-event
  and delayed patterns (not just on average).
- **Falsifies/weakens:** no difference on multi-event patterns; or the
  long-sequence model is better only on short patterns and worse on
  long ones (overfitting to sequence length).

## H5 — Learned silence controls false alarms

A learned silence/signal mechanism can achieve useful recall while
controlling false alarms.

- **Supports:** high recall on target patterns with a low false-alarm
  rate per stream-day on long noise stretches, without a hand-written
  rules layer doing the detection.
- **Falsifies/weakens:** recall is only achieved by signaling
  frequently (no useful silence); or false alarms are controlled only
  by a threshold so conservative that recall collapses; or a rules
  engine is doing the actual detection while the model formats outputs.

## H6 — Adapted architecture beats the large-LLM monitoring pipeline on cost

An adapted architecture can achieve a lower cost per million events
than a conventional large-LLM monitoring pipeline.

- **Supports:** measured cost per million events (compute + idle) is
  lower than the periodic-summarization / large-LLM baseline at
  comparable detection quality.
- **Falsifies/weakens:** cost is lower only at much worse detection
  quality; or the adapted architecture's training cost, amortized
  realistically, erases the inference saving; or the large-LLM baseline
  is cheaper once batching is accounted for.

## Method note

Hypotheses are tested by experiments registered in `experiments/`
with the hypothesis stated *before* the run. A hypothesis is not
"supported" by a single short synthetic run: H2, H3, and H6 require
long-stream evidence, and H5 requires long noise stretches. Negative
results are reported, not buried.
