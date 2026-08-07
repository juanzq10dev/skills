---
title: Excessive entities
triggers:
  - "the entities layer has grown large or ambiguous"
  - "deciding whether to create an entity for a piece of business logic"
  - "where to put CRUD calls or the authenticated user and token"
  - "entities cross-import each other and @x is spreading"
  - "asking whether a project can skip the entities layer"
---

# Excessive entities

`entities/` is visible to every layer except `shared`, so a change there can ripple through the
whole app. Over-populating it produces ambiguity about what belongs, coupling, and constant
import dilemmas. Six rules, in the order they pay off.

## 0. Consider having no `entities` layer

Omitting it does not break FSD — it simplifies the architecture and keeps the layer available for
later scaling. A **thin client** (data processing mostly on the backend, client logic limited to
exchanging data) usually needs none. A **thick client** with real client-side business logic is
the candidate. The distinction is not binary; parts of one app can differ.

## 1. Avoid preemptive slicing

v2.1 favors **deferred** decomposition. Put the code in the `model` segment of the page (or widget
or feature) first, and revisit once business requirements are stable. The later code moves into
Entities, the less dangerous the refactor.

## 2. Avoid unnecessary entities

Do not create an entity per piece of business logic. Use the types from `shared/api` and keep the
logic in the current slice's `model`. When the logic really is reused, put _only the logic_ in the
entity and leave the data definitions in `shared/api`.

```text
entities/order/
├── index.ts
└── model/apply-discount.ts   ← uses OrderDto from shared/api
shared/api/
├── index.ts
└── endpoints/order.ts        ← the DTO lives here
```

## 3. Exclude CRUD from entities

CRUD is boilerplate with little business logic; in `entities/` it buries the meaningful code.

```text
shared/api/
├── client.ts
├── index.ts
└── endpoints/
    ├── order.ts      ← all order CRUD
    ├── products.ts
    └── cart.ts
```

Complex operations (atomic updates, rollbacks, transactions) _may_ justify Entities — evaluate,
don't default.

## 4. Store authentication data in `shared`

Prefer `shared/auth` or `shared/api` over a `user` entity for tokens and auth DTOs. Auth responses
are context-specific (private vs. public profile) and rarely reusable, and putting them in
Entities pushes you toward `entities`→`shared` imports or `@x`.

```text
shared/
├── auth/
│   ├── use-auth.ts    ← authenticated user info / token
│   └── index.ts
└── api/…
```

Full placement discussion: `../guides/auth.md`.

## 5. Minimize cross-imports

Design entities around **isolated business contexts** so `@x` is not needed at all.

```text
❌ entities/{order, order-item, order-customer-info}   each with @x/
✅ entities/order-info/{index.ts, model/order-info.ts}
```

Docs: <https://feature-sliced.design/docs/guides/issues/excessive-entities>
