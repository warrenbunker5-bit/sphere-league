# Sphere League: AI development notes

Shared project memory for the owner, Claude (primary developer) and ChatGPT (design consultant and reviewer). Keep it short and current. Record decisions and the reasons for them, not conversations.

Last updated: 2026-11-18 (v0.13)

## Design philosophy (set by the owner)

- **Faithful:** Sphere League stays faithful to the feel of FFX Blitzball: a sphere pool, stat-driven encounters, special moves, status effects and copying moves from opponents. It is an original game, with its own names, art and teams, not a copy of FFX assets.
- **Improve:** grow the existing game step by step. No rewrites, no replacing working systems without a reason, and no dropping working features to try out new architecture.
- **Pause-and-resolve encounters are central.** When a defender reaches the ball carrier, play stops and the encounter is resolved from stats and choices. This stays.
- **Talk before big changes.** Changes to design, scope, balance or architecture are discussed with the owner before they are built.

## Technical overview

- The whole game is in `index.html`: one HTML5 Canvas, about 1,400 lines of minified-style JavaScript, with no build step and no dependencies.
- It is a PWA (`manifest.webmanifest`, `sw.js`, `icons/`) hosted on GitHub Pages at https://warrenbunker5-bit.github.io/sphere-league/
- It is designed for phones in portrait. The logical canvas is 180×320, scaled to fit the screen.
- Saves go to `localStorage` under the key `sphereLeague.v1`.
- Main global state is `G`. `G.state` drives the screen and game phase (`title`, `play`, `encounter`, `defEnc`, `aiEnc`, `flight`, `goal`, `team`, `scout`, `season` and others).

### Encounter system (how it works now)

| Function | Role |
|---|---|
| `encounterCheck()` | Triggers when an opponent who is awake comes within 9 units of the carrier and the carrier isn't immune. The engaged defenders are every opponent within 16 units. |
| `simBreak(c, defs, mv, tk)` | Carrier END plus move power, against the summed ATK of the defenders. The top defender counts in full and the others at 45%. Mirage keeps only the top defender. |
| `simPass(c, to, engaged, mv)` | PAS plus power, minus distance. It is reduced in turn by BLK from engaged defenders (60%, then 40%), then defenders in the passing lane (60%), then the receiver's marker (40%). The ball is intercepted when the remaining value reaches 0. |
| `simShot(c, engaged, mv)` | SHT plus power, minus distance past 40 units. It is reduced by engaged defenders, then lane blockers (skipped by Curveball), then compared with the keeper's CAT (plus Iron Wall). A sleeping keeper only gets a small reflex chance. |
| `doBreak` / `doPass` / `doShot` | Spend SP, apply HP costs, run the sim, then animate. A failed break gives a tackle or a loose ball; the chance of a loose ball falls as the defender's CAT rises, and is guaranteed if the carrier is exhausted. |
| `landFlight()` | Resolves a pass or shot when the ball arrives, and applies status effects to everyone in `touched`. |
| `startAiEnc()` / `aiChoose()` | The AI carrier picks the best option from simulated odds. |
| `aiTackleFor()` | The AI defender picks a tackle move (70% chance when one is available). |
| `odds(fn, n)` | Monte Carlo odds shown on buttons (40 to 100 runs). |

Stats: SPD, END, ATK, PAS, BLK, SHT, CAT. HP is scaled to END, and `hpF` lowers output when HP is low. Status effects are Poison, Sleep, Weak and Slow.

## Mechanics to preserve

- Pause-and-resolve encounters with odds shown on each option.
- Special moves with SP cost, cooldowns and rank-ups from use (3 and 8 uses).
- Copying moves from opponents (the "Studying %" chance grows after each failed attempt).
- Loose-ball scrambles: speed decides who gets there first, and CAT plus some luck decides who holds on. **The owner likes this. Keep it as it is.**
- Sleep makes the carrier drop the ball, and a sleeping player wakes when hit by a pass or when a goal is scored.
- Season, scouting, bench, growth curves and contract renewals (v0.12). Formations and substitution scouting (v0.13).

## Known issues and observations

- **Fixed in v0.14 (PR #2):** defence choice only with a ready special tackle; status effects hitting the keeper on a goal; pass odds aimed at the run target instead of the real pass spot; odds re-simulated every frame in the move sheet.
- Displayed odds use 200 Monte Carlo samples (about ±7 points at 50%). Tested within 3 SE of real outcomes.
- **Auto-match caveat:** `tests/sim.html` runs AI vs AI, so it measures mechanics, not human play.

## Current priorities

1. **Encounter mechanics: built in v0.14 (PR #2), waiting for owner testing and merge.**
2. Owner backlog below, in the order the owner chooses.
3. Improve the owner, Claude and ChatGPT workflow so the owner decides rather than relays messages (planned 2026-11-19).

## Owner backlog (ideas raised 2026-11-18, not yet approved for building)

- **Team and recruiting:** compare how a player's stats would change if they switched position (the `posPen` penalties).
- **Stats guide:** a tutorial or info screen on which stats help with which actions.
- **Time-out button:** one per half, for substitutions, possibly with options to restore a player's stamina or HP.
- **"Get open" attacking formation:** forwards move much more to shake off defenders, at a stamina cost.
- **Shot status effects and the keeper:** done in v0.14 (see Decisions log).

Earlier roadmap items are in `ROADMAP.md`: wake-up runs, a single stamina bar, landscape mode, contract expiry, choosing who studies which opponent, a soft cap on dominant players, signature move chains, and balance testing.

## Completed milestones

- v0.10: sleep makes the carrier drop the ball, calmer stamina, pace setting.
- v0.11: pass, shoot and dribble menu; quit to title.
- v0.12: season, scouting, bench, growth curves.
- v0.13: engaged defenders block, honest halftime, scouting when making subs, formations.
- v0.14: closest defender leads; defence choice every time with a free basic tackle and STOP %; the winner of an interaction is not affected by status (keeper exception on saves); pass odds match the real pass; cached 200-sample odds; `tests/` pages.

## Decisions log

| Date | Decision | Reason |
|---|---|---|
| 2026-11-18 | Adopted a three-way collaboration: owner, Claude, ChatGPT (see `AI_REVIEW_GUIDELINES.md`) | Get independent views on design, balance and code, while the owner keeps final say |
| 2026-11-18 | First development focus is encounter mechanics | Owner priority |
| 2026-11-18 | **Closest engaged defender is the lead** in every encounter type (break, pass, shot, human and AI) | The defender who made contact; easy to read on screen |
| 2026-11-18 | **Default status rule: whoever wins an interaction is not affected by the loser's status move.** For example, a carrier who breaks through a Sting Tackle is not poisoned. | The move failed, so its effect shouldn't land. This is the standing default; exceptions may be added later |

| 2026-11-18 | **Keeper exception:** a keeper who saves a status shot (catches it) *is* affected. On a goal the shot never touched the keeper, so the keeper is not affected. | Keeps the "sleep the keeper, then score" strategy alive |
| 2026-11-18 | Encounter plan approved (P1, P3–P6); P2 auto-resolve deferred; extra-defender falloff left for later | Owner, after ChatGPT review on #1 |
| 2026-11-18 | Basic tackle is free (no SP, no extra HP cost); Drain only steals HP on a won tackle | ChatGPT review, owner agreed |

## Open questions

- Undertow (the team with the most status moves) is about 15% less dangerous under the status rule (away goals 4.16 to 3.52 per auto-match; statuses landed down 24%). Retune it later?
- Third and later defender falloff: deferred. 3+ engaged defenders happens only about once per 50 to 100 auto-matches.

