#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 09:17:47 2026

@author: twi
"""

from flask import Blueprint, current_app, jsonify, request
from app.infrastructure.db.engine import make_engine, make_session_factory
from app.infrastructure.db.repositories import TickerStreamRepo

bp = Blueprint("api_streaming", __name__, url_prefix="/api/streaming")

def _session():
    engine = make_engine(current_app.config["DATABASE_URL"])
    Session = make_session_factory(engine)
    return Session()

@bp.get("/latest")
def latest():
    ticker = request.args["ticker"]
    s = _session()
    try:
        repo = TickerStreamRepo(s)
        row = repo.latest_bar(ticker)
        if not row:
            return jsonify({"ticker": ticker, "latest": None})
        return jsonify({
            "ticker": ticker,
            "latest": {
                "ts": row.ts.isoformat(),
                "open": float(row.open) if row.open is not None else None,
                "high": float(row.high) if row.high is not None else None,
                "low": float(row.low) if row.low is not None else None,
                "close": float(row.close) if row.close is not None else None,
                "volume": float(row.volume) if row.volume is not None else None,
            }
        })
    finally:
        s.close()

@bp.get("/bars")
def bars():
    ticker = request.args["ticker"]
    limit = int(request.args.get("limit", "5000"))
    s = _session()
    try:
        repo = TickerStreamRepo(s)
        rows = repo.last_bars(ticker, limit=limit)
        return jsonify({"ticker": ticker, "bars": [
            {
                "ts": r.ts.isoformat(),
                "open": float(r.open) if r.open is not None else None,
                "high": float(r.high) if r.high is not None else None,
                "low": float(r.low) if r.low is not None else None,
                "close": float(r.close) if r.close is not None else None,
                "volume": float(r.volume) if r.volume is not None else None,
            } for r in rows
        ]})
    finally:
        s.close()

@bp.post("/start")
def start():
    # MVP stub: in Teil C ersetzen wir das durch SparkOperator create SparkApplication
    return jsonify({"ok": True, "note": "stub"})

@bp.post("/stop")
def stop():
    return jsonify({"ok": True, "note": "stub"})
