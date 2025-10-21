#!/usr/bin/env bash
# Script de arranque para Render
cd app
exec uvicorn main:app --host 0.0.0.0 --port $PORT
