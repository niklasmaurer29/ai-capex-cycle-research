# NVIDIA earnings-event screen - observed market reactions

## Results

| Release | Reference date | Window | NVDA return | QQQ return | Relative return vs QQQ |
|---|---|---|---:|---:|---:|
| FY2026 Q3 | 19 Nov 2025 | Next trading day | -3.2% | -2.4% | -0.8pp |
| FY2026 Q3 | 19 Nov 2025 | Fifth trading day | -3.4% | +2.4% | -5.8pp |
| FY2026 Q4 | 25 Feb 2026 | Next trading day | -5.5% | -1.2% | -4.2pp |
| FY2026 Q4 | 25 Feb 2026 | Fifth trading day | -6.4% | -1.0% | -5.4pp |
| FY2027 Q1 | 20 May 2026 | Next trading day | -1.8% | +0.2% | -2.0pp |
| FY2027 Q1 | 20 May 2026 | Fifth trading day | -4.1% | +3.1% | -7.3pp |
| FY2027 Q2 | 26 Aug 2026 | Next trading day | +8.7% | +1.4% | +7.4pp |
| FY2027 Q2 | 26 Aug 2026 | Fifth trading day | +7.0% | -0.3% | +7.3pp |

## How to read this

The reactions were not uniform. The first three selected releases were followed
by negative short-window relative performance versus QQQ, whereas the FY2027
Q2 release produced a strong positive relative move. That is useful evidence
that NVIDIA's share price can react to the gap between reported results and
market expectations, rather than to headline growth alone.

It would be a mistake to turn this four-event observation into a rule such as
“strong results mean the stock rises” or “the market always sells the news.”
The screen is intentionally descriptive. The next research step should compare
reported revenue, guidance and management commentary with what the market had
already expected before each event.

## Reproducibility

The official release-date inputs are in
[`../data/nvda_earnings_events.csv`](../data/nvda_earnings_events.csv); the
versioned price observations are in
[`../data/nvda_qqq_event_prices.csv`](../data/nvda_qqq_event_prices.csv). Run:

```bash
python3 src/build_earnings_event_study.py
```

to recreate the locally generated CSV in `output/`.

Read the full methodology and limitations in
[`05_earnings_event_method.md`](05_earnings_event_method.md).
