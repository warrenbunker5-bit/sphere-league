# Sphere League character rigs

Characters are 2D cut-out puppets: separate painted parts joined at pivots and animated in code
(`drawRig` / `rigPose` in index.html). Everything about a form lives in data, so art and motion can be
upgraded without touching game code.

## Files
- `art/rig/<slug>/` - cut part PNGs + `rig.json` (what the game loads). Add the slug to `RIG_SLUGS` and the files to `sw.js` CORE.
- `tools/sheets/<slug>.png` - the source parts sheet it was cut from (masters also in Drive / Sphere League / 05 - Rig Parts / <slug>/).
- `tools/<slug>.json` - the cut spec for that sheet.
- `tools/cut_form.py sheet.png art/rig/<slug> tools/<slug>.json` - re-cuts a form. A better sheet with the same layout drops in with one command.

## Parts sheet rules (for the artist)
- Transparent PNG, every piece separated by 20+ px. Same style, line weight and scale as human_m (whole figure about 1000 px tall). Higher resolution is better; the cutter scales.
- Required: head, head_sleep, torso, pelvis, upper_arm, forearm (hand included), thigh, shin. One of each limb; the far side is a mirrored, darkened copy.
- Kit (torso, pelvis) in neutral gray; it is tinted to team colours. Skin in the form's real colours.
- Extra anatomy as chains of 2-3 segments: tail1..3, tent1a/1b, wing, fin, lure... Overlap 15-20% past each joint with rounded caps so joints never gap.
- Fully opaque interiors. (Pilot sheets faded light colours to partial alpha; the cutter repairs it, but clean art is better.)

## rig.json
- `parts`: limbs have `a` (joint toward body) and `b` (next joint) pivots; torso has `neck`, `shoulder`, `hip`; pelvis `waist`, `leg`; heads `neck`. Coordinates are pixels in each part's own PNG.
- `height`: full figure height in px at native scale. `headScale`: head size (default 1.3). `tint`: parts whose gray is team-coloured.
- `move`: `tempo` (swim speed multiplier) and `stroke`: `crawl` (default), `tailwhip`, `jet` or `undulate`. New strokes are added in `rigPose`.
- `chains`: tails, tentacles, wings, fins, lures, antennae. `{parts, from: torso|pelvis|head, pt, ang, swimAng, amp[], lag, speed, phase, layer: back|front, far}`.
  Each segment adds `amp[j]*sin(2pi*phase - j*lag)` to the one before (a traveling wave, base to tip), and lags slightly when the body turns. `ang` is used treading, `swimAng` swimming (radians in the body frame: 0 forward, pi/2 toward the feet). `from: head` chains move with the head.
- `poseAdd`: per-form tweaks added to a pose's joint angles, e.g. `{"shoot":{"body":-0.2,"ua":0.3}}`, for signature moves.

## Adding or upgrading a form
1. Artist delivers a parts sheet following the rules above.
2. Copy `tools/<similar form>.json` to `tools/<slug>.json`, set each piece's index (contact sheet: `python3 tools/seg.py`-style numbering, row then x), joint end and chains.
3. Run cut_form.py, add the slug to `RIG_SLUGS` and the files to sw.js, preview with a rig sheet / GIF, tune `chains`, `move` and `poseAdd`.
