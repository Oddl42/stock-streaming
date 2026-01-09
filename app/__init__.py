#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 15:49:17 2026

@author: twi
"""

from flask import Flask
from app.web.blueprints.tickers import bp as tickers_bp
from app.web.blueprints.charts import bp as charts_bp
from app.web.blueprints.streaming import bp as streaming_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.config.Settings")

    app.register_blueprint(tickers_bp)
    app.register_blueprint(charts_bp)
    app.register_blueprint(streaming_bp)

    return app
