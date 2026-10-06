# Initial fact base - reported capex and NVIDIA operating evidence

## Scope and method

This first fact base compares the latest fully reported fiscal periods available
in the selected source documents. Microsoft has a 30 June fiscal year-end; the
other hyperscalers use 31 December; NVIDIA's fiscal 2026 ended on 25 January
2026. These dates are intentionally retained rather than presented as one
identical reporting period.

For the hyperscalers, the common diagnostic is:

```text
Operating cash flow less raw purchases of property and equipment
```

It is **not** described as AI-only capex or issuer-reported free cash flow.
The disclosures have different lease and sale-proceeds treatments.

## Hyperscaler cash-investment screen

| Company | Fiscal period end | Operating cash flow | Raw P&E purchases | Year-on-year P&E growth | Cash flow less raw P&E |
|---|---|---:|---:|---:|---:|
| Microsoft | 30 Jun 2025 | USD 136,162m | USD 64,551m | 45.1% | USD 71,611m |
| Alphabet | 31 Dec 2025 | USD 164,713m | USD 91,447m | 74.1% | USD 73,266m |
| Amazon | 31 Dec 2025 | USD 139,514m | USD 131,819m | 58.8% | USD 7,695m |
| Meta | 31 Dec 2025 | USD 115,800m | USD 69,691m | 87.1% | USD 46,109m |

Combined raw P&E purchases were USD 357,508m, compared with USD 217,267m in
the corresponding prior reported periods. This is a **64.5%** increase, but it
does not prove that the full increase was AI-specific or that it flowed directly
to NVIDIA.

## NVIDIA operating evidence

| Metric | FY2026 ended 25 Jan 2026 | Prior year | Observation |
|---|---:|---:|---|
| Total revenue | USD 215,938m | USD 130,497m | Up 65.5% year on year |
| Data Center revenue | USD 193,737m | USD 115,186m | Up 68.2% year on year; 89.7% of total revenue |
| Operating income | USD 130,387m | USD 81,453m | Reported consolidated operating income |
| Operating cash flow | USD 102,718m | USD 64,089m | Reported cash-flow line |
| Cash flow less P&E and intangibles | USD 96,676m | USD 60,853m | Project calculation, not issuer-reported free cash flow |

## What the data says - and does not say

1. The selected hyperscalers reported sharply higher cash investment in property
   and equipment across their latest fiscal periods.
2. NVIDIA simultaneously reported 68.2% growth in Data Center revenue, led by
   its accelerated-computing and AI platforms.
3. These observations are consistent with a strong infrastructure-investment
   cycle, but they do not establish direct causality. Each company has multiple
   customers, suppliers, asset categories and reporting dates.
4. Amazon's raw P&E purchases absorbed 94.5% of operating cash flow in this
   screen, compared with 47.4% at Microsoft, 55.5% at Alphabet and 60.2% at
   Meta. This is a funding-capacity diagnostic, not a credit score.

## Definitions that matter

- **Microsoft:** additions to property and equipment include facilities, data
  centres and computer systems; the company does not label the total as AI-only
  capex.
- **Alphabet:** 2025 capital expenditures were primarily technical
  infrastructure and office facilities; purchases of P&E in the cash-flow
  statement were USD 91,447m.
- **Amazon:** its reported free-cash-flow measure uses P&E purchases net of
  sale proceeds and incentives. The common screen above uses the unnetted
  cash-flow line instead.
- **Meta:** reported 2025 capital expenditures of USD 72,220m, including P&E
  purchases and finance-lease principal payments. The common screen uses the
  P&E-purchases line of USD 69,691m.
- **NVIDIA:** Data Center is an end-market revenue category, while Compute &
  Networking is a reportable segment. They are not interchangeable.

## Sources

All original figures, definitions and page references are recorded in
[`02_source_register.csv`](02_source_register.csv). The reproducible
calculation is in [`build_initial_fact_base.py`](../src/build_initial_fact_base.py).
