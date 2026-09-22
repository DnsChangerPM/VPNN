# Game Plan: Neon Void Runner

## Risk Tasks

### 1. Third-person flight camera and procedural combat arena
- **Why isolated:** The game combines a chase-style camera, continuous movement, procedural enemy spawning, projectile motion, and proximity collisions.
- **Approach:** Keep the arena bounded to a deterministic rectangular playfield, use a single update loop with explicit arrays for drones, crystals, and projectiles, and follow the player with a damped UniversalCamera. The `?demo` flag drives deterministic movement and fire for visual proof.
- **Verify:** Camera remains behind the ship during lateral movement; projectiles travel toward the arena; enemy approach, hit points, shield damage, and crystal pickup all transition without clipping or runaway entities.

## Main Build

Neon sci-fi arena shooter rendered with Babylon.js. The player pilots a cyan/pink hovercraft, shoots incoming magenta drones, collects purple energy crystals, survives enemy bolts, and advances waves while the HUD exposes score, shield, wave, and combo.

- **Assets:** `art/nebula.webp` is the generated 1600x900 backdrop texture; `art/reference.webp` is the generated visual target. All gameplay geometry is procedural Babylon meshwork with emissive materials.
- **Verify:**
  - WASD/arrow movement and Space/click shooting respond immediately.
  - Drones move toward the player, fire, take two hits, and disappear on destruction.
  - Crystal pickups increment score and combo; shield visibly decreases on hits.
  - HUD remains readable and responsive on desktop and mobile; touch controls appear on narrow screens.
  - No missing textures, placeholder UI, or browser console errors during `?demo` capture.
  - `pnpm check` and `pnpm build` pass.
  - GitHub Actions deploys the Vite `dist` folder to GitHub Pages.
