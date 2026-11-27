# PLAN.md - Kế hoạch chuyển đổi TsuDEV → TsuMIND

> **Agent ở repo con đọc bản này trong `.standards/docs/`:** đây là kế hoạch TOÀN HỆ của repo bộ quy ước, không phải
> kế hoạch của repo bạn (kế hoạch của bạn là `docs/PLAN.md` ở gốc repo bạn). Việc của repo bạn đến qua phiếu `TM7`
> trong `logs/handover/` của chính repo bạn.

> Nguồn sự thật về tiến độ theo Phase (`AGENT_PROTOCOL.md` mục 4.2). Một ngữ cảnh làm MỘT Phase; xong Phase đánh `[x]`,
> cập nhật `logs/STATE.md`, commit, viết phiếu bàn giao rồi DỪNG.
> Đặc tả: [`TSUMIND_MIGRATION.md`](TSUMIND_MIGRATION.md) (mục 0.3 có quyết định + ánh xạ task P0-P11).
> Đặt tên: [`NAMING_CONVENTION.md`](NAMING_CONVENTION.md). Chủ dự án chốt làm ngay, 27/11/2026 (D-08).

Ký hiệu: **[OWNER]** chỉ chủ dự án làm được (đăng nhập, 2FA, tạo token, bấm Allow, thanh toán - R-05).
**[Gx]** cổng phê duyệt ở `TSUMIND_MIGRATION.md` R-04.

## Phase TM1 - Nền móng: quy ước đặt tên, kế hoạch, bộ logo

- [x] `docs/NAMING_CONVENTION.md` v1.1.0: danh mục mọi sản phẩm (mục 3.4), chốt mục 17
- [x] `docs/TSUMIND_MIGRATION.md` v1.1: mục 0.3 quyết định D-08..D-12, hạ tầng thật, ánh xạ Phase
- [x] `scripts/check-naming.sh` (cảnh báo mặc định, `NAMING_STRICT=1` chặn, `NAMING_LEGACY=1` quét tên cũ)
- [x] Bộ logo `assets/brand/tsumind/`: nguồn (ảnh gốc + SVG vẽ tay), `build.mjs` (tách nền giả + watermark, AVIF/WebP/PNG,
      favicon 7 lớp, PWA + maskable, icon app, og-image, avatar), `--check` không cần phụ thuộc chạy trong CI
- [x] `BRAND_ASSETS.md` mục 16, `AGENTS.md`, `00-INDEX.md`, `CHANGELOG.md`, `VERSION` 10.0.0, `MANIFEST.sha256`

**Nghiệm thu:** `check-standards.sh` + `build.mjs --check` xanh ở CI; PR merge; nhãn `v10.0.0`.

## Phase TM2 - Sổ tay nhận diện thương hiệu + quy chuẩn giao diện thống nhất

- [x] [OWNER] Bộ logo: chủ dự án giao **bộ logo chính thức + Sổ tay** 27/11/2026 (thay bộ thử TM1); nguồn ở
      `assets/brand/tsumind/source/`, `build.mjs` sinh 75 tệp. Chốt: văn bản giữ `TsuMIND`, phông theo Sổ tay
- [x] `v10.2.0` (28/11/2026): chuẩn hoá lại bộ logo từ **5 hình chủ dự án chốt** (bộ zip xén mất nửa dưới con cú):
      `source/original` → `tools/make_masters.py` (Real-ESRGAN x4, tách nền, squircle siêu elip) → `source/master` →
      `build.mjs` 122 tệp (AVIF/WebP/PNG, `.ico`, `.icns`, Linux hicolor, Android adaptive + themed, logo ngang nền sáng)
- [x] `docs/BRAND_GUIDELINES.md` v1.0.0: biến thể, vùng an toàn, cỡ tối thiểu, hệ màu Sổ tay (Midnight Navy `#0A1B3D`,
      Deep Circuit Blue `#13408A`, Electric Blue `#1E9BFF`, Neon Cyan `#3CD2F5`, Chrome Silver `#E4EAF4`, Slate Gray
      `#5B6B85`) + bảng WCAG đo được, phông Exo 2 / Inter / JetBrains Mono, giọng văn, điều cấm, bảo hộ, đa nền tảng
- [x] Token: `tokens/products/tsumind.json` (hue 249 Electric Blue, Exo 2); `tsudev.json` giữ với `supersededBy` tới
      Phase TM6 (repo `tsudev` đọc cứng tệp này); tên sản phẩm viết liền; `gen-product-palette` + `check-products` +
      `check-contrast` xanh
- [x] Quy chuẩn bố cục chung: `DESIGN_SYSTEM.md` mục 3.1 (header, nội dung, chân trang, nút, overlay một lớp, thang
      z-index, không chồng lấn) + `ECOSYSTEM_IDENTITY.md` mục 4.4 (khối "Thuộc hệ sinh thái TsuMIND")

**Nghiệm thu:** chủ dự án duyệt sổ tay; cổng tương phản xanh; PR merge (MINOR).

## Phase TM3 - Hồ sơ pháp lý và công bố hệ sinh thái số

- [x] Tra văn bản HIỆN HÀNH (nguồn chính thức): Luật Bảo vệ dữ liệu cá nhân 2025 + nghị định hướng dẫn (thay phần lớn
      NĐ 13/2023), NĐ 52/2013 + 85/2021 (TMĐT, thông báo website với Bộ Công Thương), Luật An ninh mạng, Luật ATTT mạng,
      NĐ 147/2024 (dịch vụ Internet), cơ quan quản lý sau sáp nhập (Bộ KH&CN thay Bộ TT&TT)
- [x] `docs/LEGAL_COMPLIANCE.md` + `templates/legal/`: thông tin chủ sở hữu (chân trang), chính sách bảo vệ DLCN,
      điều khoản sử dụng, chính sách an toàn thông tin, hồ sơ đánh giá tác động xử lý DLCN (Bộ Công an - A05), mẫu
      thông báo website (online.gov.vn), quy trình xử lý yêu cầu của chủ thể dữ liệu
- [x] Phiếu sang repo `tsudev` đưa khung nội dung vào chân trang, `/terms`, `/privacy`, `/security`
- [x] Ghi rõ: tài liệu mẫu không thay tư vấn pháp lý; [OWNER] ký, nộp, khai MST

**Tiến độ 28/11/2026:** [OWNER] còn treo ký/nộp/khai MST, luật sư rà soát, đóng mục "cần xác minh" (`LEGAL_COMPLIANCE.md` mục 8).

**Nghiệm thu:** mỗi nghĩa vụ có trích dẫn điều khoản + ngày tra; chủ dự án duyệt; PR merge.

## Phase TM4 - Kiểm kê + zone `tsumind.com` + `tsumind-infra`

- [x] [OWNER] Tạo API token Cloudflare có hạn, lưu `~/.config/tsudev/cloudflare-tsumind.env` (`KEY=VALUE`, 600, khoá
      `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `TSUMIND_CF_ZONE_ID`) - kiểm 28/11/2026: `active`, hết hạn
      27/12/2026, đọc được zone `tsumind.com` (active, đúng account, 0 bản ghi DNS). Đầu TM4 dò quyền ghi thật
- [ ] [OWNER] 2FA passkey; auto-renew + transfer lock; xác minh email ICANN
- [ ] Repo `tsudev-org/tsumind-infra` (private): `inventory/` P0-T02..T06 sinh bằng API, `adr/`, `runbooks/`, `iac/`
- [ ] Phần A: DNSSEC, Full (strict), TLS 1.2+/1.3, Always HTTPS, CT monitoring, WAF free + custom rules (Log trước),
      rate limit `id.`, Bot Fight, header bảo mật, `security.txt`, Email Routing + SPF/DMARC `p=none`, Resend gửi đi,
      `v=spf1 -all` cho subdomain không gửi thư, Web Analytics, Notifications, CAA sau khi đối chiếu CA
- [ ] IaC (OpenTofu + provider Cloudflare, ADR 0001), workflow plan/apply có phê duyệt, drift + backup DNS + audit tuần
- [ ] Trang giữ chỗ `tsumind.com` (Worker tĩnh, header bảo mật đủ) cho tới TM6

**Nghiệm thu:** danh mục cuối Phần A đạt (trừ HSTS preload - G4); chi phí 0 đồng.

## Phase TM5 - Danh tính `id.tsumind.com`

- [ ] P3-T01..T12: đa issuer, chung kho người dùng, cookie `__Host-`, OAuth Google/GitHub/Apple thêm redirect URI mới
      (giữ cũ), WebAuthn Related Origins hoặc đăng ký lại passkey (ADR), CORS/CSP, email xác thực
- [ ] Làm trong repo sở hữu `id.` - phiếu sang phiên repo đó

## Phase TM6 - Website gốc `tsumind.com`

- [ ] Repo `tsudev`: `config/topology.json` thêm domain mới, rebrand hiển thị, SEO, logo TM1, trang pháp lý TM3,
      `/security` có Tuyên bố liên tục khoá (P7-T03), danh bạ `/apps` dùng tên chuẩn
- [ ] Chạy song song `tsudev.com` ↔ `tsumind.com`; nghiệm thu `curl` từng subdomain (P1-T40)

## Phase TM7 - Từng repo sản phẩm

- [ ] Phiếu `TM7` sang mỗi repo (tsucwico, tsuswico, tsucontact, tsutramon, tsudisk, tsufiles, tsuscan, tsuguard,
      tsulink, lotus-share, sound-db, qulythuchi, app-la-ban, tsudev-ui-flutter, linux-packages, scoop-bucket,
      homebrew-tap): rebrand hiển thị, website `*.tsumind.com`, updater cầu nối, `check-naming.sh` → `NAMING_STRICT=1`
- [ ] Bảng theo dõi tiến độ ở `logs/STATE.md`

## Phase TM8 - Tổ chức GitHub + CI/CD

- [ ] [OWNER] Tạo org `tsumind-org` giữ tên (miễn phí) ngay - chống chiếm tên
- [ ] ADR chọn: đổi tên `tsudev-org` → `tsumind-org` hay chuyển từng repo; đối chiếu quy tắc tên cũ bất khả xâm phạm
      (`AGENTS.md` mục 4); bật lại secret scanning/push protection/CodeQL sau chuyển; ruleset, 2FA bắt buộc

## Phase TM9 - Khoá ký liên tục + phân phối gói

- [ ] Tuyên bố liên tục khoá ký bằng khoá hiện tại; KHÔNG xoay khoá (D-06)
- [ ] winget `tsumind.*` mới + cầu nối ID cũ (G8), Scoop/Homebrew/APT-RPM gói `tsumind-*` + gói chuyển tiếp

## Phase TM10 - Chuyển hướng, SEO, email, thông báo

- [ ] Redirect Rules `tsudev.com` → `tsumind.com` theo từng host đã ổn định, ngoại lệ API/JWKS/`.well-known`;
      Search Console Change of Address; email `@tsumind.com` (giữ forwarding `@tsudev.com` vĩnh viễn)

## Phase TM11 - Nghiệm thu + ngừng dần

- [ ] P10-T01..T08; sau tối thiểu 30 ngày (D-10) gỡ tài nguyên thay thế; GIỮ VĨNH VIỄN `tsudev.com` + redirect + khoá
      công khai cũ
