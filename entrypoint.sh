#!/bin/sh
alembic upgrade head
python seed.py
uvicorn app.main:app --host 0.0.0.0 --port 8000