# PHIẾU ĐỀ XUẤT - Cho phép sản phẩm dùng logo riêng (BRAND_ASSETS mục 1, 2, 7)

- **Mã phiếu**: 20261112-01
- **Từ**: phiên `tsudev-trafficmonitor` (12/11/2026) - **Đến**: phiên phụ trách `tsudev-standards`
- **Ủy quyền**: chủ dự án chọn "Thêm phiếu đề xuất sửa quy ước chung" (chat 12/11/2026)
- **Trạng thái**: ĐÓNG (13/11/2026) - chủ dự án duyệt; nhận vào v3.6.0 (`BRAND_ASSETS.md` mục 1, 2, 15)

## Bối cảnh

Chủ dự án đổi toàn bộ logo/icon/favicon của `tsudev-trafficmonitor` sang logo sản phẩm riêng
`logo-tsudev-trafficmonitor.png` (hình cú mạch điện + chữ "tsudev", nền đen). `BRAND_ASSETS.md` hiện bắt buộc:

- mục 2: icon (favicon, icon ứng dụng, khay, avatar) `MUST` dùng **dấu hiệu thu gọn chung** `brand/logo-mark.png`;
- mục 7, 9: mọi tài sản `MUST` sinh từ bản gốc chính thức qua dây chuyền `packages/brand/build-assets.js` (repo `tsudev`)
  hoặc `tools/brand/` - `MUST NOT` lấy nguồn khác.

`tsudev-trafficmonitor` đã ghi lệch chuẩn ở `AGENTS.md` mục B.4 (PR "logo tsudev-trafficmonitor").

## Đề xuất (bản MINOR, ví dụ v3.5.0)

Thêm mục "Logo sản phẩm" vào `BRAND_ASSETS.md`:

1. Một sản phẩm `MAY` có logo riêng nếu chủ dự án duyệt. Khi đó repo `MUST` có:
   - ảnh gốc duy nhất ở `assets/brand/source/` (cạnh ngắn >= 1024 px), cấu hình sinh ở `assets/brand/brand.json`;
   - một script sinh mọi bản (`tools/brand/build_brand.py` hoặc tương đương), kèm chế độ `--check`;
   - dấu hiệu thu gọn KHÔNG chữ cắt từ chính logo đó cho icon <= 40 px (quy tắc "không chữ ở cỡ nhỏ" của mục 2 giữ nguyên);
   - đủ bảng sản phẩm bắt buộc ở mục 9 (favicon.ico 16-256, apple-touch nền đặc, PWA + maskable, og-image, icon ứng dụng).
2. Liên kết về hệ sinh thái giữ nguyên (chân trang về tsudev.com, ECOSYSTEM_IDENTITY).
3. Website `SHOULD` phục vụ ảnh thương hiệu bằng `<picture>` AVIF -> WebP -> PNG.

Tham khảo cài đặt mẫu: `tsudev-org/tsudev-trafficmonitor` - `assets/brand/README.md`, `tools/brand/build_brand.py`.

## Việc cần làm ở repo này

- [ ] Chủ dự án duyệt hướng đề xuất.
- [ ] Sửa `docs/BRAND_ASSETS.md`, tăng phiên bản, CHANGELOG, phát hành tag.
- [ ] Báo lại phiên `tsudev-trafficmonitor` để đồng bộ quy ước và gỡ dòng lệch chuẩn ở B.4.

## Bổ sung - `tsudev-lotus` (đổi tên Lotus Share), phiên tsudev-lotus-0e, 12/11/2026

- Chủ dự án cũng chọn logo riêng cho Lotus Share (chat 11/11/2026); lệch chuẩn ghi ở `AGENTS.md` mục B.4 của repo đó.
- Cài đặt: nguồn `support/brand/lotus-share/logo-source.png` -> `tools/prepare_brand.py` (tách nền trắng: nét đậm màu giữ
  đặc, nền/quầng sáng chuyển trong suốt; bản 1024; WebP/AVIF; `accent.json` màu nhấn) -> `tools/gen_icons.py` (icon mọi
  nền tảng) -> `website/scripts/brand_assets.py` (favicon, PWA, `<picture>` AVIF/WebP/PNG, OG).
- Điểm cần quy ước quyết: (1) ảnh gốc 466 px < 1024 px của đề xuất trên - hiện phóng to có làm nét, nên yêu cầu bản gốc
  lớn/vector; (2) bản MỘT MÀU (khay, icon đơn sắc Android, thanh menu macOS) phải bỏ quầng sáng bán trong suốt (ngưỡng
  alpha) - nên ghi thành quy tắc; (3) thống nhất thư mục nguồn (`assets/brand/` hay `support/brand/`).

## Bổ sung - mảng trò chơi (org `TsuGameLabs`, 6 game), phiên tsudev-game-kit-ce, 12/11/2026

- Mục tiêu chủ dự án nêu (chat 12/11/2026, trả lời GĐ5 phiếu `tsudev-game-kit` 20261112-02): **mỗi dự án có đặc
  trưng / phong cách / giao diện riêng** để trông chân thực, chuyên nghiệp hơn. Trò chơi đã bắt đầu theo hướng này ở
  phần lối chơi (vd `chu-chim-vo-canh` đổi sang bản sắc Núi Cấm: chim sáo, vách đá, trái thốt nốt).
- Hiện cả 6 game dùng chung dấu hiệu tsudev; favicon / PWA / og-image sinh bằng công cụ RIÊNG
  `tsudev-game-kit/tools/sinh-thuong-hieu.mjs` (chỉ thu nhỏ từ đầu ra 512 px của `packages/brand/build-assets.js`),
  vì dây chuyền chính thức chỉ ghi vào `apps/*/public/` của repo `tsudev` (lệch chuẩn ghi ở `AGENTS.md` B.4 của game-kit).
- Đề nghị gộp vào bản MINOR của phiếu này:
  1. `packages/brand/build-assets.js` (hoặc `tools/brand/` của bộ quy ước) nhận `--nguon <ảnh gốc>` và
     `--dich <thư mục>` (+ `--check`), để repo không có `apps/*/public/` - trò chơi, trang sản phẩm - dùng ĐÚNG một dây
     chuyền thay vì công cụ riêng. Có tuỳ chọn này thì game-kit bỏ `sinh-thuong-hieu.mjs`.
  2. Logo riêng của sản phẩm (mục đề xuất 1 ở trên) áp cho cả trò chơi; `og-image` `MAY` là ảnh chụp sản phẩm + tên
     sản phẩm + dấu hiệu tsudev nhỏ ở góc (thay vì chỉ dấu hiệu chung) để mỗi liên kết chia sẻ nhận ra được sản phẩm.
  3. Thống nhất thư mục nguồn (`assets/brand/source/` như đề xuất) - game-kit sẽ dùng `brand/<id-game>/source/`
     nếu quy ước cho phép nguồn tập trung cho nhiều repo.
- Khi bản quy ước phát hành: báo `~/projects/tsugamelabs/tsudev-game-kit/logs/handover/` để đồng bộ và gỡ dòng B.4.

## Bổ sung - logo chính `tsudev.com` đổi sang `logo-tsudev.png`, phiên tsudev-06 (phiên 49), 13/11/2026

- Chủ dự án yêu cầu (chat 13/11/2026): tsudev.com lấy `logo-tsudev.png` (1254x1254, cú + chữ "tsudev", nền đen) làm
  biểu tượng / logo / favicon, dùng NGUYÊN logo không biến dạng; bản thu nhỏ / favicon chỉ xoá nền, GIỮ chữ "tsudev".
- Đã làm ở repo `tsudev` (nhánh `feat/phien-49-chuan-hoa-logo-icon-auth`): nguồn duy nhất
  `packages/brand/source/logo-tsudev.png`; `build-assets.js` xoá nền đen bằng flood fill có rào đóng hình thái học
  (không thủng mặt cú trên nền sáng), mọi cỡ `fit: contain` trên khung vuông. Đầu ra mới: `brand/logo-tsudev{,-256}.png`,
  `brand/logo-tsudev-{48,96,144,192}.{avif,webp}`; favicon / PWA / apple-touch / og-image = nguyên logo. Đã GỠ
  `logo-mark*`, `logo-full*`, `logo-wordmark*` (không repo nào nhúng từ tsudev.com - đã quét `~/projects`).
- Lệch chuẩn hiện tại, cần quy ước quyết:
  1. mục 2 / 12.1: favicon và icon <= 40 px nay CÓ CHỮ (chủ dự án chọn) - trái quy tắc "không chữ ở cỡ nhỏ" của đề xuất
     trên. Đề nghị: quy tắc thành `SHOULD`, cho phép chủ dự án miễn trừ có ghi chép.
  2. mục 1 (bảng tên tệp `logo-full` / `logo-mark` / `logo-wordmark`, `logo-full-dark`): các tên này không còn ở
     tsudev.com; logo mới tự có nền tối riêng nên không cần bản `-dark`.
  3. apple-touch / maskable nay nền đặc `#0A0A0A` (logo vẽ cho nền đen), không còn `#EEF4FB`.
- ⚠️ Ảnh hưởng `tsudev-game-kit/tools/sinh-thuong-hieu.mjs`: nó thu nhỏ từ `android-chrome-512x512.png` của tsudev.com.
  Lần chạy sau sẽ ra logo MỚI (có chữ, nền trong suốt) - đúng ý chủ dự án là đồng nhất, nhưng phiên game nên chạy lại
  có chủ đích và soát bằng mắt ở 16/32 px.
- Danh bạ `/apps` nay hiện LOGO THẬT của app có logo riêng (tsudev-trafficmonitor, tsudev-files, Lotus Share, La bàn) -
  lấy từ website của app bằng `packages/brand/build-eco-icons.js`. cwico, tsudev SWICO, tsudev-contact và 6 game chưa
  có logo riêng nên tạm vẽ ô màu riêng + glyph; repo nào có logo riêng thì báo phiên `tsudev` thêm một dòng vào
  `SOURCES` của script đó.

## Kết quả (13/11/2026, phiên tsudev-06)

- Chủ dự án ủy quyền hoàn tất (chat 13/11/2026). v3.6.0: `BRAND_ASSETS.md` mục 1-2 (logo tsudev mới, có chữ ở mọi cỡ),
  mục 15 (logo sản phẩm riêng `MAY`, các `MUST` đi kèm). Điểm (1) ảnh gốc nhỏ → `SHOULD` cạnh ngắn >= 1024px hoặc SVG,
  ghi nợ; (2) bản một màu cho khay → `MAY` cắt dấu hiệu riêng; (3) thư mục nguồn thống nhất `assets/brand/source/`.
- Đề nghị `--nguon/--dich` cho `build-assets.js` của game-kit: CHƯA làm - mục 15 cho phép repo có script riêng theo mẫu.
- Repo con: đồng bộ v3.6.0 rồi gỡ dòng lệch chuẩn logo ở `AGENTS.md` (cwico, swico, contact ghi ở B.2; trafficmonitor,
  lotus-share ghi ở B.4).

