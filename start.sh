#!/usr/bin/env bash
# Script de arranque para Render / Railway
exec python -m uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
