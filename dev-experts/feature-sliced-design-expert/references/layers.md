---
title: Layers and the import rule
triggers:
  - "deciding which of the 7 layers a file or folder belongs on"
  - "checking whether an import is legal in FSD"
  - "an import goes sideways or upwards and needs to be fixed"
  - "explaining what app, pages, widgets, features, entities or shared are for"
  - "someone asks about the processes layer"
---

# Layers

7 layers, most responsibility/dependency first. Folders are lowercase and live at the FSD root
(usually `src/`). **Never invent a new layer** — the names are standardized, and Steiger's
`fsd/typo-in-layer-name` treats anything else as an error.

```text
src/
├── app/          # everything that makes the app run: routing, entrypoint, providers, global styles
├── processes/    # DEPRECATED — move contents to features/ and app/
├── pages/        # full screens (or router blocks under nested routing)
├── widgets/      # large self-sufficient UI blocks, reused across pages
├── features/     # reused user-facing interactions
├── entities/     # business entities the project works with (user, post, order)
└── shared/       # reusable, business-agnostic foundation
```

Most projects need only **Shared, Pages and App**. Add a lower layer only when reuse actually
forces it — see `../decomposition.md`.

## Import rule on layers

> A module (file) in a slice can only import other slices when they are located on layers
> **strictly below**.

```ts
// features/aaa/api/request.ts
import { x } from "@/entities/user"; // ✅ lower layer
import { y } from "@/shared/api"; // ✅ lower layer
import { z } from "../lib/cache"; // ✅ same slice, relative
import { w } from "@/features/bbb"; // ❌ same layer → cross-import
import { v } from "@/pages/home"; // ❌ higher layer
```

**App and Shared are exceptions**: they are a layer _and_ a slice at once, so they have no
slices, only segments, and their segments may import each other freely.

## Layer semantics

| Layer         | Holds                                                                                                                                                                                                                                                                                                                                    | Typical segments                                                                                                                                                        |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shared**    | connections to the outside world (backend, libraries, env) and self-contained internal libraries. No business domains.                                                                                                                                                                                                                   | `api`, `ui` (UI kit — may be business-_themed_, never business-_logic_), `lib` (focused libraries, each with a README — not a helpers dump), `config`, `routes`, `i18n` |
| **Entities**  | real-world concepts the business names: User, Post, Group. Visual representation is for reusing _appearance_; attach differing logic via props/slots.                                                                                                                                                                                    | `model` (store, schemas), `api`, `ui`                                                                                                                                   |
| **Features**  | the main interactions users care to do. **Not everything needs to be a feature** — a good indicator is that it is reused on several pages. Too many features drown out the important ones.                                                                                                                                               | `ui` (the form), `api`, `model` (validation, internal state), `config` (feature flags)                                                                                  |
| **Widgets**   | large self-sufficient UI blocks. If a block is most of a page's content and is never reused, it is **not** a widget — put it in the page. Under nested routing (Remix/React Router), use Widgets the way flat routing uses Pages: full router blocks with their own fetching, loading and error boundaries. Page layouts also live here. | `ui`, `api`, `model`                                                                                                                                                    |
| **Pages**     | one page per slice; several near-identical pages (sign-in/sign-up) may share one slice. No limit on how much code a page holds as long as it stays navigable. Non-reused UI blocks belong here, not in Widgets.                                                                                                                          | `ui` (page + loading + error boundaries), `api`; a dedicated `model` is uncommon                                                                                        |
| **App**       | app-wide matters, technical (providers) and business (analytics). No slices.                                                                                                                                                                                                                                                             | `routes`, `store`, `styles`, `entrypoint`                                                                                                                               |
| **Processes** | **Deprecated.** Do not add it. Keep router- and server-level logic in App instead. Steiger flags it via `fsd/no-processes`.                                                                                                                                                                                                              | —                                                                                                                                                                       |

## Entity relationships

Entities are slices, so by default they cannot know about each other. Keep the _business logic of
their interaction_ in a higher layer (Features or Pages). When one entity's data object genuinely
contains another, make it explicit with the `@x` cross-import notation rather than working around
it — see `public-api.md`.

Docs: <https://feature-sliced.design/docs/reference/layers>
