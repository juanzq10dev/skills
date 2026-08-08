---
title: OpenTelemetry
triggers:
  - "exporting traces, metrics, or logs from agents"
  - "attributing agent activity to a service, tenant, or end user"
  - "short-lived runs exit before telemetry is flushed"
  - "controlling whether prompts or tool contents reach the backend"
---

# OpenTelemetry

Docs: https://code.claude.com/docs/en/agent-sdk/observability

Telemetry is configured entirely through environment variables in `env` — there are
no SDK options for it.

| Signal        | Contains                                              | Enable with                                                      |
| ------------- | ----------------------------------------------------- | ---------------------------------------------------------------- |
| Metrics       | Tokens, cost, sessions, lines of code, tool decisions | `OTEL_METRICS_EXPORTER`                                          |
| Log events    | Per prompt, API request, API error, tool result       | `OTEL_LOGS_EXPORTER`                                             |
| Traces (beta) | Spans per interaction, model request, tool call, hook | `OTEL_TRACES_EXPORTER` + `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` |

```python
OTEL_ENV = {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "CLAUDE_CODE_ENHANCED_TELEMETRY_BETA": "1",   # traces only
    "OTEL_TRACES_EXPORTER": "otlp",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "http/protobuf",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4318",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer your-token",
}
options = ClaudeAgentOptions(env=OTEL_ENV)
```

```typescript
options: { env: { ...process.env, ...otelEnv } }   // TS: env replaces, so spread
```

Short-lived calls can exit before the default export interval elapses. Lower it:

```python
{"OTEL_METRIC_EXPORT_INTERVAL": "1000",
 "OTEL_LOGS_EXPORT_INTERVAL": "1000",
 "OTEL_TRACES_EXPORT_INTERVAL": "1000"}
```

## Tagging

`OTEL_SERVICE_NAME` names the agent; `OTEL_RESOURCE_ATTRIBUTES` carries
`service.version`, `deployment.environment`, and per-request `enduser.id` /
`tenant.id`. **URL-encode user-supplied values** (`quote()` /
`encodeURIComponent()`) before interpolating them into that comma-separated string.

## Sensitive data is opt-in

| Variable                  | Adds                                                                                                                                                                                                      |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `OTEL_LOG_USER_PROMPTS=1` | Prompt text on `user_prompt` events and the `interaction` span                                                                                                                                            |
| `OTEL_LOG_TOOL_DETAILS=1` | Tool input arguments: file paths, shell commands, search patterns                                                                                                                                         |
| `OTEL_LOG_TOOL_CONTENT=1` | Full tool input and output bodies as span events (60 KB default, `CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH`); requires tracing                                                                                 |
| `OTEL_LOG_RAW_API_BODIES` | Full Messages API request/response JSON. `1` inlines (truncated); `file:<dir>` writes untruncated with a `body_ref`. **Includes the entire conversation history** and implies consent to everything above |

Enable the narrowest one that answers your question.
