#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 16:01:09 2026

@author: twi
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def make_engine(database_url: str):
    return create_engine(database_url, pool_pre_ping=True)

def make_session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
