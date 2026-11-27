# TsuMIND - Quy ước đặt tên thống nhất toàn hệ sinh thái

| Mục | Giá trị |
|---|---|
| Tên tài liệu | TsuMIND Naming Convention (TMNC) |
| Phiên bản | 1.1.0 (bộ quy ước `v10.0.0`) |
| Trạng thái | Bắt buộc áp dụng (Normative) |
| Phạm vi | Mọi dự án, repo, website, ứng dụng, thư viện, script, pipeline thuộc hệ sinh thái TsuMIND |
| Đối tượng | Lập trình viên, kỹ sư DevOps, người viết tài liệu, **và mọi AI agent/coding agent** |
| Ngôn ngữ tài liệu | Tiếng Việt (thuật ngữ kỹ thuật giữ nguyên tiếng Anh) |
| Vị trí chuẩn | `tsudev-org/tsudev-standards` `docs/NAMING_CONVENTION.md`; repo con đọc bản chỉ-đọc ở `.standards/docs/` |
| Đi cùng | [`TSUMIND_MIGRATION.md`](TSUMIND_MIGRATION.md) (kế hoạch chuyển TsuDEV → TsuMIND), [`BRAND_ASSETS.md`](BRAND_ASSETS.md) mục 16 (bộ logo TsuMIND) |

> **Từ khóa bắt buộc.** Các từ **PHẢI / KHÔNG ĐƯỢC** là yêu cầu bắt buộc; **NÊN / KHÔNG NÊN** là khuyến nghị mạnh, chỉ bỏ qua khi có lý do được ghi lại trong PR; **CÓ THỂ** là tùy chọn.

---

## 0. Chỉ thị dành cho AI agent (đọc trước)

Nếu bạn là AI agent hoặc coding agent làm việc trong bất kỳ repo nào của TsuMIND:

1. **PHẢI** đọc toàn bộ tài liệu này trước khi tạo, đổi tên hoặc sửa bất kỳ file, thư mục, định danh, chuỗi hiển thị nào có chứa tên thương hiệu.
2. **KHÔNG ĐƯỢC** tự sáng tạo biến thể tên mới. Chỉ dùng các dạng được liệt kê ở **Mục 3** và **Mục 5**.
3. **PHẢI** chọn dạng viết theo *ngữ cảnh sử dụng* (Mục 5), không chọn theo cảm tính hay theo thói quen.
4. Khi gặp biến thể sai (Mục 4) trong code đang có: nếu nằm trong phạm vi nhiệm vụ thì **sửa luôn**; nếu ngoài phạm vi thì **ghi nhận trong PR** và không lan truyền thêm.
5. Khi không chắc dạng nào đúng: **dừng lại và hỏi chủ dự án**, không đoán.
6. Trước khi hoàn tất nhiệm vụ, **PHẢI** chạy kiểm tra ở Mục 14 và đối chiếu checklist Mục 15.

---

## 1. Mục đích và nguyên tắc nền tảng

### 1.1 Mục đích
Hiện tại cùng một thương hiệu đang xuất hiện dưới nhiều cách viết (`TsuMIND`, `tsumind`, `TSUMIND`, `Tsu MIND`, `TSU MIND`; và với dự án Cwico: `Cwico`, `TsuCWICO`, `TSUCWICO`, `tsuwico`, `Tsu Cwico`, `TSU Cwico`). Điều này gây nhiễu nhận diện thương hiệu, khó tìm kiếm, dễ lỗi khi tự động hóa và làm hệ sinh thái trông thiếu chuyên nghiệp. Tài liệu này quy định **một nguồn sự thật duy nhất** cho việc đặt tên.

### 1.2 Nguyên tắc
| # | Nguyên tắc | Ý nghĩa |
|---|---|---|
| P1 | **Một thương hiệu - một tên chuẩn** | Mỗi thực thể có đúng một tên chuẩn (canonical name). Mọi dạng khác là *dẫn xuất theo ngữ cảnh* hoặc *bị cấm*. |
| P2 | **Dạng viết theo ngữ cảnh** | Hiển thị cho người dùng, định danh trong code, đường dẫn file, biến môi trường… mỗi loại có một kiểu viết cố định. |
| P3 | **Dẫn xuất máy móc được** | Từ tên chuẩn có thể suy ra mọi dạng khác bằng quy tắc, không cần phán đoán. |
| P4 | **Nhất quán xuyên dự án** | Cùng một khái niệm ở repo A và repo B phải đặt tên theo cùng một mẫu. |
| P5 | **Rõ nghĩa, tìm được** | Tên mô tả đúng vai trò; không viết tắt tùy tiện; grep được. |
| P6 | **Ổn định** | Định danh công khai (bundle ID, package name, URL, tên API) không đổi tùy tiện sau khi phát hành. |

---

## 2. Thuật ngữ

| Thuật ngữ | Định nghĩa |
|---|---|
| **Hệ sinh thái** | Toàn bộ sản phẩm, repo, website, tài liệu thuộc thương hiệu TsuMIND. |
| **Tên chuẩn (canonical name)** | Tên thương hiệu duy nhất, đúng chính tả và viết hoa, dùng làm gốc để dẫn xuất. |
| **Slug** | Dạng chữ thường, không dấu, nối bằng `-`, dùng cho repo, URL, thư mục. |
| **Token** | Một từ cấu thành tên. Ví dụ `TsuMIND` gồm hai token: `tsu`, `mind`. |
| **Sản phẩm (product)** | Một dự án độc lập thuộc hệ sinh thái, ví dụ Cwico. |
| **Module** | Thành phần bên trong một sản phẩm (core, ui, cli, updater…). |

---

## 3. Danh mục thương hiệu chuẩn (Brand Registry)

Đây là **nguồn sự thật**. Mọi dự án mới phải được thêm vào bảng này trước khi bắt đầu code.

### 3.1 Thương hiệu gốc

| Thuộc tính | Giá trị chuẩn |
|---|---|
| Tên chuẩn (hiển thị) | **TsuMIND** |
| Cách đọc | "Tsu-Mind" |
| Token cho định danh code | `TsuMind` (PascalCase), `tsuMind` (camelCase), `tsu_mind` (snake_case) |
| Slug | `tsumind` |
| Hằng/biến môi trường | `TSUMIND` |
| Cách viết hoa | `Tsu` viết hoa chữ đầu, `MIND` viết hoa toàn bộ, **liền nhau, không khoảng trắng** |

### 3.2 Sản phẩm: Cwico

| Thuộc tính | Giá trị chuẩn |
|---|---|
| Tên đầy đủ (tiếng Việt) | **Bộ công cụ rà quét và gỡ bỏ phần mềm Windows chuyên sâu** |
| Tên thương hiệu sản phẩm (hiển thị) | **TsuCwico** |
| Tên rút gọn trong ngữ cảnh đã rõ thuộc TsuMIND | **Cwico** |
| Token cho định danh code | `TsuCwico` (Pascal), `tsuCwico` (camel), `tsu_cwico` (snake) |
| Slug | `tsucwico` |
| Hằng/biến môi trường | `TSUCWICO` |
| Dạng đầy đủ kèm hệ sinh thái | `TsuMIND Cwico` (dùng trong văn bản giới thiệu, tiêu đề website, tài liệu) |
| Mô tả ngắn (tagline VI) | Rà quét sâu, gỡ sạch phần mềm Windows. |
| Mô tả ngắn (tagline EN) | Deep scan and thorough uninstall toolkit for Windows. |

> **Quy tắc dùng tên rút gọn.** `Cwico` chỉ được dùng khi ngữ cảnh đã rõ đang nói về sản phẩm này (ví dụ đoạn thứ hai trở đi của một tài liệu). Lần xuất hiện đầu tiên trong mỗi tài liệu, màn hình, trang web PHẢI dùng `TsuCwico` hoặc `TsuMIND Cwico`.

### 3.3 Mẫu đăng ký cho sản phẩm mới

Mỗi sản phẩm mới phải điền đủ bảng sau và được chủ dự án duyệt:

```yaml
product:
  canonical_display: TsuXxxx          # tên thương hiệu sản phẩm
  short_display: Xxxx                 # tên rút gọn (nếu có)
  full_name_vi: "..."                 # tên đầy đủ tiếng Việt, viết hoa chữ cái đầu câu
  full_name_en: "..."
  slug: tsuxxxx
  pascal: TsuXxxx
  camel: tsuXxxx
  snake: tsu_xxxx
  env_prefix: TSUXXXX
  tagline_vi: "..."
  tagline_en: "..."
```

### 3.4 Danh mục sản phẩm hiện có (chốt 27/11/2026)

Chủ dự án chốt 27/11/2026: tên sản phẩm có tiền tố `Tsu` **viết liền** (`TsuCwico`, không `Tsu Cwico`). Áp dụng ngay cho
mọi văn bản mới; văn bản cũ đổi theo Phase chuyển đổi của từng repo ([`TSUMIND_MIGRATION.md`](TSUMIND_MIGRATION.md) Phase
TM7). Tên không có tiền tố `Tsu` giữ nguyên. Cột "Bất biến" là định danh đã phát hành `MUST NOT` đổi (Mục 9, Mục 13 ý 2).

| Sản phẩm | Hiển thị cũ | Hiển thị chuẩn | Slug / repo | Website | Tiền tố env | Bất biến giữ nguyên |
|---|---|---|---|---|---|---|
| Hệ sinh thái | TsuDEV | **TsuMIND** | `tsumind` (repo hiện `tsudev`) | `tsumind.com` | `TSUMIND_` | `com.tsudev.*` đã phát hành |
| Cwico | Tsu Cwico | **TsuCwico** | `tsucwico` | `cwico.tsumind.com` | `TSUCWICO_` | winget `tsudev.cwico` (cầu nối) |
| Swico | Tsu Swico | **TsuSwico** | `tsuswico` | `swico.tsumind.com` | `TSUSWICO_` | winget `tsudev.SWICO` (cầu nối) |
| Contact | Tsu Contact | **TsuContact** | `tsucontact` | `contact.tsumind.com` | `TSUCONTACT_` | Scoop `tsudev-contact` (cầu nối) |
| Tramon | Tsu Tramon | **TsuTramon** | `tsutramon` | `tramon.tsumind.com` | `TSUTRAMON_` | winget `tsudev.TrafficMonitor` (cầu nối) |
| Disk | TsuDisk | **TsuDisk** | `tsudisk` | `disk.tsumind.com` | `TSUDISK_` | - |
| Files | TsuFiles | **TsuFiles** | `tsufiles` | `files.tsumind.com` | `TSUFILES_` | khoá cập nhật Velopack hiện tại |
| Scan | Tsu Scan | **TsuScan** | `tsuscan` | `scan.tsumind.com` | `TSUSCAN_` | - |
| Guard | TsuGuard | **TsuGuard** | `tsuguard` | `guard.tsumind.com` | `TSUGUARD_` | - |
| Link (thư viện) | Tsu Link | **TsuLink** | `tsulink` | - | `TSULINK_` | - |
| Lotus Share | Lotus Share | Lotus Share | `lotus-share` | `lotus.tsumind.com` | `LOTUS_SHARE_` | `com.tsudev.lotus` |
| Sound Db | Sound Db | Sound Db | `sound-db` | `sound.tsumind.com` | `SOUND_DB_` | - |
| Quly Thu Chi | Quly Thu Chi | Quly Thu Chi | `qulythuchi` | `qulythuchi.tsumind.com` | `QULYTHUCHI_` | - |
| La bàn | La bàn | La bàn | `app-la-ban` | `compass.tsumind.com` | `COMPASS_` | - |
| Giao diện Flutter dùng chung | `tsudev_ui` | `tsumind_ui` | `tsudev-ui-flutter` → `tsumind-ui-flutter` | - | - | gói cũ giữ bản cuối trỏ sang gói mới |

- Định danh **mới** (sản phẩm chưa phát hành, gói mới): `com.tsumind.<sanpham>`, winget `tsumind.<sanpham>`, Scoop/APT
  `tsumind-<sanpham>` hoặc slug sản phẩm.
- Định danh **đã phát hành** (`com.tsudev.lotus`, `tsudev.cwico`...): giữ nguyên, thêm định danh mới song song theo
  [`TSUMIND_MIGRATION.md`](TSUMIND_MIGRATION.md) Phase TM9. Gắn `TMNC-EXCEPTION` tại chỗ khai báo.
- Mảng trò chơi `TsuGameLabs` là thương hiệu riêng, không thuộc bảng này.

---

## 4. Biến thể bị cấm và dạng thay thế

Các dạng dưới đây **KHÔNG ĐƯỢC** xuất hiện trong code, tài liệu, giao diện, metadata, tên repo hoặc tên file mới. Dạng đúng phụ thuộc ngữ cảnh (Mục 5).

### 4.1 Thương hiệu gốc

| Biến thể sai | Lý do | Thay bằng |
|---|---|---|
| `Tsumind` | MIND phải viết hoa | `TsuMIND` (hiển thị) / `TsuMind` (định danh) |
| `tsumind` (trong văn bản hiển thị) | Chữ thường chỉ dùng cho slug | `TsuMIND` |
| `TSUMIND` (trong văn bản hiển thị) | Chỉ dùng cho hằng/biến môi trường | `TsuMIND` |
| `Tsu MIND`, `Tsu Mind` | Có khoảng trắng | `TsuMIND` |
| `TSU MIND`, `TSU Mind` | Có khoảng trắng, sai hoa/thường | `TsuMIND` |
| `Tsu-MIND`, `Tsu_MIND` | Có dấu nối | `TsuMIND` |

### 4.2 Sản phẩm Cwico

| Biến thể sai | Lý do | Thay bằng |
|---|---|---|
| `Cwico` (xuất hiện lần đầu, thiếu tiền tố) | Thiếu nhận diện hệ sinh thái | `TsuCwico` hoặc `TsuMIND Cwico` |
| `TsuCWICO` | Viết hoa sai ở phần sản phẩm | `TsuCwico` |
| `TSUCWICO` (hiển thị) | Chỉ dành cho hằng/biến môi trường | `TsuCwico` |
| `tsuwico` | **Thiếu chữ `c`, sai chính tả** | `tsucwico` (slug) hoặc `TsuCwico` |
| `Tsu Cwico` | Có khoảng trắng | `TsuCwico` |
| `TSU Cwico` | Có khoảng trắng, sai hoa/thường | `TsuCwico` |
| `tsu-cwico` | Tách token bằng dấu nối | `tsucwico` (slug thương hiệu liền) |

> **Ngoại lệ cần chủ dự án duyệt:** nếu repo hiện có đã công khai dưới tên cũ và việc đổi tên làm hỏng liên kết, hãy dùng cơ chế redirect của nền tảng (Mục 16) thay vì xóa tên cũ.

---

## 5. Ma trận dạng viết theo ngữ cảnh

Đây là bảng quan trọng nhất. **Chọn dạng viết dựa vào nơi tên xuất hiện.**

| Ngữ cảnh | Quy tắc | TsuMIND | TsuCwico |
|---|---|---|---|
| Văn bản hiển thị cho người dùng (UI, website, tài liệu, README, store listing) | Tên chuẩn | `TsuMIND` | `TsuCwico` / `TsuMIND Cwico` |
| Tiêu đề phần mềm (title bar, About, splash) | Tên chuẩn | `TsuMIND` | `TsuCwico` |
| Tên repo GitHub, tên thư mục gốc, URL | slug chữ thường | `tsumind` | `tsucwico` |
| Tên repo có hậu tố vai trò | `slug-vaitro` | `tsumind-core` | `tsucwico-cli` |
| Tên file, thư mục thông thường | `kebab-case` | `tsumind-config.json` | `tsucwico-scanner.md` |
| Namespace / package (C#, Kotlin, Java) | PascalCase theo từng cấp | `TsuMind` | `TsuMind.Cwico` |
| Class, struct, enum, interface, type | PascalCase | `TsuMindClient` | `TsuCwicoScanner` |
| Hàm, phương thức, biến (JS/TS, Swift, Kotlin, Java, Dart) | camelCase | `tsuMindVersion` | `scanInstalledApps()` |
| Hàm, biến, module (Python, Rust, Ruby) | snake_case | `tsu_mind_version` | `scan_installed_apps()` |
| Hằng số | SCREAMING_SNAKE_CASE | `TSUMIND_API_URL` | `TSUCWICO_MAX_DEPTH` |
| Biến môi trường | `TSUMIND_` hoặc `TSUCWICO_` + tên | `TSUMIND_ENV` | `TSUCWICO_LOG_LEVEL` |
| Khóa cấu hình (JSON/YAML/TOML) | `snake_case` | `tsumind_env` | `deep_scan` |
| Khóa i18n / localization | `dot.separated.lowercase` | `tsumind.app.name` | `tsucwico.scan.title` |
| CSS class, ID, custom property | `kebab-case`, tiền tố sản phẩm | `.tsumind-header` | `--tsucwico-accent` |
| Tên bảng/cột CSDL | `snake_case`, số nhiều cho bảng | `tsumind_users` | `tsucwico_scan_results` |
| Endpoint API (URL path) | `kebab-case`, số nhiều | `/v1/tsumind/projects` | `/v1/cwico/scan-jobs` |
| Tên sự kiện/analytics | `snake_case` | `tsumind_app_opened` | `tsucwico_scan_completed` |
| Tên file thực thi Windows | PascalCase + `.exe` | `TsuMIND.exe` | `TsuCwico.exe` |
| Bundle ID / Package ID | Reverse-DNS chữ thường | `com.tsumind.app` | `com.tsumind.cwico` |
| Tên Docker image | `slug` | `tsumind/core` | `tsumind/cwico` |

> **Quy tắc viết hoa từ viết tắt trong định danh.** Trong PascalCase/camelCase, `MIND` được xử lý như **một từ thường** (`TsuMind`, `tsuMind`), không viết `TsuMIND` hay `tsuMIND`. Dạng `TsuMIND` chỉ dành cho **văn bản hiển thị**.

### 5.1 Quy tắc dẫn xuất máy móc

Từ tên chuẩn `TsuXxxx`, tách token `tsu` + `xxxx`:

```
display   : TsuXxxx                     (giữ nguyên)
slug      : tsuxxxx                     (chữ thường, nối liền)
pascal    : TsuXxxx
camel     : tsuXxxx
snake     : tsu_xxxx
env       : TSUXXXX_ + TÊN_BIẾN
reverse   : com.tsumind.xxxx            (sản phẩm nằm dưới tên miền hệ sinh thái)
```

---

## 6. Repo, thư mục và file

### 6.1 Repo
- Dạng: `tsumind` cho repo gốc/tổng quan; `tsu<sanpham>` hoặc `tsumind-<sanpham>` cho sản phẩm; **chọn một mẫu duy nhất và áp dụng cho mọi sản phẩm** (xem Mục 17, điểm cần xác nhận).
- Repo phụ trợ: `<slug-sanpham>-<vaitro>` với vai trò thuộc danh sách: `core`, `cli`, `ui`, `api`, `web`, `docs`, `installer`, `updater`, `sdk`, `infra`, `plugins`.
- **KHÔNG** dùng chữ hoa, khoảng trắng, dấu gạch dưới, hoặc tên cá nhân trong tên repo.

Ví dụ đúng: `tsucwico`, `tsucwico-cli`, `tsucwico-docs`, `tsumind-web`.
Ví dụ sai: `TsuCWICO`, `Tsu Cwico`, `tsu_cwico`, `tsuwico`, `Cwico-new`, `cwico-final-v2`.

### 6.2 Thư mục dự án (`~/projects/*`)
- Tên thư mục gốc của dự án trên máy phát triển **PHẢI trùng slug repo**.
- Thư mục con dùng `kebab-case` (ngoại lệ: thư mục quy ước của ngôn ngữ, ví dụ Python package dùng `snake_case`, C# project dùng PascalCase theo namespace).

Cấu trúc khuyến nghị:

```text
tsucwico/
├─ README.md
├─ LICENSE
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ docs/
│  ├─ naming-convention.md         # liên kết/bản sao quy ước này
│  └─ architecture.md
├─ src/
│  ├─ TsuMind.Cwico.Core/          # C#: tên project = namespace
│  └─ TsuMind.Cwico.Cli/
├─ tests/
├─ scripts/
└─ .github/
   └─ workflows/
```

### 6.3 File
| Loại file | Quy tắc | Ví dụ |
|---|---|---|
| Tài liệu Markdown thường | `kebab-case.md` | `scan-engine-design.md` |
| Tài liệu chuẩn của repo | `UPPERCASE.md` | `README.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md` |
| Source theo ngôn ngữ | Theo quy ước ngôn ngữ (Mục 8) | `ScanEngine.cs`, `scan_engine.py`, `scan-engine.ts` |
| Script shell/PowerShell | `kebab-case` + đuôi đúng | `build-release.ps1`, `clean-cache.sh` |
| File cấu hình | `kebab-case` hoặc theo công cụ | `tsucwico.config.json`, `.editorconfig` |
| Workflow CI | `kebab-case.yml` | `build-windows.yml`, `release-testflight.yml` |
| Tài nguyên (ảnh, icon) | `kebab-case`, mô tả + kích thước | `tsucwico-logo-512.png` |
| File phát hành (artifact) | `<TênChuẩn>-<phiênbản>-<nềntảng>.<đuôi>` | `TsuCwico-1.2.0-win-x64.exe` |

**KHÔNG** dùng khoảng trắng, ký tự có dấu tiếng Việt, hoặc hậu tố mơ hồ (`final`, `new`, `copy`, `v2`, `backup`) trong tên file.

---

## 7. Đặt tên trong code (nguyên tắc chung)

### 7.1 Quy tắc chung
1. Tên viết bằng **tiếng Anh**, không dấu, không viết tắt khó hiểu. Chấp nhận các từ viết tắt phổ biến: `id`, `url`, `api`, `ui`, `db`, `cli`, `io`, `ctx`, `cfg`.
2. Tên phải **mô tả mục đích**, không mô tả kiểu dữ liệu (`installedApps` thay vì `list1`, `appArray`).
3. Hàm đặt bằng **động từ**: `scanRegistry`, `removeLeftoverFiles`.
4. Biến boolean bắt đầu bằng `is`, `has`, `can`, `should`: `isElevated`, `hasLeftovers`.
5. Tập hợp dùng **số nhiều**: `installedApps`; phần tử đơn dùng số ít: `installedApp`.
6. **Không** nhúng tên thương hiệu vào tên hàm/biến nội bộ nếu namespace/module đã thể hiện sẵn (`TsuMind.Cwico.Scanner` thay vì `TsuCwicoScanner` bên trong namespace `TsuMind.Cwico`). Chỉ gắn tiền tố thương hiệu cho **định danh công khai** hoặc **dùng ngoài phạm vi module** (biến môi trường, tên bảng, tên sự kiện, CSS, khóa i18n).
7. Không dùng tên gây nhầm với thương hiệu bên thứ ba.

### 7.2 Mẫu đặt tên theo loại

| Loại | Mẫu | Ví dụ |
|---|---|---|
| Class dịch vụ | `<DanhTừ><VaiTrò>` | `RegistryScanner`, `LeftoverCleaner` |
| Interface | `I` + PascalCase (C#/Java) / PascalCase không tiền tố (Swift, TS ưu tiên) | `IUninstaller` |
| Enum | PascalCase số ít; giá trị PascalCase (C#/Swift) hoặc SCREAMING_SNAKE (Python/TS) | `ScanMode.Deep` |
| Exception/Error | `<Mô tả>Exception` / `<Mô tả>Error` | `RegistryAccessException` |
| Test | `<Đơn vị>Tests` + tên hành vi | `ScannerTests.ReturnsEmptyWhenNoApps` |
| Thư viện nội bộ | `tsumind-<chứcnăng>` | `tsumind-logging` |

---

## 8. Quy ước theo ngôn ngữ

| Ngôn ngữ | Namespace/Package | Class/Type | Hàm/Phương thức | Biến/Tham số | Hằng | File |
|---|---|---|---|---|---|---|
| **C# / .NET** | `TsuMind.Cwico.Core` | PascalCase | PascalCase | camelCase; field riêng `_camelCase` | PascalCase hoặc `SCREAMING` cho `const` công khai theo nhóm | `PascalCase.cs` |
| **PowerShell** | Module `TsuMind.Cwico` | n/a | `Verb-TsuCwicoNoun` | `$camelCase` | `$script:UPPER` | `kebab-case.ps1` |
| **Python** | `tsumind_cwico` | PascalCase | snake_case | snake_case | SCREAMING_SNAKE | `snake_case.py` |
| **TypeScript/JS** | `@tsumind/cwico-*` (npm scope) | PascalCase | camelCase | camelCase | SCREAMING_SNAKE | `kebab-case.ts` (component React: `PascalCase.tsx`) |
| **Swift** | Module `TsuMindCwico` | PascalCase | camelCase | camelCase | camelCase (`static let`) | `PascalCase.swift` |
| **Kotlin/Java (Android)** | `com.tsumind.cwico.*` (chữ thường) | PascalCase | camelCase | camelCase | SCREAMING_SNAKE | `PascalCase.kt` |
| **Dart/Flutter** | `tsumind_cwico` | PascalCase | camelCase | camelCase | camelCase / `kPrefix` không dùng; ưu tiên camelCase | `snake_case.dart` |
| **Shell/Bash** | n/a | n/a | `snake_case` | `snake_case`; biến export `UPPER` | UPPER | `kebab-case.sh` |
| **SQL** | n/a | n/a | n/a | `snake_case` | n/a | `NNN_mota_ngan.sql` |

Ví dụ PowerShell cho cmdlet công khai: `Get-TsuCwicoLeftover`, `Invoke-TsuCwicoScan`.

---

## 9. Định danh phân phối và hệ thống

| Hạng mục | Quy tắc | Ví dụ |
|---|---|---|
| Bundle ID iOS/macOS | `com.tsumind.<sanpham>` chữ thường | `com.tsumind.cwico` |
| Application ID Android | Như trên | `com.tsumind.cwico` |
| Windows Product Name (metadata `.exe`) | Tên chuẩn hiển thị | `TsuCwico` |
| Windows Company Name | `TsuMIND` | `TsuMIND` |
| Windows File Description | Tên đầy đủ tiếng Việt hoặc tagline | xem Mục 11 |
| Thư mục cài đặt | `%ProgramFiles%\TsuMIND\TsuCwico` | |
| Dữ liệu người dùng | `%AppData%\TsuMIND\TsuCwico` | |
| Registry key | `HKCU\Software\TsuMIND\TsuCwico` | |
| Tên Windows Service | `TsuCwicoService` | |
| Tên file log | `tsucwico-YYYYMMDD.log` | `tsucwico-20261127.log` |
| Mutex / pipe name | `TsuMIND.TsuCwico.<mục đích>` | `TsuMIND.TsuCwico.SingleInstance` |
| URL scheme / deep link | `tsucwico://` | |
| Tên miền/đường dẫn web | slug chữ thường | `tsumind.<tên-miền>/cwico` |

> Định danh công khai (bundle ID, Application ID, URL scheme, tên service) là **bất biến** sau phát hành. Đổi chúng cần phê duyệt riêng của chủ dự án vì ảnh hưởng cập nhật, dữ liệu người dùng và chữ ký.

---

## 10. CI/CD, release và phiên bản

### 10.1 Pipeline
| Hạng mục | Quy tắc | Ví dụ |
|---|---|---|
| Tên workflow (`name:` trong YAML) | Tiếng Anh, Title Case, có tên sản phẩm | `TsuCwico - Build Windows` |
| Tên job/step | `kebab-case` cho `id`, mô tả rõ cho `name` | `id: build-win-x64` |
| Secrets / Variables | `TSUMIND_` hoặc `TSUCWICO_` + mô tả, SCREAMING_SNAKE | `TSUCWICO_SIGNING_CERT_BASE64` |
| Tên artifact | Như Mục 6.3 | `TsuCwico-1.2.0-win-x64` |
| Cấu hình Codemagic/Xcode Cloud | Tên workflow `tsucwico-<nềntảng>-<mụcđích>` | `tsucwico-ios-testflight` |

### 10.2 Git
| Hạng mục | Quy tắc | Ví dụ |
|---|---|---|
| Nhánh chính | `main` | |
| Nhánh làm việc | `<loại>/<mô-tả-kebab>` với loại ∈ `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `release` | `feat/deep-registry-scan` |
| Commit | Conventional Commits, tiếng Anh, thì hiện tại | `feat(scanner): add leftover folder detection` |
| Scope commit | Tên module viết thường | `scanner`, `ui`, `installer` |
| Tag phát hành | `v` + SemVer | `v1.2.0`, `v1.3.0-beta.1` |
| Tiêu đề PR | Giống commit | |
| Nhãn issue | `kebab-case` | `good-first-issue`, `needs-triage` |

Nếu commit/PR nhắc đến thương hiệu, phải dùng dạng hiển thị chuẩn (`TsuMIND`, `TsuCwico`).

---

## 11. Nội dung giới thiệu, mô tả và tài liệu

### 11.1 Quy tắc ngôn ngữ và giọng văn
- Tên thương hiệu viết **đúng nguyên dạng ở mọi vị trí**: đầu câu, giữa câu, tiêu đề. **KHÔNG** tự động viết hoa toàn bộ hay hạ chữ thường (kể cả khi dùng CSS `text-transform` hay hàm đổi hoa/thường cho tiêu đề; phải loại tên thương hiệu khỏi phép đổi).
- Tên đầy đủ tiếng Việt viết **hoa chữ cái đầu câu**, không viết hoa từng từ: "Bộ công cụ rà quét và gỡ bỏ phần mềm Windows chuyên sâu".
- Thuật ngữ nước ngoài giữ nguyên: Windows, GitHub, TestFlight, App Store.
- Văn phong: rõ ràng, chuyên nghiệp, trung tính; tránh khẩu ngữ, tránh tuyên bố tuyệt đối không kiểm chứng ("tốt nhất", "100% sạch").

### 11.2 Khối giới thiệu chuẩn (boilerplate)

**Tiếng Việt - dạng ngắn (1 câu):**
> **TsuCwico** là bộ công cụ rà quét và gỡ bỏ phần mềm Windows chuyên sâu thuộc hệ sinh thái **TsuMIND**.

**Tiếng Việt - dạng đầy đủ (đoạn mở đầu README/website):**
> **TsuCwico** (tên đầy đủ: *Bộ công cụ rà quét và gỡ bỏ phần mềm Windows chuyên sâu*) giúp rà quét ứng dụng đã cài, phát hiện và dọn dẹp tệp, thư mục, mục registry còn sót lại, giúp giải phóng dung lượng ổ đĩa. Dự án thuộc hệ sinh thái **TsuMIND**.

**English - short:**
> **TsuCwico** is a deep scan and uninstall toolkit for Windows, part of the **TsuMIND** ecosystem.

> Mô tả tính năng trong boilerplate phải khớp thực tế sản phẩm; người phụ trách cập nhật khi tính năng thay đổi.

### 11.3 Khối ghi chú cuối tài liệu/README
```markdown
---
© TsuMIND. Thuộc hệ sinh thái TsuMIND.
```

### 11.4 Mẫu README tối thiểu
```markdown
# TsuCwico

> Bộ công cụ rà quét và gỡ bỏ phần mềm Windows chuyên sâu - thuộc hệ sinh thái TsuMIND.

## Giới thiệu
## Tính năng
## Yêu cầu hệ thống
## Cài đặt
## Sử dụng
## Phát triển
## Quy ước đặt tên
Xem [TSUMIND_NAMING_CONVENTION.md](docs/naming-convention.md).
## Giấy phép
```

### 11.5 Header file mã nguồn (tùy chọn nhưng nên thống nhất)
```text
// TsuMIND - TsuCwico
// <Mô tả ngắn vai trò của file>
```

### 11.6 Metadata gói/ứng dụng
| Trường | Giá trị |
|---|---|
| `name` (package.json, pyproject…) | slug hoặc scope (`tsucwico`, `@tsumind/cwico-core`) |
| `displayName` / `title` | `TsuCwico` |
| `description` | Tagline EN (gói công khai) hoặc VI (ứng dụng nội địa) |
| `author` / `publisher` / `company` | `TsuMIND` |
| `homepage`, `repository` | URL slug chuẩn |

---

## 12. Ví dụ đối chiếu đúng/sai

| Tình huống | ❌ Sai | ✅ Đúng |
|---|---|---|
| Tiêu đề trang web | `TSU Cwico - Gỡ phần mềm` | `TsuCwico - Gỡ bỏ phần mềm Windows chuyên sâu` |
| Tên repo | `TsuCWICO`, `tsuwico` | `tsucwico` |
| Biến môi trường | `tsucwico_log` | `TSUCWICO_LOG_LEVEL` |
| Class C# | `TsuCWICOScanner` | `TsuCwicoScanner` hoặc `Scanner` trong `TsuMind.Cwico` |
| Namespace | `Tsumind.CWICO` | `TsuMind.Cwico` |
| Tên file thực thi | `tsu cwico.exe` | `TsuCwico.exe` |
| Khóa i18n | `TSU_CWICO_TITLE` | `tsucwico.app.title` |
| Văn bản UI | `Chào mừng đến với TSU MIND` | `Chào mừng đến với TsuMIND` |
| Bundle ID | `com.TsuMIND.TsuCWICO` | `com.tsumind.cwico` |
| Tên artifact | `cwico_final_v2.exe` | `TsuCwico-1.2.0-win-x64.exe` |
| Hàm | `DoStuff()`, `scan1()` | `ScanInstalledApps()` |

---

## 13. Ngoại lệ được phép

Chỉ các trường hợp sau được giữ nguyên tên không theo quy ước:
1. Tên do **bên thứ ba** quy định (tên API, tên thư viện, khóa registry hệ điều hành, tên file hệ thống).
2. **Tương thích ngược** đã phát hành công khai (định danh bất biến ở Mục 9, dữ liệu người dùng cũ, URL đã phát hành) - phải có cơ chế redirect/migration.
3. **Trích dẫn nguyên văn** (changelog lịch sử, issue cũ, tài liệu trích dẫn).
4. Tên **bắt buộc** do kho ứng dụng/nền tảng áp đặt (khi tên chuẩn đã bị chiếm): phải được chủ dự án phê duyệt và ghi lại trong Brand Registry.

Mọi ngoại lệ **PHẢI** ghi chú ngay tại vị trí đó bằng comment ngắn:
```text
// TMNC-EXCEPTION: tên do Windows quy định, không đổi.
```

---

## 14. Kiểm tra tự động

### 14.1 Quét biến thể bị cấm (grep)

```bash
# Chạy ở thư mục gốc repo. Kết quả rỗng = đạt.
grep -RInE --exclude-dir={.git,node_modules,build,dist,bin,obj,.venv} \
  -e '\bTsumind\b' \
  -e '\bTsu[ _-]MIND\b' \
  -e '\bTSU[ _-]?MIND\b' \
  -e '\bTsuCWICO\b' \
  -e '\bTSU[ _-]?CWICO\b' \
  -e '\bTsu[ _-]Cwico\b' \
  -e '\btsuwico\b' \
  -e '\btsu-cwico\b' \
  . | grep -v 'TMNC-EXCEPTION'
```

> Lưu ý: dòng `TSUMIND_...` / `TSUCWICO_...` (biến môi trường, hằng) là **hợp lệ** nên mẫu trên dùng ranh giới từ `\b` và loại trừ hậu tố `_`; nếu công cụ báo nhầm, kiểm tra thủ công theo Mục 5.

### 14.2 Tích hợp CI
- Thêm bước **naming-lint** vào workflow `pull_request`, chạy lệnh ở 14.1 và **làm fail build** khi có kết quả.
- Dùng `.editorconfig` và linter của ngôn ngữ (Roslyn analyzers, ESLint `naming-convention`, `ruff`/`pylint`, SwiftLint, ktlint, `dart analyze`) để ép quy ước chữ hoa/thường trong code.
- Thêm `CODEOWNERS` cho file Brand Registry và tài liệu này.

### 14.3 Quy ước ESLint mẫu (TypeScript)
```json
{
  "rules": {
    "@typescript-eslint/naming-convention": [
      "error",
      { "selector": "default", "format": ["camelCase"] },
      { "selector": "typeLike", "format": ["PascalCase"] },
      { "selector": "variable", "modifiers": ["const", "global"], "format": ["UPPER_CASE", "camelCase"] }
    ]
  }
}
```

---

## 15. Checklist trước khi mở PR

- [ ] Mọi tên thương hiệu trong văn bản hiển thị là `TsuMIND` / `TsuCwico` (không khoảng trắng, đúng hoa/thường).
- [ ] Repo, thư mục, URL dùng slug chữ thường đúng mẫu.
- [ ] Định danh code đúng kiểu theo ngôn ngữ; `MIND` được xử lý là `Mind` trong PascalCase/camelCase.
- [ ] Biến môi trường, hằng, secret dùng tiền tố `TSUMIND_` / `TSUCWICO_`.
- [ ] Không có biến thể bị cấm ở Mục 4 (đã chạy lệnh Mục 14.1).
- [ ] Tên hàm là động từ, tên biến mô tả rõ, boolean có tiền tố `is/has/can/should`.
- [ ] Tên file/artifact không chứa `final`, `new`, `copy`, `v2`.
- [ ] Nội dung giới thiệu/mô tả dùng đúng boilerplate Mục 11.
- [ ] Định danh công khai không bị đổi ngoài phê duyệt.
- [ ] Ngoại lệ (nếu có) đã gắn `TMNC-EXCEPTION` và nêu lý do trong PR.

---

## 16. Quy trình đổi tên/di chuyển hệ thống cũ (migration)

Áp dụng cho các repo/thư mục/website đang dùng tên sai (ví dụ `TsuCWICO`, `tsuwico`, `Tsu Cwico`).

| Bước | Hành động |
|---|---|
| 1 | Kiểm kê: chạy lệnh Mục 14.1 và liệt kê mọi vị trí dùng tên cũ (code, tài liệu, CI, website, store, metadata). |
| 2 | Chốt tên đích trong Brand Registry (Mục 3). |
| 3 | Đổi tên repo trên nền tảng (GitHub tự redirect URL cũ); cập nhật remote cục bộ: `git remote set-url origin <url-mới>`. |
| 4 | Đổi tên thư mục cục bộ trong `~/projects/*` cho trùng slug repo. |
| 5 | Sửa nội dung: tên hiển thị, định danh code, cấu hình CI, secrets (tạo secret mới theo tiền tố chuẩn, xóa secret cũ sau khi pipeline xanh). |
| 6 | Website: đặt redirect 301 từ URL cũ sang URL mới; cập nhật `canonical`, `sitemap`, `og:title`. |
| 7 | Định danh bất biến (bundle ID, service name…): **không đổi** trừ khi có phê duyệt; nếu đổi, có kế hoạch migrate dữ liệu người dùng. |
| 8 | Ghi vào `CHANGELOG.md`: "Chuẩn hóa tên theo TsuMIND Naming Convention v1.0.0". |
| 9 | Chạy lại kiểm tra Mục 14 và checklist Mục 15 trước khi gộp PR. |

Nên tách việc đổi tên thành **PR riêng**, không trộn với thay đổi tính năng, để dễ review và dễ hoàn tác.

---

## 17. Các điểm đã chốt (27/11/2026)

| # | Điểm | Đã chốt |
|---|---|---|
| 1 | Dạng viết tên sản phẩm | `Tsu` + từ viết hoa chữ đầu, viết liền: `TsuCwico`, `TsuSwico`, `TsuTramon` |
| 2 | Mẫu tên repo sản phẩm | `tsu<sanpham>` (đúng mẫu đang chạy: `tsucwico`, `tsuswico`, `tsufiles`); repo phụ trợ `<slug>-<vaitro>` |
| 3 | Namespace | `TsuMind.<SanPham>` (C#: `TsuMind.Cwico`); repo đã phát hành giữ namespace cũ tới đợt tái cấu trúc của chính repo đó |
| 4 | Reverse-DNS | `com.tsumind.<sanpham>` cho định danh MỚI; định danh đã phát hành giữ nguyên (Mục 3.4) |
| 5 | Tên đầy đủ và tagline | Mỗi repo tự điền mẫu Mục 3.3 vào tài liệu brand của mình, chủ dự án duyệt trong PR |
| 6 | Tên miền và URL | `tsumind.com`; sản phẩm ở subdomain một cấp `<sanpham>.tsumind.com` (không dùng `tsumind.com/<sanpham>`); `tsudev.com` chuyển hướng 301 vĩnh viễn |

## 18. Quản trị tài liệu

| Hạng mục | Quy định |
|---|---|
| Chủ sở hữu | Chủ dự án TsuMIND |
| Vị trí chuẩn | `docs/naming-convention.md` trong mỗi repo (hoặc liên kết tới repo trung tâm) |
| Thay đổi | Qua PR có phê duyệt của chủ sở hữu; tăng phiên bản theo SemVer |
| Phiên bản patch | Sửa lỗi chính tả, làm rõ |
| Phiên bản minor | Thêm sản phẩm/ngôn ngữ/ngữ cảnh mới |
| Phiên bản major | Thay đổi tên chuẩn hoặc quy tắc làm vỡ tương thích |

### Lịch sử thay đổi
| Phiên bản | Ngày | Nội dung |
|---|---|---|
| 1.1.0 | 2026-11-27 | Vào bộ quy ước `v10.0.0`: danh mục mọi sản phẩm (Mục 3.4), chốt Mục 17, bỏ em-dash. |
| 1.0.0 | 2026-11-27 | Bản đầu tiên: chuẩn hóa thương hiệu TsuMIND, sản phẩm Cwico, quy ước repo/file/code/nội dung giới thiệu. |
