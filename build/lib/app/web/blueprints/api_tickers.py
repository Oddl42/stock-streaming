#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 09:13:32 2026

@author: twi
"""

from flask import Blueprint, current_app, jsonify, request
from app.infrastructure.db.engine import make_engine, make_session_factory
from app.infrastructure.db.repositories import SelectedTickerRepo
from app.infrastructure.massive.rest_client import MassiveRestClient
from app.services.tickers_service import TickersService

bp = Blueprint("api_tickers", __name__, url_prefix="/api")

def _session():
    engine = make_engine(current_app.config["DATABASE_URL"])
    Session = make_session_factory(engine)
    return Session()

@bp.get("/tickers")
def tickers():
    client = MassiveRestClient(
        base_url=current_app.config["MASSIVE_REST_BASE"],
        api_key=current_app.config["MASSIVE_API_KEY"],
        mock=current_app.config["MASSIVE_MOCK"],
    )
    svc = TickersService(client)
    return jsonify(svc.get_all_tickers())

@bp.get("/selected-tickers")
def selected_list():
    s = _session()
    try:
        repo = SelectedTickerRepo(s)
        rows = repo.list_all()
        return jsonify([{
            "ticker": r.ticker, "name": r.name, "market": r.market,
            "primary_exchange": r.primary_exchange, "locale": r.locale
        } for r in rows])
    finally:
        s.close()

@bp.post("/selected-tickers")
def selected_upsert():
    payload = request.get_json(force=True)
    rows = payload.get("rows", [])
    s = _session()
    try:
        repo = SelectedTickerRepo(s)
        repo.upsert_many(rows)
        s.commit()
        return jsonify({"ok": True})
    finally:
        s.close()

@bp.delete("/selected-tickers/<ticker>")
def selected_delete(ticker: str):
    s = _session()
    try:
        repo = SelectedTickerRepo(s)
        repo.delete_one(ticker)
        s.commit()
        return jsonify({"ok": True})
    finally:
        s.close()
