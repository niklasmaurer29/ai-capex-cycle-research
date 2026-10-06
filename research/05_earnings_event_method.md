# NVIDIA earnings-event study - method

## Purpose

This screen asks a narrow markets question: how did NVIDIA's share price move
over short windows around four official earnings-release dates? It is designed
to complement the project’s fundamental capex and cash-flow analysis, not to
create a trading signal or make an investment recommendation.

## Event dates

The event-date reference is the publication date on NVIDIA's official Newsroom
release. The four releases are listed in
[`../data/nvda_earnings_events.csv`](../data/nvda_earnings_events.csv) and the
source register records their URLs.

## Price and benchmark data

- **NVIDIA:** daily `Close/Last` observations for NVDA from Nasdaq Historical
  Quotes.
- **Benchmark:** daily `Close/Last` observations for the Invesco QQQ Trust
  (QQQ), used as a simple Nasdaq-100 proxy rather than as a model-derived
  expected return.
- **Snapshot date:** 6 October 2026. The 12 values used in the screen are
  versioned in [`../data/nvda_qqq_event_prices.csv`](../data/nvda_qqq_event_prices.csv).

The inputs are unadjusted daily closing-price observations as supplied by the
source. No adjustment field is assumed or added by the project.

## Return convention

For each release date *t*, the screen uses the closing price on the release
date as its common starting point and measures close-to-close returns to:

1. the next US trading day (*t+1*); and
2. the fifth subsequent US trading day (*t+5*).

The return is calculated as:

```text
Return = (closing price at observation date / closing price at release-date close - 1) × 100
```

The relative figure is a simple percentage-point difference:

```text
Relative return versus QQQ = NVDA return - QQQ return
```

It is **not** a regression-based abnormal return, alpha or causal estimate.

## Important limitations

1. Four observations are too few for statistical inference.
2. Other company news, sector news and macro moves can affect either price
   during the same window.
3. QQQ is a practical technology-growth benchmark, not a perfect hedge for
   NVIDIA's semiconductor-specific exposure.
4. The study describes a historical price pattern; it does not prove that the
   earnings release caused the move and does not predict the next release.

The reproducible calculation is in
[`../src/build_earnings_event_study.py`](../src/build_earnings_event_study.py).
