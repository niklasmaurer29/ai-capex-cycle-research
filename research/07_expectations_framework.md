# Expectations framework - why strong results can still produce a weak stock reaction

## The key distinction

This project separates three different questions:

1. **Did NVIDIA execute against its own previously published guidance?**
2. **What did the market appear to reward or penalise in the short-window price reaction?**
3. **Did the result exceed the external expectations already embedded in the share price?**

Only the first two can be tested from the versioned, public inputs in this
repository. A true consensus beat/miss analysis would require a dated,
licensable analyst-consensus dataset; it is therefore not asserted here.

## Management-guidance bridge

| Guided quarter | Revenue guidance | Actual revenue | Actual vs midpoint | Actual vs high end | China Data Center compute assumption |
|---|---:|---:|---:|---:|---|
| FY2026 Q4 | USD 65.0bn ±2% | USD 68.1bn | +4.8% | +USD 1.8bn | Not stated in the guidance bullet |
| FY2027 Q1 | USD 78.0bn ±2% | USD 81.6bn | +4.6% | +USD 2.0bn | No revenue assumed |
| FY2027 Q2 | USD 91.0bn ±2% | USD 96.2bn | +5.7% | +USD 3.4bn | No revenue assumed |
| FY2027 Q3 | USD 108.0bn ±2% | Pending | — | — | No revenue assumed |

The results show that reported revenue exceeded the high end of NVIDIA's own
revenue range for each of the three reported quarters. This is an execution
observation, not evidence that the company beat sell-side consensus.

## Connecting the guidance bridge to the event study

FY2026 Q4 and FY2027 Q1 both exceeded management's prior guidance range, yet
the next-trading-day relative returns in the event screen were **-4.2pp** and
**-2.0pp** versus QQQ. By contrast, FY2027 Q2 also exceeded the range and was
followed by a **+7.4pp** next-day relative return.

This is the central Markets insight from the project: the stock reaction is not
a mechanical response to high reported growth or an own-guidance beat. It is
more plausibly shaped by the difference between the result and the market's
pre-existing expectations, alongside the outlook and risk narrative. The data
do not isolate causality.

## What a Markets analyst should monitor before the next release

| Driver | Why it matters | Public evidence in this project | Question to ask |
|---|---|---|---|
| Revenue and next-quarter guide | Growth must be assessed against what investors had anticipated, not only against the prior year. | Revenue-guidance bridge and official releases | Does the new guide extend, maintain or reset the revenue trajectory? |
| Data Center demand | The capex thesis depends on hyperscaler spending reaching NVIDIA's Data Center business. | FY2026 Data Center revenue and hyperscaler P&E screen | Is demand broadening across customers and products, or becoming more concentrated? |
| China and policy exposure | Policy can affect the addressable market and the confidence investors place in forward guidance. | NVIDIA assumed no China Data Center compute revenue in FY2027 Q1, Q2 and Q3 guidance. | Does management maintain that assumption, quantify a change or identify a new constraint? |
| Gross margin and product transition | A new platform ramp can change mix, supply costs and margins even while revenue is strong. | Official outlooks disclose gross-margin ranges alongside revenue. | Is the revenue guide supported by stable economics, or is the market focusing on the margin path? |
| Hyperscaler funding capacity | Higher capex is supportive only if customers can finance it and keep spending. | 2025 reported operating cash flow and P&E-purchase screen | Are capex plans still rising, and how much cash generation remains after investment? |

## How to explain this in an interview

> “I did not equate strong revenue growth with a positive share-price reaction. I compared NVIDIA's results with its own prior guidance, then mapped the price response relative to QQQ. Three reported quarters exceeded management's revenue range, but two still underperformed QQQ immediately afterwards. That taught me to separate execution from expectations and to monitor the next guide, China assumptions, margins and hyperscaler capex rather than rely on a single headline number.”

## Method note

The numerical bridge is produced by
[`../src/build_guidance_bridge.py`](../src/build_guidance_bridge.py) from
[`../data/nvidia_revenue_guidance_bridge.csv`](../data/nvidia_revenue_guidance_bridge.csv).
Release URLs and source references are recorded in
[`02_source_register.csv`](02_source_register.csv). For the price method and
limitations, see [`05_earnings_event_method.md`](05_earnings_event_method.md).
