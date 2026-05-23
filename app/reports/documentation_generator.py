from pathlib import Path
from datetime import datetime


def generate_system_documentation():

    Path(
        "docs/releases"
    ).mkdir(

        parents=True,

        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M"
    )

    file_path = (

        Path(
            "docs/releases"
        )

        /

        f"{timestamp}_system_snapshot.md"
    )

    with open(

        file_path,

        "w",

        encoding="utf-8"

    ) as f:

        f.write(
            content
        )

    print(

        f"\nDocumentation generated:\n"
        f"{file_path.resolve()}\n"
    )

content = f"""
# TradingSystem Architecture Snapshot

Generated: 

---

# Executive Summary

TradingSystem is an intelligent portfolio operating system combining:

- HMRC tax intelligence
- Portfolio analytics
- Market intelligence
- Macro intelligence
- AI recommendation engines
- Excel dashboarding

---

# System Architecture

```text
INPUT_TRANSACTIONS
        ↓

Import Pipeline
        ↓

Transaction Database
        ↓

Portfolio Engine
        ↓

Inventory Engine
        ↓

Tax Engine
        ↓

Market Intelligence
        ↓

Macro Intelligence
        ↓

AI Scoring
        ↓

Position Sizing
        ↓

Excel Outputs"""


if __name__ == "__main__":

    generate_system_documentation()