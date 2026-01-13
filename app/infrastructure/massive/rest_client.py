#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 16:00:35 2026

@author: twi
"""

import requests
from datetime import datetime
from dateutil.parser import isoparse

class MassiveRestClient:
    def __init__(self, base_url: str, api_key: str, mock: bool = False):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.mock = mock

    def list_all_tickers(self) -> list[dict]:
        if self.mock:
            return [
                {"name": "Apple Inc.", "ticker": "AAPL", "market": "stocks", "primary_exchange": "NASDAQ", "locale": "us"},
                {"name": "Microsoft", "ticker": "MSFT", "market": "stocks", "primary_exchange": "NASDAQ", "locale": "us"},
            ]

        # TODO: URL + Params exakt nach Massive "all-tickers" Doku einsetzen
        #url = f"{self.base_url}/docs/rest/stocks/tickers/all-tickers"
        url = f"{self.base_url}/v3/reference/tickers?market=stocks&active=true&order=asc&limit=1000&sort=ticker&apiKey={self.api_key}"
        raise NotImplementedError(f"Setze echten Endpoint/Params für Massive: {url}")

    def get_custom_bars(self, ticker: str, start: datetime, end: datetime, timeframe: str) -> list[dict]:
        if self.mock:
            # Dummy OHLCV-Serie
            import random
            from datetime import timedelta
            ts = start
            out = []
            price = 100.0
            while ts <= end and len(out) < 200:
                o = price
                c = o + random.uniform(-1, 1)
                h = max(o, c) + random.uniform(0, 0.5)
                l = min(o, c) - random.uniform(0, 0.5)
                out.append({"ts": ts.isoformat(), "open": o, "high": h, "low": l, "close": c, "volume": random.randint(1000, 10000)})
                price = c
                ts += timedelta(days=1) if timeframe == "1d" else timedelta(minutes=1)
            return out

        # TODO: Endpoint nach Massive "custom-bars" Doku einsetzen
        raise NotImplementedError("Implementiere Massive custom-bars REST Call.")
