"""Build a transparent NVIDIA earnings-event return screen.

The screen measures short, close-to-close returns around four official NVIDIA
earnings-release dates. QQQ is used only as a simple Nasdaq-100 proxy. The
relative return is a difference in returns, not a regression-based alpha and
not evidence that earnings alone caused the observed price movement.
"""

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVENTS_INPUT = PROJECT_ROOT / "data" / "nvda_earnings_events.csv"
PRICES_INPUT = PROJECT_ROOT / "data" / "nvda_qqq_event_prices.csv"
OUTPUT = PROJECT_ROOT / "output" / "nvda_earnings_event_screen.csv"

HORIZONS = ("one_trading_day", "five_trading_days")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def percentage_return(start: float, end: float) -> float:
    return (end / start - 1) * 100


def build_screen() -> list[dict[str, str | float]]:
    events = read_rows(EVENTS_INPUT)
    prices = read_rows(PRICES_INPUT)
    price_lookup = {(row["event_id"], row["horizon"]): row for row in prices}
    screen: list[dict[str, str | float]] = []

    for event in events:
        event_id = event["event_id"]
        base = price_lookup[(event_id, "event_date")]
        base_nvda = float(base["nvda_close_usd"])
        base_qqq = float(base["qqq_close_usd"])
        for horizon in HORIZONS:
            observation = price_lookup[(event_id, horizon)]
            nvda_return = percentage_return(base_nvda, float(observation["nvda_close_usd"]))
            qqq_return = percentage_return(base_qqq, float(observation["qqq_close_usd"]))
            screen.append(
                {
                    "event_id": event_id,
                    "fiscal_period": event["fiscal_period"],
                    "release_date": event["release_date"],
                    "horizon": horizon,
                    "observation_date": observation["trading_date"],
                    "nvda_event_date_close_usd": base_nvda,
                    "nvda_observation_close_usd": float(observation["nvda_close_usd"]),
                    "nvda_return_pct": round(nvda_return, 1),
                    "qqq_event_date_close_usd": base_qqq,
                    "qqq_observation_close_usd": float(observation["qqq_close_usd"]),
                    "qqq_return_pct": round(qqq_return, 1),
                    "relative_return_vs_qqq_pct_points": round(nvda_return - qqq_return, 1),
                    "definition_note": "Close-to-close return from release-date close; relative return is NVDA return minus QQQ return.",
                }
            )
    return screen


def write_csv(path: Path, rows: list[dict[str, str | float]]) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    screen = build_screen()
    write_csv(OUTPUT, screen)
    print("NVIDIA earnings-event screen\n")
    for row in screen:
        print(
            f"{row['fiscal_period']} | {row['horizon']}: "
            f"NVDA {row['nvda_return_pct']:+.1f}% | "
            f"QQQ {row['qqq_return_pct']:+.1f}% | "
            f"relative {row['relative_return_vs_qqq_pct_points']:+.1f}pp"
        )
    print(f"\nSaved screen to: {OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
