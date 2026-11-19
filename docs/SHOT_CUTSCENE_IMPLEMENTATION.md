# Sphere League — Cinematic Shot Sequence (Owner-approved visual direction)
Date: 2026-11-19
Status: Approved creative direction for Claude implementation; not a claim that code or production art has been integrated.

## Goal
Make shot resolution a short, exciting, legible underwater sports highlight on the existing 180×320 canvas. Preserve established chunky cartoon, thick dark outlines, deep navy, cyan/team-color accents, Lilita One-style typography. Keep the actual shot mechanics authoritative: do not rewrite outcome calculations.

## Existing code integration points (main/index.html as reviewed)
- drawSeq(c,t) renders the sequence; seqNodes(c), seqStopAt(c,n), seqBall(c,n,t) determine path and outcomes.
- Cut verdict currently distinguishes GOAL, keeper SAVED/REFLEX SAVE, defender BLOCKED, and pass INTERCEPTED.
- Existing shot power labels, defender deductions, dodges, keeper CAT, audio cutEvents, and quick-scenes setting should remain functional.
- Current player renderer is tiny (~14–20 logical units); use portraits and camera crops for cinematic closeups, not full-size match sprites.

## Four visual variations
1. GOAL: shooter wind-up; ball streak with team-color energy; each encountered defender gets a quick dodge or power-loss beat; final keeper showdown; ball breaches goal mouth; energetic ripple/bubble burst, short freeze-frame, GOAL stamp and score update. Avoid implying goal before outcome confirmed.
2. SAVED / REFLEX SAVE: keeper lunges or dives and catches/deflects the ball; strong splash/radial impact, short freeze-frame, SAVED verdict; support existing asleep-keeper/reflex-save outcome labels as determined by game.
3. BLOCKED / INTERCEPTED: defender lunges into lane and stops ball, sharp contact burst and ricochet/possession cue; stop shot sequence immediately at that defender; distinguish shot BLOCKED from pass INTERCEPTED according to current mechanics. Do not show keeper confrontation afterward.
4. BEATEN: near-miss, slight slow motion and streak passing defender, BEATEN pop; ball continues to next defender or keeper. This is an intermediate event, NOT a new terminal shot result.

## Approximate animation beats (adjust for number of defenders)
- 0–350 ms: shooter wind-up and launch, camera/ball focus.
- 350–950 ms: defender beats, ~150–250 ms each; show actual power deductions as '-N' and current shot power; dodge does not deduct.
- 950–1350 ms: keeper showdown only if ball reaches keeper; brief speed ramp / slow-motion.
- 1350–1900 ms: outcome reveal, colored title, impact, short hold, return to match.
- Allow extension for multiple defenders, and honor existing quick-scenes playback preference.
- Audio: launch, encounter contact/dodge, keeper impact, distinct goal/save/block payoff. Respect mute/accessibility and reduce excessive screen shake/flashes.

## Visual assets and layout
The four-panel cutscene concept was reviewed and approved by Warren in ChatGPT. It is a concept reference, not a sliced production sprite pack. Use the approved portraits in Drive and existing game asset pipeline. Maintain 180×320 mobile legibility; do not put dense labels over action. Keep game-drawn text dynamic (player names, score, shot power, outcomes).
Art reference folder: https://drive.google.com/drive/folders/1ou1-zF41beeAnyw5Se0S7ow7cSYB0Rsg

## Acceptance criteria
- Four distinct visual reactions including BEATEN as nonterminal beat.
- Shot power deductions and winner are faithful to actual mechanics.
- Correct branch and possession on goal, save, block/intercept; no false goal or extra keeper beat after defender stop.
- Looks readable at 180×320, 12 athletes on arena; no loss of current quick-scene behavior.
- Claude should implement or propose a small testable PR, then ask Warren to evaluate in game.
