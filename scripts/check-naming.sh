#!/usr/bin/env bash
# check-naming.sh - cổng kiểm quy ước đặt tên TsuMIND (docs/NAMING_CONVENTION.md mục 14).
#
# Quét file được git theo dõi, tìm biến thể tên bị cấm (mục 4). Dòng có `TMNC-EXCEPTION`
# được miễn (mục 13).
#
#   ./scripts/check-naming.sh                 cảnh báo, luôn thoát 0 (giai đoạn chuyển dần)
#   NAMING_STRICT=1 ./scripts/check-naming.sh thoát 1 khi còn vi phạm (bật ở CI sau Phase TM7 của repo)
#   NAMING_LEGACY=1 ...                       quét thêm tên thương hiệu CŨ "TsuDEV"/"tsudev.com" trong văn bản
#                                             (dùng ở Phase TM7-TM10; tệp/dòng hợp lệ khai ở allowlist-legacy.txt)
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

patterns=(
  '\bTsumind\b'
  '\bTsu[ _-]MIND\b'
  '\bTsu[ _-]Mind\b'
  '\bTSU[ _-]MIND\b'
  '\bTsu[ _-]?(CWICO|SWICO|TRAMON|CONTACT)\b'
  '\bTsu (Cwico|Swico|Contact|Tramon|Scan|Link)\b'
  '\bTSU (Cwico|Swico|Contact|Tramon|Scan|Link)\b'
  '\btsuwico\b'
)
if [[ "${NAMING_LEGACY:-0}" == 1 ]]; then
  patterns+=('\bTsuDEV\b' '\btsudev\.com\b')
fi

allow=()
[[ -f allowlist-legacy.txt ]] && mapfile -t allow < <(grep -vE '^\s*(#|$)' allowlist-legacy.txt)

regex=$(IFS='|'; echo "${patterns[*]}")
hits=$(git grep -nIP "$regex" -- . ':!*.lock' ':!package-lock.json' ':!MANIFEST.sha256' \
  ':!docs/NAMING_CONVENTION.md' ':!scripts/check-naming.sh' 2>/dev/null \
  | grep -v 'TMNC-EXCEPTION' || true)
for a in "${allow[@]:-}"; do
  [[ -z "$a" ]] && continue
  hits=$(printf '%s\n' "$hits" | grep -v -- "^$a" || true)
done
hits=$(printf '%s\n' "$hits" | sed '/^$/d')

if [[ -z "$hits" ]]; then
  echo "check-naming: OK - không có biến thể tên bị cấm."
  exit 0
fi
n=$(printf '%s\n' "$hits" | wc -l)
printf '%s\n' "$hits" | head -50
echo "check-naming: $n dòng dùng biến thể tên bị cấm (docs/NAMING_CONVENTION.md mục 4)."
if [[ "${NAMING_STRICT:-0}" == 1 ]]; then exit 1; fi
echo "check-naming: chế độ cảnh báo (NAMING_STRICT=1 để chặn)."
