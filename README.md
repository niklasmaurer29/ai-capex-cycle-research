# The AI Capex Cycle: NVIDIA, Hyperscalers & Market Expectations

A source-backed markets research case study on the relationship between
hyperscaler investment, NVIDIA's data-centre economics and the market's
valuation expectations.

## Research question

> Are the reported AI-infrastructure investments of Microsoft, Alphabet,
> Amazon and Meta translating into sustainable NVIDIA earnings and cash flow,
> or is market pricing moving ahead of the underlying economics?

## Why this matters

The project links three parts of a markets analysis that are often considered
separately:

1. **Capital expenditure:** reported data-centre and AI-infrastructure spending
   by the large cloud platforms.
2. **Operating evidence:** NVIDIA data-centre revenue, profitability and cash
   generation.
3. **Market expectations:** valuation, earnings-event reaction and the risks
   embedded in the investment case.

It is designed as an educational exercise for Equity Research, Global Markets,
Equity Capital Markets, Sales & Trading and ETF/index-related applications. It
is not investment advice and will not issue a buy, hold or sell recommendation.

## Coverage universe

| Role in the research question | Companies |
|---|---|
| AI-compute supplier | NVIDIA |
| Hyperscaler demand indicators | Microsoft, Alphabet, Amazon, Meta |
| Optional contextual indicators | Semiconductor and technology ETFs, disclosed market data and policy rates |

## Research design

The project will retain each issuer's reported definitions and fiscal-year-end
dates. Annual-report evidence is not treated as automatically comparable merely
because it appears in the same table. Market-price observations will be given a
separate, explicit date so that valuation work does not use hindsight.

The finished case study will include:

- a source register with official annual-report URLs and page references;
- a fact base for capex, revenue, profitability and free cash flow;
- an earnings-event and valuation screen with fixed observation dates;
- a short market note that separates evidence, catalysts, risks and open
  diligence questions; and
- an interactive Streamlit dashboard that reads the versioned inputs.

## Workflow

1. Collect only official company disclosures and record each figure's definition.
2. Build a reproducible fact base before drawing any conclusion.
3. Align market data to disclosed reporting periods and calculate transparent
   valuation metrics.
4. Test the investment-cycle narrative against earnings, cash flow and risks.
5. Present the findings in a market note and dashboard.

## Repository structure

```text
research/          Research brief, source register, methodology and market note
data/              Versioned, source-checked numerical inputs
src/               Reproducible calculations and dashboard code
output/            Locally generated files; not committed
source_documents/  Local annual reports; PDFs are intentionally not committed
```

Start with [`research/01_project_brief.md`](research/01_project_brief.md).
The first source-backed numbers and their comparability caveats are in
[`research/04_initial_fact_base.md`](research/04_initial_fact_base.md).
The reproducible earnings-event methodology and results are in
[`research/05_earnings_event_method.md`](research/05_earnings_event_method.md)
and [`research/06_earnings_event_screen.md`](research/06_earnings_event_screen.md).
The management-guidance bridge and expectations framework are in
[`research/07_expectations_framework.md`](research/07_expectations_framework.md).
