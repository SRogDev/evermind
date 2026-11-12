# Evermind

**Continuous Intelligence — Applied Model Architecture Research**

Evermind investigates whether a pretrained small language model can be
architecturally adapted and trained to operate as a persistent,
instruction-free intelligence over continuous event streams — maintaining
internal state across an effectively unbounded stream while keeping state
size and inference cost bounded and very low.

> **Research status: foundation only.** This repository establishes the
> research home, the questions, the principles, and the Python/PyTorch
> environment. **No architecture or model has been implemented or
> validated yet.** No weights have been downloaded, no training has run,
> and no dataset has been created. See
> [`docs/research-charter.md`](docs/research-charter.md).

## Mission

Create a new kind of model: an intelligence that remains logically
connected to an external information stream and continuously processes
incoming events over long periods — hours, days, or longer — without
being restarted as a new conversation for each event and without
receiving a new instruction or prompt for every event.

The model learns what deserves attention. It processes events, updates
its internal state, and emits a structured signal only when it detects
something relevant according to the persistent signal configuration
established for that connection or organization. Otherwise, it remains
silent.

The central research challenge is not maximizing context length or
building the best general-purpose context engine. It is making
continuous intelligence operationally practical: **persistent inference,
bounded state, low latency, high throughput, and extremely low cost.**

**Core identity: a continuously operating intelligence, not a chatbot.**

## What "Continuous Intelligence" means here

Continuous Intelligence is Evermind's working research framing, not a
claim that it is already an established formal ML subfield. In this
project it means:

- **Continuity lives inside the model.** The model maintains and updates
  its own operational state as events arrive. The runtime may manage
  connections, transport, scheduling, isolation, and persistence of the
  model's actual inference state, but it must not simulate intelligence
  by repeatedly summarizing history and injecting that summary as a new
  prompt. External storage may help durability or recovery; it is not a
  substitute for the model's internal continuous-processing mechanism.
  This is **not** an external-memory-first architecture.
- **One persistent logical session per stream.** Events arrive over time;
  the model processes each new event incrementally and carries its
  internal state forward. It does not restart a fresh conversational
  context for each event, and the session can remain logically active for
  long periods. Logical continuity does not mean wasting compute on empty
  time — the system should not require a continuously busy GPU when no
  events are arriving. (This does not assume one permanently open
  autoregressive generation call; the engineering mechanism is an open
  research question.)
- **Zero Instruction during operation.** Evermind receives no new
  instruction, conversational prompt, or task description for each event.
  The model learns its signal-detection behavior during training and
  adaptation. An organization may establish a **persistent signal
  configuration** before or when a stream is initialized — for example,
  the kinds of events or patterns to surface. That is configuration of
  the ongoing system, not a prompt repeated for every event. How the
  configuration should influence the model (learned adapters,
  initialization/configuration encoding, a dedicated conditioning
  mechanism, or another method) remains a research question. It must
  never be solved by inserting a natural-language instruction into every
  event.
- **Silence is a first-class output.** The model must not produce a
  response for every event. Its operational outcomes are **silence** (no
  signal is warranted) or **signal** (a relevant pattern was detected and
  a structured signal is emitted). Silence is not a missing response or
  an error; it is intended behavior, represented and evaluated
  explicitly.
- **Evermind detects; other systems act.** Evermind only emits structured
  signals. It does not call tools, browse the internet, execute external
  actions, invoke APIs on its own, run workflows, or modify external
  systems. A separate application, Harness, or workflow engine decides
  what to do with an emitted signal.
- **Continuous stream processing, not periodic summarization.** Evermind
  processes incoming events as a continuing stream, updating state
  incrementally. It is not a system that polls an application every few
  minutes, summarizes recent activity with a large LLM, and looks for
  noteworthy changes. Periodic processing may be used as a baseline in
  experiments, but it is not the target architecture.
- **Bounded state and low operating cost.** The objective is effectively
  unbounded operating duration without an ever-growing inference state.
  The goal is not merely a model that can remain connected, but one
  whose continuous operation is economically viable at high event
  volumes.

The full invariants are recorded verbatim in
[`docs/continuous-intelligence-principles.md`](docs/continuous-intelligence-principles.md)
and in Section 2 of the repository creation plan
(`docs/plans/repository-creation-plan.md`).

## Primary research question

> Can a pretrained approximately 3B-parameter language model be adapted
> into a continuously operating event-stream intelligence whose internal
> state remains bounded, whose state updates are incremental, and whose
> operating cost is low enough for sustained high-volume use — without
> per-event instructions?

Supporting questions, falsifiable hypotheses, baselines, and the
evaluation plan live in [`docs/research/`](docs/research/).

## Initial model candidate

**SmolLM3-3B-Base** (Hugging Face), model identifier
`HuggingFaceTB/SmolLM3-3B-Base` — the **Base** checkpoint, not an
instruction-tuned/chat checkpoint.

- Model card: <https://huggingface.co/HuggingFaceTB/SmolLM3-3B-Base>
- Upstream project: <https://github.com/huggingface/smollm>
- Technical report: Bakouch et al. (2025), *SmolLM3: smol,
  multilingual, long-context reasoner*,
  <https://huggingface.co/blog/smollm3> (citation as given on the
  official model card; see [`docs/references/README.md`](docs/references/README.md)).

Why this starting point: ~3B parameters is a reasonable
capacity/cost starting point; open weights with an Apache 2.0 model
license as stated by the upstream project (verify the exact model card
and artifact terms before redistribution or commercial deployment); a
documented Transformer architecture (decoder-only, GQA, NoPE,
pretrained on 11.2T tokens, 64k training context with YaRN
extrapolation to 128k); and a practical base for architectural
adaptation while retaining useful pretrained representations. **3B is an
initial candidate, not a scientific conclusion** — do not claim it is
proven optimal. The base model is replaceable in research code so later
comparisons are possible.

**No weights are downloaded in this repository.** The model identifier
and upstream source are recorded here; weights are only fetched in a
separately approved experimental phase, after verifying the model card,
license, upstream terms, tokenizer terms, and training/data
documentation.

## Evermind vs. Small Lab

Evermind and Small Lab are separate research efforts and must not be
conflated:

- **Evermind** is applied model-architecture research: adapt a
  pretrained small model into a continuously operating intelligence
  (internal state, bounded cost, learned silence/signal). Its output is
  a model architecture and the evidence for it.
- **Small Lab** (a separate repository) is the small-model training
  laboratory: training small models from scratch or from pretraining,
  studying what small models can learn. Its output is trained models and
  training knowledge.

Evermind starts from a *pretrained* model and asks an *architectural*
question; Small Lab asks a *training* question. They may inform each
other, but neither is a part of the other, and no code, dependency, or
decision is shared implicitly — anything shared later is an explicit,
recorded decision.

## Repository map

```text
evermind/
├── README.md                  # This file: mission, principles, setup
├── pyproject.toml             # Python 3.12, PyTorch core, model-loading extra
├── uv.lock                    # Locked dependency resolution
├── .python-version            # 3.12
├── docs/
│   ├── research-charter.md    # Vision, problem, questions, hypotheses, scope
│   ├── problem-definition.md  # Formal definitions (event, state, signal, ...)
│   ├── continuous-intelligence-principles.md  # The Section 2 invariants
│   ├── architecture/          # Conceptual architecture research (no selection)
│   │   ├── overview.md
│   │   ├── internal-state-and-continuity.md
│   │   ├── kv-cache-research.md
│   │   ├── candidate-architectures.md
│   │   └── runtime-and-sdk-boundary.md
│   ├── research/              # Questions, hypotheses, baselines, evaluation, data
│   │   ├── research-questions.md
│   │   ├── hypotheses.md
│   │   ├── baselines.md
│   │   ├── evaluation-plan.md
│   │   └── dataset-strategy.md
│   ├── decisions/             # Decision records (template; none recorded yet)
│   ├── references/            # Literature-recording format + verified sources
│   └── plans/
│       └── repository-creation-plan.md  # The plan that created this repo
├── src/evermind/              # Research package namespace (no implementation yet)
│   ├── model/ state/ events/ signals/ training/ evaluation/ runtime/
├── experiments/               # Future experiment organization + config template
├── tests/unit/                # CPU smoke test (import + PyTorch available)
├── tests/integration/         # Reserved for future integration tests
├── scripts/                   # Reserved for future research tooling
└── .github/workflows/ci.yml   # CPU CI: install, tests, lint/format — no weights
```

Each `src/evermind/*/` directory contains a short README describing what
will eventually live there. Those READMEs are placeholders, not
implementations.

## Technical stack and setup

- **Python 3.12** (see `.python-version`; PyTorch 2.x and
  transformers ≥ 4.53 both support Python 3.12 — verified by resolution,
  not assumed).
- **PyTorch** as the primary deep-learning framework. The training loop,
  when it exists, will be explicit and inspectable — Hugging Face
  Trainer will not be used as a black box for the core research loop.
- **Hugging Face libraries** (`transformers`, `tokenizers`,
  `safetensors`) only for loading, tokenization, and interoperability.
- **`uv`** for Python project and dependency management.
- **pytest** for tests, **Ruff** for linting/formatting.

```bash
# 1. Install uv (https://docs.astral.sh/uv/), then:
uv sync --all-extras        # create .venv, install torch + model-loading + dev deps
uv run pytest               # minimal CPU smoke test
uv run ruff check .         # lint
uv run ruff format --check .  # format check
```

### CPU setup — and its limits

This foundation installs and validates on CPU. The smoke test only
verifies the package imports and PyTorch is available; it loads no
model. **Actual model adaptation and training will require suitable GPU
resources** — a 3B-parameter model cannot be meaningfully adapted or
trained on CPU. GPU setup, accelerator selection, and training budgets
are decisions for the approved experimental phase, not this foundation.

No CUDA-specific package index is hard-coded in `pyproject.toml`: the
default PyPI index is used, so the same project resolves on CPU-only
machines and on GPU machines alike.

## Explicit non-goals (repository creation)

- No SmolLM3 weight or tokenizer downloads.
- No fine-tuning, training, or modification of any model.
- No attention, KV-cache, recurrent-state, or signal-head implementation.
- No final architecture selection.
- No dataset creation or download; no application-domain selection.
- No production inference server, cloud deployment, or multi-tenant
  serving.
- No full Python SDK; no message broker or database.
- No LangGraph, Polygrow, JEV, or other system integration.
- No web browsing, tool use, agentic behavior, or external actions.
- No periodic summarization; no per-event prompting shortcut.
- No claim that continuous operation, bounded memory, or low cost has
  already been achieved.
- Licensed under MIT — see [`LICENSE`](LICENSE) (decided by the owner
  2026-11-11; the upstream model's Apache 2.0 license does not
  determine this repository's code license).

## Evaluation philosophy

Evermind must not declare success merely because it can keep a socket
open, retain a cache, or classify isolated events. A model that retains
all previous tokens in an ever-growing cache does not satisfy the
bounded-state objective; one that receives a new instruction per event
violates Zero Instruction; one that relies on an external LLM to
summarize the stream does not demonstrate internal continuity; a rules
engine doing the detection while the model formats alerts does not
demonstrate learned Continuous Intelligence; a model that signals on
every event does not demonstrate useful silence; one that works on short
synthetic examples but degrades over long streams has not demonstrated
sustained continuity; and an accurate but prohibitively expensive system
has not achieved the central objective. Negative results are valuable:
if a simpler bounded-cache baseline performs as well as a novel
recurrent architecture at lower cost, that is reported honestly. See
[`docs/research/evaluation-plan.md`](docs/research/evaluation-plan.md).

## Contributing / next step

Do not begin experimental-phase work (architecture implementation,
training, datasets) without a separate instruction from the owner. The
most consequential open questions before that phase are listed in
[`docs/research-charter.md`](docs/research-charter.md#unresolved-decisions)
— application domain, architecture-selection criteria, and
evaluation thresholds among them.
