# PHIẾU ĐỀ XUẤT - Thêm "Đăng nhập với Apple" làm nhà cung cấp liên kết thứ tư (AUTH_AND_ACCOUNT.md mục 3)

- **Mã phiếu**: 20261119-01
- **Từ**: agent-qulythuchi (phiên P9a), 19/11/2026 - theo yêu cầu chủ dự án: "đăng nhập là tài khoản Google/Apple ID,
  không đăng nhập thì là khách"
- **Đến**: phiên kế tiếp của `tsudev-standards` (chủ dự án duyệt)
- **Trạng thái**: ĐÓNG - phát hành v4.3.0 (21/11/2026)

## 1. Vì sao
- `AUTH_AND_ACCOUNT.md` mục 3 cấm thêm nhà cung cấp thứ tư khi chưa có đề xuất được duyệt ⇒ qulythuchi CHƯA làm Apple.
- App Store Review Guideline 4.8: app iOS có đăng nhập bên thứ ba (Google) PHẢI có "Sign in with Apple" (hoặc lựa
  chọn tương đương quyền riêng tư). Mọi app iOS của hệ (qulythuchi đang hoãn iOS) sẽ vướng khi phát hành.
- Người dùng iPhone/Mac quen Apple ID; Apple cho phép ẩn email (`privaterelay.appleid.com`).

## 2. Đề xuất sửa chuẩn
1. Mục 3: thứ tự Google, **Apple**, GitHub, Tài khoản tsudev. Nút Apple theo Human Interface Guidelines (đen/trắng,
   logo Apple chính chủ). Apple chỉ BẮT BUỘC hiện trên iOS/macOS/web; Android/Windows/Linux `MAY`.
2. Mục 3.1: Apple phạm vi `name email`; mục 5: email ẩn `@privaterelay.appleid.com` coi là đã xác minh nhưng KHÔNG gộp
   tự động với tài khoản email thật (người dùng tự liên kết ở `/tai-khoan/bao-mat`).
3. Mục 15: `GET /api/v1/auth/providers/apple` (+ callback `form_post` vì Apple trả POST).
4. Chi phí: cần Apple Developer Program (99 USD/năm - chủ dự án đang hoãn) cho Services ID + khóa `.p8`.

## 3. Việc kéo theo khi duyệt
- Repo `tsudev` (IdP): provider Apple trong NextAuth, `idp_hint=apple` (phiếu `tsudev` 20261119-QT4 mở rộng).
- RP (qulythuchi...): thêm `apple` vào danh sách `provider` cho phép (`services/sync-api/src/auth/oidc.ts`
  `LOGIN_PROVIDERS`, `apps/app/lib/sync/pkce.dart` `loginProviders`) + nút.

## 4. Kết quả xử lý
- 19/11/2026 - agent-qulythuchi: mở đề xuất.
- 21/11/2026 - phiên tsudev-standards: DUYỆT có điều chỉnh, phát hành v4.3.0 (`AUTH_AND_ACCOUNT.md` v3.2.0 mục 3.2). Khác đề xuất: Apple `MUST` chỉ khi sản phẩm phát hành App Store (trên mọi nền tảng của sản phẩm đó), còn lại `MAY`; không mua Apple Developer Program chỉ để có nút trên web; nút ẩn khi IdP chưa bật. Phiếu sang `tsudev` và `qulythuchi`.
