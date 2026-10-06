# Project brief - the AI capex cycle

## Objective

Build a transparent, historical research case study on whether reported
hyperscaler AI infrastructure investment provides evidence for sustainable
NVIDIA operating performance and the valuation expectations reflected in market
prices.

## Analytical frame

```text
Hyperscaler capex and AI infrastructure spending
                    ↓
Demand environment for accelerated computing
                    ↓
NVIDIA data-centre revenue, margins and cash generation
                    ↓
Earnings expectations, valuation and market reaction
```

This is an analytical framework, not a claim of direct causality. The
hyperscalers buy from multiple suppliers, capital expenditure includes items
beyond AI hardware and NVIDIA revenue has customer and geographic exposures
that must be documented separately.

## Questions to answer

1. How did the disclosed capex or infrastructure-spending figures of Microsoft,
   Alphabet, Amazon and Meta evolve over the selected reporting periods?
2. How did NVIDIA's data-centre revenue, operating profitability and free cash
   flow evolve over the same broad period?
3. What does each issuer's disclosure actually measure, and which comparisons
   are valid only with caveats?
4. How did NVIDIA shares react to reported earnings and guidance on fixed,
   disclosed event dates?
5. Which assumptions must hold for the market's valuation expectations to be
   met, and which reported indicators would challenge them?

## Evidence hierarchy

| Priority | Evidence | Use |
|---|---|---|
| 1 | Annual reports, 10-K filings and quarterly shareholder letters | Financial figures, definitions and management disclosures |
| 2 | Official investor-relations earnings releases and presentations | Event dates, guidance and reported KPIs |
| 3 | Official exchange, issuer or index-provider market data | Dated market-capitalisation and price observations |
| 4 | Reproducible public price series | Historical event-return calculations, with source and date recorded |

Search results, news articles and AI-generated summaries may help identify a
document but are not final evidence for a reported figure.

## Definition guardrails

- Do not call every hyperscaler cash-flow line "AI capex" unless the issuer
  explicitly does so. Preserve the reported label and definition.
- Do not infer NVIDIA revenue directly from another company's capex figure.
- Fix a market-data observation date before calculating valuation multiples.
- Separate historical evidence from forward guidance, estimates and scenarios.
- Do not label the outcome an "AI bubble". Test the gap, if any, between
  reported cash-flow evidence and the expectations implied by valuation.

## Proposed deliverables

1. `02_source_register.csv` - issuer, source, page, metric, definition and
   verification status.
2. `03_fact_base.md` - source-backed operating and capex evidence.
3. `04_event_study_method.md` - dated earnings-event methodology and caveats.
4. `05_market_note.md` - a concise evidence, catalyst and risk summary.
5. `src/dashboard.py` - an interactive view of the completed fact base.

## Interview explanation

> I did not begin by calling the AI investment cycle a bubble. I separated the
> reported spending signals from the supplier's operating results and from the
> valuation the market assigned. That let me identify what had already been
> delivered in revenue and cash flow, what was still an expectation, and which
> disclosures would validate or challenge the thesis.
