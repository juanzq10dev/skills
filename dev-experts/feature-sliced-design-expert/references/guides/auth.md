---
title: Authentication and token storage
triggers:
  - "building login, registration, OAuth or 2FA screens"
  - "deciding where the access token and current user live"
  - "the API client needs a token owned by an entity"
  - "implementing logout, token refresh or automatic logout on failure"
---

# Authentication

Three steps: get credentials, send them, store the token.

## 1. Getting credentials

A login/registration screen is simple enough that it needs no decomposition — one Pages slice,
both forms inside it. A login **dialog** usable from any page is a Widget instead.

```text
pages/login/ui/{LoginPage.tsx, RegisterPage.tsx, index.ts}
widgets/login-dialog/{ui/LoginDialog.tsx, index.ts}
```

Client-side validation schema goes in the page's `model`, consumed from `ui`:

```ts
// pages/login/model/registration-schema.ts
import { z } from "zod";

export const registrationData = z
  .object({
    email: z.string().email(),
    password: z.string().min(6),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
  });
```

## 2. Sending them

The request goes in `shared/api` or the login page's `api` segment (`api-requests.md`). For 2FA,
keep the one-time-password screen and its request in the **same** `login` slice.

## 3. Storing the token

**A cookie is the ideal storage** — no manual handling, and almost nothing for the architecture to
decide. With a server-side framework, put the cookie infrastructure in `shared/api`. Only when
cookies are not an option does the placement question below arise.

**In Shared (default).** Plays well with an API client in `shared/api`: the token is freely
available to every request function, and `login()`/`logout()` update it. Refresh becomes a client
middleware — on a token-expired status, refresh, store, retry. Drawback: token management has no
dedicated home. If that logic grows, split it out into `shared/auth` and keep requests in
`shared/api`.

**In Entities.** A `user` (or current-user / "viewer" / "me") entity with a reactive store in
`model` can hold both token and user object, and can then encode real business logic — expiry,
invalidation. The challenge is exposing the token to `shared/api` without breaking the import
rule. Three options:

1. Pass the token explicitly on every request — simplest, quickly cumbersome, incompatible with a
   middleware-based client.
2. Expose it through a context or global store (`localStorage`), with the key in `shared/api` and
   the reactive store exported from the entity; the provider is set up on App. Declarative "pull",
   but creates an implicit dependency on a higher layer — emit a clear error if it is missing.
3. Subscribe and inject the token into the client whenever the store changes. Same implicit
   dependency, imperative "push".

Before choosing Entities, read `../issues/excessive-entities.md` §4 — it argues for `shared/auth`
in most cases.

**In Pages/Widgets — do not.** App-wide state does not belong in the login page's `model`.

## Logout and failure handling

Keep the logout request next to the login one if requests live in `shared/api`; otherwise next to
the button that triggers it (e.g. the header widget's `api` segment), with the store update in
that widget's `model`. **Always clear the token store when a logout or refresh request fails.**
That cleanup is pure business logic — `model` if the token lives in an entity, `shared/auth` if
splitting it out of `shared/api` keeps that segment coherent.

Docs: <https://feature-sliced.design/docs/guides/examples/auth>
