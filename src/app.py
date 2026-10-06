"""Interactive dashboard for the AI Capex Cycle research project.

The dashboard reads versioned local inputs only. It is an educational research
tool, not investment advice or a live market-data application.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RESEARCH_DIR = PROJECT_ROOT / "research"

COMPANY_COLORS = {
    "Microsoft": "#00A4EF",
    "Alphabet": "#4285F4",
    "Amazon": "#FF9900",
    "Meta": "#0081FB",
}


@st.cache_data
def load_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / filename)


@st.cache_data
def load_text(filename: str) -> str:
    return (RESEARCH_DIR / filename).read_text(encoding="utf-8")


def percent_change(current: float, prior: float) -> float:
    return (current / prior - 1) * 100


def format_bn(value_usd_m: float) -> str:
    return f"USD {value_usd_m / 1_000:.1f}bn"


def title_block(title: str, subtitle: str) -> None:
    st.title(title)
    st.caption(subtitle)


def bar_chart(
    frame: pd.DataFrame,
    value_field: str,
    title: str,
    tooltip: list[dict[str, str]],
) -> None:
    colors = [COMPANY_COLORS[company] for company in frame["company"]]
    st.vega_lite_chart(
        frame,
        {
            "title": {"text": title, "anchor": "start", "fontSize": 16},
            "mark": {"type": "bar", "cornerRadiusTopRight": 4, "cornerRadiusTopLeft": 4},
            "encoding": {
                "x": {"field": "company", "type": "nominal", "sort": None, "title": None},
                "y": {"field": value_field, "type": "quantitative", "title": "USD bn"},
                "color": {
                    "field": "company",
                    "type": "nominal",
                    "scale": {"range": colors},
                    "legend": None,
                },
                "tooltip": tooltip,
            },
            "height": 330,
        },
        width="stretch",
    )


def investment_cycle() -> None:
    hyperscalers = load_csv("hyperscaler_capex_inputs.csv").copy()
    nvidia = load_csv("nvidia_fy2026_inputs.csv").iloc[0]
    hyperscalers["ppe_growth_pct"] = (
        hyperscalers["raw_ppe_purchases_current_usd_m"]
        / hyperscalers["raw_ppe_purchases_prior_usd_m"]
        - 1
    ) * 100
    hyperscalers["cash_flow_less_ppe_usd_m"] = (
        hyperscalers["operating_cash_flow_current_usd_m"]
        - hyperscalers["raw_ppe_purchases_current_usd_m"]
    )
    hyperscalers["ppe_current_usd_bn"] = (
        hyperscalers["raw_ppe_purchases_current_usd_m"] / 1_000
    )
    hyperscalers["cash_flow_less_ppe_usd_bn"] = (
        hyperscalers["cash_flow_less_ppe_usd_m"] / 1_000
    )

    combined_current = hyperscalers["raw_ppe_purchases_current_usd_m"].sum()
    combined_prior = hyperscalers["raw_ppe_purchases_prior_usd_m"].sum()
    data_center_growth = percent_change(
        nvidia["data_center_revenue_usd_m"],
        nvidia["prior_data_center_revenue_usd_m"],
    )
    data_center_share = (
        nvidia["data_center_revenue_usd_m"] / nvidia["total_revenue_usd_m"] * 100
    )

    title_block(
        "The AI Capex Cycle",
        "Reported fiscal-period data only. Different fiscal year ends and definitions remain visible.",
    )
    left, centre, right = st.columns(3)
    left.metric(
        "Combined hyperscaler raw P&E",
        format_bn(combined_current),
        f"{percent_change(combined_current, combined_prior):+.1f}% year on year",
    )
    centre.metric(
        "NVIDIA Data Center revenue",
        format_bn(nvidia["data_center_revenue_usd_m"]),
        f"{data_center_growth:+.1f}% year on year",
    )
    right.metric("Data Center share of revenue", f"{data_center_share:.1f}%", "FY2026")

    bar_chart(
        hyperscalers,
        "ppe_current_usd_bn",
        "Raw property-and-equipment purchases",
        [
            {"field": "company", "type": "nominal", "title": "Company"},
            {
                "field": "ppe_current_usd_bn",
                "type": "quantitative",
                "title": "Raw P&E purchases",
                "format": ".1f",
            },
            {
                "field": "ppe_growth_pct",
                "type": "quantitative",
                "title": "Year-on-year growth",
                "format": ".1f",
            },
        ],
    )
    bar_chart(
        hyperscalers,
        "cash_flow_less_ppe_usd_bn",
        "Operating cash flow less raw P&E purchases",
        [
            {"field": "company", "type": "nominal", "title": "Company"},
            {
                "field": "cash_flow_less_ppe_usd_bn",
                "type": "quantitative",
                "title": "Cash flow less raw P&E",
                "format": ".1f",
            },
        ],
    )

    with st.expander("Comparability safeguard"):
        st.write(
            "The capex chart uses raw cash-flow lines. It is not AI-only capex, "
            "not direct NVIDIA spend and not comparable to issuer-reported free cash flow."
        )
        st.dataframe(
            hyperscalers[
                ["company", "fiscal_period_end", "reported_measure", "comparability_note"]
            ],
            hide_index=True,
            width="stretch",
        )


def earnings_data() -> pd.DataFrame:
    events = load_csv("nvda_earnings_events.csv")
    prices = load_csv("nvda_qqq_event_prices.csv")
    baseline = prices[prices["horizon"] == "event_date"].set_index("event_id")
    observations = prices[prices["horizon"] != "event_date"].copy()
    observations["nvda_return_pct"] = observations.apply(
        lambda row: (
            row["nvda_close_usd"] / baseline.loc[row["event_id"], "nvda_close_usd"] - 1
        )
        * 100,
        axis=1,
    )
    observations["qqq_return_pct"] = observations.apply(
        lambda row: (
            row["qqq_close_usd"] / baseline.loc[row["event_id"], "qqq_close_usd"] - 1
        )
        * 100,
        axis=1,
    )
    observations["relative_return_pct_points"] = (
        observations["nvda_return_pct"] - observations["qqq_return_pct"]
    )
    return observations.merge(
        events[["event_id", "fiscal_period", "release_date"]], on="event_id"
    )


def earnings_reactions() -> None:
    returns = earnings_data()
    title_block(
        "Earnings reactions",
        "Close-to-close historical returns around official NVIDIA release dates; QQQ is a Nasdaq-100 proxy.",
    )
    labels = {
        "one_trading_day": "Next trading day",
        "five_trading_days": "Fifth trading day",
    }
    horizon = st.segmented_control(
        "Return window",
        options=list(labels),
        format_func=labels.get,
        default="one_trading_day",
    )
    selected = returns[returns["horizon"] == horizon].copy()
    selected["event_label"] = selected["fiscal_period"] + " / " + selected["release_date"]
    selected["NVDA"] = selected["nvda_return_pct"].round(1)
    selected["QQQ"] = selected["qqq_return_pct"].round(1)
    chart_data = selected.melt(
        id_vars=["event_label"],
        value_vars=["NVDA", "QQQ"],
        var_name="security",
        value_name="return_pct",
    )

    st.vega_lite_chart(
        chart_data,
        {
            "title": {"text": "Return from earnings-date close", "anchor": "start", "fontSize": 16},
            "mark": {"type": "bar", "cornerRadiusTopRight": 3, "cornerRadiusTopLeft": 3},
            "encoding": {
                "x": {"field": "event_label", "type": "nominal", "title": None},
                "xOffset": {"field": "security"},
                "y": {"field": "return_pct", "type": "quantitative", "title": "Return (%)"},
                "color": {
                    "field": "security",
                    "type": "nominal",
                    "scale": {"domain": ["NVDA", "QQQ"], "range": ["#76B900", "#6B7280"]},
                    "title": None,
                },
                "tooltip": [
                    {"field": "event_label", "type": "nominal", "title": "Release"},
                    {"field": "security", "type": "nominal", "title": "Security"},
                    {
                        "field": "return_pct",
                        "type": "quantitative",
                        "title": "Return",
                        "format": ".1f",
                    },
                ],
            },
            "height": 360,
        },
        width="stretch",
    )

    table = selected[
        [
            "fiscal_period",
            "release_date",
            "trading_date",
            "NVDA",
            "QQQ",
            "relative_return_pct_points",
        ]
    ].copy()
    table["relative_return_pct_points"] = table["relative_return_pct_points"].round(1)
    table.columns = [
        "Fiscal period",
        "Release date",
        "Observation date",
        "NVDA return (%)",
        "QQQ return (%)",
        "Relative return (pp)",
    ]
    st.dataframe(table, hide_index=True, width="stretch")
    st.info(
        "A positive or negative relative return is descriptive only. It is not a "
        "causal estimate, a trading signal or a buy/hold/sell view."
    )


def guidance_bridge() -> None:
    guidance = load_csv("nvidia_revenue_guidance_bridge.csv").copy()
    guidance["guidance_low_end_usd_bn"] = guidance["guidance_midpoint_usd_bn"] * (
        1 - guidance["guidance_tolerance_pct"] / 100
    )
    guidance["guidance_high_end_usd_bn"] = guidance["guidance_midpoint_usd_bn"] * (
        1 + guidance["guidance_tolerance_pct"] / 100
    )
    reported = guidance[guidance["actual_revenue_usd_bn"].notna()].copy()
    pending = guidance[guidance["actual_revenue_usd_bn"].isna()].iloc[0]
    reported["actual_vs_high_end_usd_bn"] = (
        reported["actual_revenue_usd_bn"] - reported["guidance_high_end_usd_bn"]
    )

    title_block(
        "Management-guidance bridge",
        "Comparison with NVIDIA's own prior guidance range, not with external consensus estimates.",
    )
    first, second, third = st.columns(3)
    first.metric("Reported quarters above own high end", "3 / 3")
    second.metric(
        "FY2027 Q2 revenue versus midpoint",
        "+5.7%",
        "+USD 3.4bn versus high end",
    )
    third.metric("FY2027 Q3 guidance midpoint", "USD 108.0bn", "Result pending")

    chart_data = reported.melt(
        id_vars=["guided_quarter"],
        value_vars=[
            "guidance_low_end_usd_bn",
            "guidance_high_end_usd_bn",
            "actual_revenue_usd_bn",
        ],
        var_name="measure",
        value_name="revenue_usd_bn",
    )
    chart_data["measure"] = chart_data["measure"].replace(
        {
            "guidance_low_end_usd_bn": "Guidance low end",
            "guidance_high_end_usd_bn": "Guidance high end",
            "actual_revenue_usd_bn": "Reported revenue",
        }
    )
    st.vega_lite_chart(
        chart_data,
        {
            "title": {
                "text": "Reported revenue versus own guidance range",
                "anchor": "start",
                "fontSize": 16,
            },
            "mark": {"type": "bar", "cornerRadiusTopRight": 3, "cornerRadiusTopLeft": 3},
            "encoding": {
                "x": {"field": "guided_quarter", "type": "nominal", "title": None},
                "xOffset": {"field": "measure"},
                "y": {"field": "revenue_usd_bn", "type": "quantitative", "title": "USD bn"},
                "color": {
                    "field": "measure",
                    "type": "nominal",
                    "scale": {"range": ["#9CA3AF", "#4B5563", "#76B900"]},
                    "title": None,
                },
                "tooltip": [
                    {"field": "guided_quarter", "type": "nominal", "title": "Quarter"},
                    {"field": "measure", "type": "nominal", "title": "Measure"},
                    {
                        "field": "revenue_usd_bn",
                        "type": "quantitative",
                        "title": "Revenue",
                        "format": ".2f",
                    },
                ],
            },
            "height": 360,
        },
        width="stretch",
    )

    table = reported[
        [
            "guided_quarter",
            "guidance_midpoint_usd_bn",
            "guidance_low_end_usd_bn",
            "guidance_high_end_usd_bn",
            "actual_revenue_usd_bn",
            "actual_vs_high_end_usd_bn",
            "china_data_center_compute_assumption",
        ]
    ].copy()
    table.columns = [
        "Guided quarter",
        "Guidance midpoint (USD bn)",
        "Low end (USD bn)",
        "High end (USD bn)",
        "Actual revenue (USD bn)",
        "Actual minus high end (USD bn)",
        "China Data Center compute assumption",
    ]
    st.dataframe(table, hide_index=True, width="stretch")
    st.warning(
        f"FY2027 Q3 guidance is USD {pending['guidance_low_end_usd_bn']:.2f}bn–"
        f"{pending['guidance_high_end_usd_bn']:.2f}bn. NVIDIA assumed no Data Center "
        "compute revenue from China; the result was pending at the project cut-off."
    )


def market_memo() -> None:
    title_block(
        "Market memo",
        "A source-backed summary of the investment cycle, market expectations and open diligence question.",
    )
    left, right = st.columns(2)
    with left:
        st.subheader("Core insight")
        st.write(
            "Three quarters exceeded NVIDIA's own revenue range, but the short-window "
            "share-price reaction varied sharply. Execution must be separated from expectations."
        )
    with right:
        st.subheader("Next question")
        st.write(
            "Will NVIDIA's next guidance change implied revenue, margin or China assumptions "
            "more than the market already expects?"
        )
    with st.expander("Read the full market memo", expanded=True):
        st.markdown(load_text("08_market_memo.md"))


def main() -> None:
    st.set_page_config(page_title="AI Capex Cycle Research", page_icon="📈", layout="wide")
    st.markdown(
        """
        <style>
            .block-container { max-width: 1280px; padding-top: 2.2rem; padding-bottom: 3rem; }
            [data-testid="stMetricValue"] { font-size: 1.65rem; }
            [data-testid="stSidebar"] { border-right: 1px solid #E5E7EB; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.sidebar:
        st.header("AI Capex Cycle")
        st.caption("NVIDIA, hyperscalers and market expectations")
        page = st.radio(
            "Navigate",
            ["Investment cycle", "Earnings reactions", "Guidance bridge", "Market memo"],
            label_visibility="collapsed",
        )
        st.divider()
        st.caption("Research cut-off: 6 October 2026")
        st.caption("Educational research only — not investment advice.")

    if page == "Investment cycle":
        investment_cycle()
    elif page == "Earnings reactions":
        earnings_reactions()
    elif page == "Guidance bridge":
        guidance_bridge()
    else:
        market_memo()


if __name__ == "__main__":
    main()
