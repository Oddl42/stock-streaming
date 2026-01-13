#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 15:58:56 2026

@author: twi
"""

from datetime import datetime
from app.infrastructure.massive.rest_client import MassiveRestClient

class MarketDataService:
    def __init__(self, client: MassiveRestClient):
        self.client = client

    def get_bars(self, ticker: str, start: datetime, end: datetime, timeframe: str) -> list[dict]:
        return self.client.get_custom_bars(ticker, start, end, timeframe)
