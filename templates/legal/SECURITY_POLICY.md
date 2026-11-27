# Mẫu Chính sách an toàn thông tin

> Mẫu, không thay tư vấn pháp lý. Căn cứ: Luật An ninh mạng 116/2025/QH15 (hiệu lực 01/07/2026, thay Luật ATTT mạng 2015 và Luật
> ANM 2018); Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15; NĐ 356/2025/NĐ-CP. Chuẩn kỹ thuật nội bộ: `docs/SECURITY_BASELINE.md`.
> Chỉ ghi điều **đang thực hiện thật**. Hiệu lực: [OWNER: DD/MM/YYYY].

## 1. Mục tiêu

Bảo đảm bảo mật, toàn vẹn, sẵn sàng của hệ thống và dữ liệu người dùng trong toàn bộ hệ sinh thái TsuMIND.

## 2. Biện pháp kỹ thuật

- Mã hoá khi truyền TLS 1.2 trở lên; HSTS; dữ liệu nhạy cảm mã hoá khi lưu; mật khẩu băm bằng thuật toán hiện đại, không lưu bản rõ.
- Xác thực nhiều lớp (passkey, 2FA) cho quản trị; phân quyền tối thiểu; nhật ký truy cập lưu [OWNER: số ngày] ngày.
- Vá lỗi định kỳ, quét phụ thuộc và mã (Dependabot, CodeQL, quét bí mật); phụ thuộc ghim phiên bản.
- Bản phát hành ký số, công bố giá trị băm; ứng dụng **chứng thực toàn vẹn** và bắt buộc cập nhật bản mới nhất.
- Bí mật quản lý bằng kho bí mật của nền tảng, không đưa vào mã nguồn; xoay khoá theo quy trình.
- Sao lưu mã hoá, kiểm tra khôi phục; tách môi trường phát triển và vận hành.

## 3. Biện pháp quản lý

- Phụ trách an toàn thông tin: [OWNER: họ tên, email security@...].
- Hợp đồng bảo mật và xử lý dữ liệu với nhà cung cấp; đánh giá nhà cung cấp trước khi dùng.
- Soát xét chính sách ít nhất mỗi năm.

## 4. Báo cáo lỗ hổng

Gửi security@[OWNER] hoặc theo `/.well-known/security.txt`. Xác nhận trong 5 ngày làm việc; không truy cứu người báo cáo thiện chí,
không phá hoại, không lấy dữ liệu người dùng.

## 5. Ứng phó sự cố

1. Phát hiện, ghi nhận (thời gian, hệ thống, loại dữ liệu, số lượng).
2. Cô lập, ngăn lan rộng; xoay khoá nếu liên quan bí mật.
3. Đánh giá phạm vi dữ liệu cá nhân bị ảnh hưởng.
4. Lập biên bản; **thông báo cơ quan chuyên trách của Bộ Công an chậm nhất 72 giờ** kể từ khi phát hiện (Mẫu 08, Luật 91/2025 Điều 23, NĐ 356 Điều 28) và thông báo người bị ảnh hưởng.
5. Khắc phục, rút kinh nghiệm, cập nhật biện pháp.

## 6. Hợp tác với cơ quan nhà nước

Đầu mối: [OWNER: họ tên, email, điện thoại trực 24 giờ]. Theo Luật ANM Điều 25 khoản 2, khi lực lượng chuyên trách bảo vệ an ninh
mạng thuộc Bộ Công an yêu cầu bằng văn bản, thư điện tử, điện thoại hoặc hình thức đã xác nhận:

| Yêu cầu | Hạn |
| --- | --- |
| Cung cấp thông tin người dùng | 24 giờ (khẩn cấp đe dọa an ninh quốc gia, tính mạng: 03 giờ) |
| Ngăn chặn chia sẻ, xoá thông tin, gỡ dịch vụ/ứng dụng vi phạm | 24 giờ (khẩn cấp đe dọa an ninh quốc gia: 06 giờ) |

Mọi yêu cầu được ghi nhật ký (ai, khi nào, nội dung, người xử lý); không trả lời ngoài thẩm quyền, báo chủ sở hữu ngay.

## 7. Lưu trữ nhật ký và dữ liệu theo luật

Thời hạn lưu thông tin người dùng sau khi kết thúc dịch vụ và việc lưu dữ liệu tại Việt Nam: theo nghị định hướng dẫn Luật ANM 2025
([OWNER: cập nhật khi ban hành; hiện cần xác minh]).
