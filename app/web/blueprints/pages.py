#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 09:12:56 2026

@author: twi
"""

from flask import Blueprint, render_template
bp = Blueprint("pages", __name__)

@bp.get("/")
def index():
    return render_template("tickers.html")

@bp.get("/tickers")
def tickers_page():
    return render_template("tickers.html")

@bp.get("/charts")
def charts_page():
    return render_template("charts.html")

@bp.get("/streaming")
def streaming_page():
    return render_template("streaming.html")
