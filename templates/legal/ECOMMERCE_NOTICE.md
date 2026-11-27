# Mẫu chuẩn bị thông báo website thương mại điện tử (Bộ Công Thương, `online.gov.vn`)

> Mẫu chuẩn bị, không thay tờ khai chính thức. Căn cứ: Luật Thương mại điện tử 122/2025/QH15; NĐ 248/2026/NĐ-CP Điều 23, 24
> (hiệu lực 01/07/2026; NĐ 52/2013 và 85/2021 hết hiệu lực). Tờ khai thật: **Mẫu số 01 Phụ lục II** NĐ 248/2026, tải ở
> `online.gov.vn` hoặc `vbpl.vn`. **[OWNER] khai, ký, nộp; agent không nộp thay.**

## 1. Xác định diện

| Câu hỏi | Trả lời | Hệ quả |
| --- | --- | --- |
| Web có chức năng đặt hàng/thanh toán trực tuyến bán gói Pro của chính mình? | [OWNER] (28/11/2026: có chức năng mua gói Pro) | Nền tảng **kinh doanh trực tiếp có chức năng đặt hàng trực tuyến**: phải **được xác nhận thông báo trước khi vận hành** (Điều 23 khoản 1) |
| Web chỉ giới thiệu, thanh toán hoàn toàn trong cửa hàng ứng dụng? | [OWNER] | Nghĩa vụ nhẹ hơn; vẫn công bố thông tin chủ sở hữu. **Cần xác minh** với Sở Công Thương |
| Có mở chợ cho người bán bên thứ ba? | Không (chính sách hiện tại) | Không thuộc diện đăng ký nền tảng trung gian |

## 2. Cơ quan, quy trình

- UBND cấp tỉnh xác nhận thông báo (Điều 24 khoản 5), qua Hệ thống quản lý hoạt động TMĐT. Quy trình theo Mục 1 Phụ lục I NĐ 248/2026.
- Cổng nộp: `online.gov.vn`. Kinh nghiệm DK2 (AKB `tsudev#LES-20261124-2353-23b4`, theo NĐ cũ): tài khoản cá nhân đăng ký ở
  `dichvucong.moit.gov.vn`, Bộ duyệt tài khoản trước khi nộp; trang tải lại khi lỗi nên xoá tệp CCCD và mật khẩu đã nhập. Đối chiếu
  lại với quy trình theo NĐ 248/2026 (**cần xác minh**).
- Chủ thể là cá nhân không đăng ký kinh doanh: **cần xác minh** với Sở Công Thương có được thông báo hay phải đăng ký hộ kinh doanh/doanh nghiệp.

## 3. Hồ sơ (Điều 24 khoản 1)

- [ ] Tờ khai Mẫu số 01 Phụ lục II: [OWNER điền theo `OWNER_INFO.md`]
- [ ] Giấy phép/chứng chỉ nếu bán hàng hoá, dịch vụ thuộc ngành có điều kiện (phần mềm thông thường: thường không); [OWNER xác nhận]
- [ ] Nội dung công khai trên website khớp tờ khai: thông tin chủ quản, chính sách bảo mật, khiếu nại, giá, thanh toán, hoàn tiền,
      cung cấp và chấm dứt dịch vụ (NĐ 248 Điều 4, 5, 7, 8, 10, 15, 16): `FOOTER_OWNER.md`, `PRIVACY_POLICY.md`, `TERMS_OF_USE.md`, `/chinh-sach-thanh-toan`

## 4. Sau khi được xác nhận

- Đặt biểu tượng/số xác nhận ở chân trang đúng hướng dẫn của `online.gov.vn`.
- **Đổi tên miền hoặc tên ứng dụng (TM10), đổi người chịu trách nhiệm, đổi giấy tờ đăng ký, đổi điều kiện giao dịch: sửa đổi trong 20 ngày làm việc** (Điều 23 khoản 3). Đổi mã số thuế: chấm dứt thông báo và thông báo lại (khoản 4 điểm c).
- Nếu đã có xác nhận trước 01/07/2026: được hoạt động theo nội dung cũ đến hết **30/06/2027**, trong thời gian đó phải sửa đổi theo NĐ 248 (Điều 53).
- Ngừng hoạt động hoặc chuyển nhượng: chấm dứt thông báo (khoản 4 điểm b).
- Cơ quan có thể chấm dứt nếu không phản hồi yêu cầu qua hệ thống quá 30 ngày (khoản 5): theo dõi hộp thư đăng ký.

## 5. Bằng chứng lưu riêng tư
Tờ khai đã nộp, số xác nhận, ảnh chụp trang xác nhận (xoá thông tin định danh nhạy cảm), ngày nộp. Không đưa CCCD, mật khẩu, mã OTP vào repo, AKB hay phiếu.
