#!/usr/bin/env bash
# check-central-login.sh - cổng kiểm "một cổng đăng nhập" (AUTH_AND_ACCOUNT.md mục 2.1).
#
#   .standards/scripts/check-central-login.sh            # liệt kê nghi vấn, luôn thoát 0
#   .standards/scripts/check-central-login.sh --strict   # có nghi vấn thì thoát 1 (dùng cho CI)
#
# Chỉ in `luật tệp:dòng`, KHÔNG in nội dung dòng (dòng có thể chứa bí mật).
# Ngoại lệ ở tệp `.central-login-allow` tại gốc repo, mỗi dòng:  <LUẬT> <đường dẫn hoặc glob>  # lý do
# Dòng thiếu lý do không có hiệu lực. Repo cài đặt CỔNG (tsudev) khai các trang của cổng ở đó.
# Đây là lưới quét, không phải bằng chứng đầy đủ: vẫn phải rà tay giao diện đăng nhập.
set -euo pipefail

STRICT=0
[[ "${1:-}" == "--strict" ]] && STRICT=1
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

ALLOW_RULES=(); ALLOW_GLOBS=()
if [[ -f .central-login-allow ]]; then
  while read -r rule glob hash reason || [[ -n "${rule:-}" ]]; do
    [[ -z "${rule:-}" || "$rule" == \#* ]] && continue
    if [[ "${hash:-}" != "#" || -z "${reason:-}" ]]; then
      echo "LƯU Ý .central-login-allow: dòng '$rule ${glob:-}' thiếu '# lý do' - bỏ qua" >&2
      continue
    fi
    ALLOW_RULES+=("$rule"); ALLOW_GLOBS+=("$glob")
  done < .central-login-allow
fi

allowed() { # <luật> <tệp>
  local i
  for i in "${!ALLOW_RULES[@]}"; do
    # shellcheck disable=SC2053
    [[ "${ALLOW_RULES[$i]}" == "$1" && "$2" == ${ALLOW_GLOBS[$i]} ]] && return 0
  done
  return 1
}

files() {
  git ls-files -z --cached --others --exclude-standard -- \
    . ':(exclude).standards' ':(exclude)logs' ':(exclude)*.md' ':(exclude)*.lock' ':(exclude)*lock.json' \
    ':(exclude)*.min.js' ':(exclude)**/node_modules/**' ':(exclude)**/vendor/**' ':(exclude)third_party' \
    ':(exclude)**/test/**' ':(exclude)**/tests/**' ':(exclude)test' ':(exclude)tests' ':(exclude)e2e' \
    ':(exclude)**/__tests__/**' ':(exclude)*.test.*' ':(exclude)*.spec.*' ':(exclude)*_test.*'
}

COUNT=0
report() { # <luật> <tệp> <dòng>
  allowed "$1" "$2" && return 0
  printf 'NGHI %s %s:%s\n' "$1" "$2" "$3"
  COUNT=$((COUNT + 1))
}

scan() { # <luật> <regex mở rộng>
  local rule="$1" re="$2" hit f rest
  while IFS= read -r hit; do
    f="${hit%%:*}"; rest="${hit#*:}"
    report "$rule" "$f" "${rest%%:*}"
  done < <(files | xargs -0 -r grep -I -n -H -i -E -e "$re" -- 2>/dev/null || true)
}

# L1 ô mật khẩu (web, Flutter, Android, SwiftUI/UIKit, WinUI/WPF, Qt, Win32).
scan L1-o-mat-khau 'type[[:space:]]*[=:][[:space:]]*[{]?["'\'']password["'\'']|obscureText:[[:space:]]*true|SecureField\(|isSecureTextEntry|textPassword|<PasswordBox|QLineEdit::Password|(^|[^A-Za-z0-9_])ES_PASSWORD|KeyboardType\.Password'
# L2 SDK / nút đăng nhập của nhà cung cấp.
scan L2-sdk-nha-cung-cap 'google_sign_in|sign_in_with_apple|play-services-auth|GoogleSignIn|ASAuthorizationAppleIDProvider|SignInWithAppleButton|@react-oauth/google|accounts\.google\.com/gsi|github\.com/login/oauth|(next-auth|@auth/core)/providers/(google|github|apple)'
# L3 WebView hứng đăng nhập.
scan L3-webview-dang-nhap '(webview|WKWebView|WebView2).*(oauth|authorize|login|signin)|(oauth|authorize|login|signin).*(webview|WKWebView|WebView2)'
# L4 password grant.
scan L4-password-grant 'grant_type["'\'']?[[:space:]]*[=:,][[:space:]]*["'\'']?password'

# L5 trang đăng nhập riêng (theo tên tệp định tuyến).
PAGES='login|signin|sign-in|signup|sign-up|register|dang-nhap|dang-ky|forgot-password|reset-password|quen-mat-khau|dat-lai-mat-khau'
while IFS= read -r f; do
  report L5-trang-dang-nhap "$f" 1
done < <(files | tr '\0' '\n' | grep -i -E \
  "(^|/)(pages|app|routes)/(.*/)?(($PAGES)(\.(tsx|jsx|ts|js|vue|svelte|astro|html|php)|/(page|index|\+page)\.[a-z]+))$|(^|/)(public|site|web|static|docs-site)/(.*/)?($PAGES)(\.html|/index\.html)$" || true)

if [[ $COUNT -eq 0 ]]; then
  echo "Một cổng đăng nhập: không thấy nghi vấn."
  exit 0
fi
echo "Một cổng đăng nhập: $COUNT nghi vấn. Sửa, hoặc khai ngoại lệ kèm lý do trong .central-login-allow."
[[ $STRICT == 1 ]] && exit 1
exit 0
