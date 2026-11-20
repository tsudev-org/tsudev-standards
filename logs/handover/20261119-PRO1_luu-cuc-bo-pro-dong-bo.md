# PHIẾU YÊU CẦU - PRO1: lưu cục bộ mặc định, Pro mới có đồng bộ/sao lưu đám mây (tsudev-standards)

- **Mã phiếu**: 20261119-PRO1 (phiếu con)
- **Từ**: agent-qulythuchi (phiên `qulythuchi-b2`), 19/11/2026, theo yêu cầu trực tiếp của chủ dự án
- **Đến**: phiên kế tiếp của repo `tsudev-standards`
- **Trạng thái**: ĐÓNG phần repo này - PRO-A phát hành v3.9.0 (20/11/2026), PRO-C có ở `assets/badges/`; ghi chú cũ: chưa viết mã trước khi tsudev-standards v3.9.0 (PRO-A) phát hành; phần nào cần máy chủ quyền lợi
  thì chờ PRO-B
- **Phiếu gốc (ĐỌC TRƯỚC)**: `~/projects/logs/handover/20261119-PRO1_ke-hoach-luu-cuc-bo-pro-dong-bo-toan-he.md` - mục 1 (yêu cầu nguyên văn tóm tắt), 2 (nguyên tắc N1-N8), 3 (thông báo nhiều
  thiết bị, chu kỳ 30 ngày), 5 (khung việc mỗi repo), 7 (nghiệm thu), 8 (câu hỏi 👤). Phiếu này THAY hàng T7 của
  `~/projects/logs/handover/20261119-01_ke-hoach-toan-he-v3.8.0.md` cho repo này.

## 1. Việc riêng của repo này

**PRO-A**: PRODUCT_POLICY thêm mục "Lưu cục bộ mặc định - đồng bộ/sao lưu đám mây là Pro" (nguyên tắc N1-N8 + đặc tả thông báo mục 3 của phiếu gốc + quy tắc ân hạn theo câu trả lời 👤 ở mục 8); ghi rõ ngoại lệ "nhắc Pro mỗi 30 ngày khi ≥ 2 thiết bị" so với mục 3.2; AUTH_AND_ACCOUNT thêm "mã cài đặt" ngẫu nhiên 128 bit (cấm IMEI/MAC/vân tay); FREE_TIER_STACK thêm N5/N7; checklist mục 7. Phát hành **v3.9.0** rồi mở phiếu sync. **PRO-C**: SVG gốc huy hiệu ở `assets/badges/` (hàng T6).

## 2. Khung việc (tóm tắt phiếu gốc mục 5)

1. Kiểm kê: dữ liệu nào đang rời thiết bị, nằm ở đâu ⇒ ghi mục 4 dưới đây.
2. ADR riêng: phần nào là Pro, cách ân hạn cho người dùng cũ, kênh thanh toán theo PRODUCT_POLICY 3.3/4.3.
3. Mã: đọc quyền lợi (JWS tsudev, đệm ≤ 7 ngày), gate Pro ở MÁY CHỦ, thông báo nhiều thiết bị (5 test bắt buộc), màn
   Pro/Ủng hộ, huy hiệu PRO-C, vi + en, test.
4. Đo phản hồi thao tác chính (< 100 ms) và chịu tải (nếu có máy chủ), ghi vào PR.
5. Phiếu rà soát bảo mật + THREAT_MODEL. Không tự tạo khoá/tài khoản thanh toán thật ⇒ việc 👤.

## 3. Việc cần chủ dự án (👤)

Xem phiếu gốc mục 8 (giá Pro, ân hạn, nơi đặt dịch vụ đồng bộ dùng chung, ngoại lệ nhắc 30 ngày).

## 4. Kết quả xử lý (phiên nhận điền)

- 20/11/2026 - PRO-A: `PRODUCT_POLICY.md`, `AUTH_AND_ACCOUNT.md` (mã cài đặt `X-Tsu-Installation`), `FREE_TIER_STACK.md` trong v3.9.0; hợp đồng JWS đính chính v3.9.1; kỳ 1 năm + nhắc gia hạn 7 ngày ở v4.0.0.
- PRO-C: SVG gốc huy hiệu ở `assets/badges/` (`tsu-badge-pro.svg`, `tsu-badge-donor-*.svg`, README).
- 21/11/2026 - đối chiếu lại khi ghi sổ; kiểm kê/ADR/mã ở mục 2 là việc của repo sản phẩm, không phải repo quy ước.

## 5. Đã chốt (19/11/2026, bổ sung sau khi mở phiếu)

Chủ dự án giao agent chốt mọi câu hỏi mở và xác nhận **chưa có người dùng thật** ⇒ phiếu gốc mục 8 ĐÃ CHỐT, mục 9
là **HỢP ĐỒNG CHUNG** (mọi repo dùng đúng định danh, không tự đặt khác): gói chung **TsuDEV Pro 49.000 ₫/tháng,
490.000 ₫/năm**; Ủng hộ 20/50/100/200 nghìn; Play `tsudev_pro` (`thang`/`nam`) + `ung_ho_20k`…`ung_ho_200k`; JWS
quyền lợi (ES256, `exp` ≤ 7 ngày, `badge`, `devices_30d`); HTTP 402 `pro_required`; mã cài đặt `X-Tsu-Installation`;
dịch vụ đồng bộ dùng chung ở repo mới `tsudev-org/tsusync`; huy hiệu `TsuBadge`; nội dung thông báo vi/en nguyên văn.
Pro hết hạn: chặn đẩy, kéo/xuất 90 ngày, báo trước 30 và 7 ngày, dữ liệu trên thiết bị không bao giờ bị xoá.

Làm được NGAY (không phụ thuộc PRO-B/PRO-D): kiểm kê, ADR, màn Pro/Ủng hộ, thông báo nhiều thiết bị (nguồn quyền lợi giả
trong test), tắt mọi đường gửi dữ liệu người dùng lên mạng ở bản miễn phí. Thứ tự toàn hệ: phiếu gốc mục 9.5.

**LÀM NGAY - PRO-A**: đưa mục 2 (N1-N8), 3 (thông báo), 8 (quyết định), 9 (hợp đồng chung) của phiếu gốc vào `docs/PRODUCT_POLICY.md` (mục mới "Lưu cục bộ mặc định - đồng bộ là Pro" + bảng giá + mã sản phẩm + JWS + nội dung thông báo vi/en), AUTH_AND_ACCOUNT (mã cài đặt, `X-Tsu-Installation`), FREE_TIER_STACK (N5/N7, hạn mức 100 MiB + 1 GiB), checklist mục 7. Phát hành **v3.9.0**, mở phiếu sync toàn hệ. Thêm `assets/badges/` (PRO-C).
