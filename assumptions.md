# Assumptions

*Independent case study by Matt Walker. Northwind Air is fictional and every figure below is
synthetic. Not affiliated with or endorsed by Hopper.*

Every driver in the model, with the basis it rests on. This is the same table as the Assumptions
tab of the Google Sheet, which is the live version.

**Basis** is one of:

- `posting-stated`: taken from Hopper's own job posting for this role
- `industry-public`: a published industry or statutory figure
- `illustrative`: invented for this exercise, with no claim to accuracy

Nothing here is drawn from Hopper's internal data. Hopper's actual margins, pricing and loss ratios
are not public, are not used, and are not implied anywhere in the model.

## Operating drivers

| Driver | Value | Unit | Basis |
|---|---|---|---|
| Direct digital bookings, Year 1 | 2,400,000 | bookings | illustrative |
| Booking growth, annual | 4.0% | % a year | illustrative |
| Average ticket price, Year 1 | $340.00 | CAD | illustrative |
| Ticket price inflation, annual | 2.0% | % a year | illustrative |
| Offer eligibility rate | 85.0% | % of bookings | illustrative |
| Fintech attach rate, Year 1 | 16.0% | % of offers | illustrative |
| Fintech attach rate, Year 2 | 21.0% | % of offers | illustrative |
| Fintech attach rate, Year 3 | 23.0% | % of offers | illustrative |
| Premium price, share of ticket | 7.0% | % of ticket | illustrative |
| Unearned premium at year end, share of GWP | 8.0% | % of GWP | illustrative |

The Year 3 attach rate of 23% sits deliberately below the roughly 30% that Hopper's own posting
reports for its consumer app, on the reasoning that a partner-controlled booking flow converts
less well than an owned one. That gap is a judgment, not a measurement.

## Underwriting

| Driver | Value | Unit | Basis |
|---|---|---|---|
| Policy exercise rate | 6.0% | % of policies | illustrative |
| Refund share of ticket | 85.0% | % of ticket | illustrative |

## Hopper costs

| Driver | Value | Unit | Basis |
|---|---|---|---|
| Payment processing, share of GWP | 2.6% | % of GWP | illustrative |
| Claims servicing cost per claim | $12.00 | CAD | illustrative |
| Customer support cost per policy | $0.35 | CAD | illustrative |
| Premium tax, share of GWP | 2.0% | % of GWP | industry-public |
| Programme operating cost, annual | $900,000 | CAD | illustrative |
| Integration capital cost | $3,200,000 | CAD | illustrative |
| Amortisation period | 3 | years | illustrative |

## Finance

| Driver | Value | Unit | Basis |
|---|---|---|---|
| Discount rate, Hopper | 12.0% | % | illustrative |
| Tax rate | 26.5% | % | industry-public (Canadian combined federal and provincial) |

## Northwind side

| Driver | Value | Unit | Basis |
|---|---|---|---|
| Integration cost, Northwind | $1,200,000 | CAD | illustrative |
| Programme operating cost, annual | $600,000 | CAD | illustrative |
| Displaced ancillary sales, share of policies | 12.0% | % of policies | illustrative |
| Margin per displaced sale | $18.00 | CAD | illustrative |
| Discount rate, Northwind | 9.0% | % | illustrative |

Northwind's side is modelled because a deal only closes if it clears both parties' hurdles. The
displaced ancillary line reflects that an airline selling refundable fares loses some of that
margin when a cancellation product sits next to it.

## Deal terms

| Term | As proposed | Counter |
|---|---|---|
| Revenue share rate | 40.0% | 40.0% |
| Revenue share base | gross written premium | net revenue after claims |
| Salvage recovery rate | 35.0% | 55.0% |
| Minimum guarantee, Year 1 | $4,000,000 | $1,500,000 |
| Minimum guarantee, Year 2 | $4,000,000 | $1,750,000 |
| Minimum guarantee, Year 3 | $4,000,000 | $2,000,000 |
| Loss-ratio corridor applies | no | yes |
| Corridor trigger, earned loss ratio | n/a | 45.0% |
| Stepped revenue share rate | n/a | 30.0% |
| Guarantee suspended when corridor trips | n/a | yes |

## Hopper facts used, and where they came from

All three are from the job posting for this role:

- Roughly 30% of consumer app customers attach a fintech product. Used only as the upper reference
  point for the white-label attach assumption above.
- Customers who attach are 1.6x more likely to book again. Computed as an upside bridge and
  **excluded from the base case**, because it is a correlation rather than a demonstrated causal
  effect.
- HTS is more than 90% of the business, and partners include Capital One, Air Canada, Uber, RBC and
  Nubank. Used as context for why a mid-size carrier deal of this shape is plausible.

## How the two scenario drivers move

Bear and bull move their drivers together rather than one at a time, because attach, exercise and
salvage are correlated in practice. A book that attaches poorly is usually also adversely selected.

| | Attach, Years 1 to 3 | Exercise rate | Salvage recovery |
|---|---|---|---|
| Bear | 12% / 15% / 17% | 7.5% | 45.0% |
| Base | 16% / 21% / 23% | 6.0% | 55.0% |
| Bull | 19% / 25% / 28% | 5.2% | 60.0% |
