# Sphere League — Encounter VS Screen (approved visual direction)
Date: 2026-11-19
Status: Warren approved concept art direction, not yet production-ready UI or implementation.

## Appearance
Use the established chunky comic-cartoon underwater style, deep navy, bold dark outlines, cyan and contrasting team-color accents, expressive race-specific portraits, big VS centerpiece, and clear PASS / SHOOT / BREAK / SPECIAL action buttons at the bottom. The illustrative concept shows Human attacker vs Pelarian Octarine defender. Names, stats, and teams in the concept are placeholders, not canonical game data.

## Implementation constraints
- Actual canvas is 180×320; preserve readable tap targets and bottom action area (~75 logical units).
- Simplify compared with the high-resolution concept: show only the most relevant action stats instead of seven crowded stat rows. Values, portraits, player names, move availability and colors should be rendered dynamically from game state.
- Do not change mechanics, race stat balance, roster, or game actions as part of this visual work.
- Use approved portrait sheets in Google Drive: https://drive.google.com/drive/folders/1ou1-zF41beeAnyw5Se0S7ow7cSYB0Rsg
- Provide working 180×320 mockup and test readability/tapability on an actual phone before declaring done.

## Next steps
Claude: implement or propose the responsive layout using existing encounter state and existing game action handlers; retain keyboard/accessibility and current interactions. Request Warren's in-game review.
