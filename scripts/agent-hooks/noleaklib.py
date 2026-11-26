"""Thu vien dung chung cho noleak-guard.py va noleak-inspect.py.

Quy tac Zero Secret Exposure (chu du an 26/11/2026). Module nay KHONG BAO GIO tra ve
hay in gia tri bi mat: chi ten khoa, do dai, loai, so dong.
"""
import os
import re

HOME = os.path.expanduser("~")

# Duoi tep la tai lieu/mau/ma nguon: ten chua "token"/"secret" van KHONG coi la tep bi mat.
SAFE_SUFFIX = re.compile(
    r"\.(md|mdx|rst|adoc|html?|css|scss|ts|tsx|js|jsx|mjs|cjs|py|dart|rs|go|cs|java|kt|swift|"
    r"c|cc|cpp|h|hpp|rb|php|sh|ps1|sql|vue|svelte|astro|xml|arb|lock|snap|golden|png|svg|pub)$", re.I)
TEMPLATE = re.compile(r"\.(example|sample|template|dist|defaults|schema)(\.[a-z]+)?$", re.I)

SECRET_BASENAME = re.compile(
    r"^(\.env(\..+)?|[^/]+\.env(\.[^/]+)?|\.envrc|.*\.jwk|\.dev\.vars(\..+)?|\.npmrc|\.pypirc|\.netrc|\.git-credentials|\.credentials\.json|"
    r"credentials(\.json|\.toml|\.ya?ml)?|hosts\.ya?ml|key\.properties|rclone\.conf|"
    r"id_(rsa|dsa|ecdsa|ed25519)(_[\w-]+)?|.*\.(pem|key|p12|pfx|jks|keystore|p8|ppk|gpg|kdbx|secret|secrets)(\.b64|\.base64)?|"
    r"service[-_]?account.*\.json|.*(token|secrets?|passwd|password|apikey|api[-_]key|credentials?)(\.[\w]+)?)$",
    re.I)

SECRET_DIR_PARTS = (
    "/.ssh/", "/.config/gh/", "/.aws/", "/.config/.wrangler/", "/.wrangler/config/", "/.docker/config",
    "/.kube/", "/.gnupg/", "/.config/tsudev/", "/secrets-local/", "/.config/gcloud/", "/.azure/", "/.android/", "/.secrets/",
)
DIR_SAFE = re.compile(r"(\.pub|known_hosts(\.old)?|/\.ssh/config|authorized_keys)$")


def is_secret_path(p: str) -> bool:
    if not p:
        return False
    p = p.strip().strip("'\"")
    p = os.path.expanduser(p.replace("$HOME", HOME))
    base = os.path.basename(p.rstrip("/"))
    if not base or TEMPLATE.search(base) or base.endswith(".pub"):
        return False
    if "/ephemeral/" in p or base == "flutter_native_integration.env":
        return False  # tep build Flutter tu sinh
    if re.search(r"(^|[-_.])pub(lic)?([-_.]|$)", base, re.I) and re.search(r"\.(jwk|pem|key|asc)$", base, re.I):
        return False  # khoa CONG KHAI
    norm = "/" + p.lstrip("/")
    if any(d in norm for d in SECRET_DIR_PARTS) and not DIR_SAFE.search(norm):
        return True
    if SAFE_SUFFIX.search(base):
        return False
    return bool(SECRET_BASENAME.match(base))


# Chuoi bi mat do tin cay cao (dung de quet output va noi dung sap ghi).
HIGH_CONF = [
    ("GitHub token", r"\b(gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})"),
    ("Anthropic key", r"\bsk-ant-[A-Za-z0-9_-]{20,}"),
    ("OpenAI key", r"\bsk-(proj|svcacct|admin)-[A-Za-z0-9_-]{40,}|\bsk-[A-Za-z0-9]{20}T3BlbkFJ[A-Za-z0-9]{20}"),
    ("AWS access key", r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("Google API key", r"\bAIza[0-9A-Za-z_-]{35}\b"),
    ("Google OAuth secret", r"\bGOCSPX-[A-Za-z0-9_-]{20,}"),
    ("Slack token", r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    ("Stripe key", r"\b(sk|rk)_live_[0-9a-zA-Z]{20,}"),
    ("npm token", r"\bnpm_[A-Za-z0-9]{36}\b"),
    ("Resend key", r"\bre_[A-Za-z0-9]{8,}_[A-Za-z0-9]{16,}"),
    ("Private key", r"-----BEGIN (RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY( BLOCK)?-----\s*(\\n)?[A-Za-z0-9+/=]{60,}"),
    ("JWT", r"\beyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{20,}"),
    ("Cloudflare token", r"(?i)\b(CF|CLOUDFLARE)_API_TOKEN\s*[=:]\s*['\"]?[A-Za-z0-9_-]{40}\b"),
    ("Gan gia tri bi mat", r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|PASSWD|API_KEY|PRIVATE_KEY|CLIENT_SECRET)\s*[=:]\s*['\"]?"
                           r"(?![A-Za-z_]*\$|\$\{?|<|\*{3}|x{6}|your|changeme|example|placeholder|redacted|dummy|test|fake|null|none|true|false)"
                           r"(?![A-Za-z_][\w]*\.[A-Za-z_])(?=[A-Za-z0-9/+_.=-]*\d)[A-Za-z0-9/+_.=-]{24,}"),
]
HIGH_CONF_RE = [(n, re.compile(r)) for n, r in HIGH_CONF]


GENERIC = "Gan gia tri bi mat"


def find_secrets(text: str, generic: bool = False):
    """Tra ve danh sach (loai, so lan) - KHONG tra ve chuoi khop.

    generic=False: chi mau dang khoa that cua nha cung cap (dung cho output, ghi tep).
    generic=True: them mau `TEN_SECRET=gia_tri_dai` (dung cho commit/PR - test gia hay khop mau nay).
    """
    out = []
    for name, rx in HIGH_CONF_RE:
        if name == GENERIC and not generic:
            continue
        n = len(rx.findall(text))
        if n:
            out.append((name, n))
    return out


KEY_RE = re.compile(r"^\s*(export\s+)?([A-Za-z_][A-Za-z0-9_.-]*)\s*=")
YAML_RE = re.compile(r"^\s*-?\s*([A-Za-z_][\w.-]*)\s*:(\s|$)")
INI_RE = re.compile(r"^\s*\[[^\]]+\]\s*$")


def inspect_file(path: str) -> dict:
    """Siêu dữ liệu an toàn của tệp bí mật. Không bao giờ chứa giá trị."""
    r = {"path": path, "exists": os.path.exists(path)}
    if not r["exists"] or os.path.isdir(path):
        return r
    st = os.stat(path)
    r["size"] = st.st_size
    r["mode"] = oct(st.st_mode & 0o777)
    r["group_or_world_readable"] = bool(st.st_mode & 0o077)
    try:
        with open(path, "rb") as f:
            data = f.read(1_000_000)
    except Exception as e:  # noqa: BLE001
        r["error"] = type(e).__name__
        return r
    if b"\x00" in data[:4096]:
        r["format"] = "binary"
        return r
    text = data.decode("utf-8", "replace")
    if "PRIVATE KEY" in text and "-----BEGIN" in text:
        r["format"] = "pem-private-key"
        return r
    keys, raw_lines, n = [], [], 0
    fmt = None
    stripped = text.lstrip()
    if stripped.startswith("{"):
        import json
        try:
            obj = json.loads(text)
            r["format"] = "json"
            r["keys"] = sorted(obj.keys()) if isinstance(obj, dict) else []
            return r
        except Exception:
            pass
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(";") or s.startswith("//"):
            continue
        n += 1
        m = KEY_RE.match(line)
        if m:
            fmt = fmt or "KEY=VALUE"
            val = line.split("=", 1)[1].strip().strip("'\"")
            keys.append((m.group(2), "rong" if not val else f"co gia tri, dai {len(val)}"))
            continue
        m = YAML_RE.match(line)
        if m:
            fmt = fmt or "yaml/toml"
            keys.append((m.group(1), "-"))
            continue
        if INI_RE.match(line):
            continue
        raw_lines.append(i)
    r["content_lines"] = n
    r["keys"] = keys
    if raw_lines:
        r["format"] = "RAW_TOKEN" if not keys else "MIXED_RAW"
        r["raw_line_numbers"] = raw_lines[:20]
    else:
        r["format"] = fmt or "empty"
    return r


def is_raw(path: str) -> bool:
    try:
        return inspect_file(path).get("format") in ("RAW_TOKEN", "MIXED_RAW")
    except Exception:
        return False


STOP_MSG = (
    "HARD STOP - tep bi mat KHONG dung dinh dang KEY=VALUE: `{path}` (dong {lines}). "
    "Theo quy tac Zero Secret Exposure: DUNG moi thao tac doc/su dung token trong tep nay, KHONG in noi dung, "
    "KHONG thu cach doc khac. BAO NGAY cho chu du an: duong dan tep + 'thieu dinh dang KEY=VALUE' de chu du an "
    "tu sua thanh `TEN_BIEN=gia_tri`."
)
