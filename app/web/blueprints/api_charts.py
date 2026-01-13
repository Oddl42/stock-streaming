#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 09:14:06 2026

@author: twi
"""

from flask import Blueprint, current_app, jsonify, request
from datetime import datetime, date
from dateutil.parser import isoparse
from app.infrastructure.massive.rest_client import MassiveRestClient
from app.services.market_data_service import MarketDataService

bp = Blueprint("api_charts", __name__, url_prefix="/api")

@bp.get("/aggregates")
def aggregates():
    ticker = request.args["ticker"]
    tf = request.args.get("tf", "1d")
    start = isoparse(request.args["from"])
    end = isoparse(request.args["to"])

    client = MassiveRestClient(
        base_url=current_app.config["MASSIVE_REST_BASE"],
        api_key=current_app.config["MASSIVE_API_KEY"],
        mock=current_app.config["MASSIVE_MOCK"],
    )
    svc = MarketDataService(client)
    bars = svc.get_bars(ticker, start, end, tf)
    return jsonify({"ticker": ticker, "timeframe": tf, "bars": bars})
