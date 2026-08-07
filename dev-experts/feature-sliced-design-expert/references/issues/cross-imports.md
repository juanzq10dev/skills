---
title: Cross-imports
triggers:
  - "one slice imports another slice on the same layer"
  - "features or widgets have become coupled to each other"
  - "Steiger reports fsd/forbidden-imports or fsd/no-cross-imports"
  - "two entities genuinely reference each other in the domain"
  - "choosing between merging slices, pushing logic down, or composing from a page"
---

# Cross-imports

An import **between different slices within the same layer** — `features/cart` → `features/product`,
`widgets/header` → `widgets/sidebar`. Prohibited by the import rule on layers (`../layers.md`).

`shared` and `app` have no slices, so imports _within_ them are **not** cross-imports.

Why it is a smell: ownership of the shared logic becomes unclear; slices can no longer be tested
in isolation; every edit needs more context held in mind; and one-way dependencies drift into
bidirectional ones, which locks the slices together permanently.

## Entities layer

Usually caused by splitting entities too finely. **Before reaching for `@x`, ask whether the two
boundaries should simply be merged.** `@x` (`../public-api.md`) is a necessary compromise, not a
recommended approach — an explicit gateway for unavoidable domain references, never a general
reuse mechanism. Overuse locks entity boundaries together.

## Features and widgets — four strategies

Use the **first** that fits.

**A. Merge the slices.** If they always change together, they are one slice in practice.

```text
features/profile          ┐
features/profileSettings  ┘ → features/profile
```

**B. Push the shared domain flow down into `entities/`.** Domain types and domain logic only; UI
stays in features/widgets. If `features/auth` and `features/profile` both need session validation,
put it in `entities/session` and import it from both.

**C. Compose from a higher layer (pages/app)** — inversion of control. The upper layer assembles
slices that do not know about each other.

```tsx
// pages/UserDashboardPage.tsx
import { UserProfilePanel } from "@/features/userProfile";
import { ActivityFeed } from "@/features/activityFeed";

export function UserDashboardPage() {
  return (
    <div>
      <UserProfilePanel />
      <ActivityFeed />
    </div>
  );
}
```

When one feature needs to _render_ something owned by another, invert with render props (React) or
slots (Vue):

```tsx
// features/commentList/ui/CommentList.tsx — knows nothing about userProfile
interface CommentListProps {
  comments: Comment[];
  renderUserAvatar?: (userId: string) => React.ReactNode;
}
```

```tsx
// pages/PostPage.tsx — the page injects it
<CommentList
  comments={comments}
  renderUserAvatar={(id) => <UserAvatar userId={id} />}
/>
```

```vue
<!-- Vue equivalent: features/commentList/ui/CommentList.vue -->
<li v-for="comment in comments" :key="comment.id">
  <slot name="avatar" :userId="comment.userId" />
</li>
```

**D. Allow it, but only through the Public API.** Accepts the cross-import while bounding the
damage: export a hook or component from the slice's `index.ts` and import only that. Never reach
into another slice's `model`, `store`, or internal files.

```ts
// features/auth/index.ts
export { useAuth } from "./model/useAuth";
export { AuthButton } from "./ui/AuthButton";
```

## When an existing cross-import must be refactored

Treat it as a problem — not a style preference — when you see:

- a direct dependency on another slice's store/model/business logic
- deep imports into another slice's internal files
- **bidirectional** dependencies (A→B and B→A)
- changes in one slice repeatedly breaking another
- flows that belong in `pages`/`app` being forced into same-layer imports

Docs: <https://feature-sliced.design/docs/guides/issues/cross-imports>
