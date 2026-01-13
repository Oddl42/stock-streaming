#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 15:58:29 2026

@author: twi
"""

from app.infrastructure.massive.rest_client import MassiveRestClient

class TickersService:
    def __init__(self, client: MassiveRestClient):
        self.client = client

    def get_all_tickers(self) -> list[dict]:
        return self.client.list_all_tickers()
