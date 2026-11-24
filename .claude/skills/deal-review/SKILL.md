---
name: deal-review
description: Review a driver-based deal model against its own assumptions before it goes to a decision-maker. Use when a partnership, revenue share or underwritten-product model needs checking for arithmetic ties, unsupported assumptions, favourable-case bias, and terms that look protective but are neutralised by another term.
---

# Deal review

A model that is arithmetically correct can still be wrong in ways that matter. This skill checks
the four failure modes that actually reach decision-makers.

## 1. Does it tie?

- Every derived cell holds a formula, not a pasted result. Spot-check the summary figures and any
  number quoted in the accompanying memo.
- Where two engines compute the same thing (a scenario block and a main model, a spreadsheet and a
  script), find the tie check. If there is none, build one: the difference between the two, which
  must read zero.
- Re-derive one year's headline figure by hand from the assumptions alone. If it disagrees with
  the model, the model is wrong until proven otherwise.
- Check for error values and for ranges that stop short of the data.

## 2. Is every assumption labelled, and is the favourable one labelled honestly?

- Each input needs a basis: sourced, published, or invented. Anything that cannot be given one is
  not an assumption, it is a guess wearing one.
- List the assumptions the recommendation depends on most, by how far each can move before the
  answer flips. That list, not the base case, is what the decision-maker needs.
- Find every assumption that helps the recommendation and ask what would have to be true. Where
  the evidence is correlational rather than causal, say so and keep it out of the base case. State
  the test that would settle it.

## 3. Which term actually drives the outcome?

- Vary each commercial term alone, across its plausible range, and rank them by effect. Headline
  percentages often matter less than the base they apply to, the floors under them, or the
  definitions behind them.
- Check whether any term is non-binding in the expected case. A term that never binds is free to
  concede and should be traded for one that does.
- Model the counterparty's side too. A deal that fails their hurdle does not close, and the split
  of value created is the thing a negotiation is actually about.
- Separate growing the total value from moving each side's share of it. Say which a given term does.

## 4. Do the protective terms survive contact with each other?

This is the check most often skipped, and the one most likely to find something.

- For each clause meant to protect against a downside, run the downside **with and without that
  clause**. If the two are identical, the clause is worth nothing.
- When a clause is worth nothing, find the term that absorbed it. Floors, guarantees, caps and
  minimums commonly neutralise rate adjustments, because the condition that triggers the
  adjustment is the same condition that makes the floor bind.
- Protective terms have to be drafted as a set and tested as a set.

## Output

Lead with whether the recommendation survives the review. Then: ties that failed, assumptions that
cannot be supported, the ranked list of what the answer actually depends on, and any clause that
does not do what it appears to do. Quote the figures.
