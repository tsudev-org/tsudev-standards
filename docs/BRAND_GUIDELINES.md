# SỔ TAY NHẬN DIỆN THƯƠNG HIỆU TSUMIND (v1.0.0)

| Mục | Giá trị |
|---|---|
| Phiên bản | 1.1.0 (bộ quy ước `v10.2.0`, 28/11/2026) |
| Nguồn | Sổ tay Quy chuẩn Nhận diện Thương hiệu TSUMIND v1.0 do chủ dự án giao 27/11/2026, chuẩn hoá theo bộ quy ước; hình logo: 5 hình chủ dự án chốt 28/11/2026 |
| Trạng thái | Bắt buộc (Normative) cho mọi sản phẩm, website, tài liệu, kênh truyền thông của hệ sinh thái |
| Đi cùng | [`NAMING_CONVENTION.md`](NAMING_CONVENTION.md) (cách viết tên), [`BRAND_ASSETS.md`](BRAND_ASSETS.md) mục 16 (tệp logo), [`DESIGN_SYSTEM.md`](DESIGN_SYSTEM.md) (token giao diện), [`TSUMIND_MIGRATION.md`](TSUMIND_MIGRATION.md) (lộ trình) |

> Tài liệu này nói về **thương hiệu**: ý nghĩa, biến thể logo, tỷ lệ, màu, phông, giọng văn, điều cấm, bảo hộ.
> Màu giao diện cụ thể (nút, liên kết, nền) lấy từ token - KHÔNG chép mã màu ở đây vào CSS.

## 1. Thương hiệu

**TsuMIND** là hệ sinh thái phần mềm, công cụ và ứng dụng đa nền tảng (Windows, macOS, Linux, Android, iOS), phát triển
từ hệ sinh thái TsuDEV. `Tsu` là dấu ấn người sáng lập, `MIND` là trí tuệ, tư duy: *công cụ thông minh, gọn nhẹ, đáng
tin cậy*.

- **Tuyên ngôn:** "TsuMIND - Công cụ thông minh cho mọi nền tảng."
- **Giá trị cốt lõi:** Thông minh (giải đúng vấn đề) · Tin cậy (an toàn, minh bạch, tôn trọng dữ liệu người dùng) ·
  Đồng bộ (trải nghiệm thống nhất mọi thiết bị) · Bền vững (hệ sinh thái mở rộng liên tục).
- **Tính cách:** công nghệ, sắc sảo, điềm tĩnh, chuyên nghiệp.

### 1.1. Cách viết tên (chủ dự án chốt 27/11/2026)

- Văn bản, giao diện, tài liệu, cửa hàng ứng dụng: **`TsuMIND`** - đúng nguyên dạng ở mọi vị trí
  ([`NAMING_CONVENTION.md`](NAMING_CONVENTION.md) mục 3). Sản phẩm: `TsuCwico`, `TsuSwico`... (mục 3.4).
- Dải chữ **TSUMIND** in hoa trong logo là **đồ hoạ** (kiểu chữ kim loại), không phải cách viết tên. `MUST NOT` gõ
  `TSUMIND` trong văn bản để "giống logo"; `TSUMIND_` chỉ là tiền tố hằng/biến môi trường.
- Giai đoạn chuyển tiếp: "TsuMIND (trước đây là TsuDEV)".

## 2. Ý nghĩa logo

Linh vật **cú công nghệ** trong huy hiệu tròn:

| Thành phần | Ý nghĩa |
|---|---|
| Cú | Trí tuệ, quan sát, cảnh giác - gắn với `MIND` |
| Đôi mắt xanh phát sáng | Tập trung, tầm nhìn |
| Đường mạch điện | Nền tảng công nghệ, kết nối các sản phẩm trong hệ sinh thái |
| Huy hiệu tròn | Tính trọn vẹn của hệ sinh thái; dễ chuyển thành biểu tượng ứng dụng |
| Dải chữ TSUMIND | Nhận diện tên, kiểu chữ kim loại hiện đại |

## 3. Biến thể logo

Tệp ở `assets/brand/tsumind/dist/` (bảng đầy đủ: [`BRAND_ASSETS.md`](BRAND_ASSETS.md) mục 16).

| Biến thể | Tệp | Dùng khi |
|---|---|---|
| Logo chính (huy hiệu + dải chữ) | `logo/tsumind-logo-primary-*` | Trang giới thiệu, ảnh bìa, tài liệu, bao bì số |
| Logo ngang (cú + chữ) | `horizontal/tsumind-logo-horizontal-*` (nền tối), `-light-*` (nền sáng) | Header website, email, thanh điều hướng, tài liệu ngang |
| Biểu tượng (cú trong vòng tròn, không chữ) | `symbol/tsumind-symbol-*` | Ảnh đại diện, watermark, chỗ hẹp |
| Dải chữ | `wordmark/tsumind-wordmark-*` | Ghép cạnh biểu tượng khi bố cục cần tách |
| Biểu tượng ứng dụng | `app-icon/*`: ô vuông nền liền (iOS, cửa hàng), squircle (macOS `.icns`, Windows `.ico`, Linux) | iOS, Android, Windows, macOS, Linux |
| Favicon + PWA | `favicon/*` | Tab trình duyệt, màn hình chính |

**Quy tắc chọn:** vùng hiển thị càng nhỏ, biến thể càng đơn giản. Dưới 64px dùng biểu tượng thu gọn; dưới 32px dùng
favicon (biểu tượng tròn thu nhỏ có làm nét).

## 4. Cấu trúc, vùng an toàn, cỡ tối thiểu

- **Vùng an toàn:** khoảng trống tối thiểu quanh logo bằng **X = chiều cao chữ "T" của dải chữ** (xấp xỉ 1/8 chiều
  rộng logo chính). Không đặt chữ, hình hay mép khung trong vùng này.
- **Cỡ tối thiểu:**

| Biến thể | Màn hình | In ấn |
|---|---|---|
| Logo chính | rộng ≥ 120px | 25 mm |
| Logo ngang | cao ≥ 28px | 8 mm |
| Biểu tượng thu gọn | ≥ 32px | 8 mm |
| Favicon | 16px (bản giản lược riêng) | - |

- Luôn giữ nguyên tỷ lệ (logo chính 1:1, biểu tượng 1:1, logo ngang ~2,2:1).
- **Lưới biểu tượng ứng dụng:** vùng an toàn 80% khung, cú căn giữa; bo góc theo nền tảng - không tự bo trước với iOS.
- Logo là ảnh raster chi tiết: chỉ **thu nhỏ** từ nguồn, `MUST NOT` phóng to quá kích thước nguồn; web dùng
  `<picture>` AVIF → WebP → PNG với `srcset` 1x/2x/3x. Không vector hoá tự động (thử 27/11/2026: mất viền đậm và độ sâu).

## 5. Hệ màu thương hiệu

Giá trị tham chiếu của Sổ tay (cần đối chiếu lại trên tệp vector gốc trước khi in).

| Tên | HEX | RGB | Vai trò |
|---|---|---|---|
| **Midnight Navy** | `#0A1B3D` | 10, 27, 61 | Nền chính; chữ tiêu đề trên nền sáng; `theme-color` |
| **Deep Circuit Blue** | `#13408A` | 19, 64, 138 | Màu phụ, nền khối, đường viền |
| **Electric Blue** | `#1E9BFF` | 30, 155, 255 | Màu nhấn chính (nút, liên kết) - xem lưu ý tương phản |
| **Neon Cyan** | `#3CD2F5` | 60, 210, 245 | Điểm nhấn phát sáng, viền, biểu tượng |
| **Chrome Silver** | `#E4EAF4` | 228, 234, 244 | Chữ trên nền tối, bề mặt sáng |
| **Slate Gray** | `#5B6B85` | 91, 107, 133 | Chữ phụ trên nền sáng, đường kẻ |

- **Tỷ lệ dùng:** 60% Midnight Navy / Deep Circuit Blue · 25% Chrome Silver · 15% Electric Blue + Neon Cyan.
- **Trạng thái giao diện:** dùng token chung `success`/`warning`/`danger` của `design-tokens.json` (đã kiểm WCAG), không
  dùng mã thô của Sổ tay (`#22C55E`, `#F59E0B`, `#EF4444`) cho chữ.
- **Đơn sắc:** trắng trên nền tối; Midnight Navy trên nền sáng; đen 100% khi in một màu (hoá đơn, tem, dấu).

### 5.1. Tương phản đo được (WCAG 2.2, đo 28/11/2026 bằng `scripts/color-lib.mjs`)

| Cặp (chữ / nền) | Tỷ lệ | Kết luận |
|---|---|---|
| Chrome Silver / Midnight Navy | 14,04 | Đạt AAA - chữ thường trên nền tối |
| Chrome Silver / Deep Circuit Blue | 8,16 | Đạt AAA |
| Neon Cyan / Midnight Navy | 9,48 | Đạt AAA |
| Electric Blue / Midnight Navy | 5,81 | Đạt AA (chữ thường) |
| Midnight Navy / trắng | 16,98 | Đạt AAA |
| Slate Gray / trắng | 5,40 | Đạt AA |
| Slate Gray / Midnight Navy | 3,14 | **Trượt chữ thường** - chỉ đường kẻ, chữ ≥ 24px |
| Electric Blue / trắng | 2,92 | **Trượt** - không làm chữ, liên kết, nút chữ trắng trên nền sáng |
| Neon Cyan / trắng | 1,79 | **Trượt** - không bao giờ làm chữ trên nền sáng |

Hệ quả bắt buộc:

- Nút và liên kết ở giao diện lấy từ token `tokens/products/tsumind.json` (`data-product="tsumind"`), sinh từ sắc độ
  Electric Blue (hue 249) và đã qua cổng WCAG: nút chính Tối `#4DAAFF` (chữ mực đen), Sáng `#046CB6` (chữ trắng).
- Nút nền Electric Blue thuần `MUST` dùng chữ Midnight Navy (5,81), `MUST NOT` dùng chữ trắng (2,92).

## 6. Phông chữ (chủ dự án chốt 27/11/2026)

| Vai trò | Phông | Ghi chú |
|---|---|---|
| Tiêu đề, tên sản phẩm | **Exo 2** (SemiBold/Bold) | Có tiếng Việt; token `fontDisplay` của `tsumind` |
| Tiêu đề trang trí cỡ lớn | Orbitron | Chỉ chữ không dấu (không đủ dấu tiếng Việt), cỡ ≥ 32px |
| Nội dung, giao diện | **Inter** (Regular/Medium) | Đủ dấu tiếng Việt; trùng `typography.font-family` chung |
| Mã, thông số, phiên bản | **JetBrains Mono** | |
| Dự phòng | Segoe UI, Roboto, Arial, sans-serif | |

- Tất cả giấy phép SIL OFL. Tự lưu trữ (self-host) - không gọi Google Fonts lúc chạy (quyền riêng tư, 0 đồng).
- Kiểm hiển thị đủ `ă â ê ô ơ ư đ` và 5 dấu thanh trước khi dùng phông mới.
- Thang cỡ web: H1 40/48 · H2 32/40 · H3 24/32 · Nội dung 16/26 · Chú thích 13/20.
- Be Vietnam Pro (bộ logo TM1, đã thay) không còn thuộc bộ nhận diện TsuMIND; sản phẩm khác giữ `fontDisplay` riêng.

## 7. Giọng văn

- Ngắn gọn, rõ ràng, chuyên nghiệp, thân thiện; tránh thổi phồng, không hứa điều không kiểm chứng.
- Cam kết hiển thị nhất quán ở chân trang mọi sản phẩm: tên chủ sở hữu, liên hệ, liên kết chính sách.
- Văn bản do chủ dự án đứng tên ([`AGENT_PROTOCOL.md`](AGENT_PROTOCOL.md) mục 6.1).
- Chi tiết văn phong giao diện: [`ECOSYSTEM_IDENTITY.md`](ECOSYSTEM_IDENTITY.md) mục 8.

## 8. Được phép và điều cấm

**Được phép:** đặt logo trên Midnight Navy, nền tối đồng nhất hoặc nền trắng; co giãn theo tỷ lệ.

**`MUST NOT`:**

- Kéo giãn, nghiêng, xoay, bóp méo; phóng to quá kích thước nguồn.
- Đổi màu ngoài hệ màu; thêm bóng đổ, viền ngoài, hiệu ứng mới.
- Đặt trên nền hoạ tiết rối hoặc tương phản thấp.
- Tách hay sắp xếp lại thành phần (cú, mạch, dải chữ) ngoài các biến thể ở mục 3.
- Thay dải chữ bằng phông khác hay gõ lại bằng chữ.
- Dùng logo để ngụ ý bảo trợ, hợp tác, chứng nhận không có thật.

## 9. Bảo hộ thương hiệu - việc của chủ dự án

Agent không làm thay các bước pháp lý; chỉ chuẩn bị tài liệu khi được yêu cầu.

1. Tra cứu trùng/tương tự ("TsuMIND", logo hình cú) ở Cục Sở hữu trí tuệ và WIPO Global Brand Database.
2. Đăng ký nhãn hiệu "TsuMIND" + logo tại Cục Sở hữu trí tuệ Việt Nam - nhóm gợi ý **9** (phần mềm tải về), **42**
   (dịch vụ phần mềm), **35** (nếu có thương mại điện tử).
3. Đăng ký quyền tác giả logo và phần mềm tại Cục Bản quyền tác giả.
4. Giữ hồ sơ chứng minh: tệp gốc, ngày tạo, lịch sử phiên bản (repo này giữ tệp nguồn + chuỗi băm `MANIFEST.json`).
5. Tên miền: `tsumind.com` đã đăng ký (Cloudflare Registrar); cân nhắc `.vn`, `.app`, `.dev`.
6. Dùng ™ khi chưa có văn bằng; ® chỉ sau khi được cấp.

> **Lưu ý nguồn gốc hình:** logo được tạo với sự hỗ trợ của công cụ AI. Quyền tác giả với hình do AI tạo có thể bị hạn
> chế - trước khi đăng ký nên có nhà thiết kế hoặc luật sư sở hữu trí tuệ rà tính phân biệt và quyền tác giả.

## 10. Triển khai đa nền tảng

| Nền tảng | Chuẩn |
|---|---|
| Website | Header: logo ngang cao 36-44px; chân trang: logo ngang (đơn sắc khi nền phức tạp). `<head>`: `favicon.ico` + PNG 32px, `apple-touch-icon` 180px, PWA 192/512 + maskable, `theme-color` `#0A1B3D`. Open Graph 1200x630 (`social/og-image-1200x630.png`) |
| Windows | `app-icon/tsumind-app.ico` 16/24/32 (biểu tượng tròn) + 48/64/128/256 (squircle) |
| macOS | `app-icon/tsumind.icns` (squircle theo lưới Apple 824/1024, 16-1024 gồm @2x) |
| Linux | `app-icon/linux/hicolor/<cỡ>/apps/tsumind.png` 16-512px |
| Android | Adaptive icon 108dp, vùng an toàn 66dp: nền `android-adaptive-background-1024.png` (Midnight Navy), trước `android-adaptive-foreground-1024.png` (cú); themed icon `android-adaptive-monochrome-1024.png`; ảnh cửa hàng `google-play-icon-512.png` |
| iOS | 1024x1024 vuông, không trong suốt, không tự bo góc (`app-icon/tsumind-app-icon-1024.png`) |

**Sản phẩm con:** giữ logo riêng ([`BRAND_ASSETS.md`](BRAND_ASSETS.md) mục 15) và bản sắc màu riêng
(`tokens/products/<id>.json`); nối về nhà chung bằng khối "Thuộc hệ sinh thái TsuMIND"
([`ECOSYSTEM_IDENTITY.md`](ECOSYSTEM_IDENTITY.md) mục 4.4). Tên sản phẩm theo [`NAMING_CONVENTION.md`](NAMING_CONVENTION.md)
mục 3.4. Khung huy hiệu chung cho icon sản phẩm con (Sổ tay mục 8) là việc thiết kế sau, cần chủ dự án duyệt từng icon.

## 11. Lộ trình

Theo [`TSUMIND_MIGRATION.md`](TSUMIND_MIGRATION.md) và [`PLAN.md`](PLAN.md) (Phase TM1-TM11). Sau chuyển đổi giữ
`tsudev.com` chuyển hướng vĩnh viễn (D-10), tối thiểu 12-24 tháng theo Sổ tay.

## 12. Cập nhật sổ tay

Đổi nhận diện ⇒ chủ dự án thay hình ở `assets/brand/tsumind/source/original/`, chạy `tools/make_masters.py` rồi `build.mjs`
([`BRAND_ASSETS.md`](BRAND_ASSETS.md) mục 16.1), nâng phiên bản tài liệu này và ghi
`CHANGELOG.md`. Lưu tệp vector gốc (SVG/AI) khi chủ dự án có.
