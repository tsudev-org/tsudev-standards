# PHIẾU YÊU CẦU - Cập nhật PACKAGING.md theo kho APT/RPM thực tế + `catalog.json`

- **Mã phiếu**: 20261113-01
- **Từ**: phiên `linux-packages-1e` (repo `tsudev-org/linux-packages`) - **Đến**: phiên repo `tsudev-standards`
- **Thời điểm**: 13/11/2026
- **Trạng thái**: ĐÓNG - phát hành v4.4.0 (21/11/2026)

## 1. Lệch giữa PACKAGING.md v1.0.0 và thực tế

| Mục | Văn bản hiện tại | Thực tế (linux-packages, từ 13/11/2026) |
| --- | --- | --- |
| 5 | Không nói về danh mục máy đọc | `https://pkg.tsudev.com/catalog.json` (schema 1): chỉ gói đang có trong kho, phiên bản, kiến trúc, lệnh `apt`/`dnf`, lệnh thêm kho, vân tay khóa. Tự kiểm khớp chỉ mục APT + `.rpm` khi dựng |
| 7.2 | APT/RPM: repo sản phẩm "nfpm → ký → đẩy lên R2 bằng `wrangler r2 object put`" | Dựng **tập trung** ở `tsudev-org/linux-packages` từ `products.json` + `packaging/package.json` của repo sản phẩm; đẩy qua API S3 của R2; repo sản phẩm **không** giữ khóa ký hay token R2. Kiểm bản mới mỗi giờ, cần duyệt Environment `packages` |
| 7.3 | `verify-install` trên `ubuntu-latest` | Cài thật từ `pkg.tsudev.com` trên Ubuntu 22.04/24.04, Debian 12/13, Fedora + ARM64 (Ubuntu 24.04, Debian 12, Fedora) sau mỗi lần xuất bản; hỏng thì mở Issue |
| 8 | "Khối sinh từ `packaging/package.json` lúc build" | Với APT/DNF: sinh từ `catalog.json` lúc build (đúng tinh thần "kênh chưa có gói thì không hiện" - catalog chỉ gồm gói đã có) |
| 8 | - | Scoop / Homebrew cũng có `catalog.json` schema 1 ở gốc repo (scoop-bucket PR #3, homebrew-tap PR #2): `https://raw.githubusercontent.com/tsudev-org/{scoop-bucket,homebrew-tap}/main/catalog.json`, CI từ chối nếu cũ, workflow cập nhật sinh lại cùng commit. Trường chung: `name`, `version`, `arch`, `install`, `installFull`, `replacedBy` (đổi tên). winget: không có repo riêng - website kiểm mã winget tồn tại trong `microsoft/winget-pkgs` lúc build |
| 3 | - | Repo private (TsuGameLabs): repo công khai riêng `TsuGameLabs/tsudev-<id>-releases` chỉ chứa README, LICENSE, `packaging/package.json` + Releases (phương án A, phiếu linux-packages 20261112-01) |

## 2. Việc cần làm

1. Sửa mục 3, 5, 7, 8 theo bảng trên; nâng phiên bản tài liệu (v1.1.0) + ghi thay đổi.
2. Mục 6: ghi `install.sh` đọc `catalog.json`, so vân tay với giá trị cứng trong script (không tin vân tay tải về).
   Phần cài đặt nằm ở repo `tsudev` (phiếu `tsudev/logs/handover/20261113-02`).
3. Ghi kết quả mục 3 dưới đây.

## 3. Kết quả xử lý (phiên nhận điền)

- 21/11/2026 - phiên tsudev-standards: DUYỆT, `PACKAGING.md` v1.2.0 trong v4.4.0. Mục 3.1 (dựng tập trung, repo `-releases` cho repo private), 5 + 5.1 (`catalog.json` schema 1 ba kênh, API S3, đối chiếu hằng ngày), 6 (đọc catalog + vân tay ghi cứng trong script), 7 (bỏ `wrangler`, `verify-install` APT/RPM ở kho gói x64 + ARM64), 8.1 (lệnh sinh lúc build). Đã đối chiếu `pkg.tsudev.com/catalog.json` và `scoop-bucket/catalog.json` đang chạy, CI `linux-packages` (`ci.yml`, `xuat-ban.yml`, `doi-chieu-kenh.yml`), `tsudev` `install.sh` (`FINGERPRINT`).
