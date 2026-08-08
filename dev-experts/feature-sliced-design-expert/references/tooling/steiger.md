---
title: Steiger — installing, running and configuring
triggers:
  - "setting up the FSD linter in a project or in CI"
  - "running the architecture check in watch mode"
  - "disabling a rule for a folder such as shared"
  - "upgrading a steiger config from the 0.4 format"
---

# Steiger

Universal file-structure and project-architecture linter, with a built-in ruleset for FSD.
Versions at time of writing: `steiger` 0.6.0, `@feature-sliced/steiger-plugin` 0.7.0 (beta).

```bash
npm i -D steiger
npm i -D @feature-sliced/steiger-plugin   # required for the FSD rules

npx steiger ./src            # zero-config
npx steiger ./src --watch    # -w, re-checks on change
```

Point it at the **FSD root** — the folder containing the layers — not the repo root.

## Configuration

Zero-config by default. Configure via `cosmiconfig`: `steiger.config.ts` or `steiger.config.js` at
the project root. The shape follows ESLint's flat config, and `defineConfig` gives autocompletion.

```javascript
// ./steiger.config.js
import { defineConfig } from "steiger";
import fsd from "@feature-sliced/steiger-plugin";

export default defineConfig([
  ...fsd.configs.recommended,
  {
    // disable the public-api rule only for the Shared layer
    files: ["./src/shared/**"],
    rules: {
      "fsd/public-api": "off",
    },
  },
  {
    files: ["./src/widgets/**"],
    ignores: ["**/discount-offers/**"],
    rules: { "fsd/no-segmentless-slices": "off" },
  },
  { ignores: ["**/__mocks__/**"] }, // ignore paths for every rule
]);
```

Later objects override earlier ones, so spread `...fsd.configs.recommended` first.

Steiger is **not yet extendable with custom rules**. The full built-in ruleset:
`steiger-rules.md`.

Docs: <https://github.com/feature-sliced/steiger>
