---
title: Routing leaked below the Pages layer
triggers:
  - "URLs or paths are hardcoded inside entities, features or widgets"
  - "changing a route requires edits scattered across layers"
  - "deciding where redirect logic belongs"
---

# Routing leaked below Pages

Upstream marks this article WIP; the rule below is the whole of it.

**Situation** — URLs to pages are hardcoded in layers beneath `pages`:

```jsx
// ❌ entities/post/card
<Card>
  <Card.Title href={`/post/${data.id}`} title={data.name} />
</Card>
```

**Problem** — URLs are not concentrated in the Pages layer, where routing responsibility belongs.
Ignore it and changing a URL means hunting through every layer except `pages`, and a simple
product card has silently taken on part of the page's responsibility.

**Solution** — decide how URLs and redirects are handled at the Pages layer and above, then pass
them down through composition, props, or factories:

```jsx
// ✅ pages/feed owns the URL
<PostCard post={post} href={`/post/${post.id}`} />
```

Route _constants_ and matching patterns may live in `shared/routes` (or `shared/router`) — a
constant is not routing logic. The router configuration itself belongs in `app/routes`
(`../layers.md`).

Docs: <https://feature-sliced.design/docs/guides/issues/routes>
