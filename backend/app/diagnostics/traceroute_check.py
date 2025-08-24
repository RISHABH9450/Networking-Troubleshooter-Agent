import platform, subprocess, shlex
from typing import Dict, Any
from app.diagnostics.dns_check import normalize_target


def traceroute_run(target: str) -> Dict[str, Any]:
    host = normalize_target(target)
    is_windows = platform.system().lower() == "windows"
    cmd = f"tracert -d -h 15 {shlex.quote(host)}" if is_windows else f"traceroute -n -m 15 {shlex.quote(host)}"
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
        ok = proc.returncode == 0 or (proc.stdout and "traceroute" in proc.stdout.lower())
        # Limit output to last ~50 lines to avoid bloat
        lines = proc.stdout.splitlines()[-50:]
        return {"ok": ok, "host": host, "raw": "\n".join(lines)}
    except Exception as e:
        return {"ok": False, "host": host, "error": str(e)}