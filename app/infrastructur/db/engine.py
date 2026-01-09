#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 16:01:09 2026

@author: twi
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import current_app

def make_session_factory():
    engine = create_engine(current_app.config["DATABASE_URL"], pool_pre_ping=True)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
