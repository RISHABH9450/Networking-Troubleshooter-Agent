# utils/explain.py
"""
Maps raw diagnostic results to Beginner-friendly and Expert-friendly explanations.
"""

from typing import Dict, Any

def explain_dns(result: Dict[str, Any], mode: str = "beginner") -> str:
    if mode == "beginner":
        return "✅ DNS looks fine!" if result.get("status") else "❌ DNS resolution failed."
    return f"Queried {result.get('server')} → {result.get('ip', 'N/A')}, status={result.get('status')}"

def explain_ssl(result: Dict[str, Any], mode: str = "beginner") -> str:
    if mode == "beginner":
        return "🔒 SSL is valid!" if result.get("valid") else "⚠️ SSL certificate is invalid or expired."
    return f"Issuer={result.get('issuer')}, Expiry={result.get('expiry')}, Valid={result.get('valid')}"

def explain_http(result: Dict[str, Any], mode: str = "beginner") -> str:
    if mode == "beginner":
        return "🌐 Website is reachable." if result.get("status_code") == 200 else "⚠️ Website not reachable."
    return f"Status={result.get('status_code')}, Headers={result.get('headers',{})}"

def explain_ping(result: Dict[str, Any], mode: str = "beginner") -> str:
    if mode == "beginner":
        return f"📶 Ping {result.get('host')} is reachable." if result.get("reachable") else f"❌ Cannot reach {result.get('host')}"
    return f"RTT={result.get('rtt_ms')}ms, PacketLoss={result.get('loss_percent')}%"

def explain_geoip(result: Dict[str, Any], mode: str = "beginner") -> str:
    if mode == "beginner":
        return f"🌍 Server is located in {result.get('country')}, {result.get('city')}."
    return f"IP={result.get('ip')}, ASN={result.get('asn')}, Location={result.get('country')}/{result.get('city')}"
