# SKILLS

A set of software development skills, distributed as a Claude Code plugin marketplace.

## Skills

| Skill | Description |
| :---- | :---------- |
| `create-expert-skill` | Turns a documentation URL, `llms.txt`, or GitHub repo into a "library expert" skill |
| `htmx-expert` | Expert guidance for htmx 2.0.x — attributes, swaps, events, extensions, and UI patterns |
| `python-code-writing` | Conventions for writing Python |
| `skill-review` | Scores a skill against a 6-criterion analytic rubric and returns located, prioritized fixes |
| `ts-code-writing` | Conventions for writing TypeScript |

## Install

Run these in Claude Code on any machine:

```
/plugin marketplace add juanzq10dev/skills
/plugin install dev-skills@juanzq10dev
/reload-plugins
```

The skills are namespaced by the plugin, so you invoke them as `/dev-skills:htmx-expert`,
`/dev-skills:ts-code-writing`, and so on. Claude also loads them automatically when a task
matches their description.

Equivalent from a terminal, without starting a session:

```bash
claude plugin marketplace add juanzq10dev/skills
claude plugin install dev-skills@juanzq10dev
```

To confirm the install and see which skills were picked up:

```bash
claude plugin details dev-skills
```

### Updating

```
/plugin marketplace update juanzq10dev
/plugin update dev-skills@juanzq10dev
```

### Uninstalling

```
/plugin uninstall dev-skills@juanzq10dev
/plugin marketplace remove juanzq10dev
```

## Local development

To work on the skills and use them at the same time, register the marketplace from your
clone instead of from GitHub. It then tracks the working tree directly:

```bash
git clone git@github.com:juanzq10dev/skills.git
claude plugin marketplace add "$PWD/skills"
claude plugin install dev-skills@juanzq10dev
```

Edits to a `SKILL.md` take effect in the current session. Changes to `plugin.json`,
`hooks/`, `agents/`, or `.mcp.json` need `/reload-plugins`.

Re-adding the marketplace under the same name replaces the previous entry, so you can
switch between the local clone and GitHub at any time.

## Layout

```
.claude-plugin/
  marketplace.json   catalog listing the dev-skills plugin
  plugin.json        plugin metadata (name, version)
skills/
  <skill-name>/
    SKILL.md         entrypoint, with YAML frontmatter
    references/      supporting files, loaded on demand
```

`marketplace.json` declares `"source": "./"`, which makes the repository root itself the
plugin. Skills are discovered by the default scan of `skills/`, so adding a new skill is
just a new directory with a `SKILL.md` — no manifest change needed.

Validate the manifests after editing them:

```bash
claude plugin validate .
```
