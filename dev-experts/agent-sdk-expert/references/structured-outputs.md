---
title: Structured JSON output
triggers:
  - "the agent's answer must be validated JSON, not prose"
  - "using Zod or Pydantic to type an agent's final result"
  - "error_max_structured_output_retries, or the schema was ignored"
---

# Structured JSON output

Docs: https://code.claude.com/docs/en/agent-sdk/structured-outputs

Pass a JSON Schema as `outputFormat` / `output_format`. The agent still uses any
tools it needs; the SDK validates the final output against the schema and re-prompts
on mismatch, then puts it on `ResultMessage.structured_output`.

```typescript
for await (const message of query({
  prompt: "Research Anthropic and provide key company information",
  options: {
    outputFormat: {
      type: "json_schema",
      schema: {
        type: "object",
        properties: {
          company_name: { type: "string" },
          founded_year: { type: "number" },
        },
        required: ["company_name"],
      },
    },
  },
})) {
  if (
    message.type === "result" &&
    message.subtype === "success" &&
    message.structured_output
  ) {
    console.log(message.structured_output);
  }
}
```

```python
async for message in query(
    prompt="Research Anthropic and provide key company information",
    options=ClaudeAgentOptions(output_format={"type": "json_schema", "schema": schema}),
):
    if isinstance(message, ResultMessage) and message.structured_output:
        print(message.structured_output)
```

## Zod and Pydantic

The SDK validates against **JSON Schema draft-07**, and rejects schemas declaring a
newer draft. Zod targets 2020-12 by default, so convert explicitly:

```typescript
const schema = z.toJSONSchema(FeaturePlan, { target: "draft-7" }); // then parse the result
const parsed = FeaturePlan.safeParse(message.structured_output);
```

```python
output_format={"type": "json_schema", "schema": FeaturePlan.model_json_schema()}
plan = FeaturePlan.model_validate(message.structured_output)
```

## Error handling

`subtype: "error_max_structured_output_retries"` means no valid output remained —
either repeated validation failures, or a model fallback retracting a completed
output with no successful retry. Read the result's `errors` list to tell them apart
before rewriting the schema.

## Common Anti-Patterns

- Trusting `subtype == "success"` alone → a run can succeed with
  `structured_output` absent. Check both (`troubleshooting.md`).
- Deeply nested schemas with many required fields → harder to satisfy; start simple,
  make fields optional where the task may not supply them.
- Assuming an invalid schema is ignored → since v2.1.205 it fails the run at startup
  naming the problem. `"format"` keywords are accepted as annotations, not enforced.
