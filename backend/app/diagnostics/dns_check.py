import socket
from typing import Dict, Any

def normalize_target(target: str) -> str:
    if target.startswith("http://") or target.startswith("https://"):
        target = target.split("//", 1)[1]
    return target.split("/", 1)[0]


def dns_resolution(target: str) -> Dict[str, Any]:
    host = normalize_target(target)
    try:
        ip = socket.gethostbyname(host)
        return {"ok": True, "host": host, "ip": ip}
    except Exception as e:
        return {"ok": False, "host": host, "error": str(e)}