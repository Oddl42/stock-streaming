#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 16:01:30 2026

@author: twi
"""

from sqlalchemy import select, delete, desc
from sqlalchemy.orm import Session
from app.infrastructure.db.models import SelectedTicker, TickerStream

class SelectedTickerRepo:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> list[SelectedTicker]:
        return list(self.session.scalars(select(SelectedTicker).order_by(SelectedTicker.ticker)))

    def upsert_many(self, rows: list[dict]) -> None:
        for r in rows:
            obj = self.session.get(SelectedTicker, r["ticker"]) or SelectedTicker(ticker=r["ticker"])
            obj.name = r.get("name")
            obj.market = r.get("market")
            obj.primary_exchange = r.get("primary_exchange")
            obj.locale = r.get("locale")
            self.session.merge(obj)

    def delete_one(self, ticker: str) -> None:
        self.session.execute(delete(SelectedTicker).where(SelectedTicker.ticker == ticker))

class TickerStreamRepo:
    def __init__(self, session: Session):
        self.session = session

    def last_bars(self, ticker: str, limit: int = 5000) -> list[TickerStream]:
        q = (
            select(TickerStream)
            .where(TickerStream.ticker == ticker)
            .order_by(desc(TickerStream.ts))
            .limit(limit)
        )
        return list(self.session.scalars(q))

    def latest_bar(self, ticker: str) -> TickerStream | None:
        rows = self.last_bars(ticker, limit=1)
        return rows[0] if rows else None
