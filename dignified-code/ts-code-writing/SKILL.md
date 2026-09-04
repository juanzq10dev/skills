---
name: ts-code-writing
description: Use when making a software implementation using typescript language.
---

# TypeScript Code Writing Skill

Always think in functional code, prefer pure function, and immutability.

## Best practices

- Avoid using `any`

## Functions

Prefer const syntax

```js
const fn = () => {};
```

## Async function handling

Create the helpers if they do not exists.

```js
const created = await handlePromise(
  () => {}, // promise
  () => {}, // on success
  (err) => {}, // on failure
);
```

```js
const [, err] = await safeAsync(() => fn());
if (err) {
  // handle error
}
```
