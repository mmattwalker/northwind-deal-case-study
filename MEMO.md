# Project Northwind: HTS partner deal review

**To:** CFO
**From:** Finance & Strategy
**Re:** Northwind Air white-label fintech agreement, three-year term
**Date:** November 24, 2026

*Independent case study by Matt Walker. Northwind Air is fictional and every figure is synthetic.
Not affiliated with or endorsed by Hopper.*

---

## Recommendation

Counter. Do not sign as drafted, and do not walk. As drafted the agreement is worth
**-CA$4.7M** to us on a three-year NPV, and it destroys **CA$0.4M** of joint value, meaning
Northwind's CA$4.2M gain is funded entirely out of our pocket and then some. Three changes to the
term sheet, none of which touch the headline revenue share percentage, move it to **+CA$1.2M** for
us and **+CA$0.9M** for Northwind, with **CA$2.0M** of joint value created.

## What Northwind asked for

Northwind Air carries roughly 2.4 million direct digital bookings a year and wants to white-label
Cancel For Any Reason and Disruption Assistance into its own booking flow. It has asked for 40% of
gross written premium plus a CA$4.0M annual minimum guarantee. We would fund a CA$3.2M integration
and carry the underwriting risk, which means we hold the claims exposure while paying a fixed share
of the top line.

## The revenue share rate is not the term that matters

The instinct is to negotiate the 40% down. That would be wasted effort. Under the CA$4.0M
guarantee, our NPV is negative at **every** revenue share rate, including zero:

| Revenue share rate | Partner payment, Years 1 to 3 | NPV to us |
|---|---|---|
| 0% | 4.00 / 4.00 / 4.00 | -3.94M |
| 20% | 4.00 / 4.00 / 4.00 | -3.94M |
| 30% | 4.00 / 4.00 / 4.00 | -3.94M |
| 40% (their ask) | 4.00 / 4.33 / 5.03 | -4.66M |

The guarantee floor binds in every year up to a 30% rate, so cutting the percentage changes the
payment by nothing at all. Anyone negotiating the rate in isolation is negotiating a term that does
not move the outcome. Lifting salvage recovery to 55% while keeping the CA$4.0M guarantee still
leaves us at -1.31M. The guarantee has to come down whatever else happens.

## What the percentage is a percentage of

Holding salvage at 55% and the guarantees at the levels proposed below, so that the **only**
variable is the base the rate applies to:

| Revenue share base | Highest rate we can pay at NPV = 0 |
|---|---|
| Gross written premium | **31.9%** |
| Net revenue after claims | **50.1%** |

Northwind asked for 40%. On their base we cannot afford it. On the base we should counter with, we
can afford more than they asked for. Same percentage, opposite answer.

The reason is risk transfer rather than arithmetic. A share of gross written premium is a fixed
claim on our top line that does not move when claims experience deteriorates, so Northwind is paid
the same whether the book runs at a 33% loss ratio or a 60% one. A share of net revenue after
claims puts them alongside us. There is a second, smaller effect in the same direction: premium is
earned between booking and departure, so on a growing book written premium always runs ahead of
earned premium, and a written-premium base pays Northwind on money we have not yet earned against
claims we have not yet seen.

## Salvage recovery is their cheapest concession and our most valuable ask

Claim severity is `ticket price x refund share x (1 - salvage recovery)`. Salvage recovery is the
residual value Northwind returns to us on a seat we have refunded and they can resell. Moving it
from 35% to 55% cuts severity from CA$188 to CA$130 and takes the Year 3 earned loss ratio from
47.9% to 33.2%. It costs Northwind a credit on inventory they re-sell anyway.

## No single change rescues the deal, and the guarantee is why

Changing exactly one term from the agreement as drafted, leaving everything else as Northwind
proposed it:

| Change | NPV to us | Improvement |
|---|---|---|
| Nothing (as drafted) | -4.66M | |
| Revenue share base to net revenue after claims | -3.94M | +0.73M |
| Salvage recovery 35% to 55% | -2.04M | +2.62M |
| Guarantee cut to 1.5 / 1.75 / 2.0 | -4.08M | +0.59M |
| Revenue share rate 40% to 30% | -3.94M | +0.73M |

Note what the first row of that table says. Changing the revenue share base, which is the single
most important term in the agreement, is worth only CA$0.73M on its own. That is the same as
simply cutting the rate to 30%. The reason is the guarantee: while the CA$4.0M floor binds, the
revenue share formula barely determines what we pay, so improving the formula improves almost
nothing.

Cut the guarantee first and the same change behaves completely differently:

| Cumulative | NPV to us | Step |
|---|---|---|
| As drafted | -4.66M | |
| Guarantee cut to 1.5 / 1.75 / 2.0 | -4.08M | +0.59M |
| Revenue share base to net revenue after claims | -0.49M | **+3.59M** |
| Salvage recovery to 55% | **+1.16M** | +1.65M |
| Loss-ratio corridor with guarantee suspension | +1.16M | +0.00M |

The base change is worth CA$0.73M before the guarantee is cut and CA$3.59M after it. These terms
are not separable and should not be traded one at a time. The guarantee is cheap for Northwind to
concede and it is the thing standing between us and the term that actually matters, so it goes
first in any negotiation sequence.

The corridor adds nothing in the base case, which is correct. It is insurance: it costs us nothing
when the book performs and pays only in the downside, as the next section shows.

## Terms I would push for

In this order. The guarantee comes first because it is cheap for Northwind to concede and it is
what unlocks the value of the second term.

1. **Minimum guarantee cut to CA$1.5M, CA$1.75M and CA$2.0M.** On base-case volumes the guarantee
   never binds, so it costs us nothing in the expected case while still giving Northwind a floor to
   take to their own board. It only bites in the downside, which is the point of a guarantee.
2. **Revenue share base moves to net revenue after claims, defined as earned premium less incurred
   claims.** Northwind keeps the 40% they anchored on. This is the term that decides the deal, and
   conceding the headline number buys it.
3. **Salvage recovery set at a contractual minimum of 55%**, with Northwind providing the residual
   value credit on refunded inventory.
4. **A loss-ratio corridor: if the earned loss ratio passes 45%, the revenue share rate steps down
   to 30% and the minimum guarantee is suspended for that year.** Both halves are required, for
   the reason below.

## The corridor only works if the guarantee is suspended with it

This is the one drafting point I would not let through review. In the downside case the corridor on
its own is worth exactly nothing:

| Bear case protection | NPV to us |
|---|---|
| No protection | -2.32M |
| Corridor alone, guarantee stands | **-2.32M** |
| Corridor and guarantee suspension together | **-1.10M** |

When the corridor trips, loss experience is bad, which means volumes and revenue share are low,
which means the guarantee floor is already binding. Stepping the rate from 40% to 30% then reduces
a number that is not being paid anyway. The guarantee absorbs the entire protection. Drafted
together the pair is worth CA$1.22M in the bear case. Drafted apart, clause 4 is decoration.

## Downside

On the counter terms, scenarios run **+3.26M** (bull), **+1.16M** (base) and **-1.10M** (bear).
The bear case assumes attach ramps to 17% rather than 23%, the exercise rate runs at 7.5% rather
than 6.0%, and salvage underperforms at 45%. Those drivers are correlated in practice, which is
why I have moved them together rather than one at a time.

How much room the base case has before NPV reaches zero:

| Driver | Assumed | Breakeven |
|---|---|---|
| Policy exercise rate | 6.0% | 8.5% |
| Year 3 attach rate | 23.0% | 18.1% |
| Salvage recovery | 55.0% | 34.5% |

The exercise rate is the thinnest margin and the hardest to estimate from outside, so it is where I
would want real data before signing.

## What I would validate with real data

1. **Exercise rate by route and fare class.** 2.5 points of headroom is not much, and the exercise
   rate is the driver the model is least able to defend from public information.
2. **Realised salvage recovery on refunded inventory.** Clause 3 is the single largest value lever
   and its 55% assumption is illustrative. If Northwind's own resale data says 40%, the deal is
   close to breakeven and the other terms have to work harder.
3. **Attach rate on a white-label flow rather than an owned app.** I have assumed a Year 3 rate of
   23%, below the roughly 30% the consumer app achieves, on the reasoning that a partner-controlled
   flow converts worse. That gap is an assumption, not a measurement.
4. **Claim payment timing.** The model recognises claims as incurred in the year written. Premium is
   collected at booking and claims pay out months later, so the real cash profile is better than
   this shows. I have left that float out rather than claim a benefit I cannot yet size.

## One number I have deliberately not counted

The 1.6x repeat-booking rate among customers who attach a fintech product is real and public, and
counting it would add materially to the upside. It is excluded from the base case because it is a
correlation, not a demonstrated causal effect: customers who buy cancellation cover may simply be
the kind of customers who travel more. Treating it as a benefit of the deal would be assuming the
answer. If a cohort analysis on our own data separated the two, it belongs in the model, and it
would be the first thing I would add.
