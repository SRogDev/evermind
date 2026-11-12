# Dataset Strategy

**Status:** Requirements and risks only. The initial application domain
is **explicitly undecided**. Do not scrape, generate, or download
datasets. No dataset is created in this repository.

## Why the domain comes first

Every dataset decision — what an event is, what counts as a signal,
what "rare" means, what a false alarm costs — depends on the domain.
Choosing data before the domain would silently choose the domain. The
domain requires owner approval before dataset creation.

## Future data requirements

When a domain is selected, data must provide:

- **Ordered event sequences** — order is the signal, not metadata.
- **Timestamps or explicit temporal ordering.**
- **Labels for signal and non-signal outcomes** — including labels for
  silence (this event, correctly, warranted nothing).
- **Multi-event patterns** where a signal only becomes detectable over
  time (accumulation, sequence, regime change, delayed consequence,
  absence — see `problem-definition.md`).
- **Long negative/noise stretches** — the model must learn silence, and
  silence can only be learned and measured on long stretches of
  nothing-worth-signaling.
- **Delayed signals and rare events** — low base rates, long delays
  between cause and detectable effect.
- **Realistic event rates and distributions** — including bursts and
  idle gaps, not uniform synthetic spacing.
- **Organization-specific signal configurations** where applicable —
  the same stream, different standing definitions of "worth surfacing".
- **Train/validation/test separation by stream, entity, or time** to
  prevent leakage. Random splits over events from the same stream are
  not acceptable: they leak the future into training.
- **Documented provenance, permissions, and licenses** for every
  source.

## Synthetic data

Synthetic data may be useful for controlled tests (isolating one
pattern class, testing a state mechanism at a known difficulty), but
it is **not sufficient evidence of real-world usefulness**. Any claim
resting only on synthetic data is labeled as such, and real-domain
validation remains required before the claim is treated as established.

## Risks

- **Leakage:** temporal leakage (future events in training), entity
  leakage (same organization/stream across splits), label leakage
  (the label encoded in the event itself).
- **Base-rate distortion:** a dataset with 50% signal events teaches
  a model that signals are common; real streams are overwhelmingly
  noise. Training and evaluation distributions must reflect the
  deployment regime, or the false-alarm rate will be meaningless.
- **Pattern monoculture:** a dataset built around one pattern class
  proves nothing about the others.
- **Provenance gaps:** data without documented permission and license
  cannot be distributed or used as evidence; record provenance before
  training, not after.
- **Domain lock-in:** the first domain's quirks (event format, signal
  rate, vocabulary) can silently become architectural assumptions.
  Record which choices are domain-specific so later domains can
  challenge them.
