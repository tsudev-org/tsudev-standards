# Mẫu hồ sơ đánh giá tác động xử lý dữ liệu cá nhân (Bộ Công an)

> Mẫu **khung nội dung**, không thay biểu mẫu chính thức. Biểu mẫu thật: **Mẫu số 10** (báo cáo đánh giá tác động xử lý DLCN),
> **Mẫu số 09** (chuyển xuyên biên giới), **Mẫu số 02a/02b** (thông báo gửi hồ sơ) tại Phụ lục NĐ 356/2025/NĐ-CP. Tải bản gốc ở
> Cổng thông tin quốc gia về bảo vệ DLCN hoặc `vbpl.vn`; `MUST` dùng đúng biểu mẫu đó khi nộp.
> Căn cứ: Luật 91/2025/QH15 Điều 21, 22 (và 20 cho xuyên biên giới); NĐ 356/2025 Điều 18, 19, 20.
> **[OWNER] quyết định có nộp hay không** theo `docs/LEGAL_COMPLIANCE.md` mục 5; tệp này luôn giữ riêng tư, không đăng công khai.

## Phần A. Hồ sơ đánh giá tác động xử lý DLCN (NĐ 356 Điều 19)

Hồ sơ gồm: (a) Báo cáo Mẫu 10; (b) bản sao hợp đồng/thoả thuận xử lý dữ liệu với nhà cung cấp; (c) chính sách, quy trình, biểu mẫu
về bảo vệ DLCN (dùng `PRIVACY_POLICY.md`, `DSR_PROCEDURE.md`, `SECURITY_POLICY.md`). Nộp 01 bản chính (trực tuyến, trực tiếp hoặc
bưu chính) kèm Mẫu 02a (tổ chức) hoặc 02b (cá nhân) **trong 60 ngày** từ ngày bắt đầu xử lý. Cơ quan trả kết quả trong 15 ngày;
yêu cầu hoàn thiện trong 30 ngày.

### 1. Bên kiểm soát và liên hệ (điểm a, b)
- Bên kiểm soát: [OWNER] · MST [OWNER] · địa chỉ [OWNER] · điện thoại, email [OWNER]
- Bên xử lý/bên thứ ba: [OWNER: Cloudflare, Resend, đối tác thanh toán, GitHub; vai trò từng bên]
- Nhân sự bảo vệ DLCN: [OWNER: họ tên, liên hệ, số văn bản chỉ định]

### 2. Mục đích, loại dữ liệu, hoạt động xử lý, sơ đồ luồng (điểm c)

| Hoạt động | Mục đích | Loại dữ liệu | Cơ sở | Nơi lưu | Lưu bao lâu |
| --- | --- | --- | --- | --- | --- |
| Đăng nhập cổng `id.` | Xác thực | email, tên, ảnh, mã nhà cung cấp | đồng ý/hợp đồng | [OWNER] | [OWNER] |
| Cập nhật, chứng thực ứng dụng | An toàn bản phát hành | IP, phiên bản, thiết bị | lợi ích hợp pháp | [OWNER] | [OWNER] |
| Thanh toán gói Pro | Giao dịch | mã đơn, gói, trạng thái | hợp đồng | [OWNER] | theo luật kế toán |
| Hỗ trợ | Trả lời yêu cầu | nội dung thư | đồng ý | [OWNER] | [OWNER] |
| Nhật ký an ninh | Phát hiện lạm dụng | IP, thời điểm, hành động | nghĩa vụ pháp lý | [OWNER] | [OWNER] |

Sơ đồ luồng dữ liệu: [OWNER: chèn sơ đồ; mỗi mũi tên ghi loại dữ liệu và giao thức]. Dữ liệu trong ứng dụng **chỉ ở thiết bị** (`PRODUCT_POLICY.md`).

### 3. Xin đồng ý, lưu, xoá, huỷ (điểm d)
Cách xin đồng ý (nút không tích sẵn, nhật ký bằng chứng), chính sách lưu và xoá: [OWNER: mô tả; tham chiếu NĐ 356 Điều 6].

### 4. Phương án bảo đảm an toàn (điểm đ)
Biện pháp (mã hoá, phân quyền, nhật ký, sao lưu, ký bản phát hành), sơ đồ hệ thống, tiêu chuẩn áp dụng: [OWNER: tham chiếu `SECURITY_POLICY.md` và `SECURITY_BASELINE.md`].

### 5. Kết quả đánh giá tuân thủ (điểm e)
Đối chiếu từng nghĩa vụ trong `docs/LEGAL_COMPLIANCE.md` mục 4.1: [OWNER: đạt/chưa đạt, hạn khắc phục].

### 6. Rủi ro và biện pháp giảm thiểu (điểm g)

| Rủi ro | Khả năng | Mức ảnh hưởng | Biện pháp |
| --- | --- | --- | --- |
| Lộ cơ sở dữ liệu tài khoản | [OWNER] | [OWNER] | mã hoá, tối thiểu quyền, quét bí mật |
| Lộ bí mật vận hành | [OWNER] | [OWNER] | `SECURITY_BASELINE.md` mục 12, xoay khoá |
| Nhà cung cấp lộ dữ liệu | [OWNER] | [OWNER] | hợp đồng xử lý dữ liệu, giảm tối thiểu dữ liệu gửi đi |

### 7. Cập nhật
Cập nhật **mỗi 06 tháng khi có thay đổi**, và **ngay** khi tổ chức lại/chấm dứt, đổi bên cung cấp dịch vụ bảo vệ DLCN, hoặc đổi
ngành nghề/dịch vụ liên quan (Luật 91/2025 Điều 22). Chuyển `tsudev.com` sang `tsumind.com` (TM10): cập nhật nếu hạ tầng đổi.
Cập nhật trên Cổng thông tin quốc gia hoặc tại cơ quan chuyên trách.

## Phần B. Hồ sơ đánh giá tác động chuyển DLCN xuyên biên giới (Mẫu 09; NĐ 356 Điều 17, 18)

Chỉ lập nếu dữ liệu cá nhân của người dùng Việt Nam được chuyển, lưu hoặc xử lý ở nước ngoài.

| Mục | Nội dung |
| --- | --- |
| Bên chuyển, bên nhận, quốc gia | [OWNER: nhà cung cấp, quốc gia] |
| Dữ liệu chuyển, mục đích | [OWNER] |
| Cơ sở pháp lý và hợp đồng chuyển giao | [OWNER: bản sao hợp đồng] |
| Biện pháp bảo vệ | [OWNER] |
| Đánh giá rủi ro | [OWNER] |

## Việc [OWNER]
Quyết định nộp; ký; chọn kênh nộp; theo dõi kết quả 15 ngày; giữ bản lưu. Agent không ký, không nộp.
