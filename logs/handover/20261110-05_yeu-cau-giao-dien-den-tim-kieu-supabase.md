# PHIẾU YÊU CẦU - Giao diện đen tuyền + tím, bố cục kiểu Supabase, chỉ Sáng / Tối / Hệ thống

- **Mã phiếu**: 20261110-05
- **Từ**: phiên 47 của repo `tsudev` (tsudev.com) - **Đến**: phiên kế tiếp của repo `tsudev-standards`
- **Thời điểm**: 10/11/2026
- **Trạng thái**: ĐÓNG phần nội dung (nhánh `feat/v3.4.0-giao-dien-den-tim`); chờ chủ project merge + gắn nhãn `v3.4.0`
- **Tham chiếu**: tsudev.com đã làm trước - nhánh `feat/giao-dien-tim-den-supabase` của `tsudev-org/tsudev`
  (`tokens/extensions.tsudev-web.json`, `packages/ui/src/components/ThemeToggle.tsx`, `SiteFooter.tsx`,
  `apps/frontend-main/styles/globals.css`, `apps/frontend-main/pages/_document.tsx`). Đọc các tệp đó trước khi
  tự dựng - chép HÀNH VI, đừng chép mã React nếu site của bạn không dùng React.

## 0. Riêng cho repo `tsudev-standards`

- Đây là repo BỘ QUY ƯỚC - thay đổi ở đây đi tới mọi repo qua `.standards/`. Đề xuất phát hành **v3.4.0**:
  1. `docs/DESIGN_SYSTEM.md` §1: bỏ chế độ Ấm; ba lựa chọn Sáng / Tối / Hệ thống, mặc định Tối; bộ chọn ở
     chân trang (hợp đồng §3 phiếu này).
  2. `tokens/design-tokens.json`: hoặc gỡ khối `color.warm`, hoặc đánh dấu deprecated một phiên bản trước khi gỡ
     (tsudev.com đã ngừng sinh nó và test chỉ đòi `light` + `dark` - gỡ không làm đỏ tsudev). Cân nhắc nhận
     bảng §2 làm bảng chuẩn `light`/`dark` để các repo không phải tự ghi đè.
  3. `docs/ACCESSIBILITY.md:104`, `docs/ONBOARDING.md:151`, `docs/RICH_TEXT_EDITOR.md:326`: "ba chế độ Sáng /
     Ấm / Tối" ⇒ "hai chế độ Sáng / Tối".
  4. `docs/ECOSYSTEM_IDENTITY.md`: thêm quy ước chân trang (`© tsudev` + bộ chọn giao diện) và ngôn ngữ thiết kế §4.
- Sau khi phát hành: báo repo `tsudev` để `npm run standards:sync` (nếu có) và gỡ ghi đè `brand` thừa.

## 1. Quyết định của chủ dự án (10/11/2026) - áp cho TOÀN hệ sinh thái

1. **Tông màu chủ đạo: ĐEN TUYỀN + TÍM TƯƠI.** Thay tông đen + xanh dương/xanh lá của phiên 46. Xám trung tính
   cho mọi bề mặt, tím CHỈ ở điểm nhấn (nút chính, liên kết, một quầng sáng tĩnh ở đỉnh trang).
2. **Bố cục, nút, hiệu ứng tham khảo https://supabase.com** (không chép logo/chữ/ảnh của Supabase - chỉ học
   ngôn ngữ thiết kế): nền LIỀN MẠCH, không dải nền khác màu giữa các khối, không khung đứt đoạn.
3. **Chỉ BA lựa chọn giao diện: Sáng / Tối / Hệ thống** (như supabase.com). **Bỏ chế độ Ấm** ở mọi nơi.
   Mặc định cho khách mới là **Tối**; "Hệ thống" là lựa chọn người dùng tự bật.
4. **Chân trang**: hàng cuối cùng là `© tsudev` (bên trái) + **bộ chọn giao diện** (bên phải). Nút đổi giao
   diện **chuyển từ header xuống chân trang** - phiếu `20261110-02/03` (nút Sáng/Tối ở header) được THAY bởi
   phiếu này: nếu chưa làm phiếu đó thì làm thẳng theo phiếu này; nếu đã làm thì dời nút xuống footer và thêm
   lựa chọn "Hệ thống".
5. Icon không được trùng màu với nền chỗ chứa nó; trang tải/giới thiệu app phải có biểu tượng app.

## 2. Bảng màu chuẩn (đã áp ở tsudev.com, PR `feat/giao-dien-tim-den-supabase`; mọi cặp đạt WCAG AA)

| Vai trò            | Tối (mặc định)             | Sáng                        |
| ------------------ | -------------------------- | --------------------------- |
| nền trang          | `#0A0A0A` (KHÔNG `#000`)   | `#FAFAFA`                   |
| bề mặt (card)      | `#111111`                  | `#FFFFFF`                   |
| bề mặt lồng        | `#171717`                  | `#F4F4F5`                   |
| hover              | `#1F1F1F`                  | `#EBEBED`                   |
| viền hairline      | `#242424`                  | `#E4E4E7`                   |
| viền đậm           | `#2E2E2E`                  | `#D4D4D8`                   |
| viền ô nhập/nút    | `#6E6E6E`                  | `#71717A`                   |
| chữ chính          | `#EDEDED`                  | `#0A0A0A`                   |
| chữ phụ            | `#B4B4B4`                  | `#3F3F46`                   |
| chữ mờ             | `#8F8F8F`                  | `#52525B`                   |
| liên kết           | `#C4A1FF`                  | `#6D28D9`                   |
| primary (nút chính)| `#A970FF`                  | `#7C3AED`                   |
| primary hover      | `#BB8CFF`                  | `#6D28D9`                   |
| primary active     | `#9A5CF5`                  | `#5B21B6`                   |
| chữ trên primary   | `#0A0A0A` (mực đen!)       | `#FFFFFF`                   |
| vòng focus         | `#A970FF`                  | `#7C3AED`                   |
| nhấn phụ (accent)  | `#E879F9`                  | `#A21CAF`                   |
| quầng sáng (glow)  | `rgba(169,112,255,0.16)`   | `rgba(124,58,237,0.10)`     |

⚠️ Ở chế độ Tối chữ trên nút tím là **mực đen**, không phải trắng: không mã tím nào vừa đạt 4.5:1 làm chữ trên
nền `#0A0A0A` vừa đạt 4.5:1 dưới chữ trắng (đã tính - hai ngưỡng độ sáng không giao nhau). Đừng "sửa" thành
chữ trắng.

`<meta name="theme-color">`: Tối `#0a0a0a`, Sáng `#fafafa`. `site.webmanifest`: `theme_color`/`background_color`
= `#0a0a0a`.

## 3. Bộ chọn giao diện - hợp đồng hành vi (khớp tsudev.com)

- Khoá localStorage: `tsudev-theme`, giá trị `light` | `dark` | `system`. Giá trị cũ `warm` ⇒ đọc thành
  `light` (người từng chọn Ấm muốn nền sáng). Không có/không đọc được ⇒ `dark`.
- Áp TRƯỚC KHI VẼ bằng script đồng bộ nội tuyến trong `<head>`, đặt SAU `<meta name="theme-color">` và TRƯỚC
  stylesheet (bài học cwico: đặt trước meta thì không đổi được màu thanh địa chỉ). Script đặt
  `data-theme="light|dark"` lên `<html>` và đổi `content` của meta theme-color. `system` ⇒ hỏi
  `matchMedia('(prefers-color-scheme: dark)')` và nghe sự kiện `change` khi đang chọn `system`.
- CSS KHÔNG được treo bảng màu vào `@media (prefers-color-scheme)` - chỉ JavaScript được hỏi hệ điều hành.
- Giao diện: nhóm 3 nút biểu tượng (mặt trời / mặt trăng / màn hình) bo tròn, `role="radiogroup"`
  `aria-label="Giao diện"`, mỗi nút `role="radio"` + `aria-checked` + `aria-label` (Sáng / Tối / Hệ thống),
  phím ← → chuyển lựa chọn. Nút đang chọn nền `hover`, chữ chính; nút khác chữ mờ.
- CSP: script nội tuyến cần băm `sha256-...` trong `script-src` (hoặc file `.js` cùng origin nếu CSP
  `default-src 'none'` không có `script-src`). Đổi nội dung script ⇒ đổi băm. KHÔNG nới thành `'unsafe-inline'`.

## 4. Ngôn ngữ thiết kế kiểu Supabase - danh sách kiểm

- [ ] MỘT nền liền mạch từ header tới footer: bỏ mọi dải nền khác màu (hero, đầu trang con, footer), bỏ viền
      ngang cắt trang; ranh giới giữa các khối là khoảng trống.
- [ ] Header dính, kính mờ trên CÙNG màu nền trang + một đường hairline dưới; link điều hướng chữ phụ → chữ
      chính khi hover/đang ở trang; bên phải: nút phụ + nút chính cao 32px.
- [ ] Nút chính: nền primary + viền primary-hover 1px, bo 6px, chữ `font-medium` 14px. Nút phụ: nền bề mặt +
      viền đậm, hover viền ô nhập + nền hover. Không quầng sáng quanh nút, không gradient trên nút.
- [ ] Thẻ: nền bề mặt + viền hairline, bo 8px; hover = viền đậm lên + nền sáng hơn một bậc. Không nhấc, không
      quầng màu, không viền chuyển sắc.
- [ ] Hero canh giữa, tiêu đề `font-semibold` (không extrabold), một cụm chữ tím → tím hồng tĩnh; quầng tím tĩnh
      phía sau. Không aurora/chuyển động nền, không ánh trượt.
- [ ] Nhãn nhỏ (eyebrow) kiểu mono chữ hoa màu liên kết, không phải viên thuốc có nền.
- [ ] **Icon trong nút/ô nền đặc ăn màu chữ của nút** (`currentColor`), không mang màu vai trò riêng - icon xanh
      lá/ngọc trên nút tím chính là lỗi "icon lẫn vào nền" chủ dự án báo.
- [ ] Biểu tượng app: glyph nét 1.6 trên ô bo 8px nền tím nhạt (`primary` 10% trộn bề mặt) + viền tím mờ, glyph
      màu liên kết. Chênh glyph/nền ≥ 4.5:1 ở cả hai chế độ.
- [ ] Chân trang: các cột liên kết chữ mờ → chữ chính khi hover; hàng cuối `© tsudev` + bộ chọn giao diện.
- [ ] Giữ nguyên: câu mô tả chuẩn ECOSYSTEM_IDENTITY §1, liên kết qua lại giữa các site, font tự host.

## 5. Nghiệm thu

1. Tương phản AA ở CẢ HAI chế độ (chữ 4.5:1, viền/focus 3:1).
2. Chọn Sáng → tải lại → vẫn Sáng; chọn Hệ thống → đổi chế độ máy → trang đổi theo không cần tải lại.
3. Không còn chuỗi/lựa chọn "Ấm" trong giao diện.
4. Production: CSP không chặn script chọn giao diện (console 0 lỗi), `theme-color` đúng màu từng chế độ.
5. Ghi kết quả vào mục "Kết quả xử lý" cuối phiếu này, đổi trạng thái ĐÓNG, rồi báo lại repo `tsudev`
   (phiếu báo kết quả trong `tsudev/logs/handover/` hoặc nhắn phiên tsudev).

## Kết quả xử lý

Phiên projects-0c, 10/11/2026, nhánh `feat/v3.4.0-giao-dien-den-tim`, bản **v3.4.0 (MINOR)**.

- §0.1: `DESIGN_SYSTEM.md` mục 1 - bỏ Ấm, ba lựa chọn Sáng / Tối / Hệ thống, mặc định Tối, trỏ sang hợp đồng mới.
- §0.2: KHÔNG gỡ `color.warm` và KHÔNG thay giá trị `light`/`dark` trong bản này: `VERSIONING.md` mục 1 quy định
  đổi giá trị token màu là MAJOR. Thay vào đó `meta.deprecated` đánh dấu `color.warm` ngừng dùng, gỡ ở v4.0.0; bảng
  §2 vào `ECOSYSTEM_IDENTITY.md` mục 4.2 để repo con ghi đè ở tầng riêng (như mọi repo đang làm). Đề xuất v4.0.0
  (gỡ Ấm + nhận bảng §2 làm token chuẩn) ghi ở CHANGELOG, cần chủ project duyệt.
- §0.3: ba câu "Sáng / Ấm / Tối" ⇒ "Sáng / Tối".
- §0.4: `ECOSYSTEM_IDENTITY.md` mục 4 thêm quy ước hàng cuối chân trang, mục 4.1 bộ chọn, mục 4.2 bảng màu + ngôn
  ngữ thiết kế; checklist mục 9.
- Kèm **TS-15**: `AUTH_AND_ACCOUNT.md` mục 1 xếp `tsudev-contact` vào hạng C.
- Kiểm: `build-tokens --check` khớp, `check-contrast` 39/39 cặp đạt, `check-standards` 0 lưu ý,
  `test-upstream-exempt` mọi ca đúng, `MANIFEST.sha256` sinh lại (51 tệp).
- Sau khi gắn nhãn: repo con chạy `./scripts/sync-standards.sh --ref v3.4.0`; repo `tsudev` cập nhật `.standards/`
  và kiểm `themeTokens.test.ts`.
