# Warren-approved 2D cut-out animation direction — 2026-11-20

Source: Claude's handoff of decisions discussed with Warren on 2026-11-20. This document records owner decisions; it does not claim that implementation or asset QA is complete.

## Visual target
Warren's words: “something close to Clash Royale, where the characters feel individual and unique in their style and movement but are still cartoony and fun looking, with depth and whimsy.” Swimmers must look like they are swimming; encounters and shots should feel physical like Blitzball (swim in, brace, tackle, dive), preserving approved character art.

## Locked direction
- Production game remains **2D**. The 3D lab remains a **separate experiment only**.
- Adopt **cut-out/paper-doll animation**: approved characters drawn as separate body parts and assembled/animated in code. Target smooth strokes/kicks, secondary hair/fin/tail motion, squash/stretch, tackles and dives. Avoid the PR #8 failure mode of replacing art with procedural stick-like bodies.
- **Pilot one Human male first** and seek Warren's visual approval before creating the other 18 forms.
- Six races remain cosmetic; no race-based mechanics.
- Defensive encounter rework remains deferred.

## Approved implementation batch (Claude implementing)
- Approved art replaces drawn bodies in VS and shot screens.
- Retain cyan-ring / amber-dash marker *shapes* but color with each team's actual approved palette. Preserve team colors and crests.
- Restore version number on title screen.
- Fix VS badge overlap.
- Increase visible player size / move camera closer.
- Polish movement: lean into turns, idle bob, wind-ups, bubble trails, depth scaling.
- Preserve SPECIAL button, verdict banners, and EVADED wording.

## Human male cut-out asset brief (ChatGPT responsible)
Reference approved Human male portrait and swimmer strip: brown wavy hair, transparent breather mask, gray jersey and shorts suitable for team tinting, gray wristbands, bold dark-outline cartoon style.
- Produce one upright full-body right-facing source image, arms and legs separated, approximately 900px tall on flat background.
- Deliver trimmed transparent PNG parts: head.png, head_sleep.png (eyes closed, relaxed mouth), torso.png, pelvis.png, upper_arm.png, forearm.png (open hand), fist.png (closed hand), thigh.png, shin.png (foot pointing back).
- Round limb joint ends with overlap for rotation; no cross-part contamination.
- Deliver pivots.txt with local pixel coordinates: head neck; torso neck/shoulder/hip; pelvis hip/left-leg socket/right-leg socket; upper_arm shoulder/elbow; forearm and fist elbow/wrist; thigh hip/knee; shin knee/ankle.
- Deliver assembled.png preview. Target Google Drive: Sphere League / 05 - Rig Parts / human_m/.
- **Acceptance:** visual inspection for background remnants, halos, neighbor fragments, art fidelity and clean joint overlaps before marking approved.

## Workflow
Claude implements and tests animation in code. ChatGPT prepares art parts and pivots. Warren approves the single-character pilot before scaling to 18 additional characters. PR #8 is reverted and must not be revived as a procedural-art replacement.
