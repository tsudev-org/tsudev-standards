#!/usr/bin/env python3
"""SessionStart hook (startup|clear|compact|resume): nap lai vi tri Phase dang lam.

Doc stdin JSON cua Claude Code, tim git root tu cwd, quet docs/PLAN*.md tim Phase
dau tien con muc `- [ ]`, in ra vai dong ngu canh ngan (stdout = additionalContext).
Khong bao gio lam hong phien: moi loi deu im lang, exit 0.
"""
import glob
import json
import os
import re
import subprocess
import sys


def git(cwd, *args):
    try:
        return subprocess.run(["git", "-C", cwd, *args], capture_output=True,
                              text=True, timeout=3).stdout.strip()
    except Exception:
        return ""


def first_open_phase(path):
    heading, open_count, first_item = None, 0, None
    current, found = None, None
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return None
    for line in lines:
        if re.match(r"^#{2,3}\s", line):
            current = line.strip("# \n")
            if found is None and re.search(r"🔄|⬜", line):  # kieu emoji (tsuswico)
                found, first_item = current, "(xem muc ⬜/🔄 duoi tieu de)"
        m = re.match(r"^\s*[-*]\s+(?:\[ \]|⬜|🔄)\s+(.*)", line)
        if m:
            if found is None:
                found = current or "(khong co tieu de)"
                first_item = m.group(1).strip()
            if current == found:
                open_count += 1
    if found is None:
        return None
    return found, open_count, first_item


def security_audit(root):
    """SECURITY_BASELINE 12.2: tu siet quyen tep bi mat (600), canh bao token tho / tep bi mat bi git theo doi,
    nhac phieu xoay khoa (logs/handover/*-XK*) con MO. Khong bao gio in gia tri."""
    lines = []
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        sys.dont_write_bytecode = True
        from noleaklib import inspect_file, is_secret_path
    except Exception:
        return lines
    for t in sorted(glob.glob(os.path.join(root, "logs", "handover", "*-XK*.md"))):
        try:
            head = open(t, encoding="utf-8").read(1500)
        except Exception:
            continue
        if re.search(r"Trạng thái\**:\**\s*(MỞ|ĐANG)", head):
            lines.append(f"- ⚠ PHIEU XOAY KHOA DANG MO: `{os.path.relpath(t, root)}` - MUST nhac chu du an ngay dau phien "
                         "(xoay/thu hoi bi mat da lo) truoc khi lam task; KHONG doc/in gia tri.")
    if not os.path.isdir(os.path.join(root, ".git")) and not os.path.isfile(os.path.join(root, ".git")):
        return lines
    fixed, raw, tracked = [], [], []
    for f in git(root, "ls-files", "--others", "--ignored", "--exclude-standard", "--directory").splitlines()[:5000]:
        if not f or f.endswith("/"):
            continue
        p = os.path.join(root, f)
        if not is_secret_path(p) or not os.path.isfile(p) or os.path.islink(p):
            continue
        try:
            if os.stat(p).st_mode & 0o077:
                os.chmod(p, 0o600)
                fixed.append(f)
            if not p.endswith((".pem", ".p12", ".pfx", ".keystore", ".jks", ".gpg", ".key", ".b64", ".json", ".sql", ".sh")) \
                    and inspect_file(p).get("format") in ("RAW_TOKEN", "MIXED_RAW"):
                raw.append(f)
        except OSError:
            pass
    for f in git(root, "ls-files").splitlines():
        if f and is_secret_path(os.path.join(root, f)) and not f.endswith((".crt", ".cer")) \
                and not re.search(r"(^|/)\.env\.(production|development|staging|test)$", f) and "corpus" not in f:
            p = os.path.join(root, f)
            if f.endswith((".pem", ".key")) and inspect_file(p).get("format") != "pem-private-key":
                continue  # chung chi / khoa CONG KHAI
            if f.endswith(".gpg") and "keyring" in f:
                continue  # keyring cong khai (APT)
            tracked.append(f)
    if fixed:
        lines.append(f"- [12.2] Da tu chmod 600 {len(fixed)} tep bi mat bi mo quyen: {', '.join(fixed[:4])}")
    if raw:
        lines.append(f"- [12.1 HARD STOP] Tep bi mat KHONG theo KEY=VALUE: {', '.join(raw[:4])} - bao chu du an, khong doc.")
    if tracked:
        lines.append(f"- [12.2] Tep ten bi mat DANG bi git theo doi (kiem tra co phai bi mat that): {', '.join(tracked[:4])}"
                     + (f" (+{len(tracked) - 4})" if len(tracked) > 4 else ""))
    return lines


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    cwd = data.get("cwd") or os.getcwd()
    source = data.get("source", "")
    root = git(cwd, "rev-parse", "--show-toplevel") or cwd
    out = []

    plans = sorted(glob.glob(os.path.join(root, "docs", "PLAN*.md")))
    hit = False
    for p in plans:
        r = first_open_phase(p)
        if r:
            phase, n, item = r
            rel = os.path.relpath(p, root)
            out.append(f"- Ke hoach: `{rel}` - Phase dang mo: \"{phase}\" ({n} muc chua xong), muc ke: {item[:120]}")
            hit = True
            break
    if not hit and plans:
        rels = ", ".join(f"`{os.path.relpath(p, root)}`" for p in plans[:3])
        out.append(f"- Ke hoach: {rels} (khong co checklist `[ ]` - xem Phase dang lam trong STATE)")

    for s in ("logs/STATE.md", "STATE.md"):
        if os.path.isfile(os.path.join(root, s)):
            out.append(f"- Trang thai: `{s}`")
            break
    ho = sorted(glob.glob(os.path.join(root, "logs", "handover", "*.md")))
    if ho:
        out.append(f"- Phieu ban giao moi nhat: `{os.path.relpath(ho[-1], root)}`")

    out += security_audit(root)

    if not out and source == "startup":
        return  # repo khong theo quy trinh Phase: khong chen gi khi mo phien

    branch = git(root, "branch", "--show-current")
    dirty = git(root, "status", "--porcelain")
    head = [f"[Quy trinh Phase - nguon: {source or 'session'}] Repo `{os.path.basename(root)}`"
            + (f", nhanh `{branch}`" if branch else "")
            + (f", {len(dirty.splitlines())} tep chua commit" if dirty else "")]
    if source in ("clear", "compact"):
        head.append("- Ngu canh vua duoc lam sach/nen: KHONG dua vao lich su chat; doc lai cac tep duoi day (chi phan lien quan) roi lam tiep dung Phase dang mo.")
    print("\n".join(head + out))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
