from datetime import datetime
from typing import Dict, Any
from jinja2 import Template

_TMPL = Template(
    """
# Networking Troubleshooter Report

**Target:** {{ target }}  
**Generated (UTC):** {{ ts }}  
**Health Score:** {{ score }}/100

---

## Summary
{{ summary }}

## Fix Suggestions
{% if fixes %}
{% for f in fixes %}- {{ f }}
{% endfor %}
{% else %}
- No immediate actions suggested.
{% endif %}

## Key Results
- DNS: {{ r.dns }}
- Ping: {{ r.ping }}
- SSL: {{ r.ssl }}
- HTTP: {{ r.http }}
{% if r.geoip %}- GeoIP: {{ r.geoip }}{% endif %}
{% if r.traceroute %}- Traceroute captured (see logs){% endif %}
"""
)

def to_markdown(payload: Dict[str, Any]) -> str:
    ts = datetime.utcnow().isoformat() + "Z"
    return _TMPL.render(
        target=payload.get("target"),
        ts=ts,
        score=payload.get("health_score", 0),
        summary=payload.get("summary", ""),
        fixes=payload.get("fix_suggestions", []),
        r=payload.get("results", {}),
    )