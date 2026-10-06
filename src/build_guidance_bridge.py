"""Build a management-guidance bridge for NVIDIA quarterly revenue.

This script compares reported quarterly revenue with NVIDIA's own previously
published guidance range. It deliberately does not label the result a consensus
beat or miss because no third-party consensus dataset is versioned in this
project.
"""

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT = PROJECT_ROOT / "data" / "nvidia_revenue_guidance_bridge.csv"
OUTPUT = PROJECT_ROOT / "output" / "nvidia_revenue_guidance_bridge.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def build_bridge() -> list[dict[str, str | float]]:
    bridge: list[dict[str, str | float]] = []
    for row in read_rows(INPUT):
        midpoint = float(row["guidance_midpoint_usd_bn"])
        tolerance = float(row["guidance_tolerance_pct"]) / 100
        low_end = midpoint * (1 - tolerance)
        high_end = midpoint * (1 + tolerance)
        result: dict[str, str | float] = {
            "guided_quarter": row["guided_quarter"],
            "guidance_release_date": row["guidance_release_date"],
            "guidance_midpoint_usd_bn": midpoint,
            "guidance_low_end_usd_bn": round(low_end, 2),
            "guidance_high_end_usd_bn": round(high_end, 2),
            "china_data_center_compute_assumption": row[
                "china_data_center_compute_assumption"
            ],
        }
        if row["actual_revenue_usd_bn"]:
            actual = float(row["actual_revenue_usd_bn"])
            result.update(
                {
                    "actual_revenue_usd_bn": actual,
                    "actual_release_date": row["actual_release_date"],
                    "actual_vs_guidance_midpoint_pct": round((actual / midpoint - 1) * 100, 1),
                    "actual_minus_guidance_high_end_usd_bn": round(actual - high_end, 2),
                    "result_status": "reported",
                }
            )
        else:
            result.update(
                {
                    "actual_revenue_usd_bn": "",
                    "actual_release_date": "",
                    "actual_vs_guidance_midpoint_pct": "",
                    "actual_minus_guidance_high_end_usd_bn": "",
                    "result_status": "guidance pending",
                }
            )
        bridge.append(result)
    return bridge


def write_csv(path: Path, rows: list[dict[str, str | float]]) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    bridge = build_bridge()
    write_csv(OUTPUT, bridge)
    print("NVIDIA management-guidance bridge\n")
    for row in bridge:
        if row["result_status"] == "reported":
            print(
                f"{row['guided_quarter']}: actual USD {row['actual_revenue_usd_bn']:.1f}bn | "
                f"guidance range USD {row['guidance_low_end_usd_bn']:.2f}-{row['guidance_high_end_usd_bn']:.2f}bn | "
                f"{row['actual_vs_guidance_midpoint_pct']:+.1f}% versus midpoint"
            )
        else:
            print(
                f"{row['guided_quarter']}: guidance range USD "
                f"{row['guidance_low_end_usd_bn']:.2f}-{row['guidance_high_end_usd_bn']:.2f}bn | pending"
            )
    print(f"\nSaved bridge to: {OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
