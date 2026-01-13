#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 16:01:17 2026

@author: twi
"""
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Numeric, func

class Base(DeclarativeBase):
    pass

class SelectedTicker(Base):
    __tablename__ = "selected_ticker"
    ticker: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    market: Mapped[str | None] = mapped_column(String, nullable=True)
    primary_exchange: Mapped[str | None] = mapped_column(String, nullable=True)
    locale: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

class TickerStream(Base):
    __tablename__ = "ticker_stream"
    ticker: Mapped[str] = mapped_column(String, primary_key=True)
    ts: Mapped = mapped_column(DateTime(timezone=True), primary_key=True)

    open: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    high: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    low: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    close: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    volume: Mapped[float | None] = mapped_column(Numeric, nullable=True)
