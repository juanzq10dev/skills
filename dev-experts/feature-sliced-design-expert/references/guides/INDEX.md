---
title: Placing common concerns
triggers:
  - "deciding where a specific kind of code goes: requests, tokens, types, assets, layouts"
  - "adding a new API call, form, image or shared type to an FSD project"
  - "asking whether something belongs in shared or in a slice"
type: index
---

# Placing common concerns

The layer question is answered in `../decomposition.md`. This section answers the narrower
"where does _this kind of thing_ go" question for the five concerns FSD projects hit first.

## The default that applies to all of them

**Start in the slice that uses it; move to `shared/` only when a second consumer actually
appears.** Locality is the default and reuse is the exception, not the reverse. Placing something
in `shared/` up front is the single most common over-abstraction, because `shared/` is visible to
every layer and therefore the most expensive place to change.

## Selection hierarchy

Use the **first** that applies:

1. Used by exactly one slice → put it in that slice's segment (`api`, `model`, `ui`).
2. Used by several slices and business-agnostic → `shared/<segment>`.
3. Used by several slices and business-specific → push down one layer (`entities/`, `features/`)
   — but read `../issues/excessive-entities.md` before creating an entity.
4. Needed by the whole app at startup → `app/`.

## Prohibitions

- **NEVER create `shared/types`, a `types` segment, or a `types.ts` file** — "type" describes what
  the code is, not what it is for. The same goes for `components`, `hooks`, `utils`, `helpers`,
  and a catch-all `assets` segment.
- **NEVER put an API call or a response type in `entities/` just because it names an entity.**
  Backend shapes differ from what the frontend needs; keep requests in `shared/api` or the slice's
  `api` segment so there is a place to transform them.
- **NEVER store app-wide state such as an access token in a page or widget.**

<!-- BEGIN GENERATED INDEX -->

- [API requests and the API client](./api-requests.md) — setting up the HTTP client or base URL in an FSD project; deciding whether a request function goes in shared/api or a slice; organizing generated OpenAPI clients; wiring a server-state library into the FSD structure
- [Static assets, images, fonts and global styles](./assets.md) — adding an image, icon, font or stylesheet to an FSD project; someone proposes an assets/ segment or folder; deciding between public/ and a slice folder
- [Authentication and token storage](./auth.md) — building login, registration, OAuth or 2FA screens; deciding where the access token and current user live; the API client needs a token owned by an entity; implementing logout, token refresh or automatic logout on failure
- [Page layouts and shared chrome](./page-layout.md) — several pages share a header, sidebar or footer; a layout needs to include a widget and the import rule blocks it; deciding between shared/ui, widgets and app/layouts for a layout
- [TypeScript types, DTOs, mappers and validation schemas](./types.md) — placing an interface, enum, utility type or Zod schema; typing backend responses and mapping DTOs to frontend shapes; a nested backend response forces two entities to know each other; typed Redux hooks need RootState from the App layer; adding a .d.ts file or generated OpenAPI types

<!-- END GENERATED INDEX -->
