#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 15:49:45 2026

@author: twi
"""

import os
'''
class Settings:
    MASSIVE_API_KEY = os.getenv("MASSIVE_API_KEY", "")
    MASSIVE_REST_BASE = os.getenv("MASSIVE_REST_BASE", "https://massive.com")  # anpassen
    MASSIVE_WS_URL = os.getenv("MASSIVE_WS_URL", "")  # aus Doku

    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://app:app@localhost:5432/app")

    K8S_NAMESPACE = os.getenv("K8S_NAMESPACE", "stock-ui")
    SPARK_APP_NAME = os.getenv("SPARK_APP_NAME", "massive-aggregates-stream")
'''
class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://stock:stock@localhost:5432/stock"
    )

    MASSIVE_API_KEY = os.getenv("MASSIVE_API_KEY", "")
    MASSIVE_REST_BASE = os.getenv("MASSIVE_REST_BASE", "https://api.massive.com")
    MASSIVE_MOCK = os.getenv("MASSIVE_MOCK", "true").lower() == "true"

    # Streaming / Spark später
    K8S_NAMESPACE = os.getenv("K8S_NAMESPACE", "stock-ui")
    SPARK_APP_NAME = os.getenv("SPARK_APP_NAME", "massive-aggregates-stream")
