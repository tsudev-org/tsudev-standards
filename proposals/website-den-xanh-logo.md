# Đề xuất: bảng màu website hệ sinh thái đổi "đen tuyền + tím" thành "đen tuyền + xanh logo"

> **Trạng thái**: chờ duyệt. Gửi từ repo `tsudev-org/tsudev` (phiên 57, 16/11/2026).
> Đích sửa nếu được nhận: `docs/ECOSYSTEM_IDENTITY.md` (mục bảng màu website) và câu dẫn ở
> `docs/DESIGN_SYSTEM.md` dòng 16-17. KHÔNG đụng `tokens/design-tokens.json` (bảng chuẩn): đây là lớp ghi đè cấp
> website, giống bảng tím hiện tại.

## Vì sao

- Chủ dự án chốt 16/11/2026: tsudev.com đổi sang **đen tuyền + xanh lấy từ logo** (`logo-tsudev.png`: xanh lơ
  ~`#30C8F0`, xanh dương chữ "dev" ~`#1E90FF`). Đã chạy production: tsudev#284 (`v2026.11.16.4`),
  trafficmonitor#68.
- Bộ quy ước v3.6.0 vẫn ghi tím (`#A970FF` / `#7C3AED`) là bảng của website hệ sinh thái. Repo con làm theo quy ước
  sẽ dựng lại tím - đúng kiểu lệch im lặng mà không cổng nào bắt.
- Ngoại lệ đã có quyết định riêng: **lotus.tsudev.com giữ tím hoa sen** (nhận diện riêng, 11/11). Đề xuất ghi ngoại
  lệ này tường minh thay vì để nó trông như lệch quy ước.

## Bảng đề xuất (thay bảng tím; các dòng nền/viền/chữ thường GIỮ - tsudev.com chỉ đổi sắc lạnh của bề mặt)

| Vai trò | Tối | Sáng |
| --- | --- | --- |
| `bg-base` / `bg-surface` / `bg-subtle` / `bg-hover` | `#0A0A0A` / `#0F1114` / `#15181D` / `#1C2027` | giữ `#FAFAFA` / `#FFFFFF` / `#F4F4F5` / `#EBEBED` |
| `border` / `border-strong` / `border-control` | `#22272F` / `#2C323C` / `#6E6E6E` | giữ |
| `text-link` | `#7DD3FC` | `#0757A3` |
| `primary` / `primary-hover` / `primary-active` | `#38BDF8` / `#7DD3FC` / `#0EA5E9` | `#0868C4` / `#0757A3` / `#064785` |
| `on-primary` | `#0A0A0A` (mực đen - giữ quy tắc hiện có) | `#FFFFFF` |
| `focus-ring` | `#38BDF8` | `#0868C4` |
| nhấn phụ `accent` / quầng `glow` | `#3B9EFF` / `rgba(56,189,248,0.14)` | `#0E7490` / `rgba(8,104,196,0.10)` |

Nguồn sự thật đang chạy: `tsudev-org/tsudev` `tokens/extensions.tsudev-web.json`.

## Số đo tương phản (WCAG 2.x, thấp nhất trên 4 tầng nền)

| Cặp | Tối | Sáng | Ngưỡng |
| --- | --- | --- | --- |
| `text-link` trên nền | 9.80 | 6.08 | 4.5 |
| `primary` làm chữ trên nền | 7.63 | 4.66 | 4.5 |
| `accent` làm chữ trên nền | 5.85 | 4.50 | 4.5 |
| `on-primary` trên `primary` / `-hover` / `-active` | 9.24 / 11.87 / 7.14 | 5.54 / 7.24 / 9.34 | 4.5 |
| `focus-ring` trên `bg-base` | 9.24 | 5.31 | 3 |

Cổng canh phía repo con: `packages/ui/test/contrast.test.ts` (253/253 cặp đạt ở tsudev#284). `accent` Sáng nằm sát
ngưỡng (4.50) - nếu nhận, nên để `scripts/check-contrast.mjs` canh luôn cặp này.

## Câu chữ đề xuất cho ECOSYSTEM_IDENTITY.md

> Website trong hệ sinh thái dùng **đen tuyền + xanh logo** (xanh lơ → xanh dương của `logo-tsudev.png`), ghi đè token
> màu chuẩn ở tầng repo. Ngoại lệ có quyết định riêng: lotus.tsudev.com giữ tím hoa sen. Xanh chỉ ở điểm nhấn; một
> quầng xanh lơ **tĩnh** ở đỉnh trang. Ở chế độ Tối chữ trên nút xanh là **mực đen** (xanh lơ không đạt AA dưới chữ
> trắng).

Đồng thời ghi font mono **Chivo Mono** (số 0 trơn, có tiếng Việt - chủ dự án yêu cầu 16/11; tsudev#284) nếu
ECOSYSTEM_IDENTITY có mục font.
