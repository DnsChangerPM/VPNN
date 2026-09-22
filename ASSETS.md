# Assets

**Art direction:** Neon sci-fi arena shooter with an indigo/violet space field, cyan and magenta emissive accents, crisp readable silhouettes, strong contrast, and a polished game-engine screenshot feel.

## Generated visual assets

| Name | Description | Size | Image | Runtime use |
|---|---|---:|---|---|
| nebula | Indigo/violet nebula with cyan and magenta stars; generated as a clean scenic texture | 1600x900 display | `art/nebula.webp` | Start screen backdrop and Babylon plane at the rear of the arena |
| reference | In-game screenshot target: cyan hovercraft, magenta drones, purple crystals, asteroid obstacles, HUD | 1600x900 reference | `art/reference.webp` | Visual target and art-direction record |

## Prompts

- **reference:** “In-game screenshot of a polished 3D neon space arena shooter, third-person chase camera behind a sleek cyan hover spacecraft centered in the lower middle, glowing magenta drone enemies approaching from the right and upper distance, five luminous purple energy crystals floating across the arena, chunky dark asteroids as obstacles, a huge blue-purple nebula and starfield in the background, circular arena boundary, bright cyan and magenta emissive accents, clean sharp game-engine rendering, cinematic but readable, no text, no logos, no motion blur, show a compact HUD with score top-left, shield bar top-right, combo multiplier near the center, minimap bottom-right, 16:9 composition.”
- **nebula:** “Seamless-looking deep space nebula texture, rich indigo and violet clouds with small cyan and magenta stars, high contrast but not too busy, no planets, no text, suitable as a 2D background texture for a browser game UI and sky dome, polished neon sci-fi palette.”

The ship, drones, crystals, asteroids, projectiles, arena grid, lights, and HUD are intentionally procedural so the game remains lightweight and loads quickly on GitHub Pages.
