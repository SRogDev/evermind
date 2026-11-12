# Evaluation Plan

Metrics to investigate and report. Benchmark definitions and numeric
acceptance thresholds must be approved after the first domain and data
strategy are selected — no thresholds are invented here.

## Detection quality

- Precision, recall, F1 on emitted signals vs. ground-truth signal
  events.
- False positives and false negatives, with analysis by pattern class
  (which kinds of patterns are missed, which kinds trigger false
  alarms).
- False alarms per hour or per stream-day — the operationally relevant
  rate, since a stream runs continuously.
- Signal calibration where applicable (does stated confidence match
  empirical accuracy?).

## Temporal behavior

- **Detection delay:** time (wall-clock and event count) between a
  pattern becoming detectable and the signal being emitted.
- **Multi-event pattern detection:** recall specifically on patterns
  requiring several events, reported separately from single-event
  recall.
- **State degradation over time:** detection quality as a function of
  session length (hours/days of simulated stream).
- **Recovery after checkpoint/restart:** quality before vs. after a
  state checkpoint/restore cycle.
- **Performance across long sessions:** 24-hour and multi-day
  simulations, not only short runs.

## Efficiency

- Memory footprint per active stream.
- KV-cache or recurrent-state size over time (is it actually bounded?
  measured, not asserted).
- Events per second (throughput).
- Latency p50/p95/p99 per event.
- Compute utilization.
- Energy or accelerator time where measurable.
- **Cost per million events** — the headline efficiency metric.
- Idle cost when no events arrive (a system that burns a GPU on empty
  time fails the cost objective even if its per-event cost is low).

## Long-running evaluation

- 24-hour stream simulation.
- Multi-day simulation.
- Long negative/noise intervals (silence quality under boredom).
- Bursty event arrivals.
- Rare signals (low base rate — the realistic regime, where naive
  accuracy is meaningless).
- Concurrent streams and tenant isolation (no cross-stream leakage of
  state, events, or configuration).

## Reporting rules

- Report detection quality, temporal behavior, and efficiency together:
  a result that is accurate but unbounded in state, or cheap but blind
  to delayed patterns, is a partial result, stated as such.
- Report negative results. A baseline beating a novel architecture at
  lower cost is a finding, not a failure to hide.
- Every reported number names its stream length, event distribution,
  signal rate, state budget, and compute environment — a metric without
  those is not reproducible and not comparable.
