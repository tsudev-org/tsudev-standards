#!/usr/bin/env bash
#
# test-upstream-exempt.sh - kiểm thử ngoại lệ 3 của AGENTS.md mục 7.1 (dòng kế thừa nguyên văn từ upstream).
#
# Dựng một repo "upstream" và một repo "fork" giả trong thư mục tạm, rồi chạy mục 4 của check-standards.sh qua
# từng ca. Không cần mạng (ca xác minh trực tuyến được kiểm ở repo con thật, xem CHANGELOG 3.3.0).
#
#   ./scripts/test-upstream-exempt.sh        # mã thoát khác 0 = có ca sai
set -euo pipefail

GATE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/check-standards.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
EM="$(printf '\xe2\x80\x94')"
G=(git -c user.name=test -c user.email=test@example.invalid -c commit.gpgsign=false)
FAILED=0

# Repo upstream có 2 dòng chứa em-dash.
mkdir "$TMP/fork" && cd "$TMP/fork" && git init -q .
printf 'fn a() {} // giu %s nguyen van\n' "$EM" > lib.rs
printf '# Readme\n\nUpstream %s mo ta\n' "$EM" > README.md
"${G[@]}" add -A && "${G[@]}" commit -qm upstream
UP="$(git rev-parse HEAD)"

# Fork: thêm phần riêng, khai báo upstream.
mkdir -p .standards && printf 'repo=example/upstream\nref=%s\n' "$UP" > .standards-upstream
printf 'fn b() {}\n' > fork.rs
"${G[@]}" add -A && "${G[@]}" commit -qm fork

section4() { { bash "$GATE" 2>&1 || true; } | sed -n "/^4\./,/^5\./p"; }

expect() {
  # $1 = tên ca, $2 = "dat" | "truot", $3 = chuỗi bắt buộc có trong đầu ra (rỗng = bỏ qua)
  local out; out="$(section4)"
  local ok=1
  if [[ "$2" == dat ]]; then grep -q 'TRƯỢT' <<< "$out" && ok=0; else grep -q 'TRƯỢT' <<< "$out" || ok=0; fi
  [[ -n "${3:-}" ]] && ! grep -qF -- "$3" <<< "$out" && ok=0
  if [[ $ok == 1 ]]; then echo "  ĐÚNG $1"; else echo "  SAI   $1"; echo "$out" | sed 's/^/      /'; FAILED=1; fi
}

echo "Kiểm thử ngoại lệ upstream (AGENTS.md mục 7.1, ngoại lệ 3)"
expect "dòng kế thừa nguyên văn được miễn" dat "miễn 2 dòng"

printf '// fork them %s moi\n' "$EM" >> lib.rs
expect "fork thêm dòng em-dash mới vào tệp kế thừa thì trượt" truot "lib.rs"
git checkout -q lib.rs

sed -i "s/giu $EM/giu $EM SUA/" lib.rs
expect "fork sửa một dòng kế thừa có em-dash thì trượt" truot "lib.rs"
git checkout -q lib.rs

printf '// %s\n' "$EM" > moi.rs && git add moi.rs
expect "tệp mới của fork có em-dash thì trượt" truot "moi.rs"
git rm -q --cached moi.rs && rm moi.rs

"${G[@]}" commit -q --allow-empty -m nhanh-khac && OTHER="$(git rev-parse HEAD)" && git reset -q --hard HEAD~1
sed -i "s/^ref=.*/ref=$OTHER/" .standards-upstream
expect "ref không phải tổ tiên HEAD thì trượt" truot "không phải tổ tiên"
git checkout -q .standards-upstream

sed -i "s/^ref=.*/ref=${UP:0:12}/" .standards-upstream
expect "ref viết tắt (không đủ 40 ký tự) thì trượt" truot "sai định dạng"
git checkout -q .standards-upstream

rm .standards-upstream && "${G[@]}" commit -qam bo-khai-bao
expect "không khai báo upstream thì em-dash kế thừa vẫn trượt như cũ" truot "lib.rs"

[[ $FAILED == 0 ]] && echo "KẾT QUẢ: mọi ca đúng." || { echo "KẾT QUẢ: có ca sai." >&2; exit 1; }
