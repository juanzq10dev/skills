---
title: Running in production
triggers:
  - "deploying an agent to a container, Kubernetes, or serverless"
  - "isolating tenants or untrusted code"
  - "monitoring, tracing, or budgeting a fleet of agents"
  - "sizing hosts for concurrent agents"
type: index
---

# Running in production

Everything here follows from one fact: **the SDK spawns the Claude Code CLI as a
subprocess, and that subprocess reads and writes the local filesystem.** Sessions,
memory, and settings are on disk; tools act on a real working directory.

Read in this order when standing up a deployment:

1. `hosting.md` — the subprocess model, session patterns, scaling, tenant isolation.
2. `secure-deployment.md` — sandboxing and credential handling, if the agent runs
   anything you don't fully trust.
3. `observability.md` — telemetry before you have an incident, not after.
4. `cost-tracking.md` — what `usage` and `total_cost_usd` actually count.

## Rules

- **ALWAYS bound a production agent.** There is no top-level session timeout — a
  session does not stop on its own. Set `maxTurns`, and `maxBudgetUsd` for spend.
- **ALWAYS give each session its own `cwd`.** It is the isolation boundary for
  working-directory artifacts and project-tier CLAUDE.md.
- **NEVER rely on default options for multi-tenant isolation.** Managed policy
  settings, `~/.claude.json`, and auto-memory are read regardless of
  `settingSources` (`../config/setting-sources.md`). Isolate with a per-tenant
  filesystem, `settingSources: []`, `CLAUDE_CONFIG_DIR`, and
  `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
- **NEVER put credentials where a tool can read them.** Inject them through a proxy
  outside the sandbox rather than mounting `~/.aws`, `~/.ssh`, or `.env`.

<!-- BEGIN GENERATED INDEX -->

- [Cost and token usage](./cost-tracking.md) — reporting what a run cost; token counts don't add up, or subagent spend seems missing; accumulating spend across many calls; per-model or per-step usage breakdown; extending the prompt cache TTL
- [Hosting and scaling](./hosting.md) — packaging an agent into a container or serverless function; choosing between ephemeral and long-running sessions; how many agents fit on a host; isolating tenants from each other; a session runs forever, or memory grows over a long run
- [OpenTelemetry](./observability.md) — exporting traces, metrics, or logs from agents; attributing agent activity to a service, tenant, or end user; short-lived runs exit before telemetry is flushed; controlling whether prompts or tool contents reach the backend
- [Sandboxing and credentials](./secure-deployment.md) — running an agent on untrusted code or untrusted input; choosing between a sandbox runtime, containers, gVisor, and VMs; keeping API keys out of the agent's reach; which host files must never be mounted

<!-- END GENERATED INDEX -->
