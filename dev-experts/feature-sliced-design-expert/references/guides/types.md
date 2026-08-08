---
title: TypeScript types, DTOs, mappers and validation schemas
triggers:
  - "placing an interface, enum, utility type or Zod schema"
  - "typing backend responses and mapping DTOs to frontend shapes"
  - "a nested backend response forces two entities to know each other"
  - "typed Redux hooks need RootState from the App layer"
  - "adding a .d.ts file or generated OpenAPI types"
---

# Types

**No `shared/types` folder and no `types` segment.** "Type" describes essence, not purpose. Place
each type by what it is _for_.

## Utility types

`shared/lib/utility-types/` (with a README stating what belongs) or a library like `type-fest`.
Don't overestimate reusability — a utility type used by one file belongs next to that file:

```text
pages/home/api/
├── ArrayValues.ts            ← the utility type
└── getMemoryUsageMetrics.ts  ← its only consumer
```

## Business entity types and cross-references

Real-world types are intertwined, which is exactly what the import rule forbids across slices.
Keeping requests and their types in `shared/api` sidesteps the problem entirely:

```ts
// shared/api/songs.ts
import type { Artist } from "./artists";

interface Song {
  id: number;
  title: string;
  artists: Array<Artist>;
}
```

If they must live in entity slices, two options:

1. **Parametrize** — make the connection a type slot. Works well for `Cart = { items: Product[] }`,
   poorly for tightly bound pairs like `Country`/`City`.

   ```ts
   // entities/song/model/song.ts
   interface Song<ArtistType extends { id: string }> {
     id: number;
     title: string;
     artists: Array<ArtistType>;
   }
   ```

2. **Cross-import via `@x`** (`../public-api.md`), one file per consuming entity.

## DTOs and mappers

Keep the DTO next to the request function that returns it, and the mapper next to the DTO.

```ts
// entities/song/api/dto.ts
import type { ArtistDTO } from "entities/artist/@x/song";

export interface SongDTO {
  id: number;
  title: string;
  disc_no: number;
  artist_ids: Array<ArtistDTO["id"]>;
}
```

```ts
// entities/song/api/mapper.ts
import type { SongDTO } from "./dto";

export interface Song {
  id: string;
  title: string;
  fullTitle: string;
  artistIds: Array<string>;
}

export function adaptSongDTO(dto: SongDTO): Song {
  return {
    id: String(dto.id),
    title: dto.title,
    fullTitle: `${dto.disc_no} / ${dto.title}`,
    artistIds: dto.artist_ids.map(String),
  };
}
```

**Nested DTOs** — when one response contains several entities, entities cannot avoid knowing each
other. Prefer an explicit `@x` cross-import over indirect tricks such as a middleware dispatching
into other slices: normalize in the owning entity, export the thunk through `@x`, and let the
other entity handle the same fulfilled action.

## Enums

As close to the usage as possible, in the segment matching what they represent — toast positions
in `ui`, backend response statuses in `api`. Truly project-wide enums go in `shared`, still chosen
by segment.

## Validation schemas (Zod)

Colocate with the code that uses them. Backend-response validation belongs with the request, in
`api`. Form-input validation belongs in `ui` next to the form, or `model` if `ui` is crowded.

## Global types and Redux

Generic app-agnostic types go in the appropriate `shared` segment. The one genuine exception is a
Redux `RootState`/`AppDispatch`, which is only knowable on the App layer yet needed by
`shared/store`. The sanctioned workaround is an implicit dependency via global declaration:

```ts
// app/store/index.ts
declare type RootState = ReturnType<typeof rootReducer>;
declare type AppDispatch = typeof store.dispatch;
```

```ts
// shared/store/index.ts
import {
  useDispatch,
  useSelector,
  type TypedUseSelectorHook,
} from "react-redux";

export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

## Props, ambient files and generated types

- Props/context interfaces stay in the component's file; for SFCs (Vue, Svelte) a sibling file in
  `ui`.
- `*.d.ts` required by tooling (Vite, ts-reset): fine in `src/`, tidier in `app/ambient/`.
  Typings you write for untyped packages: `shared/lib/untyped-packages/<name>.d.ts`.
- Generated types (OpenAPI): a dedicated folder such as `shared/api/openapi` with a README on how
  to regenerate.

Docs: <https://feature-sliced.design/docs/guides/examples/types>
