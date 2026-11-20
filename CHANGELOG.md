# CHANGELOG - tsudev-standards

Bộ quy ước dùng **Semantic Versioning** (`MAJOR.MINOR.PATCH`), khác với khuôn
phiên bản của app và của website. Cả ba khuôn được giải thích tại
[`docs/VERSIONING.md`](docs/VERSIONING.md).

Mới nhất trên cùng.

---

## 4.4.0 - 21/11/2026

Bản MINOR (chỉ thêm, không phá vỡ): đưa văn bản khớp hạ tầng đang chạy thật và nhận đề xuất mẫu header/chân trang.
Phiếu: `20261113-01` (linux-packages), `20261114-01` hàng tsudev-standards; đề xuất PR #52 (tsudev, phiên 53).

- `docs/PACKAGING.md` v1.2.0:
  - Mục 3.1 (mới) **dựng gói tập trung** ở `tsudev-org/linux-packages` từ `products.json` + `packaging/package.json`;
    repo sản phẩm không giữ khóa ký kho hay token R2; kiểm bản mới mỗi giờ, xuất bản qua Environment `packages` có
    duyệt; repo private phát hành qua repo công khai `<org>/tsudev-<id>-releases`.
  - Mục 5: đẩy R2 qua API S3 bằng khóa phạm vi một bucket. Mục 5.1 (mới) **`catalog.json` schema 1** cho APT/RPM,
    Scoop, Homebrew (trường `name`, `version`, `homepage`, `arch`, `install`, `installFull`, `replacedBy`), sinh cùng lần
    với kho, tự đối chiếu, job đối chiếu kênh hằng ngày.
  - Mục 6: `install.sh`/`install.ps1` đọc `catalog.json` và so vân tay khóa với giá trị **ghi cứng trong script**,
    không tin vân tay tải về.
  - Mục 7: bỏ bước `wrangler r2 object put` ở repo sản phẩm; `verify-install` APT/RPM chạy ở kho gói trên Ubuntu
    22.04/24.04, Debian 12/13, Fedora (x64) + ARM64.
  - Mục 8.1 (mới) **lệnh "Cài bằng lệnh" sinh lúc build từ danh mục**, chọn theo `homepage`; cấm chép tay, cấm gọi
    danh mục lúc chạy; gói có `replacedBy` không hiện lệnh; cổng đỏ khi khai hệ điều hành mà không có kênh.
- `docs/ECOSYSTEM_IDENTITY.md` v3.2.0: mục 4.3 (mới) **khu vực tài khoản ở header** - một nút disclosure (ảnh đại
  diện + tên) mở "Hồ sơ tài khoản", "Đăng xuất"; cấm "Đăng xuất" trần, cấm `role="menu"`; Esc/bấm ngoài/rời focus thì
  đóng; vòng tròn trơn khi phiên chưa rõ. Mục 4: cột **"Tài khoản"** ở chân trang theo phiên (`SHOULD`). Checklist mục 9.

### Hướng dẫn nâng cấp

1. Repo con sync v4.4.0 trong PR kế tiếp của nó (KHÔNG mở PR sync riêng).
2. `tsudev`: đã đạt (header #251, chân trang #252, `pkg:catalog` + `installChannels.test.ts`). Không cần làm gì.
3. Site app có trang Tải về (tsucwico, tsuswico, tsucontact, tsufiles, lotus-share, trafficmonitor...): làm khối "Cài
   bằng lệnh" sinh lúc build theo mục 8.1 (phiếu `20261114-02` đã gửi); site có đăng nhập làm mục 4.3 khi thêm đăng nhập.
4. Repo sản phẩm còn bước đẩy R2 riêng (`wrangler`) trong workflow phát hành: gỡ bước đó và token R2 khỏi secret.

## 4.3.0 - 21/11/2026

Bản MINOR (chỉ thêm, không phá vỡ): xử lý hai phiếu đề xuất đang chờ duyệt, chủ dự án uỷ quyền chọn phương án
21/11/2026. Phiếu: `20261119-01` (qulythuchi), `20261112-02` (lotus-share).

- `docs/AUTH_AND_ACCOUNT.md` v3.2.0: mục 3.2 (mới) **Đăng nhập với Apple là lối vào có điều kiện** - `MUST` cho sản phẩm
  phát hành qua App Store (Guideline 4.8), `MAY` cho phần còn lại; không mua Apple Developer Program chỉ để có nút Apple;
  nút ẩn khi IdP chưa bật; cấu hình một lần ở IdP `tsudev.com` (`idp_hint=apple`). Bẫy bắt buộc xử lý: callback
  `form_post` liên trang (không có cookie `SameSite=Lax`), tên chỉ gửi lần đầu, `client_secret` ES256 hạn 6 tháng,
  `auth/revoke` khi xoá tài khoản, thông báo máy chủ tới máy chủ, đăng ký tên miền gửi thư cho email ẩn. Mục 3.1 phạm vi
  `name email`; mục 5 email `@privaterelay.appleid.com` coi là đã xác minh nhưng không gộp tự động; mục 15 thêm
  `GET /auth/providers`, callback POST và điểm nhận thông báo của Apple; mục 16 ca kiểm thử 16; mục 17 checklist.
- `docs/PACKAGING.md` v1.1.0: mục 2.1 (mới) tên gói theo **thương hiệu riêng** được duyệt (`tsuswico`, `tsucontact`,
  `lotus-share`...) - ghi đích danh `tenRieng`, không trùng gói bản phân phối/dự án gốc. Mục 2.2 (mới) **đổi tên gói đã
  công bố**: APT gói chuyển tiếp rỗng `oldlibs`, RPM `Provides` + `Obsoletes`, Homebrew giữ cask cũ `deprecate!` +
  `replacement_cask` (`cask_renames.json` không đủ với tap riêng), Scoop giữ manifest cũ kèm `notes`, winget đã duyệt
  không đổi mã, Android không đổi `applicationId`; CI kiểm đường nâng cấp từ bản cũ thật; tên cũ giữ tối thiểu 12 tháng
  và không bao giờ dùng lại. Ghi lại đúng cách kho gói đang làm từ 12/11/2026.

### Hướng dẫn nâng cấp

1. Repo con sync v4.3.0 trong PR kế tiếp của nó (KHÔNG mở PR sync riêng).
2. `tsudev` (IdP): khi chủ dự án quyết phát hành App Store - thêm provider Apple theo mục 3.2, `GET /api/v1/auth/providers`.
   Chưa phát hành App Store thì không cần làm gì.
3. RP có đăng nhập (qulythuchi...): dựng nút nhà cung cấp từ danh sách IdP trả về, nhận `apple` khi có.
4. `linux-packages`, `scoop-bucket`, `homebrew-tap`: đối chiếu mục 2.2 (kho đã làm đúng; thêm CI kiểm nâng cấp cho
   Scoop/Homebrew nếu chưa có).

## 4.2.0 - 20/11/2026

Bản MINOR (chỉ thêm): yêu cầu chủ dự án 20/11/2026 - **sản phẩm đứng tên chủ dự án, không ghi "do AI thực hiện"**.

- `docs/AGENT_PROTOCOL.md` v2.2.0: mục 6.1 - nội dung, dữ liệu, commit/PR (không trailer `Co-Authored-By` của AI, không
  "Generated with") và biểu mẫu nền tảng đứng tên chủ dự án; tệp điều phối nội bộ (`AGENTS.md`, AKB, `logs/`) không đổi.
- `docs/STORE_SUBMISSION.md` v1.2.0: mục 0.1 - điền biểu mẫu với tư cách chủ dự án, không chọn "do AI thực hiện"; câu
  hỏi về tính năng AI thật của app (chính sách nội dung AI tạo của Google Play) vẫn trả lời đúng mã; thêm dòng checklist
  mục 3.

## 4.1.0 - 20/11/2026

Bản MINOR (chỉ thêm, không phá vỡ): yêu cầu chủ dự án 20/11/2026 - **kho tri thức dùng chung cho agent (AKB)** và chuẩn
hoá **chuỗi tin cậy phát hành** từ hai tài liệu kỹ thuật 19/11/2026. Phiếu điều phối: `20261120-02`.

- `docs/KNOWLEDGE_BASE.md` v1.0.0 (mới): chuẩn hoá đặc tả AKB gốc theo hệ tsudev - kho `~/agent-kb` ngoài repo, remote
  private `tsudev-org/agent-kb`, bản sao ổ E:; slug theo tên repo GitHub (worktree dùng chung thư mục); ranh giới với
  `logs/handover` (việc đang làm ở repo, tri thức dùng lại ở AKB); schema, ID, liên kết chéo `applied_from`; CLI `akb`
  (start/new/set/close/search/reindex/lint/sync); lint L01-L11 (L07 bí mật chặn commit); nghiệm thu đạt (39 dự án,
  9 test).
- `docs/AGENT_PROTOCOL.md` v2.1.0: mở phiên thêm `akb start` + `akb search`; đóng phiên thêm bước AKB (`akb close`,
  `akb sync`), phiếu bàn giao trỏ ID AKB thay vì chép tri thức.
- `docs/DISTRIBUTION_TRUST.md` v1.2.0: nói rõ giới hạn của huy hiệu OpenSSF và cấm né antivirus; 3.1 gói hồ sơ báo nhầm
  chuẩn + hạn **48 giờ**, đủ danh sách hãng; 4.1 `docs/threat-model.md` (STRIDE) + `docs/incident-response.md`; 4.2 yêu
  cầu theo loại sản phẩm (Electron/Tauri, web, DNSSEC/CAA/DMARC, trusted publishing); mục 5 thêm OpenSSF Best Practices
  cho MỌI repo Public, Scorecard, WDSI, xác minh Search Console bằng DNS TXT; mục 8 checklist pháp luật Việt Nam (👤
  xác nhận văn bản hiện hành); mục 9 phiếu tin cậy từng sản phẩm + Definition of Done.
- `docs/STORE_SUBMISSION.md` v1.1.0: 1.1 **sổ định danh** `docs/store/IDENTITY.md` - một nguồn cho mọi biểu mẫu, kiểm
  chéo với mã trước khi điền; trình duyệt Edge hồ sơ riêng; định dạng tệp hồ sơ `docs/store/<kenh>.md`; lý do từ chối
  ghi thêm vào AKB; 4.4 thêm OpenSSF Best Practices và Search Console/Bing.
- `docs/templates/TRUST_TICKET.md` (mới): mẫu `logs/trust/TRUST.md` (mã `TSU-<slug>`).

### Hướng dẫn nâng cấp

1. Repo con sync v4.1.0 trong PR kế tiếp của nó (KHÔNG mở PR sync riêng).
2. Repo phát hành sản phẩm: lập `logs/trust/TRUST.md` từ mẫu và `docs/store/IDENTITY.md` - theo phiếu con TR1 của repo.
3. Máy phát triển: agent đã có `akb` trong `PATH`; phiên đầu tiên của mỗi repo sau v4.1.0 backfill `02_FEATURES.md`,
   `03_RUNBOOK.md`, DEC từ ADR, ISS/LES quan trọng từ phiếu bàn giao.

---

## 4.0.0 - 20/11/2026

Bản MAJOR: quyết định chủ dự án 20/11/2026 - **TsuDEV Pro theo kỳ 1 năm, không tự gia hạn**; bỏ định danh gói tháng;
thêm `MUST` mới về nhắc gia hạn, xoá có xác minh và JWS tươi. Phiếu điều phối: `20261120-PRO2`.

- `docs/PRODUCT_POLICY.md` v1.2.0:
  - Mục 3.2, 3.3, 3.5, 7.2: một gói **TsuDEV Pro 490.000 ₫ / 1 năm**, không tự gia hạn ở mọi kênh (Play gói **trả
    trước** `nam`, App Store Non-Renewing Subscription, web VietQR); gia hạn sớm cộng dồn
    (`pro_until = max(pro_until, bây giờ) + 1 năm`); hết kỳ ⇒ **trạng thái miễn phí ("khách mời")**, ngừng đồng bộ
    lên đám mây, dữ liệu trên thiết bị giữ nguyên; tsudev.com `SHOULD` gửi thư nhắc.
  - Mục 7.4: bỏ `thang` / `com.tsudev.pro.thang`; claim tuỳ chọn `cnf.jkt` + DPoP (`SHOULD`); máy chủ nhận JWS từ app
    chỉ nhận `iat` ≤ 24 giờ (`401 reason: "stale"`); **kênh trạng thái** `POST /api/rp/entitlements/status` (không phụ
    thuộc grant 30 ngày); **xoá dữ liệu vì hết Pro `MUST` hỏi kênh trạng thái ngay trước khi xoá**, lỗi ⇒ hoãn.
  - Mục 7.5: điều khoản trước nút mua (vi/en) viết lại cho kỳ 1 năm không tự gia hạn.
  - Mục 7.6 (mới): **nhắc gia hạn 7 ngày cuối, mỗi lần mở app** + báo hết kỳ một lần - nội dung vi/en nguyên văn,
    khoá `tsu.pro_expired.notified_until`, 6 test bắt buộc.
  - Mục 8: checklist cập nhật theo các ý trên.
- `docs/STORE_SUBMISSION.md`: Play chỉ gói trả trước `nam`; App Store Non-Renewing; mục 7.6 là ngoại lệ đã duyệt.
- `docs/FREE_TIER_STACK.md` mục 3.1: xoá có xác minh.

### Hướng dẫn nâng cấp

1. **Repo có màn mua Pro** (app, tsudev.com): bỏ gói tháng khỏi giao diện và mã nguồn; chỉ còn "1 năm"; thay điều
   khoản trước nút mua bằng nguyên văn mục 7.5 mới; test so nguyên văn.
2. **Play Console** (repo đã tạo sản phẩm `tsudev_pro`): lưu trữ gói cơ sở `thang`; tạo/đổi gói `nam` sang **trả trước**
   (prepaid, P1Y, cho phép nạp thêm). Chưa tạo thì tạo đúng như trên. App Store (2027): chỉ tạo Non-Renewing
   `com.tsudev.pro.nam`.
3. **Máy chủ quyền lợi tsudev.com**: tính `pro_until` theo công thức mục 7.2; thêm kênh trạng thái + `cnf.jkt` theo
   mục 7.4; thư nhắc (`SHOULD`).
4. **Máy chủ đồng bộ** (qulythuchi, sound-db, tsuscan, app-la-ban, TsuDEV Sync...): trước khi xoá vì hết Pro gọi kênh
   trạng thái; thêm test "gia hạn trên web mà không mở app ⇒ không xoá"; JWS do app gửi lên: `iat` ≤ 24 giờ.
5. **App**: hiện nhắc gia hạn + báo hết kỳ theo mục 7.6 (Flutter dùng `ProRenewalNotice` của `tsudev_ui` khi có bản
   mới); đủ 6 test.
6. Đồng bộ bộ quy ước lên `v4.0.0` trong cùng PR với các thay đổi trên (thay cho v3.9.1 ở phiếu PRO1).

---

## 3.9.1 - 20/11/2026

Bản PATCH: đính chính hợp đồng JWS quyền lợi cho khớp máy chủ thật (tsudev#336, ADR-0002), không thêm yêu cầu mới.

- `docs/PRODUCT_POLICY.md` v1.1.1 mục 7.4: `iss` = issuer OIDC `https://tsudev.com/oidc` (không phải
  `https://tsudev.com`), JWKS `https://tsudev.com/oidc/jwks` (không có `/.well-known/jwks.json`), header `typ`
  `tsu-ent+jwt`, thân trả về `{"jws": ...}`; cách gửi client assertion của kênh RP (`Bearer`, `aud`, `exp` ≤ 300 s,
  `jti` một lần) và mã lỗi `403 insufficient_scope` / `404 unknown_subject`.

---

## 3.9.0 - 20/11/2026

Bản MINOR: quyết định chủ dự án 19/11/2026 (phiếu `20261119-PRO1`, phase PRO-A + phần SVG của PRO-C). Thêm yêu cầu
mới - mọi repo sync lên 3.9.0 trước khi làm phần Pro/đồng bộ.

- `docs/PRODUCT_POLICY.md` v1.1.0 mục 7 (mới) **Lưu cục bộ mặc định - đồng bộ/sao lưu đám mây là Pro**: nguyên tắc
  N1-N8 (cục bộ trước, miễn phí không gửi dữ liệu lên mạng, máy chủ kiểm quyền bằng JWS, chịu tải, 0 đồng); gói chung
  **TsuDEV Pro 49.000 ₫/tháng, 490.000 ₫/năm**, Ủng hộ 20/50/100/200 nghìn; Pro hết hạn ⇒ chặn đẩy, kéo/xuất 90 ngày,
  dữ liệu trên thiết bị không bao giờ bị xoá; thông báo "nhiều thiết bị chưa có Pro" (nội dung vi/en nguyên văn, chu kỳ
  30 ngày, 5 test bắt buộc) - ngoại lệ có chủ đích của mục 3.2; **hợp đồng chung** (mã sản phẩm Play `tsudev_pro`
  `thang`/`nam`, `ung_ho_*`, App Store, JWS quyền lợi ES256, `/api/me/entitlements`, `/api/rp/entitlements/*`,
  `402 pro_required`, TsuDEV Sync `tsudev-org/tsusync` + mật mã); hạn mức 100 MiB + 1 GiB; điều khoản thuê bao nguyên
  văn. Checklist thành mục 8, thêm 7 dòng.
- `docs/AUTH_AND_ACCOUNT.md` v3.1.0 mục 14.3 (mới): **mã cài đặt** ngẫu nhiên 128 bit, cấm IMEI/MAC/vân tay, header
  `X-Tsu-Installation`, máy chủ chỉ lưu HMAC; ca kiểm thử 15; checklist thêm dòng.
- `docs/FREE_TIER_STACK.md` v2.1.0 mục 3.1 (mới): đồng bộ/sao lưu đám mây ở lại trong hạn mức miễn phí (người dùng miễn
  phí không tốn dung lượng, delta theo `rev`, không poll dày, lùi thử lại, giới hạn ở máy chủ).
- `docs/STORE_SUBMISSION.md` mục 4.1: mã sản phẩm Play cố định + ghi chú ngoại lệ thông báo Pro.
- `assets/badges/` (mới): SVG gốc huy hiệu Pro + Ủng hộ (Sáng/Tối, vi/en) kèm bảng màu và số đo tương phản (thấp nhất
  6.12:1).

---

## 3.8.3 - 19/11/2026

Bản PATCH: ghi quyết định chủ dự án 19/11/2026.

- `docs/ECOSYSTEM_IDENTITY.md` v3.1.2 mục 4.2 + 4.2.1 (mới): ngoại lệ TsuFiles mở rộng - website **files.tsudev.com**
  cũng dùng **đen tuyền + tím logo cú** như kiểu "Cú đêm" của app (thay ghi chú "website vẫn theo bảng xanh" của
  v3.8.2); bảng token tím lấy mẫu từ logo, dùng lại bảng đã kiểm AA của v3.4.0.

---

## 3.8.2 - 19/11/2026

Bản PATCH: ghi quyết định chủ dự án 19/11/2026 và sửa một dòng mâu thuẫn, không thêm yêu cầu mới.

- `docs/ECOSYSTEM_IDENTITY.md` v3.1.1 mục 4.2: kiểu giao diện "Cú đêm" của app TsuFiles giữ **tím** (khớp logo con cú)
  là ngoại lệ **đã chốt** thứ hai, cạnh tím hoa sen của lotus.tsudev.com.
- Mục 2.2: `og:site_name` là `TsuDEV` (dòng cũ còn ghi `tsudev`, mâu thuẫn mục 3 và khuôn thẻ ngay trên).

---

## 3.8.1 - 19/11/2026

Bản PATCH: ghi các quyết định chủ dự án 19/11/2026, không thêm yêu cầu mới.

- `docs/PRODUCT_POLICY.md` v1.0.1 mục 3.3, 4.3: ủng hộ trong bản Google Play **chốt** dùng Google Play Billing; bản Play
  không có liên kết ủng hộ ra web.
- `docs/ECOSYSTEM_IDENTITY.md` mục 4.2: lotus.tsudev.com giữ tím hoa sen là ngoại lệ **đã chốt**; logo ảnh không vẽ lại.

---

## 3.8.0 - 19/11/2026

Bản MINOR theo yêu cầu chủ dự án 19/11/2026. Thêm hai tài liệu, đổi mặc định giao diện, tên thương hiệu và bảng màu
website. Không có cổng kiểm mới; repo con đồng bộ được ngay, việc sửa sản phẩm làm theo kế hoạch toàn hệ.

### Thêm

- `docs/PRODUCT_POLICY.md` v1.0.0: lần chạy đầu dùng **ngôn ngữ hệ thống** (dự phòng EN → VI) và **giao diện Hệ
  thống**; thứ tự nền tảng + **iOS phát triển ngay, thử trên iPhone thật qua cáp** (Apple ID miễn phí, CI macOS), nộp
  App Store/notarize đầu 2027; **không quảng cáo** - chỉ gói **Pro tháng/năm** và **Ủng hộ**, thanh toán đúng kênh
  từng nền tảng, quyền lợi gắn tài khoản TsuDEV xác minh phía máy chủ; **huy hiệu Pro / Ủng hộ** (chọn hiển thị một,
  hai hoặc ẩn; thiết kế, kích thước, chuyển động, truy cập); website sản phẩm **bắt buộc có hình ảnh + video**; mức
  kiến trúc/bảo mật tối thiểu; checklist.
- `docs/STORE_SUBMISSION.md` v1.0.0: agent đề xuất chủ dự án mở **phiên nộp duyệt riêng**, agent tự mở trình duyệt và
  điền từng trường (Google Play Console, Microsoft Partner Center, App Store Connect 2027, cổng báo nhầm antivirus,
  SignPath, Flathub); chủ dự án chỉ đăng nhập và bấm gửi; tệp hồ sơ `docs/store/<kenh>.md`; kiểm trước khi nộp.

### Đổi

- `docs/ECOSYSTEM_IDENTITY.md` v3.1.0: tên hiển thị **`TsuDEV`** (định danh máy đọc giữ chữ thường); mục 3.1 trang
  Danh sách ứng dụng của tsudev.com; bảng màu website **đen tuyền + xanh logo** thay tím (nhận tsudev-standards#55),
  icon nền tảng/icon thông tin màu xanh; bộ chọn giao diện mặc định `system`.
- `docs/DESIGN_SYSTEM.md` mục 1: mặc định **Hệ thống** (trước là Tối).
- `docs/DISTRIBUTION_TRUST.md` v1.1.0: iOS từ `SHOULD` thành `MUST` phát triển ngay; thử nghiệm kín Play; không
  quảng cáo; hồ sơ mục 5 đi qua phiên điền biểu mẫu; `CompanyName` = `TsuDEV`.
- `AGENTS.md`, `docs/00-INDEX.md`: trỏ tới hai tài liệu mới.

### Hướng dẫn cho repo con

1. `./scripts/sync-standards.sh` lên `v3.8.0`.
2. Đổi chữ hiển thị `tsudev` → `TsuDEV` (không đổi định danh máy đọc); mặc định giao diện + ngôn ngữ theo hệ thống.
3. Repo có SDK quảng cáo: gỡ ở bản kế tiếp. Repo app: lập kế hoạch Pro/Ủng hộ/huy hiệu theo `PRODUCT_POLICY.md`
   (máy chủ quyền lợi dùng chung ở tsudev.com - làm một lần, không mỗi app một bản).
4. Kế hoạch theo từng repo: `~/projects/logs/handover/20261119-01_ke-hoach-toan-he-v3.8.0.md`.

---

## 3.7.0 - 17/11/2026

Bản MINOR: thêm tài liệu mới và chuẩn hoá khuôn thẻ/tên tệp cho bản phát hành KẾ TIẾP; cổng kiểm mới chỉ ở mức LƯU Ý.
Repo con đồng bộ được ngay, không cần sửa code. Thẻ đã phát hành giữ nguyên (VERSIONING.md mục 2.4).

### Thêm

- `docs/DISTRIBUTION_TRUST.md` v1.0.0: cài không bị hệ điều hành / trình duyệt / antivirus chặn - ma trận kênh theo
  nền tảng (Microsoft Store MSIX, Developer ID + notarize, APT/RPM ký GPG, Google Play + xác minh nhà phát triển
  Android, App Store đầu 2027), chuỗi cung ứng (SHA256SUMS + Sigstore, chứng thực nguồn gốc, SBOM), phòng và gỡ báo
  nhầm antivirus (VirusTotal trong CI, không packer, PyInstaller `--onedir`), kiến trúc bảo mật app phát hành, bảng hồ
  sơ phải đăng ký, thứ tự A-B-C-D, checklist mỗi bản phát hành. Trạng thái nền tảng đo 17/11/2026.
- `scripts/check-standards.sh` mục 5b: LƯU Ý khi thẻ phát hành mới nhất của repo có `packaging/package.json` lệch khuôn
  `vYY.M.DDNN`.

### Đổi

- `docs/VERSIONING.md` v3.0.0 (phiếu toàn hệ `20261117-V1`): mục 2 chuẩn hoá thẻ git `vYY.M.DDNN` (không tiền tố,
  không hậu tố), bản thử `-beta.N`/`-rc.N`, tiêu đề Release `{Tên sản phẩm} {phiên bản}`, tên tệp
  `{tên-gói}_{phiên bản}_{os}-{arch}[-{loại}].{ext}`, Android `versionCode` `YYMDDNN`, iOS, Windows/MSIX 4 phần, gói
  Linux, bản fork (phiên bản gốc chỉ ở Release notes), quy tắc chuyển khuôn an toàn, thẻ deploy website
  `deploy-YYYY.MM.DD.N`.
- `docs/DESIGN_SYSTEM.md` mục 6, `docs/ONBOARDING.md` câu lệnh (g), `docs/PACKAGING.md`, `docs/00-INDEX.md`, `AGENTS.md`
  mục 1: theo khuôn mới và trỏ tới tài liệu mới.

### Hướng dẫn cho repo con

1. `./scripts/sync-standards.sh` lên `v3.7.0`.
2. Repo app: bản phát hành kế tiếp theo `VERSIONING.md` mục 2.2 - đọc mục 2.4 (updater đã cài) TRƯỚC khi đổi khuôn.
3. Làm `DISTRIBUTION_TRUST.md` mục 6 theo thứ tự A-B-C-D; kế hoạch theo từng repo ở
   `~/projects/logs/handover/20261117-P2_ke-hoach-phan-phoi-tin-cay-da-nen-tang.md`.

## 3.6.0 - 13/11/2026

Bản MINOR: quy tắc mới ở mức `MAY` (logo sản phẩm riêng khi chủ dự án duyệt) và cập nhật mô tả logo tsudev theo thực
tế. Repo con đồng bộ được ngay; repo đã có logo riêng gỡ dòng "lệch chuẩn logo" ở `AGENTS.md` sau khi đồng bộ.

### Đổi

- `docs/BRAND_ASSETS.md` mục 1-2: logo tsudev là `logo-tsudev.png` (cú + chữ, nền đen), dùng NGUYÊN logo ở mọi cỡ kể cả
  favicon (chủ dự án chốt 13/11/2026); bỏ bộ logo-full / logo-mark / wordmark / `-dark` đã gỡ khỏi tsudev.com.
- `docs/AUTH_AND_ACCOUNT.md`: sơ đồ trang đăng nhập dùng logo tsudev thay `logo-mark`.

### Thêm

- `docs/BRAND_ASSETS.md` mục 15: logo sản phẩm riêng - một ảnh gốc, script sinh có `--check` trong CI, đủ bộ tài sản
  mục 12, quy tắc xoá nền, giữ liên kết hệ sinh thái. Nhận đề xuất `logs/handover/20261112-01` (trafficmonitor, Lotus
  Share, trò chơi, cwico / SWICO / contact).

## 3.5.0 - 11/11/2026

Bản MINOR: thêm tài liệu mới, mọi quy tắc mới ở mức `SHOULD` / `MAY` cho repo con (bắt buộc `MUST` chỉ áp dụng khi
repo đã chọn công bố một kênh). Repo con đồng bộ được ngay, không cần sửa code.

### Thêm

- `docs/PACKAGING.md` v1.0.0: mọi app/tool tsudev cài được bằng một lệnh terminal - kênh được duyệt (winget, Scoop
  bucket `tsudev-org/scoop-bucket`, kho APT/RPM ký GPG tại `pkg.tsudev.com` trên Cloudflare R2, Homebrew tap
  `tsudev-org/homebrew-tap`, F-Droid riêng, lệnh cài một dòng), khuôn tên gói, nguồn khai báo duy nhất
  `packaging/package.json`, chữ ký SHA-256 + chứng thực Sigstore, CI cài thử thật trên ba hệ điều hành, khối
  "Cài bằng lệnh" trên website.
- `docs/00-INDEX.md`: thêm `PACKAGING.md` vào lộ trình "sắp phát hành" và danh mục.

---

## 3.4.0 - 10/11/2026

Bản MINOR theo quyết định chủ project ngày 10/11/2026: toàn hệ sinh thái chỉ còn **Sáng / Tối / Hệ thống**,
mặc định Tối, website dùng **đen tuyền + tím** kiểu Supabase. Không đổi giá trị token nào (quy tắc cứng của
`VERSIONING.md` mục 1: đổi giá trị token màu là MAJOR) - bảng màu mới nằm ở tài liệu và repo con ghi đè ở tầng
riêng. Phiếu: `logs/handover/20261110-05_yeu-cau-giao-dien-den-tim-kieu-supabase.md`.

### Thay đổi

- `docs/DESIGN_SYSTEM.md` mục 1: bỏ chế độ Ấm (`SHOULD NOT` hiển thị; `warm` đã lưu đọc thành `light`); ba lựa
  chọn Sáng / Tối / Hệ thống, mặc định Tối, "Hệ thống" đổi ngay theo hệ điều hành.
- `docs/ACCESSIBILITY.md`, `docs/ONBOARDING.md`, `docs/RICH_TEXT_EDITOR.md`: kiểm tương phản ở hai chế độ Sáng / Tối.
- `docs/AUTH_AND_ACCOUNT.md` mục 1 (**TS-15**): `tsudev-contact` là **hạng C** (app ngoại tuyến), không phải hạng A.

### Thêm

- `docs/ECOSYSTEM_IDENTITY.md` mục 4.1 **bộ chọn giao diện** (khóa `tsudev-theme`, áp trước khi vẽ, radiogroup ở
  hàng cuối chân trang cạnh `© tsudev`, CSP không `'unsafe-inline'`) và mục 4.2 **bảng màu + ngôn ngữ thiết kế của
  website** (đen tuyền + tím, nền liền mạch, nút/thẻ kiểu Supabase); checklist mục 9 thêm hai dòng.
- `tokens/design-tokens.json` `meta.deprecated`: khối `color.warm` ngừng dùng, gỡ ở v4.0.0 (schema thêm trường).

### Hướng dẫn nâng cấp

```bash
./scripts/sync-standards.sh --ref v3.4.0
./scripts/check-standards.sh
```

Không bắt buộc sửa mã. Repo có website/app đang hiện lựa chọn Ấm: làm theo phiếu `20261110-05` của repo đó.

### Dự kiến v4.0.0 (MAJOR)

Gỡ khối `color.warm`, nhận bảng mục 4.2 làm giá trị chuẩn `light`/`dark` của `tokens/design-tokens.json`, nâng
`SHOULD` của mục 1 và 4.1 lên `MUST`. Cần chủ project duyệt vì mọi repo con đổi màu theo.

## 3.3.0 - 10/11/2026

Bản MINOR: thêm một ngoại lệ có kiểm soát cho quy tắc gạch ngang. Repo không phải
fork không bị ảnh hưởng; repo fork tự chọn bật bằng một file khai báo.

### Thêm

- `AGENTS.md` mục 7.1, **ngoại lệ 3**: dòng kế thừa nguyên văn từ upstream ở repo
  fork. Khai báo ở `.standards-upstream` (`repo=`, `ref=`); miễn theo dòng, đối
  chiếu nội dung với commit upstream; `ref` phải là tổ tiên của HEAD và, với
  `STANDARDS_VERIFY_UPSTREAM=1`, phải tải được từ chính repo upstream đã khai.
- `templates/standards-upstream.example`.
- `scripts/test-upstream-exempt.sh`: 7 ca (miễn đúng dòng kế thừa; trượt khi fork
  thêm dòng, sửa dòng kế thừa, thêm file mới, `ref` không phải tổ tiên, `ref` viết
  tắt, không khai báo). Chạy trong CI của repo trung tâm.

### Sửa

- Mục 4 của `check-standards.sh`: danh sách file có en-dash in dính vào dòng LƯU Ý
  kế tiếp (thiếu xuống dòng).

### Kiểm chứng ở repo con thật

- `tsudev-lotus` (fork LocalSend, `ref=8476c091`): 71 dòng kế thừa được miễn, đã
  xác minh trực tuyến với `github.com/localsend/localsend`; cổng kiểm bắt được
  một em-dash do chính fork thêm (`website/scripts/check-dist.mjs`, mẫu chép từ
  `tsudev-files`). Ca khai `ref` là commit của fork + xác minh trực tuyến: trượt.

### Hướng dẫn nâng cấp

```bash
./scripts/sync-standards.sh --ref v3.3.0
# Chỉ repo fork: khai upstream đã gộp gần nhất
printf 'repo=<owner>/<tên>\nref=%s\n' "$(git rev-parse <nhánh-upstream-đã-gộp>)" > .standards-upstream
STANDARDS_VERIFY_UPSTREAM=1 ./scripts/check-standards.sh
git add .standards .standards-version .standards-upstream scripts/sync-standards.sh scripts/check-standards.sh
```

## 3.2.0 - 09/11/2026

Repo chuyển sang Organization `tsudev-org`. Bản MINOR: không token nào đổi giá
trị, không repo con nào phải sửa mã.

### Thêm

- `AGENTS.md` mục 4: quy tắc cứng **tên repo GitHub cũ là bất khả xâm phạm** -
  không tạo/fork/đổi tên repo thành tên cũ dưới `tsudev-tsudev`, và bật lại secret
  scanning, push protection, CodeQL sau khi chuyển repo vào org. Repo con không
  phải sửa mã; quy tắc chỉ ràng buộc thao tác trên GitHub.

### Đổi

- Mọi URL `tsudev-tsudev/tsudev-standards` → `tsudev-org/tsudev-standards`, kể cả
  `REPO` mặc định của `scripts/sync-standards.sh`. URL cũ vẫn chạy nhờ chuyển hướng
  của GitHub, nên repo con chưa đồng bộ không gãy.

### Hướng dẫn nâng cấp

Từ gốc repo con (script `3.1.1` trở lên đã đi theo gói):

```bash
./scripts/sync-standards.sh --repo tsudev-org/tsudev-standards --ref v3.2.0
./scripts/check-standards.sh
git add .standards .standards-version scripts/sync-standards.sh scripts/check-standards.sh
```

Kiểm `.standards-version` ghi `repo=tsudev-org/tsudev-standards` và
`version=3.2.0`.

---

## 3.1.1 - 25/08/2026

Sửa hướng dẫn nâng cấp của `3.1.0`. Không đổi hành vi script, không đổi nội dung
quy ước.

### Sửa

- **Hướng dẫn nâng cấp lên `3.1.0` thiếu bước bắt buộc đầu tiên.** Bản `3.1.0`
  đưa cổng kiểm vào gói đồng bộ, nhưng thay đổi đó nằm **bên trong**
  `scripts/sync-standards.sh`. Repo con nâng cấp bằng chính script cũ của nó, nên
  script cũ chép gói cũ: `.standards-version` lên `3.1.0` mà `.standards/scripts/`
  vẫn trống và `scripts/check-standards.sh` vẫn nguyên bản cũ. Bản vá tự nó
  **không triển khai được chính nó**.

  Đã kiểm chứng bằng ca thật trên cả 4 repo con trước khi viết mục này, không
  phải suy đoán.

  Đây là chi phí một lần của riêng lần chuyển từ `3.0.x` lên `3.1.x`. Từ `3.1.1`
  trở đi repo con đã cầm script mới, `.standards/scripts/sync-standards.sh` đi
  theo gói, và `--check` canh giúp phần lệch.

### Hướng dẫn nâng cấp

**Bước 1 - bắt buộc, làm trước.** Lấy script đồng bộ của bản mới:

```bash
curl -fsSL https://raw.githubusercontent.com/tsudev-tsudev/tsudev-standards/v3.1.1/scripts/sync-standards.sh \
  -o scripts/sync-standards.sh
chmod +x scripts/sync-standards.sh
```

**Bước 2 - đồng bộ và kiểm.**

```bash
./scripts/sync-standards.sh --ref v3.1.1
./scripts/check-standards.sh
./scripts/sync-standards.sh --check
```

**Bước 3 - commit, nhớ đủ bốn đường dẫn.**

```bash
git add .standards .standards-version scripts/check-standards.sh scripts/sync-standards.sh
```

Cách tự kiểm đã làm đúng: `ls .standards/scripts/` phải ra **hai** file. Ra rỗng
nghĩa là bước 1 bị bỏ qua, và lúc đó `.standards-version` vẫn ghi `3.1.1` nên
nhìn số bản là không phát hiện được.

**Điều KHÔNG đổi:** không tài liệu quy ước nào đổi nội dung, không token nào đổi
giá trị, không script nào đổi hành vi so với `3.1.0`.

---

## 3.1.0 - 25/08/2026

Bản này vá **hai lỗ hổng của chính cơ chế đồng bộ**, cả hai đều lộ ra khi phát
hành `v3.0.0` xuống 4 repo con. Không tài liệu quy ước nào đổi nội dung, không
token nào đổi giá trị, không repo con nào phải sửa mã.

### Sửa

- **`scripts/sync-standards.sh` nay mang theo cổng kiểm** (`TS-16`).

  Trước bản này, gói đồng bộ gồm `AGENTS.md`, `VERSION`, `SECURITY.md`, `docs/`,
  `tokens/`, `templates/` - **không có `scripts/`**. Repo con lấy
  `check-standards.sh` bằng một lệnh `curl` đúng một lần lúc cài đặt, rồi không
  bao giờ lấy lại.

  Hậu quả đo được: `v3.0.0` mở cổng kiểm gạch ngang từ 10 lên 47 đuôi file, và
  cải tiến đó **không đến được repo con nào**. Cả bốn repo đồng bộ xong vẫn chạy
  script cũ, cổng kiểm xanh, và không ai biết là nó đang bỏ sót `.py`, `.cs`,
  `.html`, `.sql`, `.toml`. Cổng kiểm mà tự cũ đi trong im lặng thì tệ hơn không
  có cổng kiểm, vì nó phát ra tín hiệu "đạt chuẩn" sai.

  Nay `scripts/check-standards.sh` và `scripts/sync-standards.sh` nằm trong gói,
  được `MANIFEST.sha256` băm từng byte như mọi file quy ước khác. Sau khi chép
  vào `.standards/scripts/`, lần đồng bộ **ghi đè luôn `scripts/check-standards.sh`**
  ở gốc repo con - đó là bản thật sự được chạy. `make-manifest.sh` và
  `build-tokens.mjs` **không** đi theo: chúng là việc của repo trung tâm, gửi
  xuống chỉ tạo cơ hội chạy nhầm.

  Ghi đè bằng `mv` chứ không `cp`: `cp` cắt cụt rồi ghi lại đúng inode đang mở,
  mà bash đọc script theo từng đoạn, nên ghi đè inode của một script đang chạy là
  hỏng phiên chạy. `mv` thay inode, tiến trình đang chạy giữ nguyên inode cũ.

  `sync-standards.sh` **không tự ghi đè chính nó**, chỉ cảnh báo kèm lệnh chép
  tay. Đổi công cụ bootstrap ngay giữa lúc nó đang chạy là rủi ro không đáng đổi
  lấy chút tiện lợi.

- **`--check` đối chiếu với nhãn đang ghim, không phải với `main`** (`TS-17`).

  `docs/SYNC.md` mục 5.1 chạy `./scripts/sync-standards.sh --check` không kèm
  `--ref`, mà mặc định của script là `main`. Nghĩa là cổng chặn merge của repo
  con đang trả lời câu **"tôi đã nâng cấp chưa"** thay vì câu **"bản sao của tôi
  có bị sửa trộm không"**.

  Hậu quả đo được: 09:2x ngày 25/08/2026, `v3.0.0` vào `main` ở trung tâm. Ngay
  sau đó CI trên `main` của `tsudev` đỏ (run `32834615830`, 13 dòng `LỆCH`) dù
  repo đó đang ghim `v2.8.0` hoàn toàn hợp lệ và không làm gì sai. Nó chỉ xanh
  lại lúc 09:58 sau khi đồng bộ. Việc ghim theo nhãn ở `SYNC.md` mục 7 vì vậy
  **chưa bao giờ có tác dụng thật**: repo con buộc phải chạy theo `main` ngay
  lập tức, nếu không CI đỏ.

  Nay `--check` không kèm `--ref` sẽ đọc dòng `ref=` trong `.standards-version`
  và đối chiếu với đúng nhãn đó. Muốn hỏi "đã có bản mới hơn chưa" thì truyền tay
  `--ref main`, và đó là việc của PR nâng cấp định kỳ ở mục 5.2, không phải của
  cổng chặn merge.

- **`--check` nay bắt thêm hai ca** mà trước đây lọt hoàn toàn:
  `scripts/check-standards.sh` ở gốc repo khác bản trung tâm (đây chính là lỗ
  hổng `TS-16`), và file trong `.standards/scripts/` bị sửa. Repo đang ghim bản
  cũ hơn `v3.1.0` thì hai ca này ra **lưu ý**, không ra lỗi - gói đồng bộ của bản
  đó vốn không có `scripts/`, bắt lỗi là đỏ oan.

### Thay đổi

- **`docs/SYNC.md`** lên `v3.1.0`: mục 1 liệt kê rõ gói đồng bộ gồm những gì và
  vì sao cổng kiểm thuộc về nó; mục 3 bỏ bước `curl` cổng kiểm (nay thừa); mục 4
  nhắc `git add scripts/check-standards.sh`; mục 5 thêm bảng tách hai câu hỏi
  "bị sửa trộm chưa" và "đã nâng cấp chưa"; mục 8 thêm ba dòng xử lý sự cố mới.
- **`AGENTS.md` mục 8**: ghi rõ cổng kiểm thuộc bộ quy ước, và `--check` đối
  chiếu theo nhãn đang ghim.

### Hướng dẫn nâng cấp

> **THIẾU MỘT BƯỚC - đọc mục `3.1.1` thay cho mục này.** Hướng dẫn dưới đây không
> chạy được: repo con thực hiện nó bằng `scripts/sync-standards.sh` **cũ**, mà
> toàn bộ bản vá của `3.1.0` lại nằm trong chính script đó. Chạy đúng như viết ở
> đây thì `.standards-version` lên `3.1.0` trong khi gói vẫn là gói cũ, không có
> `.standards/scripts/`, và cổng kiểm ở gốc không được cập nhật. Phát hiện lúc
> đồng bộ thật, đã sửa ở `3.1.1`.

Bản MINOR, **không repo con nào phải sửa mã**. Ba bước:

```bash
./scripts/sync-standards.sh --ref v3.1.0
./scripts/check-standards.sh
git add .standards .standards-version scripts/check-standards.sh
```

**Nhớ `git add` cả `scripts/check-standards.sh`** - lần đồng bộ này ghi đè nó, và
đó là điểm khác duy nhất so với mọi lần nâng cấp trước. Đồng bộ có sửa file đó
thì in ra dòng `Đã cập nhật scripts/check-standards.sh theo bản trung tâm.`

Nếu thấy `CẢNH BÁO: scripts/sync-standards.sh khác bản trung tâm`, chép tay đúng
một lần theo lệnh mà script in ra. Từ lần sau `--check` sẽ canh giúp.

**Điều KHÔNG đổi ở bản này:** không tài liệu quy ước nào đổi nội dung, không token
màu nào đổi giá trị, không tài sản thương hiệu nào đổi. Ba việc `QU-STD-AUTH`,
`QU-STD-TABLE`, `QU-STD-BRAND` mở ở `v3.0.0` vẫn nguyên như cũ.

---

## 3.0.0 - 24/08/2026

**Thay đổi phá vỡ.** Bộ quy ước lần đầu bắt buộc về **chức năng sản phẩm**, không
chỉ về cách viết mã. Bốn nghĩa vụ mới, mỗi nghĩa vụ đều cần repo con sửa mã. Đọc
mục "Hướng dẫn nâng cấp" ở cuối trước khi chạy `sync-standards.sh`.

### Thêm mới

- **`docs/AUTH_AND_ACCOUNT.md`** - kiến trúc xác thực và tài khoản dùng chung.

  Vấn đề nó giải: bốn sản phẩm đang có bốn cách hiểu khác nhau về "đăng nhập", và
  chưa sản phẩm nào có khái niệm tài khoản đã xác minh hay chưa. Người dùng đăng
  nhập bằng Google ở website rồi mở app ra vẫn là người lạ.

  `tsudev.com` được định nghĩa là **Nhà cung cấp danh tính duy nhất** (OIDC).
  Google và GitHub nối vào IdP chứ không nối thẳng vào từng project - nhờ vậy một
  người là một tài khoản trên toàn hệ sinh thái. Ba lối vào bắt buộc và đúng thứ
  tự: Google, GitHub, tài khoản tsudev.

  **Cơ chế Xác minh tài khoản** (mục 8) là phần lớn nhất: định nghĩa trạng thái,
  hạn ân hạn **7 ngày** kể từ lúc tạo tài khoản, ba mức hạn chế, huy hiệu hiển thị
  có đủ màu-chữ-icon, và nhắc vào ngày 3, ngày 6, ngày hết hạn. Đăng nhập bằng
  Google/GitHub với `email_verified: true` được tính là Đã xác minh ngay, không
  bắt làm lại.

  Ghi lại vì nó là quyết định bảo mật chứ không phải thao tác: **chỉ gộp danh tính
  theo email khi nhà cung cấp khẳng định email đã xác minh** (mục 5). Bỏ điều kiện
  này là mở lỗ hổng chiếm tài khoản trước khi nạn nhân kịp đăng ký. Và mọi hạn chế
  `MUST` thi hành ở tầng máy chủ - ẩn nút không phải là phân quyền.

  Sản phẩm ngoại tuyến như `tsudev-swico` xếp **hạng C**: đăng nhập là tùy chọn,
  `MUST NOT` chặn chức năng lõi sau màn hình đăng nhập, `MUST NOT` gọi mạng ngầm
  khi chưa đăng nhập. Một phần mềm rà quét máy tính mà tự gọi ra ngoài là thứ đầu
  tiên bị công cụ bảo mật gắn cờ, và đúng ra phải như vậy.

- **`docs/DATA_TABLE.md`** - chuẩn vùng bản ghi và bộ chọn số bản ghi.

  Bộ mốc chuẩn `10 | 20 | 50 | 100 | 200`, mặc định `10`, đặt ở **góc dưới bên
  trái** vùng chứa bản ghi, kể cả khi vùng đó nằm trong modal và kể cả ở màn hình
  hẹp. Không có lựa chọn "Tất cả": đó là một truy vấn không có trần.

  Hai quy tắc hành vi đáng chú ý: đổi mốc `MUST` **giữ nguyên bản ghi đầu đang
  nhìn thấy** thay vì nhảy về trang 1, và `MUST` tải lại từ máy chủ thay vì tải
  sẵn 200 dòng rồi cắt ở máy khách - nếu cắt ở máy khách thì mốc `10` không tiết
  kiệm được gì.

- **`docs/ECOSYSTEM_IDENTITY.md`** - `tsudev.com`, ảnh đại diện, trang hồ sơ.

  Ba vai của `tsudev.com` (cổng sản phẩm, nhà cung cấp danh tính, nguồn nhận diện)
  và bản mô tả chuẩn dùng nguyên văn ở mọi repo. Siêu dữ liệu bắt buộc cho web,
  desktop và kho mã, trong đó `og:site_name` `MUST` là chuỗi `tsudev` ở mọi sản
  phẩm kể cả sản phẩm có tên miền riêng.

  Chuẩn ảnh đại diện dùng chung (mục 6): thứ tự nguồn, ràng buộc tải lên, và ba
  thao tác cùng tên gọi ở mọi sản phẩm - **Tải ảnh lên / Đổi ảnh / Xóa ảnh**.
  Phần bảo mật ảnh không thương lượng: kiểm kiểu thật bằng chữ ký byte đầu, giải
  mã và mã hóa lại phía máy chủ, **xóa EXIF** (ảnh điện thoại mang theo tọa độ GPS
  nhà người dùng), từ chối `SVG` và ảnh động. Không có ảnh thì sinh **ảnh chữ cái**
  tại chỗ, không phải hình bóng người xám và không gọi Gravatar.

  Trang hồ sơ có bố cục cố định: menu dọc `220px`, nội dung tối đa `720px`, mỗi
  nhóm một thẻ và **một nút Lưu riêng** - không có nút lưu chung cho cả trang, vì
  người dùng không biết mình vừa lưu những gì.

- **`docs/BRAND_ASSETS.md` mục 12** - bộ tài sản nhận diện **bắt buộc** theo loại
  sản phẩm, kèm cổng kiểm CI mẫu. Trước bản này tài liệu mô tả *có những tài sản
  nào* nhưng không nói *project nào phải có cái gì*; khoảng trống đó là lý do một
  sản phẩm phát hành ra mà tab trình duyệt trống trơn.

- **`docs/BRAND_ASSETS.md` mục 13** - phân biệt **kho lưu** và **kho dùng**. Ghi
  lại một ca đã xảy ra thật: file `logo-tsudev.png` đặt ở thư mục làm việc, tên
  nghe như bản chính thức, hóa ra là bản sao đúng từng byte của
  `assets/brand/variants/tsudev-badge-cyan.png` - biến thể `MUST NOT` dùng cho sản
  phẩm. Tên file không phải bằng chứng, chuỗi băm mới là bằng chứng.

### Thay đổi

- **`AGENTS.md` mục 7.1** - quy ước gạch ngang được tách thành mục riêng và siết
  lên mức bắt buộc rõ ràng. Phạm vi mở rộng sang tên nhánh, tiêu đề PR, nội dung
  issue và **cả câu trả lời của agent trong hội thoại**. Bỏ cách hiểu "comment
  dùng em-dash cũng được": agent đọc `-` không kém gì đọc em-dash, nên lý do đó
  không đứng vững. Vẫn đúng hai ngoại lệ cũ: file migration bất biến, và dòng
  trích dẫn chính ký tự đó kèm mã điểm.

- **`scripts/check-standards.sh` mục 4** - cổng kiểm gạch ngang mở từ **10 đuôi
  file lên 47**. Bản cũ chỉ quét `.md .json .css .ts .tsx .js .mjs .sh .yml .yaml`,
  nghĩa là em-dash đi tự do vào `.py`, `.cs`, `.html`, `.sql`, `.toml` - đúng
  những nơi `tsudev-swico` và `tsudev-cwico` sống. Thêm cảnh báo cho en-dash
  (U+2013) ở mức `SHOULD NOT`, in kèm số dòng vi phạm để sửa thẳng. Sửa tham
  chiếu sai "AGENTS.md mục 6" thành "mục 7.1".

- **`docs/SEARCH_AND_FILTER.md` mục 7** - trần cứng `page_size` **nâng từ 100 lên
  200** để khớp mốc lớn nhất của giao diện. Đây là nới lỏng, nên nó đi kèm hai
  ràng buộc bù bắt buộc: giới hạn tần suất chặt hơn cho `page_size` từ 100 trở
  lên, và bắt buộc phân trang con trỏ khi tập dữ liệu vượt 100.000 bản ghi. Cần
  nhiều hơn 200 bản ghi thì đi đường xuất tệp chạy nền, `MUST NOT` nới trần API.
  Ví dụ `page_size` trong tài liệu đổi từ `20` sang `10` cho khớp mặc định mới.

- **`docs/DESIGN_SYSTEM.md` mục 5** - thêm mục "Vùng bản ghi" vào nhóm Data
  Display, trỏ sang `DATA_TABLE.md`. Đồng thời thay hai en-dash còn sót ở mục 3
  và 4 bằng gạch ngang ngắn.

- **`docs/SECURITY_BASELINE.md` mục 6** - thêm dẫn nhập tách vai: tài liệu này giữ
  **ngưỡng kỹ thuật**, `AUTH_AND_ACCOUNT.md` giữ **kiến trúc**. Làm chức năng
  đăng nhập thì đọc cả hai.

- **`docs/PROJECT_STRUCTURE.md` mục 3.3** - thêm 5 vị trí bắt buộc: `assets/brand/`,
  `public/` (sản phẩm sinh ra, `MUST NOT` sửa tay), thư mục luồng xác thực, thư
  mục trang tài khoản, và component bảng dùng chung.

- **`docs/BRAND_ASSETS.md` mục 10** - bảng nợ đã biết nay trống. Cả hai món nợ
  (nguồn sinh icon dưới chuẩn, bản logo cho nền tối) đã trả xong ở `v2.7.0` và
  `v2.8.0`.

- `AGENTS.md`, `docs/00-INDEX.md`, `templates/AGENTS.downstream.md` - đăng ký ba
  tài liệu mới vào bản đồ quy ước và thêm ba lối đọc theo vai trò.

### Hướng dẫn nâng cấp

Repo con `MUST` làm theo thứ tự này. Bỏ qua bước nào thì cổng kiểm sẽ đỏ ở bước
sau, hoặc tệ hơn, không đỏ mà sản phẩm sai.

**Bước 1 - trước khi đồng bộ, dọn gạch ngang.** Cổng kiểm mới quét rộng gấp gần
năm lần, nên repo đang xanh vẫn có thể đỏ ngay sau khi đồng bộ.

```bash
# Xem pham vi anh huong truoc
git grep -lP '\x{2014}' -- . | grep -v '^migrations/'
```

Sửa từng file. `migrations/` giữ nguyên, không đụng. Dòng nào phải trích chính ký
tự đó thì ghi kèm mã điểm `U+2014` trên cùng dòng.

**Bước 2 - đồng bộ và chạy cổng kiểm.**

```bash
./scripts/sync-standards.sh
./scripts/check-standards.sh
```

**Bước 3 - mở việc trong `logs/STATE.md` của repo mình.** Ba nghĩa vụ dưới đây là
thay đổi mã nguồn, `MUST NOT` làm vội trong cùng PR đồng bộ. Liệt kê trước, sửa
sau, đúng theo `docs/ONBOARDING.md` mục 2.4.

| Việc | Áp cho | Đọc |
| --- | --- | --- |
| `QU-STD-AUTH` Rà luồng đăng nhập theo chuẩn mới, cài cơ chế Xác minh tài khoản | Hạng A và B | `AUTH_AND_ACCOUNT.md` mục 17 |
| `QU-STD-TABLE` Thêm bộ chọn số bản ghi vào mọi bảng và mọi modal có bản ghi | Mọi repo có giao diện | `DATA_TABLE.md` mục 12 |
| `QU-STD-BRAND` Bổ sung tài sản nhận diện còn thiếu và siêu dữ liệu `tsudev.com` | Mọi repo | `BRAND_ASSETS.md` mục 14 và `ECOSYSTEM_IDENTITY.md` mục 9 |

**Bước 4 - máy chủ trước, giao diện sau.** Nâng trần `page_size` lên 200 kèm giới
hạn tần suất **trước khi** mở mốc 200 trên giao diện. Mở giao diện trước là tự
tạo một đường cạn tài nguyên trong khoảng thời gian ở giữa.

**Điều KHÔNG đổi ở bản này:** không token màu nào đổi giá trị, không tài sản
thương hiệu nào đổi, `logo-tsudev.png` cyan **vẫn là biến thể không dùng cho sản
phẩm**. Giao diện đang chạy không phải vẽ lại.

---

## 2.8.0 - 24/08/2026

Bổ sung thuần. Trả xong món nợ ghi ở `v2.7.0` mục 10.

### Thêm mới

- `docs/BRAND_ASSETS.md` mục 2 và 4 - **bản cho nền tối**. Hai file
  `brand/logo-full-dark.png` và `brand/logo-wordmark-dark.png` nay tồn tại thật ở
  repo `tsudev` (PR #66), sinh ra bởi chính dây chuyền `packages/brand/build-assets.js`.

  Vấn đề chúng giải: chữ navy `#11355A` của logo chỉ đạt **1.38:1** trên nền Tối
  `#0F1B2D` - dưới mọi ngưỡng WCAG. Giao diện web lách được vì dựng chữ bằng text
  ăn theo token, nhưng **ảnh in, ảnh chia sẻ và slide nền tối thì không lách được**.

  Cách làm, ghi lại vì nó là quyết định chứ không phải thao tác: đổi mực navy sang
  trắng (**17.28:1**) và **giữ nguyên chữ cam** `#FE7B2E`, vốn đã đạt **6.66:1**
  trên cùng nền đó. Bản dark vì vậy vẫn là nhận diện tsudev chứ không phải một bảng
  màu khác. Hình con cú không bị đụng tới - nó đủ tương phản trên cả hai nền.

  Quy tắc mới: trên nền tối `MUST NOT` dùng bản thường; nơi dựng được chữ bằng text
  thì vẫn `SHOULD` dùng `logo-mark.png` kèm chữ text, vì cách đó tự đúng ở cả ba
  chế độ nền mà không phải chọn file.

  Giới hạn đã ghi thẳng vào tài liệu: quầng sáng của con cú được vẽ để tan vào nền
  trắng, nên ở cỡ rất lớn trên nền tối phần đáy thân cú vẫn hơi lộ vệt sáng. Dưới
  300px không nhận ra. Sửa hết hẳn là việc của khâu thiết kế.

---

## 2.7.0 - 24/08/2026

**Sửa lỗi quan trọng về nội dung.** `v2.4.0` và `v2.6.0` mô tả sai bộ nhận diện
của hệ sinh thái. Bản này sửa lại theo bằng chứng đo được. Không repo nào kịp làm
theo phần sai, nên không có bước di trú nào.

### Chuyện đã xảy ra

`v2.4.0` dựng chuẩn thương hiệu từ mã nguồn của `tsudev-cwico`. `v2.6.0` phát hiện
file `logo-tsudev.png` trên máy cá nhân khác hẳn con cú của `cwico`, và kết luận
**sai** rằng file đó là bản gốc chính thức còn `cwico` mới là bên lệch chuẩn.

Sự thật, kiểm chứng bằng đo đạc:

- Con cú của `tsudev-cwico` và `logo-mark.png` đang chạy trên tsudev.com là **cùng
  một tác phẩm**: IoU hình dạng **0.957**, màu trung bình `[83,130,159]` so với
  `[84,131,161]`.
- Repo `tsudev` đã có sẵn dây chuyền thương hiệu hoàn chỉnh từ **02/08/2026**:
  `packages/brand/source/logo.jpeg` `2048x2048`, `build-assets.js` sinh
  `logo-full` / `logo-mark` / `logo-wordmark` / favicon / avatar.
- `logo-tsudev.png` tạo ngày **23/08/2026** và **chưa từng được dùng ở repo nào**.

Nói cho gọn: `tsudev-cwico` chưa bao giờ lệch chuẩn. Nó dùng đúng dấu hiệu chính
thức. Huy hiệu xanh cyan mới là file lạc, và `v2.6.0` đã phong nhầm nó làm bản gốc.

### Sửa lỗi

- `docs/BRAND_ASSETS.md` viết lại theo bộ nhận diện thật:
  - **Mục 1** trỏ bản gốc về `tsudev/packages/brand/source/logo.jpeg`, kèm SHA-256
    và cách chạy lại dây chuyền. Repo quy ước **không giữ bản sao** - hai bản gốc
    song song là hai bản gốc sẽ trôi khỏi nhau.
  - **Mục 2** - dấu hiệu thu gọn (`logo-mark.png`) **đã tồn tại**, là dấu hiệu mặc
    định trên giao diện và bắt buộc cho mọi icon. Logo đầy đủ có tagline nên chỉ
    dùng từ **160px** trở lên. Việc `TS-5` (tạo dấu hiệu thu gọn) vì vậy **không
    còn cần làm**.
  - **Mục 4** - chữ navy `#11355A` chỉ đạt **1.38:1** trên nền Tối, nên `MUST NOT`
    dùng `logo-full.png` và `logo-wordmark.png` trên nền tối.
  - **Mục 5** - bảng màu đo lại từ bản gốc thật (navy `#11355A`, cam `#FE7B2E`).
    Chữ dựng bằng text `MUST` lấy màu từ token `text-primary` và `text-link` - hai
    token này đã qua cổng canh nên luôn đạt chuẩn, không phải đo lại. Cam trong ảnh
    chỉ đạt **2.35:1** trên nền sáng, `MUST NOT` dùng cho chữ.
  - **Mục 7** ghi cả hai dây chuyền đang chạy thật: `build-assets.js` cho web,
    `gen_icons.py` cho desktop.
  - **Mục 11** mới - `assets/brand/variants/tsudev-badge-cyan.png`, có nhãn rõ là
    **không dùng cho sản phẩm**. Giữ lại để không mất, không phải để dùng.
- `assets/brand/tsudev-logo.png` chuyển thành
  `assets/brand/variants/tsudev-badge-cyan.png`. Vẫn nằm ngoài bộ đồng bộ.
- `docs/00-INDEX.md` cập nhật theo.

### Bài học ghi lại

`v2.4.0` viết chuẩn thương hiệu **mà chưa từng mở file ảnh ra xem**, chỉ đọc mã
nguồn và chú thích rồi suy ra. `v2.6.0` mở ảnh ra xem nhưng **chỉ xem một ảnh**,
không đi tìm xem hệ sinh thái đã có bộ nhận diện nào chưa. Quy tắc rút ra: tài sản
hình ảnh `MUST` mở ra xem và đo, và `MUST` tìm hết các nơi đang dùng nó trước khi
kết luận cái nào là chuẩn.

---

## 2.6.0 - 24/08/2026

Bổ sung thuần, kèm một chỗ **sửa lại nội dung sai của chính `v2.4.0`**. Đồng bộ
được ngay, không cần sửa mã.

### Thêm mới

- `assets/brand/tsudev-logo.png` - **bản gốc chính thức của dấu hiệu**, `1024x1024`,
  nền trong suốt. Trước bản này, bản gốc chỉ tồn tại trên **một máy cá nhân**, ngoài
  mọi repo. Mã nguồn mất thì viết lại được; bản gốc thiết kế thì không.

  File nằm **ngoài bộ đồng bộ**: `make-manifest.sh` chỉ băm `AGENTS.md`, `VERSION`,
  `SECURITY.md`, `docs`, `tokens`, `templates`, `scripts`, và `sync-standards.sh`
  cũng chỉ chép đúng bộ đó. Repo con **không** tải thêm 1.7MB nào khi đồng bộ; repo
  nào cần thì lấy riêng một lần và đối chiếu SHA-256 ghi trong tài liệu.

  Tên file cũ `logo-tsudev.png` sai quy ước đặt tên của chính `BRAND_ASSETS.md`
  mục 3, đã đổi thành `tsudev-logo.png` khi đưa vào.

### Sửa lỗi

- `docs/BRAND_ASSETS.md` - **`v2.4.0` mô tả sai bộ nhận diện**. Bản đó dựng chuẩn
  từ `tsudev-cwico` và giả định file `1024x1024` nằm rời trên máy cá nhân là bản độ
  phân giải cao của cùng một logo. **Không phải.** Kiểm chứng bằng số liệu cho thấy
  đó là hai thiết kế khác hẳn nhau:

  | | Huy hiệu chính thức | Con cú ở `tsudev-cwico` |
  | --- | --- | --- |
  | Kích thước | `1024x1024` | `222x280` |
  | Bố cục | Cú trên vòng mạch, **có chữ "tsudev" nướng sẵn** | Chỉ hình cú, không chữ |
  | Mắt | Xanh cyan `#49EBFF` | Cam hổ phách |
  | Màu `dev` | Xanh `#14AAFA` | Cam `#d2540e` |

  Hệ quả đã sửa trong tài liệu:

  1. **Tách hai dấu hiệu** (mục 2): huy hiệu đầy đủ dùng từ **96px** trở lên, dấu
     hiệu thu gọn cho mọi cỡ nhỏ hơn và mọi icon. Chữ chiếm khoảng 1/8 chiều cao
     ảnh, nên ở favicon 32px chữ còn 4px - một vệt xám. `MUST NOT` thu nhỏ huy hiệu
     đầy đủ xuống cỡ icon, và `MUST NOT` tự cắt hình cú ra khỏi huy hiệu vì chữ đè
     lên vòng mạch.
  2. **Bảng màu đo lại từ ảnh thật** (mục 5), thay cho bảng cũ lấy từ `cwico`.
  3. **Cặp màu cho wordmark dựng bằng chữ có kiểm chứng tương phản**: `#14AAFA` chỉ
     đạt **2.32:1** trên nền sáng, trượt cả ngưỡng chữ lớn, nên nền sáng dùng
     `#0B6FA8` (**4.92**) và nền tối dùng `#14AAFA` (**6.72**). Cả hai vượt 4.5:1.
  4. **Mục nợ viết lại** (mục 10): bản nhận diện chính thức **chưa có dấu hiệu thu
     gọn**, và `tsudev-cwico` đang chạy một bộ nhận diện riêng cả về hình lẫn dải
     màu. Ba việc liên quan nhau, `MUST` giải quyết cùng một lượt.
- `docs/00-INDEX.md`: thêm `assets/brand/tsudev-logo.png` vào bảng "Ngoài thư mục docs".

---

## 2.5.0 - 24/08/2026

Bổ sung thuần và một chỗ sửa tài liệu đang lệch cấu hình thật. Đồng bộ được ngay,
không cần sửa mã.

### Sửa lỗi

- `docs/GIT_WORKFLOW.md` **mục 2 và mục 4.4 - số người duyệt PR**. Checklist bảo
  vệ nhánh ghi "tối thiểu 1 người duyệt" mà không phân biệt quy mô đội. GitHub
  **không cho tự duyệt PR của chính mình**, nên repo một người đặt `1` là **tự
  khóa hoàn toàn**: PR không bao giờ đủ điều kiện merge, và cách duy nhất đi tiếp
  là tắt bảo vệ nhánh - tức là mất luôn cả phần chặn thật.

  Chính repo này đang phải đặt `required_approving_review_count = 0` để không bế
  tắc, tức là tài liệu và cấu hình thật đã lệch nhau từ `v2.0.0`.

  Nay mục 4.4 có bảng rõ ràng: từ 2 người trở lên thì **1** duyệt, một người thì
  **0** duyệt. Kèm điều kiện: đặt `0` `MUST NOT` hiểu là bỏ rà soát - vẫn bắt buộc
  mở PR, cổng kiểm xanh, giải quyết hết thảo luận, và **áp cả với admin**. Và khi
  repo có người thứ hai ghi được thì `MUST` nâng lại thành `1` ngay trong ngày cấp
  quyền.

  Ghi chú trung thực: hàng đợi mô tả lỗi này nằm ở mục 4.4, nhưng câu sai thật sự
  nằm ở checklist mục 2. Đã sửa cả hai chỗ cho khớp nhau.

### Thêm mới

- `templates/gitignore/go.gitignore` và `templates/gitignore/java.gitignore`.
  `LANGUAGE_SELECTION.md` mục 2.1 xếp Java (Spring Boot) mức ⭐ và Go mức ✅ nhưng
  bộ mẫu chưa có - cùng loại thiếu sót với `rust.gitignore` đã vá ở `v2.1.0`.

  Hai điểm đáng chú ý trong bản mẫu Go: Go build ra **file không có đuôi nằm ngay
  cạnh mã nguồn**, không mẫu chung nào bắt được chúng mà không bắt oan, nên bản
  mẫu chốt quy ước `go build -o bin/...` thay vì cố liệt kê; và `go.work` là cấu
  hình **cục bộ từng máy**, `MUST NOT` commit.

  Bản mẫu Java giữ lại `mvnw`, `maven-wrapper.properties` và `gradle-wrapper.jar`
  (chúng ghim phiên bản build cho mọi máy và cho CI), chặn
  `application-{local,dev,prod}.*` nhưng chừa `application-*.example.*`.

  Cả hai đã qua cổng kiểm mục 6b - không bản mẫu nào chặn file bắt buộc.
- `docs/GITIGNORE_POLICY.md` mục 2: thêm hai dòng ghép cho Go và Java.

---

## 2.4.0 - 24/08/2026

Bổ sung thuần. Đồng bộ được ngay, không cần sửa mã.

### Thêm mới

- `docs/BRAND_ASSETS.md` - tài sản thương hiệu lần đầu thuộc bộ quy ước: bộ file
  tối thiểu, quy tắc đặt tên, biến thể theo nền sáng/tối, màu thương hiệu, kích
  thước tối thiểu, vùng an toàn, cách sinh bộ icon, điều cấm, và checklist.

  Chuẩn được rút ra từ bộ tài sản đang chạy thật của `tsudev-cwico`
  (`assets/brand/`, `tools/gen_icons.py`, `ui/src/components/Brand.tsx`), không
  phải nghĩ ra từ đầu.

  Ba quyết định đáng chú ý:

  1. **Wordmark dựng bằng chữ thật, không phải ảnh** (`SHOULD`). Hai `span` màu
     khác nhau co giãn theo cỡ chữ hệ thống, sắc nét ở mọi DPI, chọn và tìm kiếm
     được, tự đổi màu theo chế độ nền. PNG chỉ dành cho nơi không chạy được chữ.
  2. **Màu thương hiệu KHÔNG phải token giao diện** (`MUST NOT` ghi đè token ngữ
     nghĩa). Xanh `tsu` và cam `dev` chỉ dùng cho phần nhận diện; nút bấm, liên
     kết, trạng thái vẫn đọc `tokens/design-tokens.json` như mọi nơi khác.
  3. **Bộ quy ước trung tâm không giữ file ảnh.** `MANIFEST.sha256` băm từng byte
     và repo con tải toàn bộ về, nên thêm ảnh vào đây là bắt bốn repo tải một thứ
     chúng không dùng.

  Tài liệu ghi kèm hai món nợ đã biết ở mục 11: bản gốc của `tsudev-cwico` chỉ
  `222x280` (đang bị phóng to lên 512 để sinh icon), và bản gốc `1024x1024` đúng
  chất lượng thì nằm rời ngoài mọi repo với tên sai quy ước.

### Sửa kèm

- `AGENTS.md` mục 1, `docs/00-INDEX.md`, `docs/DESIGN_SYSTEM.md` phần đầu: thêm
  lối vào tài liệu mới.
- `docs/PROJECT_STRUCTURE.md` hình trạng A: `assets/` nay ghi rõ có `brand/`.

---

## 2.3.2 - 24/08/2026

Bản vá tài liệu. Không đổi mã.

### Thêm mới

- `docs/SYNC.md` mục **3.1 - loại `.standards/` khỏi mọi công cụ tự sửa file**
  (Prettier, ESLint `--fix`, Black, `dotnet format`, `rustfmt`, và cả "format on
  save" của IDE).

  `MANIFEST.sha256` băm từng byte. Một lần Prettier chạy qua là đủ đổi dấu cách
  và xuống dòng, làm lệch băm, khiến `sync-standards.sh --check` báo lệch **vĩnh
  viễn**. Tệ hơn: cổng kiểm CI đỏ vì lý do không liên quan gì tới nội dung công
  việc, và người ta bắt đầu học cách bỏ qua nó.

  Lỗi có thật, gặp ngay ở repo `tsudev` khi áp bộ quy ước v2 - Prettier báo 26
  file "sai định dạng", trong đó 25 file là bản sao chỉ-đọc mà lẽ ra không ai
  được chạm vào.

---

## 2.3.1 - 24/08/2026

Bản vá **quan trọng cho repo .NET**.

### Sửa lỗi

- `templates/gitignore/dotnet.gitignore` có dòng `[Ll]ogs/` chặn **cả thư mục**
  `logs/` - đúng thư mục điều phối phiên mà `AGENT_PROTOCOL.md` bắt buộc phải
  commit. Bản mẫu của chính bộ quy ước mắc đúng lỗi mà `GITIGNORE_POLICY.md`
  mục 5 cảnh báo.

  Repo `swico` áp bản mẫu này và mất `.standards/templates/logs/*` khỏi bản sao
  quy ước mà không có cảnh báo nào - cho tới khi cổng kiểm mục 3b của v2.3.0 chỉ
  ra. Nay đổi thành `[Ll]ogs/*.log` và `[Ll]ogs/*.txt`.

### Thêm mới

- **Cổng kiểm mục 6b** (chỉ ở repo trung tâm): dựng thử một repo cho **từng** bản
  mẫu `.gitignore`, xác nhận không bản nào chặn `logs/STATE.md`, `logs/LOCKS.md`,
  hay file trong `.standards/`. Cổng canh để lỗi trên không tái diễn khi ai đó
  thêm bản mẫu mới.

  Đã chạy trên cả 7 bản mẫu hiện có: đều sạch.

### Repo .NET cần làm gì

```bash
./scripts/sync-standards.sh --ref v2.3.1
```

Rồi kiểm `.gitignore` của repo còn dòng `[Ll]ogs/` không; nếu còn thì thu hẹp
thành `[Ll]ogs/*.log`.

---

## 2.3.0 - 24/08/2026

Bổ sung một cổng canh cho lỗi im lặng nguy hiểm nhất tìm được cho tới nay.

### Thêm mới

- **Cổng kiểm mục 3b: file bắt buộc phải được commit.**

  Quy tắc `.gitignore` riêng của repo có thể nuốt mất chính những file mà bộ quy
  ước bắt buộc phải commit, và nuốt **hoàn toàn im lặng**. Hai ca có thật, cả hai
  đều lọt qua cổng kiểm cũ:

  | Repo | Chuyện gì xảy ra |
  | --- | --- |
  | `tsudev-cwico` | Dòng `/logs/` (vốn dành cho nhật ký chạy của ứng dụng) chặn luôn **toàn bộ** thư mục điều phối phiên. `logs/STATE.md` và `logs/LOCKS.md` có trên đĩa nhưng không bao giờ được commit - `AGENT_PROTOCOL.md` mất nền tảng mà không ai biết |
  | `swico` | Một quy tắc cũ chặn `.standards/templates/logs/*`, khiến **bản sao quy ước bị khuyết 3 file** so với bản trung tâm |

  Cổng kiểm nay xác minh: `logs/STATE.md` và `logs/LOCKS.md` tồn tại **và** thực
  sự nằm trong chỉ mục git; toàn bộ file trong `.standards/` không bị quy tắc nào
  chặn. Khi thất bại, nó in ra **đúng dòng `.gitignore` gây ra** và gợi ý cách thu
  hẹp quy tắc.

### Sửa lỗi

- Repo trung tâm bắt mọi repo phải có `logs/` theo `PROJECT_STRUCTURE.md` nhưng
  bản thân lại không có. Nay đã có, và chính cổng kiểm mới là thứ phát hiện ra.

---

## 2.2.2 - 24/08/2026

Bản vá tài liệu. Không đổi mã.

### Sửa lỗi

- `docs/SYNC.md` mục 3 hướng dẫn `cp` file mẫu từ `.standards/templates/logs/`
  ra `logs/`, nhưng file trong `.standards/` là chỉ-đọc và `cp` **giữ nguyên
  quyền đó**. Repo làm đúng theo hướng dẫn sẽ có `logs/STATE.md` không ghi được
  - tức là agent không cập nhật được trạng thái ở cuối phiên, và phiên sau mất
  toàn bộ ngữ cảnh bàn giao. Đây là hỏng đúng cơ chế mà `AGENT_PROTOCOL.md`
  dựa vào.

  Bổ sung `chmod u+w logs/STATE.md logs/LOCKS.md` vào quy trình, kèm cảnh báo ở
  `docs/ONBOARDING.md` mục 1.3 và một dòng xử lý sự cố ở `docs/SYNC.md` mục 8.

Phát hiện khi đồng bộ xuống repo `tsudev-cwico`.

---

## 2.2.1 - 24/08/2026

Bản vá **quan trọng**. Nên nâng cấp ngay nếu đã đồng bộ bằng bản 2.0.0 đến 2.2.0.

### Sửa lỗi

- `scripts/sync-standards.sh` đặt chỉ-đọc cho **cả thư mục** `.standards/`, không
  chỉ cho file. Thư mục không có quyền ghi thì git không unlink được file bên
  trong, nên `git checkout` sang nhánh khác **báo thành công nhưng bỏ sót file**:

  ```
  warning: unable to unlink '.standards/docs/a.md': Permission denied
  Switched to branch 'main'
  ```

  Hậu quả: cây làm việc lệch với nhánh mà không ai được báo lỗi, và file sót lại
  thành rác chặn mọi lần checkout sau. `git clean` và `rm -rf` cũng hỏng theo.

  Nay chỉ đặt chỉ-đọc cho file (`find -type f -exec chmod a-w`).

### Nói lại cho đúng

Quyền chỉ-đọc chỉ là **rào chắn nhẹ**: git trả lại quyền ghi sau mỗi lần
checkout. Cơ chế phát hiện sửa trộm thật sự là `sync-standards.sh --check` và
`check-standards.sh`, không phải quyền file. `docs/SYNC.md` mục 8 đã bổ sung
cách xử lý cho cây đã lỡ đồng bộ bằng bản cũ.

### Nếu đã đồng bộ bằng bản 2.0.0 đến 2.2.0

```bash
chmod -R u+w .standards
./scripts/sync-standards.sh --ref v2.2.1
```

---

## 2.2.0 - 24/08/2026

Bổ sung thuần. Đồng bộ được ngay, không cần sửa mã.

### Thêm mới

- **`.standards-allow` - miễn trừ có ghi chép cho cổng kiểm file nhạy cảm.**

  Cổng kiểm cấm mọi file khớp mẫu nhạy cảm nằm trong chỉ mục git. Quy tắc đó
  đúng trong hầu hết trường hợp, nhưng có ngoại lệ hợp lệ: `.env.production`
  của một app Next.js chỉ mang biến `NEXT_PUBLIC_*` vốn được biên dịch thẳng
  vào bundle trình duyệt, tức đã công khai theo thiết kế.

  Trước bản này, repo gặp tình huống đó chỉ có hai lối: để cổng kiểm đỏ vĩnh
  viễn, hoặc nới mẫu chặn cho cả hệ sinh thái. Cả hai đều tệ hơn vấn đề.

  Cơ chế mới đòi **đủ ba cột** `<đường dẫn> | <lý do> | <hạn>`; thiếu lý do
  hoặc thiếu hạn thì vẫn chặn. Mỗi lần chạy, dòng miễn trừ được in ra dạng
  `LƯU Ý` nên không bao giờ trở nên vô hình. Chi tiết và cảnh báo rủi ro:
  `docs/GITIGNORE_POLICY.md` mục 6. Mẫu: `templates/standards-allow.example`.

Phát hiện khi đồng bộ bộ quy ước xuống repo `tsudev`.

---

## 2.1.0 - 24/08/2026

Bổ sung thuần. Đồng bộ được ngay, không cần sửa mã.

### Thêm mới

- `templates/gitignore/rust.gitignore`. `LANGUAGE_SELECTION.md` mục 2.3 xếp Rust
  ở mức ⭐ cho đồ họa, kỹ thuật và game engine, nhưng bộ mẫu `.gitignore` lại
  chưa có bản cho Rust - repo Rust chỉ ghép được phần nền.
  Bản mới che thêm: tạo phẩm Cargo, thông tin đăng nhập `.cargo/credentials`,
  dữ liệu đo phủ và hiệu năng, thư mục build của Tauri, và **khóa ký bản cập
  nhật Tauri** (`*.tauri.key`) - lộ khóa này là mất quyền kiểm soát kênh cập
  nhật của ứng dụng đã cài trên máy người dùng.

Phát hiện khi chuẩn bị đồng bộ bộ quy ước xuống repo `tsudev-cwico`.

---

## 2.0.1 - 24/08/2026

Bản vá. Đồng bộ được ngay, không cần sửa mã.

### Sửa lỗi

- `scripts/check-standards.sh` báo nhầm file mẫu dạng `.env.<môi-trường>.example`
  là file nhạy cảm. Biểu thức cũ chỉ miễn trừ đúng `.env.example`, nên
  `.env.production.example` bị chặn oan. Cổng kiểm báo sai làm người dùng mất
  niềm tin vào cổng kiểm, và đó là cách nhanh nhất để cả nhóm học thói quen bỏ
  qua màu đỏ.
- `.gitignore` chuẩn bổ sung hai dòng miễn trừ `!.env.*.example` và
  `!.env.*.sample`, để file mẫu theo từng môi trường commit được.

Phát hiện khi chạy cổng kiểm lần đầu trên repo `tsudev`.

---

## 2.0.0 - 24/08/2026

Tái cấu trúc toàn diện. Bộ quy ước chuyển từ 6 file rời sang một hệ có cổng kiểm
tự động, cơ chế đồng bộ, và chuẩn bảo mật đầy đủ.

### Thêm mới

**Bảo mật (yêu cầu trọng tâm của bản này):**

- `SECURITY.md` - chính sách, kênh báo lỗ hổng riêng tư, cam kết thời hạn phản hồi,
  phân mức CVSS.
- `docs/SECURITY_BASELINE.md` - chuẩn bảo mật kỹ thuật bắt buộc: phân loại dữ liệu
  D0-D3, quản lý secret, 4 lớp cổng kiểm mã nguồn, chuỗi cung ứng phần mềm, xác thực
  và phân quyền, đối chiếu OWASP Top 10, header HTTP, quy trình ứng phó sự cố,
  checklist theo giai đoạn, bộ công cụ 0 đồng, và ranh giới riêng cho agent AI.
- `docs/GITIGNORE_POLICY.md` - quy tắc duy trì `.gitignore`, 10 nhóm bảo vệ, bốn
  sai lầm hay gặp.
- `.gitleaks.toml` - cấu hình quét secret, có luật riêng cho chuỗi kết nối và dữ
  liệu cá nhân Việt Nam.
- `docs/templates/SECURITY_REVIEW.md` - phiếu rà soát bảo mật đính kèm PR.

**Cơ chế đồng bộ (repo con luôn ở bản mới nhất):**

- `VERSION` và `MANIFEST.sha256` - repo con biết mình đang ở bản nào và phát hiện
  được file bị sửa tay.
- `scripts/sync-standards.sh` - đồng bộ xuống repo con, **không cần token**, tự xác
  minh toàn vẹn theo MANIFEST trước khi ghi.
- `scripts/check-standards.sh` - cổng kiểm quy ước, chạy được ở cả repo trung tâm
  lẫn repo con.
- `docs/SYNC.md` - mô hình, cài đặt lần đầu, phát hiện lệch tự động, xử lý sự cố.

**Cổng canh tự động:**

- `scripts/build-tokens.mjs` - sinh `tokens.css` từ `design-tokens.json`, có chế độ
  `--check` cho CI. Xóa hẳn khả năng hai file lệch nhau.
- `scripts/check-contrast.mjs` - kiểm 39 cặp màu đạt ngưỡng WCAG ở cả ba chế độ.
- `scripts/make-manifest.sh`.
- Workflow CI: cổng kiểm quy ước, gitleaks, CodeQL.

**Tài liệu mới:**

- `docs/00-INDEX.md` - bản đồ đọc theo vai trò.
- `docs/AGENT_PROTOCOL.md` - quy trình phiên làm việc, tách khỏi `AGENTS.md`.
- `docs/LANGUAGE_SELECTION.md` - chọn ngôn ngữ và framework theo loại project.
- `docs/FREE_TIER_STACK.md` - nhà cung cấp và hạn mức 0 đồng, ưu tiên vùng Singapore.
- `docs/RICH_TEXT_EDITOR.md` - chuẩn trình soạn thảo nội dung ngang Microsoft Word.
- `docs/SEARCH_AND_FILTER.md` - chuẩn tìm kiếm và lọc tối ưu tiếng Việt.
- `docs/GIT_WORKFLOW.md`, `docs/TESTING_QUALITY.md`, `docs/ACCESSIBILITY.md`,
  `docs/VERSIONING.md`, `docs/ONBOARDING.md`.
- `docs/templates/ADR.md`.
- `templates/gitignore/` - bản chuẩn cùng phần bổ sung cho Node, Python, .NET, C++, Mobile.
- `templates/logs/` và `templates/AGENTS.downstream.md`.
- `LICENSE` (MIT), `CONTRIBUTING.md`, `.gitattributes`, `.editorconfig`, `.env.example`.

### Thay đổi phá vỡ

1. **Giá trị `text-muted` đổi ở cả ba chế độ** để đạt WCAG AA. Bảng v1.0.0 trượt
   ngưỡng 4.5:1 ở cả ba chế độ (thấp nhất 3.69 / 4.43 / 3.89) - vi phạm chính quy
   tắc của `DESIGN_SYSTEM.md` mục 1.

   | Chế độ | Từ | Thành | Thấp nhất sau khi sửa |
   | --- | --- | --- | --- |
   | Sáng | `#5F7891` | `#52627A` | 4.99 |
   | Ấm | `#6E6552` | `#5E5646` | 5.57 |
   | Tối | `#8298B2` | `#9BB0C9` | 5.19 |

2. **Thêm token `border-control`**, `border-strong` **thu hẹp** về vai trò trang
   trí. Hai vai trò khác nhau đang bị gộp vào một token: ranh giới trang trí không
   cần đạt 3:1, ranh giới vùng tương tác thì bắt buộc. Giá trị mới:
   `#74899F` (Sáng) / `#8E8064` (Ấm) / `#6E88AE` (Tối), thấp nhất 3.05 / 3.18 / 3.73.

3. **`tokens/tokens.css` trở thành file sinh tự động.** Không sửa tay nữa. Kéo
   theo ba thay đổi tên:

   | Nơi | Trước | Sau |
   | --- | --- | --- |
   | Biến CSS | `--easing` | `--motion-easing` |
   | Biến CSS | (chưa xuất ra CSS) | `--ls-body`, `--ls-heading`, `--ls-caps-label` |
   | Khóa JSON | `typography.line-height.long-text` | `typography.line-height.long` |

   Đổi khóa JSON ảnh hưởng tới mọi nơi **đọc thẳng `design-tokens.json`** (C#,
   Python, C++), không chỉ Web.

4. **`docs/PROJECT_STRUCTURE.md` nhận hình trạng thứ hai (monorepo).** Repo phải
   tự khai mình theo hình trạng A hay B trong `AGENTS.md` phần B.

5. **`AGENTS.md` rút gọn thành điểm vào.** Nội dung chi tiết chuyển sang các tài
   liệu chuyên đề trong `docs/`. Repo con tham chiếu tài liệu, không chép nội dung.

### Hướng dẫn nâng cấp từ 1.x

```bash
# 1. Đồng bộ bản mới
./scripts/sync-standards.sh --ref v2.0.0

# 2. Tìm mọi chỗ đang ghi đè text-muted hoặc border-strong cục bộ
grep -rn "text-muted\|border-strong" src/ packages/ --include="*.css" --include="*.ts"
```

- [ ] Xóa mọi bản ghi đè cục bộ của `text-muted` - giá trị chuẩn nay đã đạt AA.
- [ ] Rà soát mọi chỗ dùng `border-strong` cho **viền nút phụ hoặc viền ô nhập**,
      đổi sang `border-control`. Giữ `border-strong` cho đường chia khối và nét
      mảnh của card.
- [ ] Chạy lại test tương phản và cập nhật ảnh chụp giao diện - màu đã đổi.
- [ ] Đổi `var(--easing)` thành `var(--motion-easing)` nếu có dùng.
- [ ] Nếu đọc thẳng `design-tokens.json` (C#, Python, C++): đổi khóa
      `line-height.long-text` thành `line-height.long`.
- [ ] Khai hình trạng A hay B trong `AGENTS.md` phần B.
- [ ] Bật cổng kiểm CI theo `docs/SYNC.md` mục 5.1.
- [ ] Chạy `./scripts/check-standards.sh` và xử lý hết vi phạm.

### Sửa lỗi

- `docs/PROJECT_STRUCTURE.md` trước đây trỏ repo trung tâm là
  `tsudev-design-tokens` - tên sai, nguồn chân lý thật là `tsudev-standards`.
- `.gitignore` và `logs/` được quy ước v1.0.0 tham chiếu nhưng **chưa bao giờ tồn
  tại trong repo**. Nay có đủ, dưới dạng bản chuẩn trong `templates/`.
- Hai đề xuất treo trong `proposals/` từ 20/08/2026 đã được nhận vào bản này.

### Vận hành

- Repo chuyển từ **Private sang Public**. Lý do đầy đủ ở `README.md`.

---

## 1.0.1 - 22/08/2026

- Thêm quy ước gạch ngang vào `AGENTS.md` mục 6: chỉ dùng hyphen `-` (U+002D)
  trong mọi văn bản, không dùng em-dash (U+2014); en-dash chỉ cho khoảng số.
  Thay toàn bộ em-dash trong repo thành hyphen (10 file, 46 chỗ).

## 1.0.0 - 19/08/2026

- Khởi tạo bộ quy ước trung tâm: `AGENTS.md`, `docs/DESIGN_SYSTEM.md`,
  `docs/PROJECT_STRUCTURE.md`, `docs/templates/HANDOVER.md`, `tokens/`.
