#!/bin/bash

# AgentHack 2025 Networking Fix Script

# Fix: Frontend Server
cd frontend
npm run dev

# Fix: Backend Server
cd backend
python -m uvicorn app.main:app --reload --port 8000
