from pathlib import Path
from datetime import datetime, timezone


from collector import (
    collect_btc_index_1m_for_last_day,
    # collect_daily_options_snapshot,
)


def main():
    today = datetime.now(timezone.utc).date().isoformat()

    base = Path("data")
    base.mkdir(parents=True, exist_ok=True)

    collect_btc_index_1m_for_last_day(
        base / f"btc_index_1m_{today}.parquet"
    )

    # collect_daily_options_snapshot(
    #     currency="BTC",
    #     output_path=base / "options" / f"btc_options_{today}.parquet",
    # )

if __name__ == "__main__":
    main()
