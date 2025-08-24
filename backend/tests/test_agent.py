# tests/test_agent.py
from app.agent import run_diagnostics

def test_agent_pipeline():
    results = run_diagnostics("example.com", mode="beginner")
    assert isinstance(results, dict)
    assert "dns" in results
    assert "ssl" in results
    assert "http" in results
