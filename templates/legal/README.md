# templates/legal - Bộ mẫu tài liệu pháp lý TsuMIND

> **Mẫu, không phải tư vấn pháp lý.** Căn cứ và trích dẫn: [`../../docs/LEGAL_COMPLIANCE.md`](../../docs/LEGAL_COMPLIANCE.md)
> (ngày tra 28/11/2026). Chủ dự án `[OWNER]` điền, ký, nộp; luật sư rà soát trước khi công bố.

## Cách dùng

1. Chép mẫu sang repo `tsudev` (website) hoặc repo sản phẩm; **không** sửa trực tiếp bản trong `.standards/`.
2. Điền mọi trường `[OWNER: ...]`; xoá dòng không áp dụng; bỏ khối "Hướng dẫn" (dòng bắt đầu bằng `>`) trước khi đăng.
3. Mỗi trường `[OWNER]` còn sót `MUST` làm cổng kiểm của repo đích đỏ (đề xuất `grep -rn "\[OWNER"` trong CI của repo đích).
4. Không ghi bí mật, số CCCD, địa chỉ nhà riêng, số tài khoản vào mẫu.

## Danh mục

| Tệp | Dùng cho | Đặt ở |
| --- | --- | --- |
| `FOOTER_OWNER.md` | Chân trang mọi website, màn "Giới thiệu" của app | Chân trang |
| `OWNER_INFO.md` | Thông tin chủ sở hữu, danh mục sản phẩm, người phụ trách | `/about`, `/gioi-thieu` |
| `PRIVACY_POLICY.md` | Chính sách bảo vệ dữ liệu cá nhân | `/privacy` |
| `TERMS_OF_USE.md` | Điều khoản sử dụng | `/terms` |
| `SECURITY_POLICY.md` | Chính sách an toàn thông tin, ứng phó sự cố, đầu mối yêu cầu pháp lý | `/security` |
| `COOKIE_POLICY.md` | Cookie và công nghệ theo dõi | `/cookie` |
| `DPIA_DOSSIER.md` | Hồ sơ đánh giá tác động xử lý DLCN (Mẫu 10) và chuyển xuyên biên giới (Mẫu 09) | Lưu riêng tư; nộp Bộ Công an |
| `ECOMMERCE_NOTICE.md` | Chuẩn bị thông báo website TMĐT (Mẫu 01 Phụ lục II NĐ 248/2026) | Lưu riêng tư; nộp `online.gov.vn` |
| `DSR_PROCEDURE.md` | Quy trình xử lý yêu cầu của chủ thể dữ liệu | Nội bộ + tóm tắt ở `/privacy` |
| `BRAND_TRANSITION_NOTICE.md` | Thông báo chuyển TsuDEV sang TsuMIND | Banner/trang `/chuyen-doi-thuong-hieu` |

Văn phong: tiếng Việt, "TsuMIND", chỉ dùng gạch ngang ngắn `-`, ngày `DD/MM/YYYY`.
