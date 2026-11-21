# Sphere League: AI development notes

Shared project memory for the owner, Claude (primary developer) and ChatGPT (design consultant and reviewer). Keep it short and current. Record decisions and the reasons for them, not conversations.

Last updated: 2026-11-19 (v0.15, branch `feat/races-and-encounters`)

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

- **Two v0.14s:** PR #2 (from v0.13) and the main v0.14 were built in parallel. `feat/races-and-encounters` merges both; PR #2 needs no separate merge once this lands.
- **Race portraits are procedural placeholders**, drawn in code from the reference PNGs in Drive (02 - Approved Artwork). Production sprites still need the approved source PNGs (see `docs/SPHERE_LEAGUE_ART_DIRECTION.md`). Race and form are assigned from a hash of the player's name, so they stay stable across saves.
- **Rivals in auto-play:** the Riptide AI still beats every rival in AI vs AI seasons. Rival players now level up at a pace tied to the Riptide's XP; human testing should decide whether rivals need more.

- **Fixed in v0.14 (PR #2):** defence choice only with a ready special tackle; status effects hitting the keeper on a goal; pass odds aimed at the run target instead of the real pass spot; odds re-simulated every frame in the move sheet.
- Displayed odds use 200 Monte Carlo samples (about ±7 points at 50%). Tested within 3 SE of real outcomes.
- **Auto-match caveat:** `tests/sim.html` runs AI vs AI, so it measures mechanics, not human play.

## Current priorities

1. **v0.15 shipped to `main` (2026-11-19).** Includes PR #2. Owner is play-testing.
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
- v0.14 (PR #2, encounters): closest defender leads; defence choice every time with a free basic tackle and STOP %; the winner of an interaction is not affected by status (keeper exception on saves); pass odds match the real pass; cached 200-sample odds; `tests/` pages.
- v0.14 (main, built the same night on owner request): club facilities (Scouting Dept, Training Center, Recovery Pool, Film Room, Fan Deck); multi-round scouting with stat ranges; rival clubs with real rosters that develop, sign and release players; unrenewed contracts leave; league news; technique cut-ins and shot/pass sequences; a sleeping carrier, interceptor or keeper can't hold the ball.
- v0.15: both v0.14 lines merged (conflicts settled by the #1 owner decisions); six cosmetic races drawn procedurally; race gallery.

## Decisions log

| Date | Decision | Reason |
|---|---|---|
| 2026-11-18 | Adopted a three-way collaboration: owner, Claude, ChatGPT (see `AI_REVIEW_GUIDELINES.md`) | Get independent views on design, balance and code, while the owner keeps final say |
| 2026-11-18 | First development focus is encounter mechanics | Owner priority |
| 2026-11-18 | **Closest engaged defender is the lead** in every encounter type (break, pass, shot, human and AI) | The defender who made contact; easy to read on screen |
| 2026-11-18 | **Default status rule: whoever wins an interaction is not affected by the loser's status move.** For example, a carrier who breaks through a Sting Tackle is not poisoned. | The move failed, so its effect shouldn't land. This is the standing default; exceptions may be added later |
| 2026-11-18 | **Keeper exception:** a keeper who saves a status shot (catches it) *is* affected. On a goal the shot never touched the keeper, so the keeper is not affected. | Keeps the "sleep the keeper, then score" strategy alive |
| 2026-11-18 | Encounter plan approved (P1, P3–P6); P2 auto-resolve deferred; extra-defender falloff left for later | Owner, after ChatGPT review on #1 |
| 2026-11-19 | Tested, requested updates ship straight to `main` so the phone app updates automatically; the AIs must not build unrequested features without owner input | Owner wants to play updates right away |
| 2026-11-18 | Basic tackle is free (no SP, no extra HP cost); Drain only steals HP on a won tackle | ChatGPT review, owner agreed |

## Open questions

- Undertow (the team with the most status moves) is about 15% less dangerous under the status rule (away goals 4.16 to 3.52 per auto-match; statuses landed down 24%). Retune it later?
- Third and later defender falloff: deferred. 3+ engaged defenders happens only about once per 50 to 100 auto-matches.


## Art assets (v0.16)
- Approved art lives in `art/` and loads through `loadArt()` / `ART` in `index.html`. Every sprite has a procedural fallback, so the game still draws if an image fails to load.
- `ball.png` / `ball_glow.png`; `sphere_interior.jpg` (drawn in world space, clipped to the sphere) and `sphere_backdrop.jpg` (screen backdrop, replaced the stadium).
- `portraits.jpg` is a 5-column atlas of 288px cells in `PORTRAIT_KEYS` order; `portraits_jersey.png` is the matching jersey mask. `portraitFor()` tints the gray jersey to the team color and caches the result. Source sheets: Drive / Sphere League / 03 - Concepts In Review / portraits_A–E.png.

## Art pass, v0.17–v0.19 (2026-11-19)
- **Shot cutscene** (`drawSeq`): BEATEN beat on shots (DODGED stays for passes), slow-motion keeper showdown (`SEQ_GK`), keeper lunge/dive, goal ripple burst, save starburst + deflection, block ricochet. Outcome math is untouched.
- **Encounter VS**: spinning team-color burst, VS emblem, stamped ENCOUNTER!, crest watermarks, portraits bob.
- **Team colors** switched to the approved crest palettes (TEAMS col/acc/shorts/gk).
- **UI kit**: `btn()` and `kitPanel()` draw the approved neon-edged style in code so any color works; buttons show a short pressed state.
- **Icons**: `iconOf()` / `drawIcon()`; shown on move menus, status chips and the technique cut-in.
- **Crests**: `drawCrest(teamKey,...)`; scoreboard, standings, title, VS.
- **Swimmers**: `art/swimmer_<slug>.png` (6 frames: tread, tread, swim, swim, brace, asleep) + `_jersey.png` mask, listed in `SWIM_SLUGS`. Forms not listed fall back to the drawn swimmer. Synthari use an empty mask (their metal body is gray, so tinting would turn the whole body team-colored).
- Source files: Drive / Sphere League / 03 - Concepts In Review.

## v0.21 (2026-11-20): actors + cut-out rig pilot
- `drawActor(p,x,y,size,{pose,ph,face,...})` is the single full-body renderer for the field, Encounter VS and shot/pass scenes. Order: cut-out rig if the form has one, else the approved 6-frame swimmer strip (`drawSpriteActor`, with squash/stretch, bob, lean, pose motion), else the old procedural body.
- Poses: tread, swim, brace, block, shoot, pass (use `wind` 0..1), hit, dive, save, sleep.
- **Cut-out rig** (`drawRig`, `rigPose`): parts + joint pivots in `art/rig/<slug>/rig.json`; angles in body frame (0 forward, PI/2 toward feet). Gray kit on torso/pelvis is tinted to the team color; far-side limbs are darkened copies. Joints ease toward target poses each frame (stored per player per context key).
- Pilot: `human` (Human male) only, cut from ChatGPT's parts sheet (Drive / 05 - Rig Parts / human_m / original_parts_sheet_01.png) by `work/cut_parts.py` style tooling. To add a form: get a parts sheet with separated pieces, cut + measure pivots, drop into `art/rig/<slug>/`, add slug to `RIG_SLUGS`.
- Team markers keep ChatGPT's ring (home) / dashed bar (away) shapes but use each team's own color. Players drawn larger (`ACTOR_FIELD`), camera closer in live play (`PLAYZ`), slight depth scale by field height.

## v0.24 balance rules (Warren-approved)
- XP: halftime XP still banks, but a pre-match save backup (`sphereLeague.v1.prematch`) is restored if the match is quit or the app is closed/reloaded mid-match. All XP from an unfinished match is lost; settings are kept.
- Exhibitions: none in the offseason; 2 XP-earning exhibitions per season week (`EX_XP_PER_WEEK`, tracked in `SAVE.exXp`). Extra exhibitions are practice only.
- Statuses roll per touch (`FX_CHANCE` by move rank; sleep on keepers is lower). Only sleep stuns. Tests force the roll with `window.__FX_ALWAYS`.
- Shots: any range under 260. `shotAccuracy` (wide roll) + `SHOT_FADE` (power loss with distance) + logistic keeper contest. Sleeping keepers get a 2-6% reflex save. Fitted to ChatGPT's target table (e.g. elite SHT40 at half court: ~15% vs awake keeper, ~58% vs sleeping).

## v0.25 AI shooting (ChatGPT proposal, Warren-approved)
- `aiShotBar`: minimum scoring odds the AI needs to shoot. Awake keeper 35% (20% if pressed); sleeping keeper 25% (10% with <5s); 12% with <6s on the shot clock; any real chance with <3s.
- `aiBestShot`: the AI compares the real odds of a basic shot vs. each special and pays a small value cost for a special, so it doesn't burn them on easy goals.
- Encounters: no distance gate; shots above the bar are weighted up.
- 720-match sim vs v0.24: Anglers losses 43%->17%, Undertow 50%->20%. Boulder Breakers is still ~80% draws (very low scoring both ways) - matchup issue, not thresholds.

## v0.26 open 1-on-1 scoring (Warren + ChatGPT)
- Warren: blockers keep a big impact (beat the blocker is the core); open shooter-vs-keeper should be better, and proximity matters (penalty-like ~75-80%).
- Refit to ChatGPT's open-shot table vs CAT18: SHT22 ~91% point blank / ~76% at 40 / ~35% at 75 / ~9% at 110 / ~0.5% half court; elite SHT40 99/96/80/51/13%.
- `SHOT_FADE` now starts at 40u; `SHOT_PROX` close-range bonus applies only to open shots (no defender touched). Keeper gv=cat*1.096, logistic scale 7.33. First engaged blocker 0.75->0.9, others 0.45->0.5, so contested shots stay where they were (SHT22 close ~12%).
- `gkPosBonus`: +5/12/20% for a keeper 10/20/35+u off the shot line, +25% if stranded. Stepping out on the line doesn't count. Fades to 0 at half court; not used vs sleeping keepers.
- AI open-shot bar 35%->25%.
- 720-match sim, total goals: Currents 2.7->3.5, Divers 2.8->3.6, Anglers 1.5->3.1, Undertow 1.0->2.3, Breakers 0.2->1.4.

## v0.27 loose ball in the crease (2026-11-21, Warren bug report)
- Bug: field players are pushed out of the crease (42 units), so a loose ball that settled there could only be taken by the keeper. If he was asleep, stunned or far off, nobody could reach it.
- Fix: the defending keeper always chases a loose ball in his own crease and gets the first 1s. After that, or at once if he is down, the crease opens to the loose-ball chasers. A field player who grabs it is still pushed out of the crease with the ball.
- Checked: keeper down, ball in crease: stuck 60/60 before, recovered 60/60 after (about 3.8s). Keeper awake: keeper still wins about 85%. cases.html 21/21; 40 auto matches, goals 199 vs 200.

## v0.28 film study + playoffs (2026-11-21, Warren-approved)
- Copying is intentional now. Before a match (FILM button on the season screen) you assign starters to study opponent starters. Slots: 2, 3 at Film Room 1, 4 at Film Room 3. Only a studier copies, only moves his slot can use, with no distance limit. Odds: 50% first sighting, +25% per miss, +10% per Film Room level. Random copying by nearby players is gone. Assignments are saved per opponent, so they carry into a playoff rematch.
- Seasons end with playoffs. After the 5-week regular season the top 4 play semis (1v4, 2v3) and the winners meet in the Championship. Semi win $150, title $400 plus a Move Manual; regular-season place prizes are unchanged. Other playoff games are simulated (simKO). A non-playoff season still simulates the bracket and names a champion.
- Playoff ties go to sudden-death OT (G.ot, G.half=3): next goal wins and both teams get +25% HP.
- Checked: 12 auto seasons played (2 titles, then missed playoffs once contracts expired without renewal, which is a test artifact); forced OT; copy within 1-3 sightings; an unassigned opponent is never copied; cases 21/21; 40 auto matches unchanged.
