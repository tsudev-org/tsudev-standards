#!/usr/bin/env bash
# =============================================================================
# setup_apple_signing.sh - TsuDEV Apple CI/CD bootstrap (Ubuntu / WSL2, không cần Mac)
# Chuẩn: tsudev-standards docs/APPLE_CICD.md mục 7. Không in giá trị bí mật ra màn hình.
#
# Lệnh (chạy theo thứ tự lần đầu):
#   doctor                                   kiểm công cụ, đồng hồ, gh, quyền kho khoá
#   init --key-id ID --issuer-id UUID --p8 TỆP   cất khoá API App Store Connect, gọi thử API
#   cert-dist [--force]                      OpenSSL tạo CSR -> API cấp "Apple Distribution" -> distribution.p12
#   csr-devid                                tạo CSR "Developer ID Application" (👤 tải lên developer.apple.com)
#   import-devid --cer TỆP.cer               ghép .cer Developer ID + khoá riêng -> developer-id.p12
#   register-bundles [--repos a/b,c/d]       đăng ký Bundle ID (app + phần mở rộng) theo registry
#   push [--repos a/b,c/d] [--dry-run]       tạo environment "apple" + đặt secrets/variables cho từng repo
#   verify [--repos a/b,c/d]                 secrets/variables đủ? Bundle ID + App Record có chưa?
#   builds <bundle_id>                       5 bản build gần nhất trên App Store Connect
#   status                                   Team ID, hạn chứng chỉ (cảnh báo < 30 ngày)
#   backup --to THƯ_MỤC                      sao lưu kho khoá, mã hoá bằng age (passphrase)
#
# Biến môi trường (tuỳ chọn):
#   TSUDEV_APPLE_KEYS      kho khoá (mặc định ~/.config/tsudev/keys/apple, chmod 700, NGOÀI mọi repo git)
#   TSUDEV_APPLE_REGISTRY  registry (mặc định: apple-apps.tsv cạnh script)
#   TSUDEV_APPLE_ENV       tên GitHub environment (mặc định: apple)
# Phụ thuộc: bash 4+, openssl 3, curl, python3 + python3-cryptography, gh (đã đăng nhập), base64, age (cho backup).
# =============================================================================
set -Eeuo pipefail
umask 077

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEYS="${TSUDEV_APPLE_KEYS:-$HOME/.config/tsudev/keys/apple}"
REGISTRY="${TSUDEV_APPLE_REGISTRY:-$SCRIPT_DIR/apple-apps.tsv}"
ENV_NAME="${TSUDEV_APPLE_ENV:-apple}"
ASC_ENV="$KEYS/asc.env"
PW_FILE="$KEYS/p12_password"
TEAM_FILE="$KEYS/team_id"
ASC_HOST="${TSUDEV_ASC_HOST:-https://api.appstoreconnect.apple.com}"   # chỉ đổi khi chạy thử

# Tên secret/variable - KHỚP hệ đang dùng (lotus-share tools/day-khoa-apple.sh, release-lotus.yml). KHÔNG đổi tên.
SECRETS=(APPLE_DIST_P12_BASE64 APPLE_DEVID_P12_BASE64 APPLE_P12_PASSWORD APPLE_ASC_KEY_P8_BASE64)
ENV_VARS=(APPLE_ASC_KEY_ID APPLE_ASC_ISSUER_ID)
REPO_VARS=(APPLE_TEAM_ID)

log()  { printf '\033[1;34m[apple]\033[0m %s\n' "$*" >&2; }
warn() { printf '\033[1;33m[cảnh báo]\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31m[lỗi]\033[0m %s\n' "$*" >&2; exit 1; }
usage() { sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

need() {
  local miss=() t
  for t in "$@"; do command -v "$t" >/dev/null 2>&1 || miss+=("$t"); done
  ((${#miss[@]} == 0)) || die "Thiếu công cụ: ${miss[*]} (xem mục 7.1 của tài liệu chuẩn)"
}
need_py() { python3 -c 'import cryptography' 2>/dev/null || die "Thiếu python3-cryptography: sudo apt install -y python3-cryptography"; }

ensure_keys_dir() {
  mkdir -p "$KEYS"
  chmod 700 "$KEYS"
  case "$(cd "$KEYS" && pwd -P)" in
    "$HOME"/projects/*) die "Kho khoá $KEYS nằm trong ~/projects - phải nằm NGOÀI mọi repo git" ;;
  esac
  if git -C "$KEYS" rev-parse --is-inside-work-tree >/dev/null 2>&1; then die "Kho khoá $KEYS nằm trong một repo git"; fi
}

load_asc() {
  [[ -f $ASC_ENV ]] || die "Chưa init. Chạy: $0 init --key-id ... --issuer-id ... --p8 ..."
  # shellcheck disable=SC1090
  source "$ASC_ENV"
  [[ -n ${ASC_KEY_ID-} && -n ${ASC_ISSUER_ID-} && -f ${ASC_P8-} ]] || die "asc.env hỏng - chạy lại init"
}

# asc METHOD PATH [TỆP_JSON] -> in JSON (stdout). Lỗi -> mã lỗi Apple ra stderr, trả 1. Không in JWT.
asc() {
  local method=$1 path=$2 body=${3:-}
  python3 -I - "$method" "$ASC_HOST$path" "$ASC_KEY_ID" "$ASC_ISSUER_ID" "$ASC_P8" "$body" <<'PY'
import base64, json, sys, time, urllib.request, urllib.error
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils
method, url, kid, iss, p8, body = sys.argv[1:7]
b64 = lambda b: base64.urlsafe_b64encode(b).rstrip(b"=")
key = serialization.load_pem_private_key(open(p8, "rb").read(), password=None)
now = int(time.time())
head = b64(json.dumps({"alg": "ES256", "kid": kid, "typ": "JWT"}, separators=(",", ":")).encode())
claims = b64(json.dumps({"iss": iss, "iat": now - 30, "exp": now + 600, "aud": "appstoreconnect-v1"},
                        separators=(",", ":")).encode())
r, s = utils.decode_dss_signature(key.sign(head + b"." + claims, ec.ECDSA(hashes.SHA256())))
token = (head + b"." + claims + b"." + b64(r.to_bytes(32, "big") + s.to_bytes(32, "big"))).decode()
data = open(body, "rb").read() if body else None
req = urllib.request.Request(url, data=data, method=method,
                             headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        sys.stdout.write(resp.read().decode() or "{}")
except urllib.error.HTTPError as e:
    try:
        errs = json.loads(e.read().decode()).get("errors", [])
    except Exception:
        errs = []
    sys.stderr.write(f"[ASC] {method} {url.split('?')[0]} -> HTTP {e.code}\n")
    for x in errs:
        sys.stderr.write(f"  - {x.get('code')}: {x.get('detail') or x.get('title')}\n")
    sys.exit(1)
except urllib.error.URLError as e:
    sys.stderr.write(f"[ASC] lỗi mạng: {e.reason}\n"); sys.exit(1)
PY
}

# json EXPR: đọc JSON từ stdin, in kết quả biểu thức Python (biến d = dữ liệu). Thay cho jq.
json() { python3 -I -c 'import json,sys; d=json.load(sys.stdin); r=eval(sys.argv[1]); print(r if not isinstance(r,(list,dict)) else json.dumps(r))' "$1"; }

# ---------------------------------------------------------------------------------------------------------------------
cmd_doctor() {
  local rc=0
  for t in openssl curl python3 gh base64 git; do
    if command -v "$t" >/dev/null 2>&1; then log "có $t"; else warn "THIẾU $t"; rc=1; fi
  done
  python3 -c 'import cryptography' 2>/dev/null && log "có python3-cryptography" || { warn "THIẾU python3-cryptography"; rc=1; }
  command -v age >/dev/null 2>&1 && log "có age (backup)" || warn "thiếu age - chỉ cần cho lệnh backup"
  openssl version | grep -q '^OpenSSL 3' || warn "Không phải OpenSSL 3 - kiểm lại cờ pkcs12 ở mục 7"
  if gh auth status >/dev/null 2>&1; then log "gh đã đăng nhập"; else warn "gh chưa đăng nhập: gh auth login"; rc=1; fi
  # Lệch đồng hồ (WSL2 sau khi máy ngủ) làm JWT bị từ chối (HTTP 401).
  local srv now skew
  srv=$(curl -sSI --max-time 15 "$ASC_HOST/v1/apps" | tr -d '\r' | sed -n 's/^[Dd]ate: //p' | head -1 || true)
  if [[ -n $srv ]]; then
    now=$(date -u +%s); skew=$(( now - $(date -u -d "$srv" +%s) )); skew=${skew#-}
    if (( skew > 60 )); then warn "Đồng hồ lệch ${skew}s so với Apple - chạy: sudo hwclock -s"; rc=1; else log "Đồng hồ lệch ${skew}s (OK)"; fi
  else
    warn "Không lấy được giờ máy chủ Apple (mạng?)"
  fi
  if [[ -d $KEYS ]]; then
    [[ $(stat -c %a "$KEYS") == 700 ]] && log "kho khoá $KEYS: 700" || { warn "kho khoá phải chmod 700"; rc=1; }
  fi
  [[ -f $REGISTRY ]] && log "registry: $REGISTRY" || warn "chưa có registry $REGISTRY"
  return $rc
}

cmd_init() {
  local key_id="" issuer="" p8=""
  while (($#)); do
    case $1 in
      --key-id) key_id=${2:?}; shift 2 ;;
      --issuer-id) issuer=${2:?}; shift 2 ;;
      --p8) p8=${2:?}; shift 2 ;;
      *) die "init: tham số lạ $1" ;;
    esac
  done
  [[ $key_id =~ ^[A-Z0-9]{10}$ ]] || die "Key ID phải đúng 10 ký tự A-Z0-9"
  [[ $issuer =~ ^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$ ]] || die "Issuer ID phải là UUID"
  [[ -f $p8 ]] || die "Không thấy tệp $p8"
  grep -q 'BEGIN PRIVATE KEY' "$p8" || die "Tệp không phải khoá .p8"
  need_py; ensure_keys_dir
  install -m 600 "$p8" "$KEYS/AuthKey_${key_id}.p8"
  printf 'ASC_KEY_ID=%s\nASC_ISSUER_ID=%s\nASC_P8=%s\n' "$key_id" "$issuer" "$KEYS/AuthKey_${key_id}.p8" > "$ASC_ENV"
  load_asc
  asc GET "/v1/apps?limit=1" >/dev/null \
    || die "API từ chối. Thường do: Individual Key (cần Team Key), vai trò không phải Admin, sai Key/Issuer ID, đồng hồ lệch."
  log "Khoá API hoạt động. Đã cất tại $KEYS."
  warn "Xoá bản .p8 gốc trong Downloads sau khi chạy 'backup' (Apple chỉ cho tải .p8 MỘT lần)."
}

ensure_password() {
  [[ -s $PW_FILE ]] || openssl rand -base64 48 | tr -dc 'A-Za-z0-9' | head -c 32 > "$PW_FILE"
  chmod 600 "$PW_FILE"
}

# make_p12 <tên>: <tên>.key + <tên>.cer (DER) -> <tên>.pem + <tên>.p12 (thuật toán macOS `security import` đọc được)
make_p12() {
  local n=$1
  openssl x509 -inform DER -in "$KEYS/$n.cer" -out "$KEYS/$n.pem"
  # Khoá công khai của chứng chỉ phải khớp khoá riêng (chặn ghép nhầm tệp).
  [[ "$(openssl x509 -in "$KEYS/$n.pem" -noout -pubkey | openssl sha256)" == \
     "$(openssl pkey -in "$KEYS/$n.key" -pubout | openssl sha256)" ]] || die "$n.cer không khớp $n.key"
  local team
  team=$(openssl x509 -in "$KEYS/$n.pem" -noout -subject -nameopt RFC2253 | sed -n 's/.*OU=\([A-Z0-9]\{10\}\).*/\1/p' | head -1)
  [[ -n $team ]] || die "Không đọc được Team ID (OU) trong chứng chỉ"
  if [[ -s $TEAM_FILE && $(<"$TEAM_FILE") != "$team" ]]; then die "Team ID của $n ($team) khác Team ID đã lưu ($(<"$TEAM_FILE"))"; fi
  printf '%s' "$team" > "$TEAM_FILE"
  ensure_password
  # OpenSSL 3 mặc định AES-256/PBKDF2: macOS `security import` có thể báo "MAC verification failed".
  # Ép 3DES + SHA1 (đọc được trên mọi macOS runner).
  openssl pkcs12 -export -inkey "$KEYS/$n.key" -in "$KEYS/$n.pem" -name "TsuDEV $n" \
    -keypbe PBE-SHA1-3DES -certpbe PBE-SHA1-3DES -macalg sha1 \
    -passout "file:$PW_FILE" -out "$KEYS/$n.p12"
  openssl pkcs12 -in "$KEYS/$n.p12" -passin "file:$PW_FILE" -noout 2>/dev/null \
    || openssl pkcs12 -legacy -in "$KEYS/$n.p12" -passin "file:$PW_FILE" -noout \
    || die "Kiểm $n.p12 thất bại"
  chmod 600 "$KEYS/$n".*
  log "$n.p12 xong - Team $team - hết hạn $(openssl x509 -in "$KEYS/$n.pem" -noout -enddate | cut -d= -f2)"
}

new_key_csr() { # new_key_csr <tên> <CN>
  openssl genrsa -out "$KEYS/$1.key" 2048 2>/dev/null
  openssl req -new -key "$KEYS/$1.key" -out "$KEYS/$1.csr" -subj "/CN=$2/O=TsuDEV/C=VN"
}

cmd_cert_dist() {
  local force=0
  [[ ${1-} == --force ]] && force=1
  need_py; ensure_keys_dir; load_asc
  if [[ -f $KEYS/distribution.p12 && $force == 0 ]]; then log "Đã có distribution.p12 (dùng --force để cấp mới)"; return 0; fi
  local n
  n=$(asc GET "/v1/certificates?filter[certificateType]=DISTRIBUTION&limit=200" | json 'len(d["data"])') || n="?"
  log "Apple Distribution hiện có: $n (Apple giới hạn số lượng; đầy thì 👤 thu hồi cái không dùng - cần đồng ý)"
  new_key_csr distribution "TsuDEV Apple Distribution"
  local body="$KEYS/.req.json" resp
  python3 -I -c 'import json,sys; print(json.dumps({"data":{"type":"certificates","attributes":{"certificateType":"DISTRIBUTION","csrContent":open(sys.argv[1]).read()}}}))' \
    "$KEYS/distribution.csr" > "$body"
  resp=$(asc POST /v1/certificates "$body") || { rm -f "$body"; die "Cấp chứng chỉ thất bại (khoá phải là Admin; có thể đã chạm giới hạn)"; }
  rm -f "$body"
  json 'd["data"]["attributes"]["certificateContent"]' <<<"$resp" | base64 -d > "$KEYS/distribution.cer"
  json 'd["data"]["id"]' <<<"$resp" > "$KEYS/distribution.cert_id"
  make_p12 distribution
}

cmd_csr_devid() {
  ensure_keys_dir
  [[ -f $KEYS/developer-id.key ]] && die "Đã có developer-id.key - xoá tay nếu thật sự muốn tạo lại"
  new_key_csr developer-id "TsuDEV Developer ID"
  log "Đã tạo $KEYS/developer-id.csr"
  log "👤 developer.apple.com > Certificates > + > Developer ID Application (G2 Sub-CA) > tải CSR này lên > tải .cer về"
  log "rồi chạy: $0 import-devid --cer <đường-dẫn>.cer   (chỉ Account Holder tạo được Developer ID; khoá API không làm được)"
}

cmd_import_devid() {
  [[ ${1-} == --cer && -f ${2-} ]] || die "Dùng: import-devid --cer TỆP.cer"
  [[ -f $KEYS/developer-id.key ]] || die "Chưa có developer-id.key - chạy csr-devid trước"
  install -m 600 "$2" "$KEYS/developer-id.cer"
  make_p12 developer-id
}

# --- registry: cột repo | app_dir | bundle_id | extensions(phẩy, '-' = không có) -------------------------------------
reg_rows() {
  [[ -f $REGISTRY ]] || die "Thiếu registry $REGISTRY"
  local only=",${1-},"
  awk -F'\t' '!/^#/ && NF>=3 && $1!="repo"' "$REGISTRY" | while IFS=$'\t' read -r repo dir bid ext; do
    [[ -z ${1-} || $only == *",$repo,"* ]] && printf '%s\t%s\t%s\t%s\n' "$repo" "$dir" "$bid" "${ext:--}"
  done
}

parse_repos() { # --repos a/b,c/d
  REPOS=""; DRY=0
  while (($#)); do
    case $1 in
      --repos) REPOS=${2:?}; shift 2 ;;
      --dry-run) DRY=1; shift ;;
      *) die "tham số lạ $1" ;;
    esac
  done
}

cmd_register_bundles() {
  parse_repos "$@"; need_py; load_asc
  local repo dir bid ext id n body
  while IFS=$'\t' read -r repo dir bid ext; do
    for id in "$bid" ${ext//,/ }; do
      [[ $id == - ]] && continue
      [[ $id =~ ^com\.tsudev\.[a-z0-9]+(\.[A-Za-z0-9]+)?$ ]] || { warn "$repo: '$id' sai quy ước com.tsudev.<ma>[.<Ext>] - bỏ qua"; continue; }
      n=$(asc GET "/v1/bundleIds?filter[identifier]=$id&limit=200" | json "len([x for x in d['data'] if x['attributes']['identifier']=='$id'])") || n=0
      if [[ $n != 0 ]]; then log "✔ $id đã đăng ký"; continue; fi
      body=$(mktemp)
      python3 -I -c 'import json,sys; print(json.dumps({"data":{"type":"bundleIds","attributes":{"identifier":sys.argv[1],"name":sys.argv[2],"platform":"IOS"}}}))' \
        "$id" "TsuDEV ${id##*.}" > "$body"
      if asc POST /v1/bundleIds "$body" >/dev/null; then log "＋ đã đăng ký $id"; else warn "đăng ký $id thất bại"; fi
      rm -f "$body"
    done
  done < <(reg_rows "$REPOS")
  warn "👤 còn phải TẠO APP RECORD trên App Store Connect cho từng bundle id chính (API không tạo được app)."
  warn "👤 Quyền đặc biệt (vd multicast của lotus-share) phải xin Apple duyệt TRƯỚC lần archive đầu."
}

ensure_environment() { # ensure_environment <repo>: environment chỉ cho main + nhãn v*
  local r=$1 have
  gh api -X PUT "repos/$r/environments/$ENV_NAME" --input - >/dev/null <<'J'
{"deployment_branch_policy":{"protected_branches":false,"custom_branch_policies":true}}
J
  have=$(gh api "repos/$r/environments/$ENV_NAME/deployment-branch-policies" --jq '.branch_policies[] | .type + ":" + .name')
  grep -qx 'branch:main' <<<"$have" || gh api -X POST "repos/$r/environments/$ENV_NAME/deployment-branch-policies" -f name=main -f type=branch >/dev/null
  grep -qx 'tag:v*' <<<"$have" || gh api -X POST "repos/$r/environments/$ENV_NAME/deployment-branch-policies" -f name='v*' -f type=tag >/dev/null
}

secret_source() { # in giá trị secret ra stdout CHỈ để pipe vào gh
  case $1 in
    APPLE_DIST_P12_BASE64) base64 -w0 "$KEYS/distribution.p12" ;;
    APPLE_DEVID_P12_BASE64) base64 -w0 "$KEYS/developer-id.p12" ;;
    APPLE_P12_PASSWORD) cat "$PW_FILE" ;;
    APPLE_ASC_KEY_P8_BASE64) base64 -w0 "$ASC_P8" ;;
  esac
}

cmd_push() {
  parse_repos "$@"; load_asc
  [[ -f $KEYS/distribution.p12 && -s $TEAM_FILE && -s $PW_FILE ]] || die "Chưa có distribution.p12/team_id - chạy cert-dist"
  local team; team=$(<"$TEAM_FILE")
  ((DRY)) || gh auth status >/dev/null 2>&1 || die "gh chưa đăng nhập"
  local repo dir bid ext s fail=0
  while IFS=$'\t' read -r repo dir bid ext; do
    if ((DRY)); then
      log "[dry-run] $repo: environment '$ENV_NAME' (main, v*); secrets: ${SECRETS[*]}; env vars: ${ENV_VARS[*]}; repo var: APPLE_TEAM_ID"
      continue
    fi
    ensure_environment "$repo" || { warn "$repo: không tạo được environment (cần quyền admin repo)"; fail=1; continue; }
    for s in "${SECRETS[@]}"; do
      if [[ $s == APPLE_DEVID_P12_BASE64 && ! -f $KEYS/developer-id.p12 ]]; then warn "$repo: chưa có developer-id.p12 - bỏ $s"; continue; fi
      secret_source "$s" | gh secret set "$s" --repo "$repo" --env "$ENV_NAME" >/dev/null || { warn "$repo: đặt $s lỗi"; fail=1; }
    done
    gh variable set APPLE_ASC_KEY_ID --repo "$repo" --env "$ENV_NAME" --body "$ASC_KEY_ID" >/dev/null || fail=1
    gh variable set APPLE_ASC_ISSUER_ID --repo "$repo" --env "$ENV_NAME" --body "$ASC_ISSUER_ID" >/dev/null || fail=1
    gh variable set APPLE_TEAM_ID --repo "$repo" --body "$team" >/dev/null || fail=1
    log "✔ $repo"
  done < <(reg_rows "$REPOS")
  ((fail == 0)) || die "Có mục đặt thất bại (xem cảnh báo)"
  log "Xong. Ghim Team ID $team vào team-id-pin của apple-testflight.yml (và APPLE_TEAM_ID_GHIM nếu repo có) - PR riêng."
}

cmd_verify() {
  parse_repos "$@"; need_py; load_asc
  local repo dir bid ext have vars s miss app rc=0
  printf '%-28s %-8s %-8s %-s\n' REPO SECRETS VARS APP_RECORD
  while IFS=$'\t' read -r repo dir bid ext; do
    have=$(gh secret list --repo "$repo" --env "$ENV_NAME" --json name --jq '.[].name' 2>/dev/null || true)
    vars=$( { gh variable list --repo "$repo" --env "$ENV_NAME" --json name --jq '.[].name'; gh variable list --repo "$repo" --json name --jq '.[].name'; } 2>/dev/null || true)
    miss=0
    for s in APPLE_DIST_P12_BASE64 APPLE_P12_PASSWORD APPLE_ASC_KEY_P8_BASE64; do grep -qx "$s" <<<"$have" || miss=$((miss+1)); done
    local vmiss=0
    for s in "${ENV_VARS[@]}" "${REPO_VARS[@]}"; do grep -qx "$s" <<<"$vars" || vmiss=$((vmiss+1)); done
    app=$(asc GET "/v1/apps?filter[bundleId]=$bid&limit=1" | json 'len(d["data"])' 2>/dev/null || echo "?")
    local a="CHƯA CÓ ($bid)"; [[ $app == 1 ]] && a="OK ($bid)"; [[ $app == "?" ]] && a="? ($bid)"
    ((miss || vmiss)) && rc=1; [[ $app == 1 ]] || rc=1
    printf '%-28s %-8s %-8s %-s\n' "$repo" "$( ((miss)) && echo "THIẾU$miss" || echo OK)" "$( ((vmiss)) && echo "THIẾU$vmiss" || echo OK)" "$a"
  done < <(reg_rows "$REPOS")
  ((rc == 0)) || warn "Có mục chưa đạt. 'CHƯA CÓ' = 👤 tạo App Record (mục 5, H3)."
  return $rc
}

cmd_builds() {
  local bid=${1:?Dùng: builds <bundle_id>} app
  need_py; load_asc
  app=$(asc GET "/v1/apps?filter[bundleId]=$bid&limit=1" | json 'd["data"][0]["id"] if d["data"] else ""')
  [[ -n $app ]] || die "Chưa có App Record cho $bid"
  asc GET "/v1/builds?filter[app]=$app&sort=-uploadedDate&limit=5&include=preReleaseVersion" | python3 -I -c '
import json, sys
d = json.load(sys.stdin)
pre = {x["id"]: x["attributes"]["version"] for x in d.get("included", []) if x["type"] == "preReleaseVersions"}
print("PHIÊN_BẢN\tBUILD\tTRẠNG_THÁI\tTẢI_LÊN")
for b in d["data"]:
    rel = (b.get("relationships", {}).get("preReleaseVersion", {}).get("data") or {}).get("id")
    a = b["attributes"]
    print("\t".join([pre.get(rel, "?"), a["version"], a["processingState"], a["uploadedDate"]]))'
}

cmd_status() {
  [[ -f $ASC_ENV ]] && log "init: OK" || warn "init: CHƯA"
  [[ -s $TEAM_FILE ]] && log "Team ID: $(<"$TEAM_FILE")" || warn "Team ID: CHƯA"
  local n
  for n in distribution developer-id; do
    if [[ -f $KEYS/$n.pem ]]; then
      log "$n hết hạn: $(openssl x509 -in "$KEYS/$n.pem" -noout -enddate | cut -d= -f2)"
      openssl x509 -in "$KEYS/$n.pem" -noout -checkend 2592000 >/dev/null || warn "$n còn < 30 ngày - xem mục 13 (gia hạn)"
    else
      warn "$n: CHƯA"
    fi
  done
}

cmd_backup() {
  [[ ${1-} == --to && -n ${2-} ]] || die "Dùng: backup --to THƯ_MỤC"
  need age; [[ -d $KEYS ]] || die "Chưa có kho khoá"
  mkdir -p "$2"
  local out; out="$2/tsudev-apple-keys-$(date +%Y%m%d-%H%M%S).tar.gz.age"
  tar -C "$KEYS" -czf - . | age -p -o "$out"
  log "Đã sao lưu (mã hoá age, passphrase do 👤 giữ): $out"
}

main() {
  local sub=${1-}; shift || true
  case $sub in
    doctor) cmd_doctor ;;
    init) need openssl python3; cmd_init "$@" ;;
    cert-dist) need openssl python3 base64; cmd_cert_dist "$@" ;;
    csr-devid) need openssl; cmd_csr_devid ;;
    import-devid) need openssl; cmd_import_devid "$@" ;;
    register-bundles) cmd_register_bundles "$@" ;;
    push) need gh base64; cmd_push "$@" ;;
    verify) need gh; cmd_verify "$@" ;;
    builds) cmd_builds "$@" ;;
    status) need openssl; cmd_status ;;
    backup) cmd_backup "$@" ;;
    -h|--help|help|"") usage 0 ;;
    *) usage 1 ;;
  esac
}
main "$@"
