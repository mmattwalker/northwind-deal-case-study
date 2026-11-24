# Project Northwind: working rules

This is an independent, synthetic case study. The rules below exist because the analysis is only
worth anything if a reader can check it.

## The Google Sheet is the single source of truth

The model lives in the Google Sheet. `index.html` and `MEMO.md` are renderings of it, never
parallel calculations. If a number appears in two places and they disagree, the Sheet wins and the
rendering is wrong.

When the Sheet changes, re-export the model table into `index.html` and re-check every figure
quoted in `MEMO.md` and `README.md`. Do not edit a number in the page or the memo on its own.

## Every derived number is a formula

In the Sheet, no cell holds a result worked out somewhere else and pasted in. Totals, ratios,
growth rates and NPVs are formulas over the cells they come from. A reader must be able to click
any number and either trace a formula or find a labelled input.

Inputs live only on the Assumptions tab, in the yellow cells. Blue text is an input, black is a
formula, green is a reference to another tab.

## Every assumption carries a basis

Each driver on the Assumptions tab has a `basis` of `posting-stated`, `industry-public` or
`illustrative`. If a number cannot be given one of those three, it does not go in the model.

## No claim about Hopper's economics without a citation

Hopper's margins, pricing, loss ratios and partner terms are not public. Nothing in this repo may
state or imply knowledge of them. The only Hopper facts permitted are those in the published job
posting for the Finance & Strategy Manager role, and each must be cited as such in
`assumptions.md`.

Northwind Air is fictional and must be labelled as fictional wherever the deal is described. Every
page and document carries the notice that the study is independent and not affiliated with or
endorsed by Hopper. No Hopper logo, wordmark or trade dress is used anywhere.

## Favourable assumptions get the harder look

Where a number helps the recommendation, say what would have to be true for it to hold, and leave
it out of the base case if the evidence is only correlational. The 1.6x repeat-booking figure is
the worked example: computed, disclosed, excluded, and the reason given.

## Writing

No em dashes. Canadian spelling, so modelling and modelled rather than modeling and modeled. No
rhetorical one-liners, no three-item lists assembled for rhythm, and no words that assert
importance without evidence. State the finding and give the number.
