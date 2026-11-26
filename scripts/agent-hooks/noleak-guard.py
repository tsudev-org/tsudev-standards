#!/usr/bin/env python3
"""Hook Zero Secret Exposure (chu du an 26/11/2026) - ap cho MOI phien, subagent, `claude -p` tren may.

PreToolUse  (Bash|Read|Grep|Write|Edit|MultiEdit|NotebookEdit): tu choi lenh/thao tac co the in hoac ghi gia tri bi mat.
PostToolUse (moi cong cu): output lo chuoi giong bi mat -> buoc agent dung, khong lap lai, bao chu du an.
Loi noi bo cua hook: im lang cho qua (khong lam hong phien) - lop quy tac trong CLAUDE.md van ap dung.
"""
import sys; sys.dont_write_bytecode = True  # khong sinh __pycache__
import json
import os
import re
import shlex
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from noleaklib import STOP_MSG, find_secrets, inspect_file, is_secret_path  # noqa: E402

INSPECT = "python3 ~/.claude/hooks/noleak-inspect.py <tep>"
READERS = {
    "cat", "tac", "head", "tail", "less", "more", "bat", "batcat", "nl", "strings", "xxd", "od", "hexdump",
    "base64", "base32", "cut", "awk", "gawk", "mawk", "sed", "sort", "uniq", "tr", "paste", "column", "jq", "yq",
    "fold", "rev", "diff", "sdiff", "vimdiff", "tee", "dd", "pr", "fmt", "expand", "iconv", "envsubst", "openssl",
}
GREPS = {"grep", "egrep", "fgrep", "rg", "ag", "ack", "zgrep"}
SECRET_VAR = re.compile(r"(?i)^(?!(OLD)?PWD$)[A-Z0-9_]*(TOKEN|SECRET|PASS(WORD|WD)?|API_?KEY|PRIVATE|CREDENTIAL|"
                        r"AUTH|COOKIE|SESSION|SIGNING|_KEY|KEY_)[A-Z0-9_]*$")


def deny(reason, event="PreToolUse"):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "permissionDecision": "deny",
                                             "permissionDecisionReason": "[Zero Secret Exposure] " + reason}},
                     ensure_ascii=False))
    sys.exit(0)


def segments(cmd):
    """Tach lenh thanh cac doan don (|, ;, &&, ||, xuong dong, $(...), `...`)."""
    parts = [cmd]
    parts += re.findall(r"\$\(([^()]*)\)", cmd)
    parts += re.findall(r"`([^`]*)`", cmd)
    out = []
    for p in parts:
        out += [s for s in re.split(r"\|\||&&|[|;\n]|\$\(|\)|`", p) if s.strip()]
    return out


def words(seg):
    try:
        w = shlex.split(seg, posix=True)
    except ValueError:
        w = seg.split()
    while w and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", w[0]) or w[0] in ("sudo", "command", "builtin", "exec",
                                                                         "nohup", "time", "xargs", "env")):
        if w[0] == "env" and len(w) == 1:
            break
        w = w[1:]
    return w


HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1[^\n]*\n(.*?)\n\s*\2\s*(?=\n|$)", re.S)


def strip_heredocs(c):
    """Bo than heredoc (du lieu/van ban/ma cho python...) - tru khi heredoc dua vao shell de thuc thi."""
    def rep(m):
        line_start = c.rfind("\n", 0, m.start()) + 1
        head = c[line_start:m.start()]
        if re.search(r"(^|[\s|;&(])(ba|z|da|k)?sh(\s+-\w+)*\s*$", head):
            return m.group(0)
        return "<<HEREDOC\n"
    return HEREDOC.sub(rep, c)


def check_bash(cmd):
    raw = cmd.strip()
    c = strip_heredocs(raw)
    # 1) Do toan bo moi truong
    for seg in segments(c):
        w = words(seg)
        if not w:
            continue
        head = os.path.basename(w[0])
        if head in ("printenv",) or (head == "env" and len(w) == 1) or (head == "export" and w[1:2] == ["-p"]) \
                or (head == "declare" and any(a in ("-p", "-x", "-px", "-xp") for a in w[1:])) \
                or (head == "set" and len(w) == 1) or (head == "compgen" and "-e" in w and "-v" not in w):
            deny(f"`{head}` in gia tri bien moi truong. Chi xem TEN bien: `compgen -v | grep -i <tu>` hoac "
                 "`[ -n \"$TEN\" ] && echo co || echo khong`.")
        # 2) echo/printf gia tri bien bi mat
        if head in ("echo", "printf", "print"):
            for m in re.finditer(r"\$\{?(#?)([A-Za-z_][A-Za-z0-9_]*)(:?[+]?)", seg):
                if m.group(1) == "#" or "+" in m.group(3):
                    continue  # ${#X} (do dai) va ${X:+co} an toan
                if SECRET_VAR.match(m.group(2)):
                    deny(f"`{head}` se in gia tri bien `{m.group(2)}`. Kiem tra an toan: "
                         f"`[ -n \"${m.group(2)}\" ] && echo \"{m.group(2)}: co, dai ${{#{m.group(2)}}}\"`.")
        # 3) Lenh lo token truc tiep
        if head == "gh" and w[1:3] == ["auth", "token"] and seg.strip() == c and "$(" not in c:
            deny("`gh auth token` in token ra man hinh. Chi dung trong thay the lenh: `GH_TOKEN=$(gh auth token) <lenh>`.")
        if head == "gh" and w[1:3] == ["auth", "status"] and any(a in ("-t", "--show-token") for a in w):
            deny("`gh auth status --show-token` in token. Dung `gh auth status` (khong co -t).")
        if head == "git" and ("credential" in w[1:3] and ("fill" in w or "get" in w)):
            deny("`git credential fill/get` in mat khau/token.")
        if head == "cloudflared" and "token" in w:
            deny("`cloudflared tunnel token` in token cua tunnel.")
        if head == "curl" and any(a in ("-v", "--verbose", "--trace", "--trace-ascii") or re.match(r"^-[a-zA-Z]*v", a)
                                  for a in w[1:]) and re.search(r"(?i)authorization|bearer|-u\s|--user|token|api[-_]?key", seg):
            deny("`curl -v/--trace` kem thong tin xac thuc se in header Authorization. Bo -v hoac dung `-sS -o /dev/null -w '%{http_code}'`.")
        # 4) Doc tep bi mat
        targets = []
        skip = set()
        if head in GREPS and "-e" not in w and "-f" not in w:
            for i, a in enumerate(w[1:], 1):  # doi so dau khong phai co la MAU tim, khong phai tep
                if not a.startswith("-"):
                    skip.add(i)
                    break
        for i, a in enumerate(w[1:], 1):
            if i in skip:
                continue
            a2 = a.lstrip("<")
            if is_secret_path(a2):
                prev = w[i - 1] if i - 1 >= 0 else ""
                if prev.endswith(">") or a.startswith(">"):
                    continue  # ghi vao tep (>), khong phai doc
                targets.append(a2)
        for m in re.finditer(r"(?<![>&0-9])<\s*([^\s<>|;&]+)", seg):
            if is_secret_path(m.group(1)):
                targets.append(m.group(1))
        if not targets:
            continue
        t0 = targets[0]
        full = os.path.expanduser(t0)
        if head in ("source", ".") or "--env-file" in seg or "env-file" in seg:
            if os.path.isfile(full) and inspect_file(full).get("format") in ("RAW_TOKEN", "MIXED_RAW"):
                r = inspect_file(full)
                deny(STOP_MSG.format(path=t0, lines=",".join(map(str, r.get("raw_line_numbers", [])))))
            continue  # nap bien vao moi truong khong in gia tri
        if head in READERS or head.startswith("python") or head in ("node", "ruby", "perl", "php", "deno", "bun"):
            if head.startswith("python") and "noleak-inspect.py" in seg:
                continue
            extra = ""
            if os.path.isfile(full) and inspect_file(full).get("format") in ("RAW_TOKEN", "MIXED_RAW"):
                extra = " " + STOP_MSG.format(path=t0, lines=",".join(map(str, inspect_file(full).get("raw_line_numbers", []))))
            deny(f"`{head}` doc noi dung tep bi mat `{t0}` co the in gia tri raw (ke ca `cut -d= -f1` khi tep khong "
                 f"co dau =). Chi xem ten khoa/sieu du lieu: `{INSPECT}`. Can dung gia tri: `set -a; . <tep>; set +a` "
                 f"roi dung bien, khong in.{extra}")
        if head in GREPS:
            if any(re.match(r"^-[a-zA-Z]*[qlLc]", a) or a in ("--quiet", "--files-with-matches", "--count", "--silent")
                   for a in w[1:]):
                continue
            deny(f"`{head}` tren tep bi mat `{t0}` in ca dong (gom gia tri). Dung `{head} -q`/`-c`/`-l`, "
                 f"hoac `{INSPECT}`.")
    # 5) Commit/PR/release chua chuoi bi mat
    if re.search(r"\b(git\s+commit|gh\s+(pr|issue|release)\s+(create|edit|comment)|gh\s+api)\b", raw):
        hits = find_secrets(raw, generic=True)
        if hits:
            deny("noi dung commit/PR/issue/release chua chuoi giong bi mat (" + ", ".join(h[0] for h in hits) + "). Go bo truoc.")


def check_file_tool(tool, ti):
    p = ti.get("file_path") or ti.get("notebook_path") or ti.get("path") or ""
    if tool == "Read" and is_secret_path(p):
        extra = ""
        if os.path.isfile(os.path.expanduser(p)) and inspect_file(os.path.expanduser(p)).get("format") in ("RAW_TOKEN", "MIXED_RAW"):
            r = inspect_file(os.path.expanduser(p))
            extra = " " + STOP_MSG.format(path=p, lines=",".join(map(str, r.get("raw_line_numbers", []))))
        deny(f"Read se dua gia tri bi mat cua `{p}` vao ngu canh. Dung `{INSPECT}` (chi ten khoa).{extra}")
    if tool == "Grep":
        mode = ti.get("output_mode", "files_with_matches")
        tgt = (ti.get("path") or "") + " " + (ti.get("glob") or "")
        if mode == "content" and (is_secret_path(ti.get("path") or "") or re.search(r"\.env|\.dev\.vars|secret|token|\.pem|\.key", ti.get("glob") or "", re.I)):
            deny(f"Grep che do content tren tep bi mat ({tgt.strip()}) in gia tri. Dung output_mode files_with_matches/count.")
    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        content = json.dumps({k: v for k, v in ti.items() if k not in ("file_path", "notebook_path")}, ensure_ascii=False)
        hits = find_secrets(content)
        if hits and not is_secret_path(p):
            deny(f"Dang ghi chuoi giong bi mat ({', '.join(h[0] for h in hits)}) vao `{p}` - tep khong phai tep bi mat "
                 "(co the bi commit/chia se). Dung bien moi truong/tep .env da gitignore; neu la du lieu gia trong test, "
                 "dung gia tri ro rang la gia (vd. `test-token-not-real`).")


def post(data):
    resp = data.get("tool_response")
    try:
        text = resp if isinstance(resp, str) else json.dumps(resp, ensure_ascii=False)
    except Exception:
        return
    hits = find_secrets(text or "")
    if not hits:
        return
    kinds = ", ".join(f"{k} x{n}" for k, n in hits)
    msg = ("[Zero Secret Exposure - HARD STOP] Output cong cu vua roi co chuoi giong bi mat: " + kinds + ". "
           "MUST: (1) KHONG lap lai, trich dan, tom tat hay ghi chuoi do vao tep/commit/PR/bao cao/AKB; "
           "(2) dung cach lam da gay ra output nay; (3) bao chu du an NGAY: cong cu + lenh/tep nguon + loai bi mat "
           "(khong kem gia tri) va de nghi thu hoi/xoay khoa neu la khoa that. Neu chac chan la du lieu gia (test/fixture) "
           "thi noi ro ly do va tiep tuc.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}}, ensure_ascii=False))


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    ev = data.get("hook_event_name", "")
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    if ev == "PostToolUse":
        post(data)
        return
    if tool == "Bash":
        check_bash(ti.get("command", ""))
    else:
        check_file_tool(tool, ti)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        pass
    sys.exit(0)
