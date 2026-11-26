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


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
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
        for k, meta in r.get("keys", []) if isinstance(r.get("keys"), list) else []:
            if isinstance(k, str) and meta is not None:
                print(f"   - {k}: {meta}")
            else:
                print(f"   - {k}")
        if r.get("format") in ("RAW_TOKEN", "MIXED_RAW"):
            lines = ",".join(map(str, r.get("raw_line_numbers", [])))
            print("   " + STOP_MSG.format(path=p, lines=lines))
            rc = 3
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
