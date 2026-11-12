# Experiments

Future experiments are organized here — one directory per experiment,
registered **before** the run, with the research question and hypothesis
stated in advance. No experiments exist yet: the experimental phase
requires separate owner approval (see `docs/research-charter.md` for
the approval criteria).

## Layout (future)

```text
experiments/
├── README.md            # This file
├── templates/
│   └── experiment.yaml  # Configuration template (not an experiment)
└── <experiment-id>/     # One directory per approved experiment
    ├── experiment.yaml  # Filled-in copy of the template
    ├── notes.md         # Design notes, observations, deviations
    └── results.md       # Results, including negative results
```

## Rules

1. **Register before running.** The `experiment.yaml` (question,
   hypothesis, baselines, metrics, compute) is written before any
   training run.
2. **One hypothesis per experiment** where possible; multi-hypothesis
   experiments name a primary hypothesis.
3. **Fair comparisons** (see `docs/research/baselines.md`): equivalent
   data, event order, signal definitions, and stated budgets.
4. **Report negative results.** A baseline beating a novel architecture
   is a finding.
5. **Reproducibility metadata is mandatory:** base model and revision,
   code commit, dataset provenance, seeds, compute environment.
6. **No weights, datasets, or large artifacts are committed here.**
   Experiments record configuration, provenance, and results; artifacts
   live outside the repository (see `.gitignore`).
