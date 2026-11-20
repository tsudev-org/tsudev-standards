# Huy hiệu Pro / Ủng hộ - SVG gốc (từ v3.9.0)

Bản vẽ gốc cho huy hiệu ở [`docs/PRODUCT_POLICY.md`](../../docs/PRODUCT_POLICY.md) mục 4. Component dùng chung (Flutter
`TsuBadge` trong `tsudev_ui`, web `<TsuBadge>` trong `@tsudev/ui`) và bản vẽ lại cho desktop .NET/Rust/C++ `MUST` lấy
đúng màu, hình và kích thước ở đây - repo sản phẩm KHÔNG tự thiết kế bản riêng.

| Tệp | Dùng khi | Nền | Viền | Chữ + biểu tượng |
| --- | --- | --- | --- | --- |
| `tsu-badge-pro.svg` | Pro, mọi giao diện | chuyển sắc ngang `#30C8F0` → `#1E90FF` | - | `#0A0A0A`, chữ `PRO` |
| `tsu-badge-donor-light.svg` / `-en-light` | Ủng hộ, giao diện Sáng | `#CCFBF1` | `#0F766E` | `#134E4A`, trái tim + `Ủng hộ` / `Supporter` |
| `tsu-badge-donor-dark.svg` / `-en-dark` | Ủng hộ, giao diện Tối | `#042F2E` | `#2DD4BF` | `#99F6E4`, trái tim + `Ủng hộ` / `Supporter` |

Tương phản chữ/nền (WCAG 2.1, đo 20/11/2026): `PRO` 6.12:1 (điểm tối nhất của chuyển sắc) - 10.04:1; Ủng hộ Sáng
8.41:1; Ủng hộ Tối 11.48:1. Viền Ủng hộ với nền trang: Sáng 5.47:1 trên `#FFFFFF`, Tối 10.64:1 trên `#0A0A0A`.

- Hình: pill, cao 20 đơn vị trong SVG; khi dùng thật cao **0,75 × chiều cao dòng** của tên, 16-20 px, cách tên 4-6 px.
- Chữ đậm 700, phông hệ thống của sản phẩm; SVG dùng `textLength` để không tràn khi thiếu phông Inter. Component nên
  vẽ chữ thật (không nhúng SVG chữ) để đọc màn hình và phóng chữ hoạt động.
- Chuyển động (shimmer của Pro mỗi 6-8 giây, tim Ủng hộ đập nhẹ khi rê/chạm) do component làm, KHÔNG nằm trong SVG;
  tắt khi giảm chuyển động.
- Nhãn đọc màn hình: `Tài khoản Pro` / `Đã ủng hộ TsuDEV` (en: `Pro account` / `Supported TsuDEV`).
