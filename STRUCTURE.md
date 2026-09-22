# Structure

- `src/main.ts` — DOM shell, HUD wiring, start menu, keyboard/touch controls, engine lifecycle.
- `src/game/scene.ts` — framework-agnostic gameplay ownership inside one Babylon scene: player, drones, crystals, projectiles, arena, camera, lights, input state, update loop, and cleanup.
- `src/style.css` — responsive neon HUD and start screen. The generated nebula texture is used as the start backdrop.
- `art/nebula.webp` — compressed generated visual asset used at runtime by Babylon and CSS.
- `art/reference.webp` — compressed generated reference image used as art-direction proof.
- `.github/workflows/deploy.yml` — GitHub Pages build/deploy workflow.

## Runtime Contract

`createGameScene(engine, canvas, ui)` returns `{ scene, start, keys, dispose }`. Babylon owns all render nodes and scene observers; the DOM owns the HUD. The `?demo` query starts the game automatically and applies deterministic steering/fire so a reviewer can see active gameplay without input.
