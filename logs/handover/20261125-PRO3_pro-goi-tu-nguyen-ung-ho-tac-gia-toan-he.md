# PHIẾU ĐIỀU PHỐI PRO3 - Pro là gói TỰ NGUYỆN ủng hộ tác giả; mọi sản phẩm miễn phí, mã nguồn mở

- **Mã phiếu**: 20261125-PRO3 - **Từ**: điều phối `projects-d6`, 25/11/2026 - **Trạng thái**: MỞ
- **Quyết định chủ dự án (25/11/2026)**: mọi dự án TsuDEV xây dựng, phát hành **miễn phí, mã nguồn mở** để cộng đồng dùng
  và đóng góp trên GitHub. **Giữ TsuDEV Pro 490.000 ₫ / 1 năm** nhưng **không bắt buộc**: người dùng tự chọn để ủng hộ
  tác giả, đổi lại tài khoản có chữ **Pro** và giao diện riêng; màn mua nói rõ đây là lựa chọn tự nguyện. Chủ dự án uỷ
  quyền phiên điều phối chọn phương án chi tiết.
- **Chuẩn**: tsudev-standards **v6.1.0**, `PRODUCT_POLICY.md` v1.3.0 **mục 3.7** (đọc nguyên văn, phiếu này chỉ tóm tắt
  và chia việc). Không đổi: giá, kỳ 1 năm không tự gia hạn, mã cửa hàng, JWS, đồng bộ (mục 7, phiếu PRO2).
- **Liên quan**: `20261120-PRO2` (kỳ 1 năm), `20261124-DK2` (Bộ Công Thương), `20261125-SEC2` (nhãn tin cậy kiểm chứng được).

## 0. Mọi agent MUST đọc - tóm tắt mục 3.7

1. **Quyền lợi Pro = danh sách đóng**: Q1 huy hiệu Pro cạnh tên · Q2 giao diện Pro (chủ đề màu thêm, biểu tượng app thay
   thế, khung ảnh đại diện - lấy từ `tsudev_ui` / `@tsudev/ui`) · Q3 đồng bộ + sao lưu đám mây E2EE. Thêm quyền lợi riêng
   ⇒ ADR + chủ dự án duyệt, chỉ được là tiện nghi thêm.
2. **Miễn phí mãi**: tính năng cốt lõi, Sáng/Tối/Hệ thống, cỡ chữ, tương phản cao, giảm chuyển động, mọi hỗ trợ tiếp cận,
   ngôn ngữ, xuất/nhập/sao lưu ra tệp, bảo mật, cập nhật bảo mật. Giao diện Pro chỉ THÊM lựa chọn, không làm bản miễn phí
   xấu đi. Huy hiệu Pro không dùng dấu tích/khiên/"Đã xác minh".
3. **Mời mua không thao túng**: lối vào Pro chỉ ở Tài khoản/Cài đặt, Giới thiệu, `tsudev.com/pro` và hai hộp thoại đã
   duyệt (7.3, 7.6). Không đếm ngược, không giảm giá giả, không confirmshaming, không chọn sẵn, không chèn giữa luồng chính.
4. **Màn mua** (mọi kênh) TRƯỚC nút thanh toán: câu định vị nguyên văn → quyền lợi đang chạy thật → điều khoản 7.5 + liên
   kết `/chinh-sach-thanh-toan` → **ô xác nhận không chọn sẵn** (nguyên văn vi/en ở 3.7.3).
5. **Gọi đúng tên**: văn bản pháp lý gọi Pro là "gói dịch vụ"; "ủng hộ tác giả" là tinh thần đặt cạnh. Ủng hộ 20k-200k
   mới là đóng góp. **Cấm** "tổ chức phi lợi nhuận / non-profit / từ thiện / tax-deductible" trong nội dung công khai.
6. **Pháp lý**: chỉ `tsudev.com` nhận thanh toán web; website sản phẩm chỉ liên kết `tsudev.com/pro?app=` /
   `ung-ho?app=`. Logo Bộ Công Thương chỉ trên đúng tên miền được duyệt (hiện: chưa có - DK2 đang chặn). Website tự bán
   sau này (dịch vụ thiệp cưới, OCOP, …) cần hồ sơ BCT riêng TRƯỚC khi bán; sàn nhiều người bán ⇒ dừng, 👤 quyết.
7. **Mã nguồn mở**: mã kiểm Pro không làm rối. Fork tự bật Q2 được - chấp nhận; Q1, Q3 do máy chủ tsudev.com kiểm.
8. Quy tắc chung: chỉ sửa repo mình; repo có phiên khác ⇒ phiếu + SendMessage; commit/PR KHÔNG ghi đồng tác giả AI.

## 1. Việc theo repo

| Repo | Việc PRO3 |
| --- | --- |
| **tsudev** (tsudev.com) | (a) `/pro`: câu định vị + ô xác nhận (nút "Đăng nhập để mua"/"Mua" vô hiệu tới khi đánh dấu), quyền lợi chỉ liệt kê cái đang chạy; (b) `/chinh-sach-thanh-toan`, `/terms`: gọi Pro là "gói dịch vụ không bắt buộc", thêm Q2 khi chạy thật, điều khoản fork không dùng tên "TsuDEV Pro"/máy chủ tsudev.com, cập nhật `PAYMENT_DOC_DATES`; (c) Q2 web: chủ đề Pro trong `@tsudev/ui` + Cài đặt → Giao diện; (d) rà toàn site: không chữ "phi lợi nhuận/non-profit", lối vào Pro đúng chỗ; (e) logo BCT ở `SiteFooter.tsx` CHỈ sau khi DK2 được duyệt (mã nhúng của cổng, ảnh tự host, alt tiếng Việt); (f) rà mô tả `/apps`, README: "miễn phí, mã nguồn mở". Đổi trang chính sách ⇒ báo điều phối để khai sửa đổi hồ sơ BCT |
| **tsudev-ui-flutter** | `ProPurchaseSheet` (câu định vị + quyền lợi + điều khoản + ô xác nhận, vi/en, test), bộ chủ đề Pro (Q2) theo token, `TsuBadge` không dấu tích; phát hành bản MINOR rồi báo các repo Flutter |
| **tsusync** | Không đổi hành vi. Rà README/tài liệu: Q3 là quyền lợi Pro, không chữ "phi lợi nhuận" |
| App/tool (qulythuchi, tsuscan, tsufiles, tsuswico, tsucwico, tsucontact, tsudev-trafficmonitor/Tsu Tramon, tsudisk, sound-db, lotus-share/tsudev-lotus, app-la-ban) | (a) rà lối vào Pro (mục 0.3) và gỡ chỗ sai; (b) màn mua đúng 0.4 (Flutter dùng `ProPurchaseSheet` khi có; desktop/web mở `tsudev.com/pro?app=`); (c) bảo đảm mục 0.2 miễn phí; (d) Q2 khi `tsudev_ui`/`@tsudev/ui` có chủ đề Pro; (e) website sản phẩm không tự nhận tiền, không logo BCT, không "phi lợi nhuận"; (f) README: "Miễn phí, mã nguồn mở; TsuDEV Pro là tuỳ chọn để ủng hộ tác giả" |
| Trò chơi TsuGameLabs (game-kit + từng game) | Như dòng App; game-kit làm phần dùng chung trước |
| **tsudev-standards** | Đã làm: v6.1.0 (PR `docs/pro3-goi-tu-nguyen`) |
| **wedding-sumy** | Chỉ mục 0.6: hiện là thiệp cưới cá nhân, nhận tiền mừng qua VietQR - KHÔNG phải bán hàng, không cần BCT. Nếu sau này bán dịch vụ thiệp cho người khác ⇒ hồ sơ BCT riêng trước khi mở bán |
| Không áp dụng | Repo UBND/xanuicam (không thuộc hệ TsuDEV), homebrew-tap, scoop-bucket, linux-packages, b4djl1h-cmdb, mieubathuong |

## 2. Việc 👤 chủ dự án

1. **DK2 - Bộ Công Thương**: tài khoản online.gov.vn đã duyệt nhưng thiếu "thông tin doanh nghiệp" ⇒ biểu mẫu báo
   "TaxCode là bắt buộc", không nộp được. Gọi **024 222 05 395** (hỗ trợ tài khoản) hỏi cách gắn MST cá nhân kinh doanh
   vào tài khoản (hoặc đăng nhập VNeID). Xong ⇒ báo phiên điều phối chạy lại biểu mẫu đã soạn sẵn.
2. Duyệt PR tsudev-standards v6.1.0.

## 3. Bảng theo dõi

| Repo | Trạng thái | PR / ghi chú |
| --- | --- | --- |
| tsudev-standards | 🟡 PR mở | v6.1.0 |
| tsudev | ⬜ | |
| tsudev-ui-flutter | ⬜ | |
| tsusync | ⬜ | |
| các repo app/game | ⬜ | mỗi repo ghi dòng của mình ở bản sao |

## 4. Điều kiện đóng

Mọi hàng mục 3 xong hoặc "không áp dụng" có lý do; `/pro` production có câu định vị + ô xác nhận; không còn chữ
"phi lợi nhuận/non-profit" công khai (grep toàn hệ); DK2 hàng BCT có trạng thái cuối.

## 5. Kết quả xử lý

- 25/11/2026 - projects-d6: mở phiếu; tsudev-standards v6.1.0 (PRODUCT_POLICY 3.7); gửi bản sao vào `logs/handover/`
  từng repo; nhắn phiên đang chạy.
