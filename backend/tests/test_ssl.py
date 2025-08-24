# tests/test_ssl
from app.diagnostics import ssl_check

def test_ssl_example():
    result = ssl_check.ssl_certificate_check("example.com")
    assert "valid" in result
    assert "issuer" in result
