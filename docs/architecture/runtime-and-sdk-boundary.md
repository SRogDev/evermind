# Runtime and SDK Boundary

**Status:** Future design boundary, documented now so the model
research is not confused with product engineering. **Neither the
production runtime nor the SDK is part of repository creation.** Nothing
in this document is implemented.

## The boundary in one sentence

The model detects; the runtime serves the model; the SDK connects
applications to the runtime; a Harness or application acts on signals.
Intelligence lives only in the model.

## Future runtime responsibilities

The future runtime may:

- Accept and authenticate stream connections.
- Associate each connection with its organization and persistent signal
  configuration.
- Manage isolated model state per connection.
- Feed events incrementally into the model.
- Persist/checkpoint actual model state for recovery where necessary.
- Manage scheduling and batching for efficient hardware utilization.
- Emit structured signals.
- Expose operational metrics and health information.

The runtime must not become an external context summarizer that
repeatedly instructs a conventional LLM. If the runtime is doing the
remembering, the research has failed — however well the system appears
to work.

## Future Python SDK responsibilities

The future SDK should make integration straightforward:

- Establish and maintain a connection to Evermind.
- Configure persistent signal preferences before or at stream
  initialization.
- Publish or forward events.
- Optionally integrate selected application endpoints through
  middleware.
- Integrate existing webhook or event producers where useful.
- Consume structured signals.
- Handle reconnection and delivery semantics clearly.

Middleware is optional and selective. Evermind must not become a
mandatory proxy in the application's normal request path.

The SDK is integration ergonomics, not intelligence.

## Multi-tenancy

The intended serving pattern is **shared model weights with isolated
per-organization/per-connection state and configuration**.

- Do not duplicate full model weights for each organization by default.
- Do not allow state, events, or signal configuration to leak across
  tenants.
- State isolation is a **requirement**, documented here, not
  prematurely implemented: no isolation mechanism, tenant model, or
  serving code exists in this repository.

The exact serving, batching, state-isolation, and resource-allocation
design remains open.

## What is explicitly not built now

- No production inference server or cloud deployment.
- No full Python SDK (the `src/evermind/runtime/` package contains only
  a placeholder README).
- No message broker or database.
- No production multi-tenant serving system.
- No authentication/authorization implementation.

The `src/evermind/runtime/` directory exists to reserve the namespace
for the future boundary — it is a placeholder, not permission to build
a production server in this phase.
