# Memory

- Replaced the former Python Telegram self-bot repository contents after explicit user confirmation.
- Chosen stack: Vite + TypeScript + Babylon.js, with no backend and no runtime API dependency.
- The game is intentionally self-contained for static hosting. Browser audio was omitted because it requires a user gesture and is not needed for the core loop.
- Generated art is compressed into WebP runtime assets under `art/` and mirrored into `src/assets/` where Babylon imports it safely for GitHub Pages subpaths.
- `?demo` is the deterministic visual verification path.
- `npm run check` and `npm run build` pass; the browser console was clean during the demo smoke test.
