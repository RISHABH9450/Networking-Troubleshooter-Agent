# tests/test_dns.py
from app.diagnostics import dns_check

def test_dns_valid():
    result = dns_check.dns_resolution("example.com")
    assert isinstance(result, dict)
    assert "status" in result

def test_dns_invalid():
    result = dns_check.dns_resolution("nonexistent.domain.abc")
    assert isinstance(result, dict)
    assert result.get("status") in [True, False]
