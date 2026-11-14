# Đề xuất: mẫu menu tài khoản ở header, cột "Tài khoản" ở chân trang, khối "Cài bằng lệnh" sinh lúc build

- **Từ**: repo `tsudev` (tsudev.com), phiên 53, 14/11/2026
- **Đích**: `docs/ECOSYSTEM_IDENTITY.md` (mục 4, mục 6) và `docs/PACKAGING.md`
- **Loại thay đổi**: thêm quy ước (MINOR) - không phá repo nào đang đạt chuẩn

## 1. Vấn đề cụ thể

1. **Header của site có đăng nhập**: quy ước chưa nói gì về khu vực tài khoản. tsudev.com tới 13/11/2026 để nút
   "Đăng xuất" TRẦN cạnh tên - bấm nhầm một lần là mất phiên (chủ dự án báo). Site con đang làm đăng nhập chung
   (kế hoạch OIDC, D1) sẽ mỗi nơi tự nghĩ một kiểu.
2. **Chân trang**: không site nào có đường tới "Bảo mật tài khoản" ngoài menu; người dùng di động không thấy.
3. **Khối "Cài bằng lệnh" ở website từng app**: 6 site app chép tay lệnh winget/Scoop/apt. Đo 13/11/2026: lệnh
   chép tay lệch tên gói thật ở 2 site sau khi `tsudev-files` đổi tên hiển thị thành TsuFiles - không cổng nào bắt.

## 2. Bằng chứng

- Header: `tsudev` PR #251 (Worker `8a1da656`), công cụ quét `~/projects/logs/tools/quet-giao-dien.cjs` ra OK ở
  390/1280 × Tối/Sáng; E2E `smoke.spec.js` nhận diện đăng nhập bằng `header button[aria-controls="tsu-user-menu"]`.
- Chân trang: `tsudev` PR #252 (đang chờ chủ sở hữu duyệt - cổng Bảo vệ bản quyền).
- Cài bằng lệnh: `pkg.tsudev.com/catalog.json` + `catalog.json` của scoop-bucket/homebrew-tap là nguồn sự thật;
  tsudev.com sinh lệnh từ bản chụp `pkgCatalog.generated.ts` (`npm run pkg:catalog`) và cổng C4
  (`packages/ui/test/installChannels.test.ts`) đỏ khi một app khai hệ điều hành mà không có kênh lệnh.

## 3. Câu chữ đề xuất

### ECOSYSTEM_IDENTITY.md - thêm mục 4.x "Khu vực tài khoản ở header"

> Site có đăng nhập `MUST` gộp ảnh đại diện + tên tài khoản thành MỘT nút mở khối liên kết gồm đúng hai mục theo
> thứ tự: "Hồ sơ tài khoản", "Đăng xuất". `MUST NOT` đặt "Đăng xuất" trần trên header. Khối dùng mẫu
> **disclosure** (`button` + `aria-expanded` + `aria-controls`), KHÔNG `role="menu"`; đóng khi Esc (trả focus về
> nút), bấm ra ngoài, hoặc focus rời khối. Khi phiên chưa xác định (đang tải), vẽ vòng tròn trơn, không đoán biến
> thể ảnh đại diện (tránh nháy).

### ECOSYSTEM_IDENTITY.md - thêm vào mục 4 (chân trang)

> Chân trang site có đăng nhập `SHOULD` có cột "Tài khoản" theo phiên: đã đăng nhập ⇒ "Bảo mật tài khoản" +
> "Hồ sơ tài khoản"; chưa ⇒ "Đăng nhập" + "Đăng ký". Ở khổ di động cột này nằm trong lưới 2 cột như các cột khác.
> (Áp dụng sau khi `tsudev` #252 được duyệt - mẫu tham chiếu là bản đó.)

### PACKAGING.md - thêm mục "Khối Cài bằng lệnh trên website app"

> Website của app có gói `MUST` hiện lệnh cài SINH LÚC BUILD từ catalog của kho (`pkg.tsudev.com/catalog.json`,
> `catalog.json` của bucket/tap), theo khoá `homepage` = website. `MUST NOT` chép tay tên gói, và `MUST NOT` gọi
> catalog lúc chạy (site tĩnh phải dựng được khi kho tạm sập; lệnh lệch sẽ lộ ra ở lần build sau, không lộ ra
> trước mặt người dùng). Gói có `replacedBy` không hiện lệnh.

## 4. Ảnh hưởng tới repo con

| Repo                                  | Việc                                                     | Ước lượng |
| ------------------------------------- | -------------------------------------------------------- | --------- |
| tsudev                                | đã đạt (header #251; chân trang khi #252 merge)          | 0         |
| 6 site app (cwico, swico, contact, trafficmonitor, tsufiles, lotus) | khối Cài bằng lệnh sinh lúc build (phiếu 20261114-02 đã gửi) | 1 phiên/repo |
| site không có đăng nhập               | không áp dụng mục header/chân trang                      | 0         |
