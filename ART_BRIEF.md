# Sphere League: art brief for a visual pass

Use this to brainstorm the look with ChatGPT (or any design helper), then bring the results back to Claude to build.

## What the game is
- Underwater ball sport played inside a giant water sphere. Inspired by the feel of Blitzball, but **all original**: our own teams, names, logos and art. Don't copy screenshots, characters or UI from Final Fantasy X.
- Portrait phone game with a Retro Bowl-style stripped-down feel. Matches run in real time, and the game pauses for "encounters" when a defender reaches the ball carrier. At that point it becomes a turn-based RPG moment: pass, shoot or break, plus special moves.
- Target look: **Clash Royale-level polish**. Chunky, readable, colorful, a bit cartoony. Not pixel art, and not realistic.

## How it's built (constraints the artist should know)
- Everything is drawn in code on one canvas, 180 × 320 logical units (scaled up to the phone screen). Right now there are no image files.
- Images can be added: transparent PNG sprites, ideally at 4× (for example, a 64 × 64 portrait drawn at 256 × 256).
- Top ~245 units: the sphere and match view. Bottom ~75 units: the action panel with buttons.

## Current palette
- Background navy `#120e2b`, panels `#1f1a48`, outlines `#1b1433`
- Lakewood Riptide (player team) teal `#22b8a8`. Rivals: orange `#f07a2a`, gold `#e6be3a`, purple `#8b55d6`, crimson `#e04a6a`, green `#3f9a4a`
- Good / bad / warning: `#7dffb0` / `#ff8a8a` / `#ffd24a`

## Move elements (each needs its own visual identity)
| Element | Moves | Current color | Current motif |
|---|---|---|---|
| Poison | Viper Pass, Toxic Shot, Sting Tackle | `#7fe04a` | rising bubbles, drips |
| Sleep | Lullaby Pass, Dream Shot, Sleeper Hold | `#b58cff` | crescent moons, z's, twinkles |
| Hex (weaken) | Hex Pass | `#ff6fcf` | rotating rune circle |
| Fire / power | Rocket Pass | `#ffb13b` | flame streaks |
| Swirl | Curveball, Spin Cycle | `#5fd3ff` | spiral, whirlpool rings |
| Ice | Avalanche Shot | `#dff4ff` | falling shards, snow |
| Mirage | Mirage | `#ff6fcf` | shimmering bands, afterimages |
| Anchor (slow) | Anchor Tackle | `#5fd3ff` | falling chains |
| Drain | Drain Tackle | `#ff5a6e` | red orbs pulled inward |
| Shield | Iron Wall | `#ffd24a` | pulsing hex grid |

## Screens that exist now (where design help matters most)
1. **Technique cut-in:** a diagonal colored band slides in, the player's portrait is on the left, the move name stamps in letter by letter, and the element effect plays behind it.
2. **Shot/pass sequence:** the shooter is on the left, defenders are lined up along the path, and the keeper is on the right. The ball travels across while its power number ticks down at each defender ("-8"), or a "DODGED!" pops up, until GOAL or SAVED.
3. **Encounter VS screen:** attacker panel against defender panel.
4. **Menus:** title hub, Season (standings, news), Team, Scouting cards, Club facilities.

## What I want from the design session
1. A short **style guide**: palette refinements, outline weight, button style, and font pairing (it's currently Lilita One).
2. **Character portrait style** for the round avatars: head-and-shoulders, team-colored jersey, readable at 24 px.
3. **Cut-in layouts** for the technique and sequence screens: where things sit, how they animate, and what makes them feel big.
4. **One visual idea per element** (table above) that reads clearly in under a second.
5. Optional: a team crest for each of the six clubs (Lakewood Riptide, Mile High Currents, Boulder Breakers, Aurora Anglers, Durango Divers, Pikes Peak Undertow).

Bring back colors as hex codes, layouts as simple sketches or descriptions with rough positions, and any art as transparent PNGs.

## Prompt to paste into ChatGPT
> I'm making an original mobile sports game called Sphere League: an underwater ball sport played inside a giant water sphere, with turn-based RPG "encounters" and special moves, inspired by the feel of Blitzball from FFX but with all-original teams and art. The art target is Clash Royale-level polish: chunky, colorful, readable on a phone. Everything is drawn on a 180×320 canvas. I've attached the art brief with my palette, the 10 move elements, and the screens. Please give me: (1) a style guide (palette, outlines, buttons, fonts), (2) a portrait style for 24px round player avatars, (3) layouts and animation beats for a "technique cut-in" and a "shot sequence" screen where the ball's power ticks down past each defender, and (4) one strong visual motif per element. Keep it original: no copyrighted characters or logos. Give colors as hex codes and positions on the 180×320 grid.
