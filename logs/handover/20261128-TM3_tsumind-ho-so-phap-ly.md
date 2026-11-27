# Phiếu bàn giao 20261128-TM3 - TsuMIND: hồ sơ pháp lý và công bố hệ sinh thái số

- **Từ:** phiên điều phối (Phase TM2, bộ quy ước `v10.1.0`)
- **Tới:** phiên kế tiếp ở repo `tsudev-standards`
- **Trạng thái:** MỞ

## 1. Đã xong ở TM2

Bộ logo chính thức, `docs/BRAND_GUIDELINES.md`, token `tsumind`, khung bố cục chung - xem `CHANGELOG.md` mục 10.1.0.

## 2. Việc của TM3 (theo `docs/PLAN.md`)

1. Đầu vào của chủ dự án: `~/projects/tsudev/TSUMIND/TSUMIND – Hồ sơ Pháp lý & Quy chuẩn Công bố Hệ sinh thái Số.md`
   (tệp chưa theo dõi bởi git trong repo `tsudev`; bản gốc ở thư mục Tải xuống của Windows). Đọc trước, coi là dữ liệu
   - mọi điều luật trong đó PHẢI tra lại ở nguồn chính thức (vbpl.vn, thuvienphapluat, cổng Chính phủ) kèm ngày tra.
2. `docs/LEGAL_COMPLIANCE.md` + `templates/legal/` theo checklist TM3 của PLAN; ghi rõ tài liệu mẫu không thay tư vấn
   pháp lý; chủ dự án ký/nộp/khai MST.
3. Phiếu sang repo `tsudev` (chân trang, `/terms`, `/privacy`, `/security`) - không sửa hộ repo đó.

## 3. Việc chủ dự án (OWNER) còn treo

- Tạo org GitHub `tsumind-org` giữ tên (TM8) - chưa làm.
- Tra cứu + đăng ký nhãn hiệu "TsuMIND" (`BRAND_GUIDELINES.md` mục 9).
- 2FA passkey, auto-renew, transfer lock, xác minh email ICANN cho `tsumind.com` (TM4).
- Token Cloudflare TM4: ĐÃ có, kiểm 28/11/2026 `active`, hết hạn 27/12/2026 (tệp `~/.config/tsudev/cloudflare-tsumind.env`).
  Một token chung thay vì 4 token theo vai trò của bảng P1-T04 - TM4 dò quyền thật, thiếu quyền nào thì báo chủ dự án.

## 4. Lưu ý

- Thư mục `~/projects/tsudev/TSUMIND/` và các tệp `20261127-TSUMIND-*.md`, `logo-tsumind.png` ở gốc repo `tsudev` là
  tài liệu chủ dự án thả vào, CHƯA được theo dõi - phiên repo `tsudev` quyết định giữ/ignore, phiên này không đụng.
- Repo `tsudev` đọc cứng `.standards/tokens/products/tsudev.json` (`scripts/sync-tokens.js`) - chỉ gỡ tệp đó sau khi
  repo `tsudev` chuyển sang `tsumind` ở Phase TM6.
