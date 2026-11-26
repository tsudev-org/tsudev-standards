#!/usr/bin/env bash
# Kiểm thử check-central-login.sh trên repo tạm (dữ liệu giả).
set -euo pipefail
GATE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/check-central-login.sh"
TMP="$(mktemp -d)"; trap 'rm -rf "${TMP:?}"' EXIT
cd "$TMP"; git init -q .
FAIL=0
ok()  { printf '  ĐẠT   %s\n' "$1"; }
bad() { printf '  TRƯỢT %s\n' "$1" >&2; FAIL=1; }
run() { set +e; OUT="$(bash "$GATE" --strict 2>&1)"; RC=$?; set -e; }

mkdir -p src .standards test
echo 'const a = 1' > src/ok.ts
echo '<input type="password">' > .standards/mau.html
echo '<input type="password">' > test/mau.html
echo '`<input type="password">`' > README.md
echo 'POSTGRES_PASSWORD: x' > docker-compose.yml
run; [[ $RC == 0 ]] && ok "repo sạch; bỏ qua .standards, test, markdown" || bad "báo nhầm: $OUT"

check() { # <luật> <tệp> <nội dung>
  mkdir -p "$(dirname "$2")"; printf '%s\n' "$3" > "$2"
  run
  if [[ $RC == 1 && "$OUT" == *"$1 $2:"* ]]; then ok "$1 $2"; else bad "$1 không bắt $2: $OUT"; fi
  rm -f "$2"
}
check L1-o-mat-khau src/a.tsx '<input type="password" />'
check L1-o-mat-khau src/b.dart 'TextField(obscureText: true)'
check L1-o-mat-khau src/c.xaml '<PasswordBox x:Name="p"/>'
check L1-o-mat-khau src/d.swift 'SecureField("x", text: $p)'
check L2-sdk-nha-cung-cap pubspec.yaml '  google_sign_in: ^6.0.0'
check L2-sdk-nha-cung-cap src/e.ts "import G from 'next-auth/providers/google'"
check L3-webview-dang-nhap src/f.kt 'webView.loadUrl(authorizeUrl)'
check L4-password-grant src/g.ts "body: 'grant_type=password&u=x'"
check L1-o-mat-khau src/h.cpp 'style = ES_PASSWORD | WS_CHILD;'
check L5-trang-dang-nhap pages/login.tsx 'export default 1'
check L5-trang-dang-nhap src/app/dang-nhap/page.tsx 'export default 1'
check L5-trang-dang-nhap public/signup.html '<p>x</p>'

printf '<input type="password" data-x="noi-dung-bi-mat-gia">\n' > src/a.html
run; [[ "$OUT" != *noi-dung-bi-mat-gia* ]] && ok "không in nội dung dòng" || bad "in nội dung dòng"
echo 'L1-o-mat-khau src/a.html # khoá kho cục bộ' > .central-login-allow
run; [[ $RC == 0 ]] && ok "ngoại lệ có lý do" || bad "ngoại lệ không hiệu lực: $OUT"
printf 'L1-o-mat-khau src/a.html' > .central-login-allow
run; [[ $RC == 1 ]] && ok "ngoại lệ thiếu lý do bị bỏ qua" || bad "ngoại lệ thiếu lý do vẫn qua"
set +e; bash "$GATE" >/dev/null 2>&1; RC=$?; set -e
[[ $RC == 0 ]] && ok "chế độ cảnh báo thoát 0" || bad "chế độ cảnh báo thoát $RC"
exit $FAIL
