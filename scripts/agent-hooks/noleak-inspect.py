#!/usr/bin/env python3
"""Kiem tra AN TOAN tep bi mat: chi in ten khoa + sieu du lieu, KHONG BAO GIO in gia tri.

Dung: python3 ~/.claude/hooks/noleak-inspect.py <tep> [<tep>...]
Ma thoat: 0 = tat ca tep dung dinh dang; 3 = co tep RAW_TOKEN/MIXED_RAW (HARD STOP, bao chu du an).
"""
import sys; sys.dont_write_bytecode = True  # khong sinh __pycache__
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from noleaklib import STOP_MSG, inspect_file  # noqa: E402


def to_env(var, path):
    """Doi tep RAW_TOKEN 1 dong thanh `VAR='gia_tri'` tai cho. Chi CHU DU AN uy quyen moi chay.

    Khong in gia tri. Kiem chung: nap lai bang bash, so sha256 gia tri cu/moi.
    """
    import hashlib
    import re
    import subprocess
    import tempfile
    if not re.fullmatch(r"[A-Z_][A-Z0-9_]*", var):
        print(f"   ten bien khong hop le: {var}")
        return 2
    p = os.path.expanduser(path)
    r = inspect_file(p)
    if r.get("format") != "RAW_TOKEN" or r.get("content_lines") != 1:
        print(f"   bo qua {path}: chi doi tep RAW_TOKEN dung 1 dong (hien: {r.get('format')}, {r.get('content_lines')} dong)")
        return 2
    with open(p, encoding="utf-8") as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    val = lines[0].rstrip("\r\n")
    h0 = hashlib.sha256(val.encode()).hexdigest()
    quoted = val if re.fullmatch(r"[A-Za-z0-9_./:@%+-]+", val) else "'" + val.replace("'", "'\\''") + "'"
    st = os.stat(p)
    d = os.path.dirname(p)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".noleak-")
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(f"{var}={quoted}\n")
        chk = subprocess.run(["bash", "-c", f'set -a; . "$1"; set +a; printf %s "${{{var}}}" | sha256sum', "_", tmp],
                             capture_output=True, text=True, timeout=10)
        h1 = chk.stdout.split()[0] if chk.stdout else ""
        if chk.returncode != 0 or h1 != h0:
            os.unlink(tmp)
            print(f"   THAT BAI {path}: nap lai khong khop (giu nguyen tep cu)")
            return 1
        os.replace(tmp, p)
        os.chmod(p, 0o600)
    except Exception as e:  # noqa: BLE001
        if os.path.exists(tmp):
            os.unlink(tmp)
        print(f"   THAT BAI {path}: {type(e).__name__}")
        return 1
    print(f"   da doi {path} -> {var}=... (quyen 600, nap lai khop sha256; quyen cu {oct(st.st_mode & 0o777)})")
    return 0


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    if argv[0] == "--to-env" and len(argv) == 3:
        return to_env(argv[1], argv[2])
    rc = 0
    for p in argv:
        r = inspect_file(os.path.expanduser(p))
        print(f"== {p}")
        if not r.get("exists"):
            print("   khong ton tai")
            continue
        if "size" not in r:
            print("   la thu muc")
            continue
        perm = r["mode"] + (" (CANH BAO: nhom/nguoi khac doc duoc - nen chmod 600)" if r["group_or_world_readable"] else "")
        print(f"   kich thuoc {r['size']} byte, quyen {perm}, dinh dang: {r.get('format', '?')}")
        for item in r.get("keys") or []:
            if isinstance(item, (tuple, list)) and len(item) == 2:
                print(f"   - {item[0]}: {item[1]}")
            else:
                print(f"   - {item}")  # khoa JSON cap 1: chi ten
        if r.get("format") in ("RAW_TOKEN", "MIXED_RAW"):
            lines = ",".join(map(str, r.get("raw_line_numbers", [])))
            print("   " + STOP_MSG.format(path=p, lines=lines))
            rc = 3
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
