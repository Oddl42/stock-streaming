#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 16:03:02 2026

@author: twi
"""

import os
import json
import time
import psycopg
from datetime import datetime, timezone
from pyspark.sql import SparkSession
from websocket import WebSocketApp  # websocket-client

DB = os.environ["DATABASE_URL"].replace("postgresql+psycopg", "postgresql")
API_KEY = os.environ["MASSIVE_API_KEY"]
WS_URL = os.environ["MASSIVE_WS_URL"]
TICKERS = [t for t in os.getenv("TICKERS", "").split(",") if t]

def upsert_bar(conn, bar: dict):
    # Erwartete Felder beispielhaft: ticker, ts, o,h,l,c,v
    conn.execute(
        """
        INSERT INTO ticker_stream (ticker, ts, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (ticker, ts) DO UPDATE SET
          open=EXCLUDED.open, high=EXCLUDED.high, low=EXCLUDED.low, close=EXCLUDED.close, volume=EXCLUDED.volume
        """,
        (
          bar["ticker"],
          bar["ts"],
          bar.get("open"), bar.get("high"), bar.get("low"), bar.get("close"), bar.get("volume")
        )
    )

def enforce_retention(conn, ticker: str, keep: int = 5000):
    # löscht alles älter als die neuesten N
    conn.execute(
        """
        DELETE FROM ticker_stream
        WHERE ticker = %s
          AND (ticker, ts) NOT IN (
            SELECT ticker, ts
            FROM ticker_stream
            WHERE ticker = %s
            ORDER BY ts DESC
            LIMIT %s
          )
        """,
        (ticker, ticker, keep)
    )

def main():
    spark = SparkSession.builder.appName("massive-ws-aggregates-1m").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    conn = psycopg.connect(DB)
    conn.autocommit = True

    def on_open(ws):
        # Auth/Subscribe: gemäß Massive WS Doku implementieren
        # ws.send(json.dumps({...}))
        pass

    def on_message(ws, message: str):
        data = json.loads(message)

        # TODO: auf das Massive "aggregates per minute" Payload mappen
        # Beispiel mapping:
        bar = {
            "ticker": data["ticker"],
            "ts": datetime.fromtimestamp(data["t"] / 1000, tz=timezone.utc),
            "open": data["o"],
            "high": data["h"],
            "low": data["l"],
            "close": data["c"],
            "volume": data.get("v"),
        }

        with conn.cursor() as cur:
            upsert_bar(cur, bar)
            enforce_retention(cur, bar["ticker"], 5000)

    def on_error(ws, err):
        print("WS error:", err)

    def on_close(ws, code, reason):
        print("WS closed:", code, reason)

    ws = WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header=[f"Authorization: Bearer {API_KEY}"],  # ggf. anders laut Doku
    )

    # Blocking run; SparkApplication bleibt aktiv
    while True:
        ws.run_forever(ping_interval=20, ping_timeout=10)
        time.sleep(5)

if __name__ == "__main__":
    main()
