#!/usr/bin/env python3
"""Status line: mo hinh | repo@nhanh | % ngu canh (canh bao theo nguong) | effort.

Khong ton token API. Nguong mau: <70% xanh, 70-89% vang, >=90% do (nen /clear hoac /compact).
"""
import json
import os
import subprocess
import sys

try:
    d = json.load(sys.stdin)
except Exception:
    d = {}

model = (d.get("model") or {}).get("display_name") or "?"
cwd = (d.get("workspace") or {}).get("current_dir") or d.get("cwd") or os.getcwd()
try:
    branch = subprocess.run(["git", "-C", cwd, "branch", "--show-current"],
                            capture_output=True, text=True, timeout=1).stdout.strip()
except Exception:
    branch = ""

cw = d.get("context_window") or {}
pct = cw.get("used_percentage")
used = None
cu = cw.get("current_usage") or {}
if cu:
    used = sum(int(cu.get(k) or 0) for k in
               ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))

# % tinh theo ngan sach nen (autoCompactWindow), khong theo cua so 1M cua mo hinh
budget = 300000
try:  # mot nguon su that: autoCompactWindow trong settings.json
    budget = int(json.load(open(os.path.expanduser("~/.claude/settings.json"))).get("autoCompactWindow") or budget)
except Exception:
    pass
if used:
    pct = used * 100.0 / budget  # khong cat o 100%: >100% nghia la phien chua nen theo nguong moi

parts = [f"\033[1m{model}\033[0m", os.path.basename(cwd) + (f"@{branch}" if branch else "")]
if pct is not None:
    pct = float(pct)
    color = "32" if pct < 70 else ("33" if pct < 90 else "31")
    txt = f"ctx {pct:.0f}%"
    if used:
        txt += f" ({used // 1000}k/{budget // 1000}k)"
    if pct > 100:
        txt += " VUOT NGUONG: /compact ngay (phien mo truoc khi doi cau hinh?)"
    elif pct >= 90:
        txt += " -> sap tu nen; xong Phase thi /clear"
    parts.append(f"\033[{color}m{txt}\033[0m")
eff = d.get("effort") or (d.get("model") or {}).get("effort")
if isinstance(eff, str):
    parts.append(f"effort {eff}")
print(" | ".join(parts))
