"""Build the first source-backed AI-capex-cycle fact base.

The script deliberately distinguishes reported cash-flow lines from AI-only
spending. It calculates a common diagnostic (operating cash flow less raw
property-and-equipment purchases) but does not call it issuer-reported free
cash flow or make an investment recommendation.
"""

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HYPERSCALER_INPUT = PROJECT_ROOT / "data" / "hyperscaler_capex_inputs.csv"
NVIDIA_INPUT = PROJECT_ROOT / "data" / "nvidia_fy2026_inputs.csv"
HYPERSCALER_OUTPUT = PROJECT_ROOT / "output" / "hyperscaler_capex_screen.csv"
NVIDIA_OUTPUT = PROJECT_ROOT / "output" / "nvidia_operating_screen.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def number(row: dict[str, str], column: str) -> float:
    return float(row[column])


def build_hyperscaler_rows() -> list[dict[str, str | float]]:
    rows: list[dict[str, str | float]] = []
    for row in read_rows(HYPERSCALER_INPUT):
        operating_cash_flow = number(row, "operating_cash_flow_current_usd_m")
        raw_ppe_purchases = number(row, "raw_ppe_purchases_current_usd_m")
        prior_raw_ppe_purchases = number(row, "raw_ppe_purchases_prior_usd_m")
        rows.append(
            {
                "company": row["company"],
                "fiscal_period_end": row["fiscal_period_end"],
                "operating_cash_flow_usd_m": operating_cash_flow,
                "raw_ppe_purchases_usd_m": raw_ppe_purchases,
                "ppe_purchase_growth_pct": round(
                    (raw_ppe_purchases / prior_raw_ppe_purchases - 1) * 100, 1
                ),
                "cash_flow_less_raw_ppe_usd_m": round(
                    operating_cash_flow - raw_ppe_purchases, 1
                ),
                "raw_ppe_as_pct_of_operating_cash_flow": round(
                    raw_ppe_purchases / operating_cash_flow * 100, 1
                ),
                "reported_measure": row["reported_measure"],
                "comparability_note": row["comparability_note"],
            }
        )
    return rows


def build_nvidia_row() -> dict[str, str | float]:
    row = read_rows(NVIDIA_INPUT)[0]
    total_revenue = number(row, "total_revenue_usd_m")
    data_center_revenue = number(row, "data_center_revenue_usd_m")
    operating_cash_flow = number(row, "operating_cash_flow_usd_m")
    ppe_and_intangible_purchases = number(row, "ppe_and_intangible_purchases_usd_m")
    prior_data_center_revenue = number(row, "prior_data_center_revenue_usd_m")
    return {
        "fiscal_period_end": row["fiscal_period_end"],
        "total_revenue_usd_m": total_revenue,
        "data_center_revenue_usd_m": data_center_revenue,
        "data_center_revenue_growth_pct": round(
            (data_center_revenue / prior_data_center_revenue - 1) * 100, 1
        ),
        "data_center_share_of_revenue_pct": round(data_center_revenue / total_revenue * 100, 1),
        "operating_income_usd_m": number(row, "operating_income_usd_m"),
        "operating_cash_flow_usd_m": operating_cash_flow,
        "cash_flow_less_ppe_and_intangibles_usd_m": round(
            operating_cash_flow - ppe_and_intangible_purchases, 1
        ),
        "definition_note": row["definition_note"],
    }


def write_csv(path: Path, rows: list[dict[str, str | float]]) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    hyperscaler_rows = build_hyperscaler_rows()
    nvidia_row = build_nvidia_row()
    write_csv(HYPERSCALER_OUTPUT, hyperscaler_rows)
    write_csv(NVIDIA_OUTPUT, [nvidia_row])

    combined_current_ppe = sum(float(row["raw_ppe_purchases_usd_m"]) for row in hyperscaler_rows)
    print("AI Capex Cycle - Initial Fact Base\n")
    for row in hyperscaler_rows:
        print(
            f"{row['company']}: raw P&E purchases USD {row['raw_ppe_purchases_usd_m']:,.0f}m | "
            f"{row['ppe_purchase_growth_pct']:.1f}% year on year"
        )
    print(f"\nCombined hyperscaler raw P&E purchases: USD {combined_current_ppe:,.0f}m")
    print(
        f"NVIDIA Data Center revenue: USD {nvidia_row['data_center_revenue_usd_m']:,.0f}m | "
        f"{nvidia_row['data_center_revenue_growth_pct']:.1f}% year on year"
    )
    print("\nImportant: raw P&E purchases are not treated as AI-only capex or issuer-reported free cash flow.")
    print(f"Saved screens to: {HYPERSCALER_OUTPUT.relative_to(PROJECT_ROOT)} and {NVIDIA_OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
