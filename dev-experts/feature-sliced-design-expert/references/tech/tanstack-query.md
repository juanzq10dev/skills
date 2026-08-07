---
title: TanStack Query (React Query)
triggers:
  - "placing query keys, query factories and mutations in an FSD project"
  - "setting up QueryClientProvider or a Suspense boundary on the app layer"
  - "implementing pagination, infinite scroll or useMutationState under FSD"
---

# Usage with TanStack Query

## Where keys go

Three valid layouts, in increasing specificity:

```text
shared/api/queries/{example.ts, another-example.ts}   ← simplest
shared/api/example/{index.ts, example.query.ts, get-example.ts, create-example.ts, …}
entities/example/api/{example.query.ts, get-example.ts, …}   ← only if entities already exist
```

Split by controller once the endpoint count grows, giving each a public API. Use `entities/` only
when the project is already divided into entities and each request maps to exactly one; for
connections between them, use `@x` (`../public-api.md`).

**Do not mix mutations with queries.** Put a mutation either in the `api` segment near its point
of use, or expose a `mutationFn` from `shared`/`entities` and call `useMutation` at the usage site.

## Query factory

```tsx
// src/shared/api/post/post.queries.ts
import { queryOptions } from "@tanstack/react-query";
import { getPosts } from "./get-posts";
import { getDetailPost, type DetailPostQuery } from "./get-detail-post";

export const POST_QUERIES = {
  all: () => ["posts"],
  lists: () => [...POST_QUERIES.all(), "list"],
  list: (page: number, limit: number) =>
    queryOptions({
      queryKey: [...POST_QUERIES.lists(), page, limit],
      queryFn: () => getPosts(page, limit),
      placeholderData: (prev) => prev, // prevents flicker when paginating
    }),
  details: () => [...POST_QUERIES.all(), "detail"],
  detail: (query?: DetailPostQuery) =>
    queryOptions({
      queryKey: [...POST_QUERIES.details(), query?.id],
      queryFn: () => getDetailPost({ id: query?.id }),
    }),
};
```

```tsx
// src/pages/post/ui/post.tsx
import { useQuery } from "@tanstack/react-query";
import { postApi } from "@/shared/api/post";

const {
  data: post,
  error,
  isLoading,
  isError,
} = useQuery(postApi.POST_QUERIES.detail({ id: parseInt(postId ?? "", 10) }));
```

Infinite scroll uses the same factory with `infiniteQueryOptions`:

```tsx
infinite: (limit: number) => infiniteQueryOptions({
  queryKey: [...POST_QUERIES.lists(), 'infinite', limit],
  queryFn: ({ pageParam }) => getPosts(pageParam, limit),
  initialPageParam: 0,
  getNextPageParam: (lastPage) =>
    lastPage.skip + lastPage.limit < lastPage.total
      ? lastPage.skip / lastPage.limit + 1
      : undefined,
}),
```

`queryOptions` is compatible with `useSuspenseQuery` — the factory needs no change.

## Mutation keys and `useMutationState`

Store mutation keys beside the query factory so a component elsewhere can read the state without
prop-drilling:

```ts
// src/shared/api/post/post.queries.ts
export const POST_MUTATIONS = {
  updateTitle: () => ["post", "update-title"],
  create: () => ["post", "create"],
};
```

```tsx
// src/widgets/save-indicator/ui/save-indicator.tsx
const isPending =
  useMutationState({
    filters: { mutationKey: POST_MUTATIONS.updateTitle(), status: "pending" },
    select: (mutation) => mutation.state.status,
  }).length > 0;
```

## Providers

`QueryClientProvider`, devtools, global error toasts and the Suspense/ErrorBoundary wrapper all
belong on the **App layer**, in `src/app/providers/`.

```tsx
// src/app/providers/query-provider.tsx
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error) => toast.error(error.message),
  }),
  mutationCache: new MutationCache({
    onError: (error) => toast.error(error.message),
  }),
  defaultOptions: {
    queries: { staleTime: 5 * 60 * 1000, gcTime: 5 * 60 * 1000 },
  },
});
```

A shared `ApiClient` class in `shared/api` standardizes headers, logging and response handling
across all of the above (`../guides/api-requests.md`).

Docs: <https://feature-sliced.design/docs/guides/tech/with-react-query>
