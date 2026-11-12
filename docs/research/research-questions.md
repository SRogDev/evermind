# Research Questions

## Primary research question

> **Can a pretrained approximately 3B-parameter language model be
> adapted into a continuously operating event-stream intelligence whose
> internal state remains bounded, whose state updates are incremental,
> and whose operating cost is low enough for sustained high-volume use
> — without per-event instructions?**

This is the question the whole program answers. Every supporting
question, hypothesis, baseline, and experiment must trace back to it.

## Supporting research questions

1. **Retention.** What information must the model retain across events
   to detect temporally distributed patterns?
2. **Bounded vs. growing state.** Can a bounded internal state preserve
   useful information that a conventional growing KV cache would
   otherwise retain?
3. **Architecture trade-offs.** Which architectural changes provide the
   best trade-off between detection quality, state size, latency,
   throughput, and compute cost?
4. **Learned silence.** Can the model learn to remain silent on
   irrelevant events while reliably emitting structured signals for
   relevant patterns?
5. **Signal configuration.** How should persistent organization-level
   signal configuration be represented without per-event prompting?
6. **Long-session behavior.** How does detection quality change over
   long sessions — for example, after 24 hours, several days, or
   simulated longer streams?
7. **Idle computation.** Can the system pause computation between events
   while preserving logical session continuity?
8. **Cost.** What is the cost per million events under realistic event
   distributions and signal rates?

## Notes on scope

- These questions are deliberately domain-free: they must be
  answerable before (and independently of) the choice of the first
  application domain, and re-answerable within each domain.
- Question 2 is the empirical core of the bounded-state claim: it is
  answered by measurement (state size and detection quality over time),
  not by architectural assertion.
- Question 5 is a design question with no accepted answer yet; proposed
  mechanisms (learned adapters, initialization/configuration encoding,
  dedicated conditioning) are candidates, not decisions.
- Question 7 separates logical continuity from compute: a "yes" that
  requires a busy GPU is not a yes.
