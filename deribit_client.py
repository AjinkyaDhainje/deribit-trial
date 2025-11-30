import requests
from typing import Any, Dict, List, Optional


class DeribitDataClient:
    def __init__(self, testnet: bool = False, timeout: int = 10):
        self.base_url = (
            "https://test.deribit.com/api/v2"
            if testnet
            else "https://www.deribit.com/api/v2"
        )
        self.session = requests.Session()
        self.timeout = timeout
        self._id = 0

    def _call(self, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        self._id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self._id,
            "method": method,
            "params": params or {},
        }
        resp = self.session.post(self.base_url, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        if "error" in data and data["error"] is not None:
            raise RuntimeError(f"Deribit error {data['error']}")
        return data["result"]

    # -------- instruments / metadata --------
    def get_instruments(
        self,
        currency: str = "BTC",
        kind: str = "option",
        expired: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Full list of instruments, e.g. all BTC options.
        """
        params = {"currency": currency, "kind": kind, "expired": expired}
        return self._call("public/get_instruments", params)

    def get_instrument(self, instrument_name: str) -> Dict[str, Any]:
        return self._call("public/get_instrument", {"instrument_name": instrument_name})

    # -------- summary, prices, greeks --------
    def get_book_summary_by_currency(
        self, currency: str = "BTC", kind: str = "option"
    ) -> List[Dict[str, Any]]:
        """
        Snapshot for all instruments of a currency + kind.
        Contains mark price, IV, greeks, OI, volume, etc.
        """
        params = {"currency": currency, "kind": kind}
        return self._call("public/get_book_summary_by_currency", params)

    def get_book_summary_by_instrument(self, instrument_name: str) -> Dict[str, Any]:
        result = self._call(
            "public/get_book_summary_by_instrument",
            {"instrument_name": instrument_name},
        )
        # API returns a list with one element
        return result[0] if isinstance(result, list) and result else result

    def get_mark_price_history(
        self, instrument_name: str, start_timestamp: int, end_timestamp: int
    ) -> List[Dict[str, Any]]:
        params = {
            "instrument_name": instrument_name,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
        }
        return self._call("public/get_mark_price_history", params)

    # -------- order book and trades --------
    def get_order_book(self, instrument_name: str, depth: int = 50) -> Dict[str, Any]:
        params = {"instrument_name": instrument_name, "depth": depth}
        return self._call("public/get_order_book", params)

    def get_last_trades_by_instrument(
        self,
        instrument_name: str,
        count: int = 100,
        include_old: bool = True,
    ) -> Dict[str, Any]:
        params = {
            "instrument_name": instrument_name,
            "count": count,
            "include_old": include_old,
        }
        return self._call("public/get_last_trades_by_instrument", params)

    # -------- index and OHLCV --------
    def get_index_price(self, index_name: str = "btc_usd") -> Dict[str, Any]:
        return self._call("public/get_index_price", {"index_name": index_name})

    def get_tradingview_ohlcv(
        self,
        instrument_name: str,
        start_timestamp: int,
        end_timestamp: int,
        resolution: str = "1",  # "1" = 1 minute, "60" = 1 hour, etc.
    ) -> Dict[str, Any]:
        params = {
            "instrument_name": instrument_name,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "resolution": resolution,
        }
        return self._call("public/get_tradingview_chart_data", params)
