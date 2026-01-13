#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 16:01:17 2026

@author: twi
"""
# app/infrastructure/db/models.py
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Integer, Float, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SelectedTicker(Base):
    __tablename__ = "selected_ticker"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class TickerStream(Base):
    __tablename__ = "ticker_stream"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True, nullable=False)

    price: Mapped[float] = mapped_column(Float, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
