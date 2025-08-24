# backend/app/main.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from .agent import run_diagnostics as run_agent
from .troubleshooter_api import router as troubleshooter_router

app = FastAPI(
    title="Networking Troubleshooter Agent",
    description="AI-powered agent for DNS, SSL, HTTP, Ping, and GeoIP diagnostics with AgentHack 2025 frontend-backend troubleshooting.",
    version="1.0.0"
)

# Include the troubleshooter router
app.include_router(troubleshooter_router)

# Allow frontend (React/Vite dev server + any deployed origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Networking Troubleshooter Agent is running 🚀"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "networking-troubleshooter-backend"}


from typing import Any, Dict

@app.get("/diagnose")
async def diagnose(
    url: str = Query(..., description="Domain or IP to check"),
    mode: str = Query("beginner", description="Explanation mode: beginner or expert")
) -> Dict[str, Any]:
    """
    Runs the troubleshooting agent against the given URL or IP.
    - url: The domain/IP to check (example: example.com)
    - mode: beginner (simplified) | expert (technical)
    """
    try:
        result = run_agent(url, mode)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
