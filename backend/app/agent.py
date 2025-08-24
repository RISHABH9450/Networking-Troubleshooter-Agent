# agent.py
from typing import Any, Dict, Mapping

from .diagnostics import dns_check, ssl_check, http_check, ping_check, geoip_check
from .utils import explain


def run_diagnostics(domain: str, mode: str = "beginner") -> Dict[str, Any]:
    """
    Run all networking diagnostic checks and return both raw and explained results.

    Args:
        domain (str): The domain/URL to test.
        mode (str): "beginner" or "expert" — decides explanation detail.

    Returns:
        dict: {
            "raw": { ... all raw outputs ... },
            "explained": { ... simplified explanations ... }
        }
    """

    # Collect raw results
    raw_results: Mapping[str, Any] = {
        "dns": dns_check.dns_resolution(domain),
        "ssl": ssl_check.ssl_certificate_check(domain),
        "http": http_check.http_check(domain),
        "ping": ping_check.ping_host(domain),
        "geoip": geoip_check.geoip_lookup(domain),
    }

    # Explain results in human-friendly format
    explained: Dict[str, Any] = {
        "dns": explain.explain_dns(raw_results["dns"], mode),
        "ssl": explain.explain_ssl(raw_results["ssl"], mode),
        "http": explain.explain_http(raw_results["http"], mode),
        "ping": explain.explain_ping(raw_results["ping"], mode),
        "geoip": explain.explain_geoip(raw_results["geoip"], mode),
    }

    return {"raw": raw_results, "explained": explained}
