---
title: File checkpointing and rewind
triggers:
  - "undoing file changes the agent made"
  - "a restore point before a risky refactor"
  - "user messages have no uuid, or no checkpoint was found"
  - "ProcessTransport is not ready for writing"
---

# File checkpointing and rewind

Docs: https://code.claude.com/docs/en/agent-sdk/file-checkpointing

Snapshots files touched by `Write`, `Edit`, and `NotebookEdit` so you can restore
them. Two options are **both required** — checkpointing itself, and the flag that
makes user-message UUIDs (the checkpoint IDs) appear in the stream:

|               | Python                                      | TypeScript                                    |
| ------------- | ------------------------------------------- | --------------------------------------------- |
| Enable        | `enable_file_checkpointing=True`            | `enableFileCheckpointing: true`               |
| Receive UUIDs | `extra_args={"replay-user-messages": None}` | `extraArgs: { "replay-user-messages": null }` |

```python
options = ClaudeAgentOptions(
    enable_file_checkpointing=True,
    permission_mode="acceptEdits",
    extra_args={"replay-user-messages": None},
)

async with ClaudeSDKClient(options) as client:
    await client.query("Refactor the authentication module")
    async for message in client.receive_response():
        if isinstance(message, UserMessage) and message.uuid and not checkpoint_id:
            checkpoint_id = message.uuid          # the restore point
        if isinstance(message, ResultMessage):
            session_id = message.session_id

# rewind later: resume the session, open the connection, then rewind
async with ClaudeSDKClient(
    ClaudeAgentOptions(enable_file_checkpointing=True, resume=session_id)
) as client:
    await client.query("")                        # empty prompt opens the connection
    async for message in client.receive_response():
        await client.rewind_files(checkpoint_id)
        break
```

```typescript
const rewindQuery = query({
  prompt: "",
  options: { ...opts, resume: sessionId },
});
for await (const msg of rewindQuery) {
  await rewindQuery.rewindFiles(checkpointId); // { dryRun: true } to preview
  break;
}
```

Rewinding needs a live connection, which is why the resume call sends an **empty
prompt** and rewinds inside the first iteration — calling `rewindFiles` before the
stream is open is what produces `ProcessTransport is not ready for writing`.

Keeping only the latest `UserMessage.uuid` gives a rolling "before this turn"
restore point; collecting them all gives multiple restore points.

## Limitations

- **`Write` / `Edit` / `NotebookEdit` only** — changes made through `Bash` are not tracked.
- **Subagent edits are not tracked or restored** (except a `context: fork` skill
  running in the foreground); use git to revert those.
- Checkpoints are tied to the session that created them.
- File content only — creating, moving, or deleting **directories** is not undone.
- Local files only.
