import time
from datetime import datetime, timedelta, timezone

import pandas as pd
from deribit_client import DeribitDataClient


def collect_btc_index_1m_for_last_day(output_path: str) -> None:
    client = DeribitDataClient(testnet=False)

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=1)

    # Deribit expects ms since epoch
    start_ms = int(start.timestamp() * 1000)
    end_ms = int(end.timestamp() * 1000)

    result = client.get_tradingview_ohlcv(
        instrument_name="BTC-PERPETUAL",  # or an index instrument if available
        start_timestamp=start_ms,
        end_timestamp=end_ms,
        resolution="1",
    )

    # result has keys: ticks, open, high, low, close, volume, cost (per docs)
    df = pd.DataFrame(
        {
            "timestamp": result["ticks"],
            "open": result["open"],
            "high": result["high"],
            "low": result["low"],
            "close": result["close"],
            "volume": result["volume"],
        }
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)

    df.to_parquet(output_path, index=False)
