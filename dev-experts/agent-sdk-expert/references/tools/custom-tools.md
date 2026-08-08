---
title: Custom tools (SDK MCP server)
triggers:
  - "letting the agent call your own function, API, or database"
  - "defining a tool with a schema and an async handler"
  - "returning an image, a file, or machine-readable JSON from a tool"
  - "controlling the error message the model sees when a tool fails"
  - "an optional tool parameter"
---

# Custom tools (SDK MCP server)

Docs: https://code.claude.com/docs/en/agent-sdk/custom-tools

Define a function, wrap it in an **in-process** MCP server (no separate process),
and pass it as `mcpServers`. Four parts: name, description, input schema, async
handler.

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, query, ClaudeAgentOptions

@tool("get_temperature", "Get the current temperature at a location",
      {"latitude": float, "longitude": float})
async def get_temperature(args):
    return {"content": [{"type": "text", "text": f"Temperature: {fetch(args)}°F"}]}

weather_server = create_sdk_mcp_server(name="weather", version="1.0.0",
                                       tools=[get_temperature])

options = ClaudeAgentOptions(
    mcp_servers={"weather": weather_server},
    allowed_tools=["mcp__weather__get_temperature"],
)
```

```typescript
import {
  tool,
  createSdkMcpServer,
  query,
} from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const getTemperature = tool(
  "get_temperature",
  "Get the current temperature at a location",
  {
    latitude: z.number().describe("Latitude"),
    longitude: z.number().describe("Longitude"),
  },
  async (args) => ({
    content: [{ type: "text", text: `Temperature: ${await fetch2(args)}°F` }],
  }),
);

const weatherServer = createSdkMcpServer({
  name: "weather",
  version: "1.0.0",
  tools: [getTemperature],
});

query({
  prompt: "What's the temperature in SF?",
  options: {
    mcpServers: { weather: weatherServer },
    allowedTools: ["mcp__weather__get_temperature"], // or "mcp__weather__*"
  },
});
```

The `mcpServers` key becomes the server segment: `mcp__{server}__{tool}`.

Schemas: TypeScript is always Zod (handler args are typed from it). Python takes a
`{name: type}` dict, or a **full JSON Schema dict** when you need enums, ranges, or
nested objects — the dict form has no enum support.

Handler returns `content` (required; blocks of type `text`, `image`, `audio`,
`resource`, `resource_link`), plus optional `structuredContent` and `isError`
(Python: `is_error`).

## Optional parameters

TypeScript: add `.default(...)` to the Zod field. Python: the dict schema makes
every key required, so **leave the parameter out of the schema**, describe it in the
description string, and read it with `args.get("hours", 12)`.

## Annotations

Fifth argument to `tool()` in TypeScript, `annotations=ToolAnnotations(...)` in
Python. `readOnlyHint` (default `false`) is the only one that changes behavior — it
enables parallel execution. `destructiveHint`, `idempotentHint`, `openWorldHint`
are informational. They are metadata, not enforcement: keep them true to the handler.

## Errors, images, structured data

An uncaught exception does **not** stop the loop — the in-process server converts it
to an error result carrying the raw message. Catch it and return `isError: true`
with a composed message when the raw exception isn't actionable for the model.

Image blocks carry raw base64 in `data` (no `data:image/...;base64,` prefix) plus a
required `mimeType`; fetch and encode in the handler, there is no URL field.
Resource blocks carry content inline in `resource.text` or `resource.blob` — the
`uri` is a label the SDK never reads.

## Common Anti-Patterns

- Setting `structuredContent` and expecting your text blocks through → when it is
  set, Claude receives the JSON plus image/resource blocks, and **text blocks are
  dropped** as assumed duplicates.
- `structuredContent` from Python's `@tool` → the decorator forwards only `content`
  and `is_error`. Run a standalone MCP server (`mcp.md`) if you need it.
- Binary `resource.blob` from Python → dropped with a warning (TypeScript only).
  Python also drops `audio` blocks; TypeScript saves them to disk and passes a path.
- Forgetting `allowedTools` → the tool is visible but every call needs permission.
