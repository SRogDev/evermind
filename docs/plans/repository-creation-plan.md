# EVERMIND
## Repository Creation Plan for Muse
### Continuous Intelligence — Applied Model Architecture Research

**Purpose:** Instruct Muse to create the initial Evermind repository and its foundational research environment.

**Execution boundary:** Repository foundation and research documentation only. Do not download model weights, implement the model, modify SmolLM3, build a production runtime or SDK, create datasets, or start training. Establish a rigorous research home ready for a separately approved experimental phase.

---

# 1. Project identity

**Name:** Evermind  
**Research direction:** Continuous Intelligence

## Working research statement

Evermind investigates whether a pretrained small language model can be architecturally adapted and trained to operate as a persistent, instruction-free intelligence over continuous event streams, maintaining internal state across an effectively unbounded stream while keeping state size and inference cost bounded and very low.

This is a working research framing, not a claim that Continuous Intelligence is already an established formal ML subfield.

## Mission

Evermind aims to create a new kind of model: an intelligence that remains logically connected to an external information stream and continuously processes incoming events over long periods — hours, days, or longer — without being restarted as a new conversation for each event and without receiving a new instruction or prompt for every event.

The model learns what deserves attention. It processes events, updates its internal state, and emits a structured signal only when it detects something relevant according to the persistent signal configuration established for that connection or organization. Otherwise, it remains silent.

The central research challenge is not maximizing context length or building the best general-purpose context engine. It is making continuous intelligence operationally practical: **persistent inference, bounded state, low latency, high throughput, and extremely low cost.**

**Core identity:** A continuously operating intelligence, not a chatbot.

---

# 2. Core principles — preserve these exactly

These principles define the project. Do not weaken, reinterpret, or silently replace them.

## 2.1 Continuity lives inside the model

The primary research direction is **internal continuity**.

The model must maintain and update its own operational state as events arrive. The runtime may manage connections, transport, scheduling, isolation, and persistence of the model's actual inference state, but it must not simulate intelligence by repeatedly summarizing history and injecting that summary as a new prompt.

External storage may be useful for durability, recovery, or engineering operations. It is not a substitute for the model's internal continuous-processing mechanism.

The primary research direction is not an external-memory-first architecture.

## 2.2 One persistent logical session

Each connected stream has a persistent logical model session.

- Events arrive over time.
- The model processes each new event incrementally.
- The internal state is carried forward and updated.
- The model does not restart a fresh conversational context for each event.
- The session can remain logically active for long periods.
- The system should not require a continuously busy GPU when no events are arriving. Logical continuity does not mean wasting compute on empty time.

Do not assume this must be implemented as one permanently open autoregressive generation call. The engineering mechanism is an open research question. The required behavior is persistent logical inference with incremental state updates.

## 2.3 Zero Instruction during operation

Evermind does not receive a new instruction, conversational prompt, or task description for each event.

The model learns its signal-detection behavior during training and adaptation. At runtime it receives the event stream and updates its state without per-event prompting.

An organization or user may establish a **persistent signal configuration** before or when a stream is initialized. For example, a business may define the kinds of events or patterns that should be surfaced. This is configuration of the ongoing system, not a prompt repeated for every event.

How this persistent configuration should influence the model — for example through learned adapters, initialization/configuration encoding, a dedicated conditioning mechanism, or another method — remains a research and design question. Do not solve it by inserting a natural-language instruction into every event.

## 2.4 Silence is a first-class output

The model must not produce a response for every event.

Its operational outcomes are:

- **Silence:** no signal is warranted.
- **Signal:** a relevant pattern has been detected and a structured signal is emitted.

Silence is not a missing response or an error. It is an intended model behavior and must be represented and evaluated explicitly.

## 2.5 Evermind detects; other systems act

Evermind only emits structured signals. It does not call tools, browse the internet, execute external actions, invoke APIs on its own, run workflows, or modify external systems.

A separate application, Harness, or workflow engine decides what to do with an emitted signal.

## 2.6 Continuous event-stream intelligence, not periodic summarization

Evermind is intended to process incoming events as a continuing stream, updating its state incrementally.

It is not a system that polls an application every five or ten minutes, summarizes recent activity with a large LLM, and then looks for noteworthy changes.

Periodic processing may be used as a baseline in experiments, but it is not the target architecture.

## 2.7 Bounded state and low operating cost

A central research objective is to support effectively unbounded operating duration without an ever-growing inference state.

The system should investigate mechanisms that keep the active state bounded or controlled while preserving useful information for future detection.

The goal is not merely to make a model that can remain connected. It is to make that continuous operation economically viable at high event volumes.

---

# 3. Initial model foundation

## Accepted initial candidate

**SmolLM3-3B-Base**, developed by Hugging Face.

- Model: https://huggingface.co/HuggingFaceTB/SmolLM3-3B-Base
- Upstream project: https://github.com/huggingface/smollm
- Research report: locate and cite the official technical report from the model card or upstream project; do not invent a citation or assume a URL.

The model has been selected as Evermind's initial base-model candidate. The repository should document this choice and its rationale, but must not download or modify the weights during repository creation.

## Why this starting point

- Approximately 3 billion parameters: a reasonable capacity/cost starting point.
- Open weights and an Apache 2.0 model license as stated by the upstream project; verify the exact model card and artifact terms before redistribution or commercial deployment.
- A documented Transformer architecture and published model-development information.
- A practical starting point for architectural adaptation while retaining useful pretrained representations.
- A research compromise between semantic capability and inference cost.

Do not claim that 3B is proven to be the optimal size. It is an initial candidate, not a scientific conclusion.

## Base-model handling

- Use the **Base** checkpoint, not an instruction-tuned/chat checkpoint, as the initial candidate.
- Do not download weights during repository creation.
- Record the exact model identifier and upstream source.
- Before later training or distribution, verify the model card, license, upstream terms, tokenizer terms, and relevant training/data documentation.
- Do not assume all components or derived artifacts have identical licensing terms without checking.
- Keep the base model replaceable in research code so later comparisons are possible, but do not broaden initial scope into a large model survey.

---

# 4. Main scientific problem

Conventional autoregressive Transformer inference commonly uses a KV cache to avoid recomputing keys and values for previous tokens. In a long-running session, a conventional cache can grow with sequence length. Attention computation and memory traffic can also become increasingly expensive as history grows.

SmolLM3's Grouped-Query Attention can reduce KV-cache size relative to standard multi-head attention, but it does not by itself solve unbounded cache growth.

## Primary research question

**Can a pretrained approximately 3B-parameter language model be adapted into a continuously operating event-stream intelligence whose internal state remains bounded, whose state updates are incremental, and whose operating cost is low enough for sustained high-volume use — without per-event instructions?**

## Supporting research questions

1. What information must the model retain across events to detect temporally distributed patterns?
2. Can a bounded internal state preserve useful information that a conventional growing KV cache would otherwise retain?
3. Which architectural changes provide the best trade-off between detection quality, state size, latency, throughput, and compute cost?
4. Can the model learn to remain silent on irrelevant events while reliably emitting structured signals for relevant patterns?
5. How should persistent organization-level signal configuration be represented without per-event prompting?
6. How does detection quality change over long sessions — for example, after 24 hours, several days, or simulated longer streams?
7. Can the system pause computation between events while preserving logical session continuity?
8. What is the cost per million events under realistic event distributions and signal rates?

**Important distinction:** Evermind is not primarily optimizing for maximum context length, perfect long-document recall, or general-purpose memory quality. The target is continuous, low-cost inference with sufficient internal state to detect meaningful patterns over time.

---

# 5. Architectural research directions to document

Muse must document candidate approaches and trade-offs. Do not select or implement a final architecture during repository creation.

## A. KV-cache management and compression

Investigate:

- Sliding-window or bounded KV cache.
- Cache eviction and retention policies.
- KV quantization or compression.
- Selective retention of tokens or representations.
- Memory and compute behavior as a stream grows.
- Information lost when old cache entries are removed.

A bounded KV cache is a useful candidate and baseline, but simple truncation may destroy information needed for delayed or cross-event patterns.

## B. Recurrent or fixed-size internal state

Investigate architectures in which new events update a compact state rather than requiring the complete token history.

Questions:

- What is the state representation?
- How is it updated?
- How does it preserve temporal information?
- How can gradients train the state-update mechanism?
- What information is irreversibly lost?
- Can the state be reset, checkpointed, restored, or isolated per connection?

## C. Hybrid Transformer–recurrent architectures

Investigate whether the pretrained Transformer backbone can be adapted with recurrent state mechanisms or other efficient sequence-processing components.

Possible research families include recurrent memory mechanisms, state-space approaches, gated delta-rule architectures, and hybrid attention/recurrent designs. These are candidates for literature review, not approved implementation choices.

## D. Event-level incremental processing

Investigate how to represent and process incoming events efficiently.

Questions:

- Are events encoded as text, structured fields, or a combination?
- Can event boundaries be represented explicitly?
- Can multiple low-level events be accumulated or processed together without turning the system into periodic summarization?
- What is the minimum computation required to update state?
- Can the model avoid expensive full autoregressive text generation for every event?

## E. Signal emission and learned silence

Investigate how the model decides whether to emit a signal.

Candidates may include a learned signal head, structured output head, confidence/calibration mechanism, or another architecture integrated with the model.

The final design must be trained and evaluated for both detection and silence. Do not add an independent rules engine that becomes the actual intelligence while the model merely formats outputs.

---

# 6. Experimental baselines to plan

Document these candidate baselines; do not implement them now.

1. **Conventional pretrained model baseline:** SmolLM3-3B-Base adapted for event classification/detection using ordinary finite-context inference.
2. **External-memory / repeated-context baseline:** a conventional model supplied with bounded or summarized history. This is a comparison baseline, not the target architecture.
3. **Bounded KV-cache baseline:** a model using a limited cache or context window.
4. **Recurrent-state candidate:** a model whose internal state is updated across events.
5. **Hybrid candidate:** a combination of pretrained attention layers and recurrent or compressed state mechanisms.

The final research design must define fair comparisons: equivalent data, event order, signal definitions, training budget where feasible, and clearly stated resource constraints.

Do not assume the most architecturally novel approach will win.

---

# 7. Training and adaptation principles

## Starting point

Evermind starts from pretrained SmolLM3-3B-Base. It is not trained from random initialization.

## Adaptation is more than a prompt or a classifier

Investigate the combination of:

- fine-tuning the pretrained backbone where justified;
- training newly introduced recurrent/state-update components;
- training event-processing and signal-emission components;
- sequence-level training that teaches behavior across multiple events;
- long-stream training or simulation that exposes state degradation and delayed patterns.

Parameter-efficient fine-tuning methods may be evaluated as baselines or tools, but **LoRA-only adaptation is not the predetermined solution**. If the research hypothesis requires changes to internal computation or state mechanisms, the training plan must support those changes.

## Training-loop policy

- Use PyTorch as the primary framework.
- Use `uv` for Python project and dependency management.
- Keep the training loop explicit and inspectable.
- Do not use Hugging Face Trainer as a black box for the core research loop.
- Use Hugging Face libraries where useful for loading, tokenization, or interoperability, while retaining control over the architecture and experimental procedure.
- Do not reinvent PyTorch or build a new deep-learning framework.

## Data requirements

Do not choose an application domain or invent a dataset during repository creation.

Future data design needs:

- ordered event sequences;
- timestamps or explicit temporal ordering;
- labels for signal and non-signal outcomes;
- multi-event patterns where a signal only becomes detectable over time;
- long negative/noise stretches;
- delayed signals and rare events;
- realistic event rates and distributions;
- organization-specific signal configurations where applicable;
- train/validation/test separation by stream, entity, or time to prevent leakage;
- documented provenance, permissions, and licenses.

Synthetic data may be useful for controlled tests, but is not sufficient evidence of real-world usefulness.

The initial application domain remains undecided and requires owner approval before dataset creation.

---

# 8. Runtime and Python SDK — intended product boundary

Document the future runtime and SDK responsibilities, but do not build them during this task.

## Conceptual system

```text
External application / event producer
              |
              v
       Evermind Python SDK
              |
      persistent connection
              |
              v
       Evermind runtime
              |
     isolated model session
              |
              v
  Continuous Intelligence model
  - pretrained backbone
  - internal persistent state
  - incremental state update
  - learned signal / silence behavior
              |
              v
     structured signal output
              |
              v
External application / Harness / workflow engine
```

## Runtime responsibilities

The future runtime may:

- accept and authenticate stream connections;
- associate each connection with its organization and persistent signal configuration;
- manage isolated model state per connection;
- feed events incrementally into the model;
- persist/checkpoint actual model state for recovery where necessary;
- manage scheduling and batching for efficient hardware utilization;
- emit structured signals;
- expose operational metrics and health information.

The runtime must not become an external context summarizer that repeatedly instructs a conventional LLM.

## Python SDK responsibilities

The future SDK should make integration straightforward:

- establish and maintain a connection to Evermind;
- configure persistent signal preferences before or at stream initialization;
- publish or forward events;
- optionally integrate selected application endpoints through middleware;
- integrate existing webhook or event producers where useful;
- consume structured signals;
- handle reconnection and delivery semantics clearly.

Middleware is optional and selective. Evermind must not become a mandatory proxy in the application's normal request path.

The SDK is integration ergonomics, not intelligence.

## Multi-tenancy

The intended serving pattern is shared model weights with isolated per-organization/per-connection state and configuration.

Do not duplicate full model weights for each organization by default. Do not allow state, events, or signal configuration to leak across tenants.

The exact serving, batching, state-isolation, and resource-allocation design remains open.

---

# 9. Repository creation tasks

## Phase 0 — Workspace and identity audit

1. Inspect the current workspace and determine whether an Evermind repository already exists.
2. If one exists, inspect it before modifying anything.
3. Inspect available user-provided development and research guidelines.
4. Confirm the repository name is `evermind` unless an exact existing name has been established.
5. Preserve existing content. Do not delete or overwrite without authorization.
6. Do not publish or change repository visibility without explicit authorization.
7. If remote repository creation is unavailable, create the local repository and report the exact manual step required.

## Phase 1 — Create a clean research repository

Use this as the initial structural proposal. Adapt only with a concrete reason and document deviations.

```text
evermind/
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── .editorconfig
├── docs/
│   ├── research-charter.md
│   ├── problem-definition.md
│   ├── continuous-intelligence-principles.md
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── internal-state-and-continuity.md
│   │   ├── kv-cache-research.md
│   │   ├── candidate-architectures.md
│   │   └── runtime-and-sdk-boundary.md
│   ├── research/
│   │   ├── research-questions.md
│   │   ├── hypotheses.md
│   │   ├── baselines.md
│   │   ├── evaluation-plan.md
│   │   └── dataset-strategy.md
│   ├── decisions/
│   │   └── README.md
│   └── references/
│       └── README.md
├── src/
│   └── evermind/
│       ├── __init__.py
│       ├── README.md
│       ├── model/
│       │   └── README.md
│       ├── state/
│       │   └── README.md
│       ├── events/
│       │   └── README.md
│       ├── signals/
│       │   └── README.md
│       ├── training/
│       │   └── README.md
│       ├── evaluation/
│       │   └── README.md
│       └── runtime/
│           └── README.md
├── experiments/
│   ├── README.md
│   └── templates/
│       └── experiment.yaml
├── tests/
│   ├── unit/
│   └── integration/
├── scripts/
│   └── README.md
└── .github/
    └── workflows/
        └── ci.yml
```

Structure rules:

- Keep `src/evermind` ready for future research implementation, but do not implement model components now.
- `model/` will eventually contain the adapted backbone and model architecture.
- `state/` will eventually contain internal state representations and update mechanisms.
- `events/` will eventually contain event representations and input processing.
- `signals/` will eventually contain structured signal/silence outputs and associated learned components.
- `training/` and `evaluation/` will contain explicit research code.
- `runtime/` is a future runtime boundary, not permission to build a production server now.
- Do not create empty directories that Git cannot track; use concise README files where placeholders are useful.
- Do not add a database, broker, dashboard, production API, cloud deployment, distributed serving stack, or SDK package at this stage.

## Phase 2 — Python project foundation

Create a valid `pyproject.toml` and initialize the environment using `uv`.

Requirements:

1. Select a Python version compatible with intended PyTorch and model-loading dependencies. Verify compatibility rather than guessing.
2. PyTorch is the primary deep-learning dependency.
3. Add only dependencies justified for the repository foundation. Likely future categories include Transformers/tokenizers, safetensors, pytest, and formatting/linting tools, but avoid installing everything before needed.
4. Keep model-loading dependencies distinct from the core PyTorch requirement where practical.
5. Generate `uv.lock` if dependency resolution succeeds.
6. Document CPU setup and explain that actual model adaptation/training will require suitable GPU resources.
7. Do not hard-code a CUDA-specific package index that is unsuitable for other environments.
8. Do not download SmolLM3 weights or datasets.
9. Provide commands for environment setup, tests, linting/formatting, and a minimal CPU smoke test.

The project must not use Hugging Face Trainer as its core training abstraction.

## Phase 3 — Write the foundational documents

These documents must contain project-specific substance, not generic AI project boilerplate.

### `README.md`

Include:
- Evermind's mission and research framing.
- The exact meaning of Continuous Intelligence in this project.
- Zero-instruction runtime principle.
- Persistent logical session and internal continuity.
- Silence as a first-class output.
- SmolLM3-3B-Base as the initial model candidate.
- The distinction between Evermind and Small Lab.
- Repository map.
- Technical stack and setup.
- Research status: foundation only; no architecture or model has been implemented or validated yet.
- Explicit non-goals.

### `docs/research-charter.md`

Create the initial research charter using the identity and principles in this plan. Include vision, research problem, primary/supporting research questions, working hypotheses, scope/non-goals, initial model candidate, evaluation principles, unresolved decisions, and criteria for approving the first experimental phase.

Clearly mark hypotheses as hypotheses, not established facts.

### `docs/problem-definition.md`

Formalize these concepts:
- event stream;
- event;
- stream/connection;
- persistent organization-level signal configuration;
- internal model state;
- state update;
- signal;
- silence;
- detection delay;
- session continuity;
- bounded state;
- event-processing cost.

Describe temporal patterns that may require multiple events before a signal is warranted. Do not choose the first application domain.

### `docs/continuous-intelligence-principles.md`

Record the invariants:
- no per-event instructions or prompts;
- internal continuity is the primary direction;
- one persistent logical session per stream;
- incremental event processing;
- silence is intentional;
- signals are structured outputs;
- Evermind does not execute actions;
- bounded state and low cost are central objectives;
- no periodic LLM summarization as the target architecture.

### `docs/architecture/overview.md`

Include conceptual data flow from external producers through SDK/runtime into the model and back out as signals.

Clearly distinguish model, internal state, runtime, SDK, and downstream application/Harness responsibilities. Do not present an unapproved architecture as final.

### `docs/architecture/internal-state-and-continuity.md`

Explain the desired persistent logical session and why internal state must be carried forward.

Discuss conventional Transformer KV cache, growth with sequence length, the distinction between logical session persistence and a permanently busy generation loop, event arrival and incremental state update, state checkpointing/recovery as an engineering concern, and the bounded-state objective.

Mark implementation mechanisms as unresolved.

### `docs/architecture/kv-cache-research.md`

Explain the research problem and compare:
- GQA and its effect on cache size, noting it does not by itself bound cache growth;
- sliding-window/bounded KV cache;
- cache eviction and selective retention;
- KV quantization/compression;
- recurrent/fixed-size state;
- hybrid attention plus recurrent state.

For each, document potential benefits, failure modes, information-loss risks, compute implications, and experiments needed.

Do not select a winning method or claim a technique will work without evidence.

### `docs/architecture/candidate-architectures.md`

Compare at least three architecture families:

1. Conventional Transformer with bounded KV cache.
2. Pretrained Transformer augmented with recurrent or fixed-size internal state.
3. Hybrid Transformer/recurrent architecture.

Include external-memory/repeated-context approaches as comparison baselines, not the main research direction.

For each, discuss expected state size, per-event compute, long-range temporal information, training complexity, compatibility with pretrained weights, likely failure modes, and evaluation needed.

### `docs/architecture/runtime-and-sdk-boundary.md`

Document future SDK/runtime responsibilities and multi-tenant boundaries from Section 8. Explicitly state that neither production runtime nor SDK is part of repository creation.

### `docs/research/research-questions.md`

List the primary and supporting research questions, with the primary question clearly distinguished.

### `docs/research/hypotheses.md`

Create falsifiable working hypotheses, such as:

- A pretrained ~3B model can be adapted to detect useful event-stream signals without per-event instructions.
- A learned internal state mechanism can preserve relevant temporal information with bounded state.
- A bounded or recurrent state architecture can reduce long-session memory growth compared with an unbounded conventional KV cache.
- Training on long event sequences can improve detection of multi-event patterns compared with independent event classification.
- A learned silence/signal mechanism can achieve useful recall while controlling false alarms.
- An adapted architecture can achieve a lower cost per million events than a conventional large-LLM monitoring pipeline.

For each hypothesis, identify evidence that would support it and results that would falsify or weaken it. Do not invent numeric thresholds; those require later approval and domain-specific evidence.

### `docs/research/baselines.md`

Document baseline families from Section 6 and requirements for fair comparisons.

### `docs/research/evaluation-plan.md`

Define metrics to investigate and report.

**Detection quality**
- precision;
- recall;
- F1;
- false positives and false negatives;
- false alarms per hour or per stream-day;
- signal calibration where applicable.

**Temporal behavior**
- detection delay;
- multi-event pattern detection;
- state degradation over time;
- recovery after checkpoint/restart;
- performance across long sessions.

**Efficiency**
- memory footprint per active stream;
- KV cache or recurrent-state size over time;
- events per second;
- latency p50/p95/p99;
- compute utilization;
- energy or accelerator time where measurable;
- cost per million events;
- idle cost when no events arrive.

**Long-running evaluation**
- 24-hour stream simulation;
- multi-day simulation;
- long negative/noise intervals;
- bursty event arrivals;
- rare signals;
- concurrent streams and tenant isolation.

Explain that benchmark definitions and numeric acceptance thresholds must be approved after the first domain and data strategy are selected.

### `docs/research/dataset-strategy.md`

Document data requirements and risks from Section 7. Keep the initial domain explicitly undecided. Do not scrape, generate, or download datasets.

### `docs/references/README.md`

Define how to record literature: paper title, authors, year, venue/preprint, canonical URL/DOI/arXiv identifier, relevant method, supported claim, limitations, and relevance to Evermind.

Do not fabricate citations. If Muse performs literature discovery during this repository task, add only verified sources and distinguish primary research from secondary commentary. A full literature review is not required yet.

### `docs/decisions/README.md`

Provide a lightweight research/architecture decision-record template. Record consequential choices, alternatives, evidence, date, owner, and whether the decision is accepted, provisional, or pending.

### `experiments/README.md` and `experiments/templates/experiment.yaml`

Explain how future experiments are organized. Provide an illustrative configuration template with fields such as experiment ID/title, research question/hypothesis, status, base model/revision, architecture variant, event representation, state mechanism, dataset/provenance, training configuration, evaluation metrics, compute environment, and reproducibility metadata.

Mark it as a template, not an approved experiment.

## Phase 4 — Minimal quality gates

Add lightweight CI that:
- installs the package in a CPU-compatible environment;
- runs basic tests;
- checks formatting/linting if configured;
- does not download SmolLM3 weights;
- does not download datasets;
- does not run model training.

Add a minimal CPU smoke test verifying the package imports and PyTorch is available. Do not implement a model architecture just to satisfy CI.

If PyTorch installation in CI is too expensive or unreliable, explain the limitation and propose a suitable minimal check rather than silently omitting validation.

---

# 10. Evaluation philosophy — avoid misleading success

The project must not declare success merely because it can keep a socket open, retain a cache, or classify isolated events.

- A model that retains all previous tokens in an ever-growing cache does not satisfy the bounded-state objective.
- A model that receives a new natural-language instruction for every event violates Zero Instruction.
- A model that relies on an external LLM to summarize the stream does not demonstrate the intended internal continuity.
- A rules engine that performs the actual detection while the model merely formats alerts does not demonstrate learned Continuous Intelligence.
- A model that emits a signal for every event does not demonstrate useful silence.
- A model that works on short synthetic examples but degrades over long streams has not demonstrated sustained continuity.
- A system that is accurate but prohibitively expensive has not achieved the central objective.

Negative results are valuable. If a simpler bounded-cache baseline performs as well as a novel recurrent architecture at lower cost, report that honestly.

---

# 11. Explicit non-goals for repository creation

Do NOT:
- Download SmolLM3 weights or tokenizer assets.
- Fine-tune, train, or modify any model.
- Implement attention, KV-cache modifications, recurrent state, or a signal head.
- Select a final architecture.
- Create or download a dataset.
- Select an application domain without owner approval.
- Build a production inference server or cloud deployment.
- Build the full Python SDK.
- Add a message broker or database.
- Implement a production multi-tenant serving system.
- Integrate LangGraph, Polygrow, JEV, or other systems.
- Add web browsing, tool use, agentic behavior, or external action execution.
- Turn Evermind into a periodic summarization system.
- Introduce per-event prompting as a shortcut.
- Claim continuous operation, bounded memory, or low cost has already been achieved.
- Publish the repository or select a repository license without owner authorization.
- Make irreversible architecture decisions.

A repository license file should only be added if the owner has selected one. The upstream model's license does not automatically determine the license of Evermind's code. If no repository license decision exists, leave it pending and report it.

---

# 12. Acceptance criteria

The task is complete only when:

1. The authorized Evermind repository exists.
2. Its identity and mission clearly describe Continuous Intelligence.
3. Documentation preserves internal continuity as the primary research direction.
4. Zero Instruction is defined correctly, including the distinction between persistent signal configuration and per-event prompts.
5. SmolLM3-3B-Base is recorded without downloading weights.
6. KV-cache growth and bounded-state research are explicitly documented.
7. At least three candidate architecture families and relevant baselines are compared conceptually.
8. Research questions, hypotheses, metrics, and dataset requirements are documented.
9. Runtime and SDK responsibilities are separated from model intelligence.
10. Multi-tenant state isolation is documented as a requirement, not prematurely implemented.
11. Python/PyTorch/`uv` foundations are configured and validated as far as the environment permits.
12. CI and basic tests do not require model downloads or training.
13. No model, production runtime, SDK, or dataset has been implemented or created.
14. Open decisions and deviations are clearly reported.

---

# 13. Final report required from Muse

When finished, provide:

1. Repository location and whether it is local or remotely created.
2. Final directory tree.
3. Python, PyTorch, and dependency-management decisions.
4. Commands executed and outcomes.
5. Test and CI validation results.
6. Documents created and their purpose.
7. Confirmation that SmolLM3 weights were not downloaded.
8. Confirmation that no architecture, training, runtime, SDK, or dataset was implemented.
9. Unresolved decisions requiring owner approval.
10. Any deviations from this plan and why they were necessary.
11. A short list of the most consequential questions to resolve before Phase 2.

Do not begin Phase 2 research implementation or training without a separate instruction from the owner.

---

# 14. Operating instruction for Muse

Work autonomously on routine repository setup and documentation. Do not ask the owner to approve every filename or ordinary implementation detail.

Pause and ask before consequential or irreversible decisions, including:
- publishing or changing repository visibility;
- selecting or adding a repository license;
- deleting or overwriting existing content;
- downloading large weights or datasets;
- choosing a final architecture;
- choosing the first application domain;
- introducing a major dependency or framework;
- changing any core principle in Section 2.

If a capability is unavailable, explain the limitation and leave the repository in the cleanest valid state possible. Never claim that a command, test, repository creation, or validation succeeded unless it actually did.
