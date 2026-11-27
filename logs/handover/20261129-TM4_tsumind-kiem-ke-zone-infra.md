# Phiếu bàn giao 20261129-TM4 - TsuMIND: kiểm kê, zone `tsumind.com`, `tsumind-infra`

- **Từ:** phiên điều phối (Phase TM3 xong, bộ quy ước `v10.3.0`)
- **Tới:** phiên kế tiếp ở repo `tsudev-standards`
- **Trạng thái:** MỞ

## 1. Đã xong ở TM3
`docs/LEGAL_COMPLIANCE.md` v1.0.0, `templates/legal/` (11 tệp), phiếu `TM3b` sang repo `tsudev`. Xem CHANGELOG 10.3.0.

## 2. Việc của TM4 (theo `docs/PLAN.md`)
Đọc Phase TM4. Token Cloudflare (`~/.config/tsudev/cloudflare-tsumind.env`) hết hạn **27/12/2026**; dò quyền ghi thật trước khi làm.
Nhà cung cấp đặt hạ tầng ngoài Việt Nam (Cloudflare, Resend): ghi vào danh sách để chốt hồ sơ chuyển xuyên biên giới (`templates/legal/DPIA_DOSSIER.md` phần B).

## 3. [OWNER] còn treo
Org `tsumind-org`; nhãn hiệu; ICANN/2FA/transfer lock; quyết định hồ sơ đánh giá tác động (Mẫu 02a/02b + 10); thông báo TMĐT (UBND tỉnh);
chỉ định nhân sự bảo vệ DLCN; điền `[OWNER]` ở `templates/legal/`; luật sư rà soát; đóng các mục "cần xác minh" (`LEGAL_COMPLIANCE.md` mục 8).

## 4. Có thể chạy song song
TM4 phần `tsumind-infra` (repo mới) không đụng tệp của tsudev-standards ngoài `logs/`. Xem câu trả lời cuối phiên TM3.
