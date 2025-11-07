#!/usr/bin/env bash
# Development server startup script

echo "Starting BonoAI FastAPI backend..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level info
