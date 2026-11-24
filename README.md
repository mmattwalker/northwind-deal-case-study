# Project Northwind

A worked deal review: should Hopper sign a white-label fintech agreement with a mid-size regional
airline, and on what terms?

**Northwind Air is fictional and every figure in here is synthetic.** This is an independent case
study by Matt Walker. It is not affiliated with or endorsed by Hopper, and it uses no non-public
information about Hopper. The only Hopper facts it draws on come from the company's own job
posting, and each one is cited in [assumptions.md](assumptions.md).

## The finding

Northwind asks for 40% of gross written premium plus a CA$4.0M annual minimum guarantee, against a
CA$3.2M integration Hopper funds and underwriting risk Hopper carries. As drafted that is worth
**-CA$4.7M** to Hopper and destroys CA$0.4M of joint value.

The revenue share percentage is not the term that matters. Under the guarantee as asked, Hopper's
NPV is negative at **every** rate including zero, because the guarantee floor binds in every year.
What the 40% is a percentage *of* is what decides the deal:

| Revenue share base | Highest rate Hopper can pay at NPV = 0 |
|---|---|
| Gross written premium | **31.9%** |
| Net revenue after claims | **50.1%** |

So the counter gives Northwind the 40% they anchored on and changes the base, the guarantee and the
salvage recovery term instead. That moves the deal to **+CA$1.2M** for Hopper, **+CA$0.9M** for
Northwind, and CA$2.0M of joint value created.

## If you have five minutes

1. **[MEMO.md](MEMO.md)** is the deliverable: the recommendation, the terms to push for, the
   downside, and what I would validate with real data before signing. Start here.
2. **[The model](https://docs.google.com/spreadsheets/d/1kRr_O-Tb6uz2LB2knqPXFNsXD436IpoC9kKuhzizzWY/edit)** is a live Google Sheet. Four tabs, every number a formula, the
   yellow cells are the only inputs. Change one and the whole thing recalculates.
3. **[assumptions.md](assumptions.md)** is every driver with the basis it rests on.

A single page with the recommendation, the full model and an interactive calculator is at
**[https://mmattwalker.github.io/northwind-deal-case-study](https://mmattwalker.github.io/northwind-deal-case-study/)**.

## What the model does and does not do

It runs three years at annual grain. Bookings flow to eligible offers, attach, policies and gross
written premium; premium earns between booking and departure; claims come from an exercise rate and
a severity built from ticket price, refund share and salvage recovery; the revenue share and
guarantee produce the partner payment; and what is left is contribution margin, EBITDA, free cash
flow and NPV for both sides. There is a bear, base and bull case, a sensitivity grid over the
revenue share rate and its base, and three breakevens.

It does not model claim development or IBNR, carry a balance sheet, or take credit for the
premium float. The float is real and would improve the cash profile, and the memo says so rather
than counting it.

The Scenarios tab carries a tie check in row 20: the base scenario NPV less the Model tab's counter
NPV, which must read zero. If the two engines ever disagree, that cell says so.

## How this was built

The model is a Google Sheet because that is where this work belongs and because it opens from a
link with nothing to install. I built it with Claude Code: the Sheet's formulas were generated from
a specification rather than typed cell by cell, and the figures were calibrated against an
independent Python implementation of the same arithmetic until the two agreed to the dollar. That
independent check is what caught a breakeven I had first computed under two inconsistent salvage
assumptions.

[CLAUDE.md](CLAUDE.md) holds the rules this repo is built under, and
[.claude/skills/deal-review](.claude/skills/deal-review/SKILL.md) is a skill that reviews a deal
model against its own assumptions. Both are how I actually work, not an illustration of it.

## Files

| File | What it is |
|---|---|
| [MEMO.md](MEMO.md) | The CFO memo. The deliverable. |
| [assumptions.md](assumptions.md) | Every driver, with its basis. |
| [index.html](index.html) | The single page: recommendation, model and calculator. |
| [build_page.py](build_page.py) | Renders the page from the same arithmetic as the Sheet, and ties to it on every build. |
| [CLAUDE.md](CLAUDE.md) | The rules this repo is built under. |
| [.claude/skills/deal-review/](.claude/skills/deal-review/SKILL.md) | A skill that reviews a deal model against its assumptions. |


## Why there is no spreadsheet file in this repo

The Google Sheet is the model. A committed `.xlsx` copy would be a second version of the same
numbers that nobody re-exports, which is the drift this repo's [CLAUDE.md](CLAUDE.md) exists to
prevent. Anyone who wants the file can take File then Download from the Sheet itself, and get a
copy that is current by construction.
