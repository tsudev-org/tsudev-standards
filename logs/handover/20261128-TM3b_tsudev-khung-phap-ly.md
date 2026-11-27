# Phiếu bàn giao 20261128-TM3b - Repo `tsudev`: đưa khung pháp lý vào website

- **Từ:** phiên điều phối tsudev-standards (Phase TM3, bộ quy ước `v10.3.0`)
- **Tới:** phiên làm việc ở repo `tsudev` (KHÔNG sửa hộ từ repo này)
- **Trạng thái:** MỞ

## Việc cần làm

Sau khi đồng bộ `./scripts/sync-standards.sh --ref v10.3.0`:

1. **Chân trang** mọi trang: dùng `templates/legal/FOOTER_OWNER.md` (bản đầy đủ). Trường `[OWNER]` do chủ dự án cung cấp
   (họ tên, MST, địa chỉ liên hệ công khai, điện thoại, người chịu trách nhiệm). Không tự điền.
2. Trang `/privacy` từ `PRIVACY_POLICY.md`; `/terms` từ `TERMS_OF_USE.md`; `/security` từ `SECURITY_POLICY.md`;
   `/cookie` từ `COOKIE_POLICY.md` (nếu chỉ dùng cookie thiết yếu: một câu, không banner); trang "Giới thiệu" từ `OWNER_INFO.md`.
3. `/chinh-sach-thanh-toan` (gói Pro): đối chiếu NĐ 248/2026 Điều 8, 10, 15, 16 (xem `docs/LEGAL_COMPLIANCE.md` mục 4.2).
4. Thêm kiểm tra CI: không còn chuỗi `[OWNER` trong trang đã build trước khi công bố.
5. `/.well-known/security.txt` khớp `SECURITY_POLICY.md` mục 4.
6. Rà theo `ECOMMERCE_NOTICE.md`: chưa mở bán trực tuyến cho tới khi chủ dự án có xác nhận thông báo (NĐ 248/2026 Điều 23).

## Lưu ý

- Số điều khoản và hạn: chỉ dùng trong `docs/LEGAL_COMPLIANCE.md`; mục "cần xác minh" chưa được viết thành cam kết công khai.
- Chủ sở hữu hiện là cá nhân không đăng ký kinh doanh (xác nhận 28/11/2026).
- Văn phong: "TsuMIND", chỉ gạch ngang `-`; chưa đổi tên miền (TM10).
