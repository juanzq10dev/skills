---
title: Electron
triggers:
  - "applying FSD to an Electron app with main, preload and renderer processes"
  - "typing and organizing IPC channels between processes"
---

# Usage with Electron

Electron's process model needs one adaptation: **each process gets its own FSD root**, plus a
common `shared` for the contract between them.

```text
src/
├── app/                    ← common app layer: entry points only
│   ├── main/index.ts
│   ├── preload/index.ts
│   └── renderer/index.html
├── main/                   ← FSD root for the main process
│   ├── features/user/ipc/{get-user.ts, send-user.ts}
│   ├── entities/
│   └── shared/
├── renderer/               ← FSD root for the renderer process
│   ├── pages/settings/{ipc/, ui/user.tsx, index.ts}
│   ├── widgets/  features/  entities/  shared/
└── shared/                 ← the only code public to both processes
    └── ipc/                ← channel names and contracts
```

Rules:

- **Each process has its own public API — you may not import from `main` into `renderer`.** Only
  `src/shared` is public to both, which is why the interaction contracts live there.
- Use a custom **`ipc` segment** for cross-process interaction.
- `pages` and `widgets` have no meaning in `src/main`; use `features`, `entities`, `shared` there.
- Segments of the top-level `app` layer should not intersect.

```ts
// src/shared/ipc/channels.ts
export const CHANNELS = {
  GET_USER_DATA: "GET_USER_DATA",
  SAVE_USER: "SAVE_USER",
} as const;

export type TChannelKeys = keyof typeof CHANNELS;
```

```ts
// src/shared/ipc/events.ts
import { CHANNELS } from "./channels";

export interface IEvents {
  [CHANNELS.GET_USER_DATA]: {
    args: void;
    response?: { name: string; email: string };
  };
  [CHANNELS.SAVE_USER]: { args: { name: string }; response: void };
}
```

```ts
// src/app/preload/index.ts
import { contextBridge, ipcRenderer } from "electron";
import { CHANNELS, type TElectronAPI } from "shared/ipc";

const API: TElectronAPI = {
  [CHANNELS.GET_USER_DATA]: () => ipcRenderer.sendSync(CHANNELS.GET_USER_DATA),
  [CHANNELS.SAVE_USER]: (args) => ipcRenderer.invoke(CHANNELS.SAVE_USER, args),
} as const;

contextBridge.exposeInMainWorld("electron", API);
```

```ts
// src/main/features/user/ipc/send-user.ts
import { ipcMain } from "electron";
import { CHANNELS } from "shared/ipc";

export const sendUser = () => {
  ipcMain.on(CHANNELS.GET_USER_DATA, (ev) => {
    ev.returnValue = { name: "John Doe", email: "john.doe@example.com" };
  });
};
```

Docs: <https://feature-sliced.design/docs/guides/tech/with-electron> ·
Example: <https://github.com/feature-sliced/examples/tree/master/examples/electron>
