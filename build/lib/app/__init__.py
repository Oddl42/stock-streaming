#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 15:49:17 2026

@author: twi
"""

from flask import Flask
from app.web.blueprints.pages import bp as pages_bp
from app.web.blueprints.api_tickers import bp as api_tickers_bp
from app.web.blueprints.api_charts import bp as api_charts_bp
from app.web.blueprints.api_streaming import bp as api_streaming_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.config.Settings")

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_tickers_bp)
    app.register_blueprint(api_charts_bp)
    app.register_blueprint(api_streaming_bp)

    return app
