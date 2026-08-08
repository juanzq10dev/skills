---
title: API requests and the API client
triggers:
  - "setting up the HTTP client or base URL in an FSD project"
  - "deciding whether a request function goes in shared/api or a slice"
  - "organizing generated OpenAPI clients"
  - "wiring a server-state library into the FSD structure"
---

# API requests

Start in `shared/api` — for many projects that is all you need. `client.ts` centralizes the base
URL, default headers and serialization; `endpoints/` holds one file per endpoint group.

```text
shared/api/
├── client.ts
├── index.ts
└── endpoints/
    └── login.ts
```

```ts
// shared/api/client.ts (axios)
import axios from "axios";

export const client = axios.create({
  baseURL: "https://your-api-domain.com/api/",
  timeout: 5000,
  headers: { "X-Custom-Header": "my-custom-value" },
});
```

```ts
// shared/api/client.ts (fetch)
export const client = {
  async post(endpoint: string, body: any, options?: RequestInit) {
    const response = await fetch(`https://your-api-domain.com/api${endpoint}`, {
      method: "POST",
      body: JSON.stringify(body),
      ...options,
      headers: { "Content-Type": "application/json", ...options?.headers },
    });
    return response.json();
  },
};
```

```ts
// shared/api/endpoints/login.ts
import { client } from "../client";

export interface LoginCredentials {
  email: string;
  password: string;
}

export function login(credentials: LoginCredentials) {
  return client.post("/login", credentials);
}
```

```ts
// shared/api/index.ts — the segment's public API
export { client } from "./client";
export { login } from "./endpoints/login";
export type { LoginCredentials } from "./endpoints/login";
```

## Slice-specific requests

A request used by exactly one slice belongs in that slice's `api` segment, built on the shared
client. It does **not** need to be re-exported from the slice's public API — nothing else will
call it.

```ts
// pages/login/api/login.ts
import { client } from "@/shared/api";

interface LoginCredentials {
  email: string;
  password: string;
}

export function login(credentials: LoginCredentials) {
  return client.post("/login", credentials);
}
```

## Anti-patterns

| Wrong                                                     | Right                                                                                                                 |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Moving requests and response types into `entities/` early | Keep them in `shared/api` or the slice's `api` segment, where the DTO can be transformed into what the frontend needs |
| Exporting every slice-local request through `index.ts`    | Export only what other slices call                                                                                    |
| Dumping generated OpenAPI output loose in `shared/`       | Give it a folder, e.g. `shared/api/openapi/`, with a README saying what it is and how to regenerate                   |

## Server-state libraries

Cache keys, shared query/mutation options, and API data types go in `shared`. Full TanStack Query
layout: `../tech/tanstack-query.md`.

Docs: <https://feature-sliced.design/docs/guides/examples/api-requests>
