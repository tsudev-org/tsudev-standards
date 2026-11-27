# Phiếu bàn giao 20261127-TM2 - TsuMIND: sổ tay thương hiệu + quy chuẩn giao diện

- **Từ:** phiên điều phối (Phase TM1, bộ quy ước `v10.0.0`)
- **Tới:** phiên kế tiếp ở repo `tsudev-standards`
- **Trạng thái:** MỞ

## 1. Đã xong ở TM1

- `docs/NAMING_CONVENTION.md` v1.1.0, `docs/TSUMIND_MIGRATION.md` v1.1 (mục 0.3: D-08..D-12), `docs/PLAN.md`.
- `scripts/check-naming.sh` (cảnh báo; CI chạy). Repo này còn 32 dòng `Tsu Swico`/`Tsu Tramon`... chủ yếu ở
  `tokens/products/*.json` `name` - đổi ở TM2 cùng lúc với token `tsumind.json`.
- Bộ logo `assets/brand/tsumind/` (52 tệp sinh, `build.mjs --check` trong CI). Sinh lại: `cd assets/brand/tsumind &&
  npm ci && node build.mjs` (~1 phút rưỡi, AVIF 1024 chậm nhất).
- Bảng màu đo từ logo (k-means 7 cụm): Ink Navy `#021023`, Deep Navy `#061E3A`, Navy `#14355C`, Steel `#1F5180`,
  Ocean `#4294C0`, Mind Cyan `#51D2EC`, Ice `#D5E1E9`. Wordmark: chữ Be Vietnam Pro 700, `Tsu` Ice/`MIND` Cyan (nền Tối),
  `Tsu` `#061E3A`/`MIND` `#1A6FA8` (nền Sáng).

## 2. Việc của TM2 (theo `docs/PLAN.md`)

1. Hỏi chủ dự án duyệt bộ logo (gửi `dist/social/og-image.png`, `dist/svg/tsumind-logo-horizontal*.svg`,
   `dist/mark/tsumind-mark-32.png`). Chỉnh SVG trong `svg/` nếu được yêu cầu, chạy lại `build.mjs`.
2. `docs/BRAND_GUIDELINES.md`: tỷ lệ cấu trúc, vùng an toàn, cỡ tối thiểu (huy hiệu ≥ 96px, dưới đó dùng mark), hệ màu +
   kiểm WCAG, phông, giọng văn, điều cấm, bảo hộ thương hiệu (nhãn hiệu là việc OWNER - Cục SHTT), triển khai đa nền tảng.
3. `tokens/products/tsumind.json` thay `tsudev.json`; đổi `name` các sản phẩm sang dạng viết liền; `gen-product-palette`
   + `check-contrast` + `check-products` xanh.
4. Quy chuẩn bố cục chung (header, chân trang, modal/popup một lớp, thang z-index, không chồng lấn) vào
   `DESIGN_SYSTEM.md`/`ECOSYSTEM_IDENTITY.md`.

## 3. Việc chủ dự án (OWNER) - không agent nào làm thay

- Duyệt logo (TM2).
- Tạo org GitHub `tsumind-org` (miễn phí) để giữ tên ngay - đo 27/11/2026 còn trống; người dùng `tsumind` đã bị người khác giữ.
- TM4: tạo API token Cloudflare tối thiểu quyền có hạn (bảng P1-T04 của `TSUMIND_MIGRATION.md`), lưu
  `~/.config/tsudev/cloudflare-tsumind.env` dạng `KEY=VALUE`, quyền 600; bật auto-renew + transfer lock; xác minh email ICANN.
- Tra cứu nhãn hiệu "TsuMIND" (Cục Sở hữu trí tuệ, WIPO Global Brand Database).

## 4. Lưu ý

- Ảnh gốc là ảnh tạo bằng công cụ AI, có watermark ✦ (script xoá). Khi đăng ký nhãn hiệu, chủ dự án cần biết nguồn
  gốc hình (quyền tác giả với hình do AI tạo có thể bị hạn chế) - ghi trong sổ tay TM2.
- Mã Phase `TM*` của kế hoạch này khác phiếu cũ `20261125-TM1b` (Tsu Tramon) - không liên quan.
