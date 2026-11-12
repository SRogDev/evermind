# Decisions

Lightweight research/architecture decision records (ADRs) for
Evermind. Record consequential choices here — with alternatives,
evidence, date, owner, and status — so later work can see *why* a
choice was made and challenge it with new evidence.

No decisions have been recorded yet beyond the foundation itself (the
initial model candidate and the principles, which are recorded in the
charter and in `continuous-intelligence-principles.md`).

## Template

Copy this template into a new file, `NNNN-short-title.md`, one file
per decision, numbered in order.

```markdown
# NNNN — Short title

- **Date:** YYYY-MM-DD
- **Owner:** (who decided)
- **Status:** accepted | provisional | pending
- **Context:** What problem was being solved? What constraints applied?
- **Decision:** What was decided, precisely.
- **Alternatives considered:** What else was on the table, and why it
  was not chosen.
- **Evidence:** What supports the decision (measurements, citations,
  verified checks). Link to experiments where applicable.
- **Consequences:** What this decision enables, and what it forecloses.
- **Revisit when:** What new evidence would reopen this decision.
```

## Statuses

- **accepted** — decided; changing it requires a new record superseding
  this one.
- **provisional** — the working choice, explicitly open to revision on
  defined evidence.
- **pending** — proposed but not decided; records the open question and
  what would decide it.
