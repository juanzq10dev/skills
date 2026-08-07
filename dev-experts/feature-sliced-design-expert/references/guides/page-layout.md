---
title: Page layouts and shared chrome
triggers:
  - "several pages share a header, sidebar or footer"
  - "a layout needs to include a widget and the import rule blocks it"
  - "deciding between shared/ui, widgets and app/layouts for a layout"
---

# Page layouts

A layout is the structure several pages share, differing only in main content.

**A layout with no business logic goes in `shared/ui` or `app/layouts`**, with props filling the
dynamic parts:

```tsx
// shared/ui/layout/Layout.tsx
import { Link, Outlet } from "react-router-dom";
import { useThemeSwitcher } from "./useThemeSwitcher";

export function Layout({ siblingPages, headings }) {
  const [theme, toggleTheme] = useThemeSwitcher();
  return (
    <div>
      <header>
        <nav>{/* … */}</nav>
        <button onClick={toggleTheme}>{theme}</button>
      </header>
      <main>
        <SiblingPageSidebar siblingPages={siblingPages} />
        <Outlet />
        <HeadingsSidebar headings={headings} />
      </main>
      <footer>{/* … */}</footer>
    </div>
  );
}
```

## When the layout needs a widget

`shared` and `widgets` cannot import from higher layers, so a layout containing business logic
cannot simply live there. Before solving that, ask whether the problem is real:

1. **Write the layout inline on the App layer**, where routing is configured. Ideal for nesting
   routers — group the routes and apply the layout to just those.
2. **Copy-paste it.** The urge to abstract is overrated for layouts, which rarely change. If one
   page later diverges, change it without touching the others; leave a comment noting the
   relationship if you're worried someone forgets.

If neither fits:

3. **Render props or slots** — pass the widget in from outside.
4. **Move the layout to `app/layouts`**, where composing any widget is legal.

Under a nested routing system, the Widgets layer can also hold full router blocks with their own
fetching, loading and error boundaries (`../layers.md`).

Docs: <https://feature-sliced.design/docs/guides/examples/page-layout>
