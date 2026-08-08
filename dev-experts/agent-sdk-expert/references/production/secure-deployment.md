---
title: Sandboxing and credentials
triggers:
  - "running an agent on untrusted code or untrusted input"
  - "choosing between a sandbox runtime, containers, gVisor, and VMs"
  - "keeping API keys out of the agent's reach"
  - "which host files must never be mounted"
---

# Sandboxing and credentials

Docs: https://code.claude.com/docs/en/agent-sdk/secure-deployment

Least privilege by resource: mount only the directories needed and prefer read-only;
restrict network to specific endpoints via a proxy; inject credentials at the proxy
rather than exposing them; drop Linux capabilities.

| Technology                                        | Isolation                 | Overhead    | Complexity  |
| ------------------------------------------------- | ------------------------- | ----------- | ----------- |
| Sandbox runtime (`@anthropic-ai/sandbox-runtime`) | Good (secure defaults)    | Very low    | Low         |
| Containers (Docker)                               | Setup dependent           | Low         | Medium      |
| gVisor                                            | Excellent (correct setup) | Medium/High | Medium      |
| VMs (Firecracker, QEMU)                           | Excellent (correct setup) | High        | Medium/High |

```bash
docker run \
  --cap-drop ALL --security-opt no-new-privileges \
  --security-opt seccomp=/path/to/seccomp-profile.json \
  --read-only --tmpfs /tmp:rw,noexec,nosuid,size=100m \
  --network none --memory 2g --cpus 2 --pids-limit 100 --user 1000:1000 \
  -v /path/to/code:/workspace:ro \
  -v /var/run/proxy.sock:/var/run/proxy.sock:ro \
  agent-image
```

`--network none` plus a mounted Unix socket routes all egress through a proxy
outside the container. `--userns-remap` and `--ipc private` harden further. gVisor
adds ~0% overhead on CPU-bound work, ~2× on simple syscalls, and **10–200× on heavy
file I/O** — measure before choosing it.

## Credentials: the proxy pattern

Keep the key outside the sandbox and let a proxy inject it:

```bash
export ANTHROPIC_BASE_URL="http://localhost:8080"     # Anthropic traffic
export HTTP_PROXY="http://localhost:8080"             # other services
export HTTPS_PROXY="http://localhost:8080"
```

For non-Anthropic services, a custom tool whose handler holds the credential
(`../tools/custom-tools.md`) keeps it out of the container entirely.

## Never mount these

`.env` / `.env.local`, `~/.git-credentials`, `~/.aws/credentials`,
`~/.config/gcloud/application_default_credentials.json`, `~/.azure/`,
`~/.docker/config.json`, `~/.kube/config`, `.npmrc`, `.pypirc`,
`*-service-account.json`, `*.pem`, `*.key`.

Mount code read-only (`-v /path/to/code:/workspace:ro`) and provide writable space
as tmpfs so nothing persists between runs.

Sandboxing complements, and does not replace, the SDK's own controls — permission
rules and `PreToolUse` hooks (`../tools/permissions.md`, `../hooks.md`) are the
in-process layer of the same defense in depth.
