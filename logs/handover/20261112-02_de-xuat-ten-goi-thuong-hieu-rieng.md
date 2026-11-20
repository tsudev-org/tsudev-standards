# PHIẾU ĐỀ XUẤT - Tên gói theo thương hiệu sản phẩm và quy trình đổi tên gói (PACKAGING.md mục 2)

- **Mã phiếu**: 20261112-02
- **Từ**: phiên `lotus-share` (12/11/2026) - **Đến**: phiên phụ trách `tsudev-standards`
- **Ủy quyền**: quyết định chủ dự án đổi tên sản phẩm Lotus Share (phiếu `~/projects/logs/handover/20261112-02`)
- **Trạng thái**: ĐÓNG - phát hành v4.3.0 (21/11/2026)

## Bối cảnh

`PACKAGING.md` mục 2 quy định Scoop/Homebrew/APT/RPM dùng khuôn `tsudev-<ten>` và mã đã công bố `MUST NOT` đổi.
Chủ dự án đổi `tsudev-lotus` thành **Lotus Share** (thương hiệu riêng, cùng đợt với phiếu 20261112-01 về logo riêng),
gói đổi thành `lotus-share`. Đã làm ngày 12/11/2026, giữ tinh thần "mã đã công bố không gãy":

| Kênh | Cách làm | Đã kiểm |
| --- | --- | --- |
| APT | gói `.deb` chuyển tiếp rỗng `tsudev-lotus` (Depends `lotus-share`, section oldlibs) | CI cài `tsudev-lotus 1.18.2-2` thật từ pkg.tsudev.com, `apt upgrade` ra `lotus-share`, `/opt/tsudev-lotus` gỡ sạch (Ubuntu 22.04/24.04, Debian 12/13) |
| RPM | `lotus-share` có `Provides: tsudev-lotus = V` + `Obsoletes: tsudev-lotus < V` | CI Fedora: `dnf upgrade` thay `tsudev-lotus 1.18.2-2` bằng `lotus-share` |
| Homebrew | cask `tsudev-lotus` giữ lại, `deprecate!` + `replacement_cask`, trỏ bản mới | CI: `brew upgrade` từ bản cũ ra `Lotus Share.app`. **`cask_renames.json` KHÔNG chuyển máy đã cài** (đã thử, CI đỏ) |
| Scoop | manifest `tsudev-lotus` giữ lại, trỏ bản mới, `notes` hướng dẫn chuyển | CI cài thử |
| winget | `tsudev.Lotus` chưa từng được duyệt -> thay bằng `tsudev.LotusShare` | - |

Công cụ: `tsudev-org/linux-packages` (`products.json` khóa `tenRieng`, `linux.formerNames` trong `packaging/package.json`).

## Đề xuất (bản MINOR)

1. Mục 2: sản phẩm có thương hiệu riêng được chủ dự án duyệt `MAY` dùng tên gói theo thương hiệu (chữ thường, gạch
   nối ASCII, không trùng gói của bản phân phối/dự án gốc), ghi đích danh ở repo kho gói (`tenRieng`).
2. Thêm mục "Đổi tên gói": mã cũ `MUST` tiếp tục nhận bản mới theo bảng trên (APT chuyển tiếp, RPM Provides+Obsoletes,
   Homebrew/Scoop giữ manifest tên cũ đã deprecate) và CI `MUST` kiểm đường nâng cấp từ bản cũ thật.
3. Ghi chú: Homebrew `cask_renames.json` không đủ cho tap bên thứ ba (không chuyển máy đã cài).

## Kết quả xử lý

-
- 21/11/2026 - phiên tsudev-standards: DUYỆT, phát hành v4.3.0 (`PACKAGING.md` v1.1.0 mục 2.1, 2.2). Đối chiếu `linux-packages/tools/dung_kho.py`: gói chuyển tiếp APT không cần `Replaces/Breaks`. Thêm: winget mã chưa duyệt mới được thay, Android không đổi `applicationId`, tên cũ giữ tối thiểu 12 tháng và không dùng lại.
