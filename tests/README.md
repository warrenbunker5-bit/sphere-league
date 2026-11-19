# Tests

Browser pages that test the game. They aren't linked from the game or cached by the service worker. Serve the repo over HTTP (a `file://` page can't reach into the game frame) and open:

- `tests/cases.html`: encounter rule checks with hand-placed players, such as closest defender leads, status effects only on a win, keeper status on a save but not on a goal, and displayed odds matching outcomes. Every line should read PASS.
- `tests/sim.html?target=../index.html&n=200&seed=1`: plays fast automatic matches (`G.auto`) with a seeded random generator and no drawing, and reports per-match averages with 95% confidence intervals. Run it against an older copy of `index.html` too (via `target=`) to compare before and after.

Both pages start from a fresh save and never write to it, so they won't touch a real save on the same address.
