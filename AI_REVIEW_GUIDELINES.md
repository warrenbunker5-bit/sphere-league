# Sphere League: AI review guidelines

How the owner, Claude and ChatGPT work together on Sphere League.

## Roles

**Owner: final decision-maker.** Sets priorities and decides gameplay direction, feature scope, design trade-offs, significant balance changes, architecture changes, and whether changes are accepted. A recommendation from either AI is not owner approval.

**Claude: primary developer.** Writes and changes the code, builds approved features, debugs, tests, manages branches and pull requests, keeps the documentation up to date, spots improvements, and recognises when a second opinion would help. Claude handles routine work without asking for reviews.

**ChatGPT: independent design consultant and technical reviewer.** Not a replacement developer. ChatGPT is brought in selectively for:
- Faithfulness to Blitzball gameplay: encounters, passing, shooting, tackling, interceptions, movement, keepers and special moves.
- Balance: stat formulas, success odds, HP and SP, AI difficulty, fairness.
- Technical review: architecture, complex state changes, regressions, mobile performance, keeping game calculations separate from animation.
- Pull request review: unintended consequences, whether the code matches the spec, and improvements that don't widen the scope.

## When to request a ChatGPT review

Request a review for changes to:
- **Gameplay mechanics:** how encounters trigger or resolve; pass, shot or tackle formulas; how multiple defenders combine; keeper logic; special move effects; possession and loose balls.
- **AI behaviour:** positioning, team tactics, defender pursuit and engagement, decision-making, difficulty.
- **Balance and progression:** stat formulas, HP and SP, growth, move strength and cost, recruiting, contracts, the season.
- **Architecture and performance:** large refactors, how game state is structured, new rendering or physics, mobile input or layout, or anything touching several unrelated systems.

No review is needed for routine bug fixes, cosmetic changes or straightforward implementation. Claude uses judgement.

## How a review request travels

ChatGPT can't see the Claude conversation, and `@ChatGPT` on GitHub notifies nobody. GitHub is the shared channel:

1. Claude opens a GitHub issue or pull request containing a **CHATGPT REVIEW REQUEST** section (template below).
2. Claude gives the owner the link.
3. The owner takes it to ChatGPT and brings ChatGPT's reply back to Claude.

Keep each request to one subsystem. Never ask for a review of the whole app.

## Review request template

```
CHATGPT REVIEW REQUEST
Project: Sphere League
Review category: Gameplay / Balance / AI / Architecture / Code Review / Other
GitHub issue or PR: [link]

What we are trying to accomplish:
[the intended improvement]

Current implementation:
[how it works now, with file paths, function names and line numbers]

Proposed implementation:
[what will change]

Already considered:
[alternatives and why they were set aside]

Questions for ChatGPT:
1. Does this preserve original Blitzball gameplay?
2. Are there overlooked gameplay or technical consequences?
3. Is there a better way to accomplish this?
4. What should be tested?

Decision needed:
[exactly what must be settled before work continues]
```

## Handling feedback

When the owner brings back ChatGPT's feedback, Claude:
1. Reads it carefully.
2. Checks it against the actual code.
3. Decides which recommendations are technically sound.
4. Explains any disagreement with specific reasons.
5. Adds the agreed points to the implementation plan.
6. Asks the owner to settle any remaining design disagreements.

Neither AI follows the other blindly or dismisses it just because it differs. The aim is a better game.

## GitHub safeguards

- Make meaningful changes on feature branches, never as experiments on `main`.
- Keep each pull request to one feature or a related group of changes, and explain each file changed and why.
- Test before asking for review, and always keep a working version of the game.
- Don't remove existing features without the owner's approval.
- Record every major balance change in `AI_DEVELOPMENT_NOTES.md`.
- Don't touch unrelated systems.
- Don't merge significant changes until the owner has reviewed and approved them.

**The owner makes all final decisions.**
