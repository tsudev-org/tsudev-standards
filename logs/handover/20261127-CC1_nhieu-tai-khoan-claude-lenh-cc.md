# PHIẾU CC1 - Nhiều tài khoản Claude trên một máy: lệnh `cc` (agent mọi dự án đọc - tuân thủ)

- **Mã phiếu**: 20261127-CC1 - **Từ**: phiên cấu hình máy, 27/11/2026 - **Gửi**: mọi phiên agent / phiên điều phối
  `tsudev-standards` - **Trạng thái**: CHỜ MERGE PR #96 (đã đạt cổng kiểm)
- **Yêu cầu chủ dự án (27/11/2026)**: dùng nhiều tài khoản Claude trên cùng máy mà đổi tức thì, không `/logout` +
  `/login` + dán mã; thấy hạn mức giờ/tuần của từng tài khoản; mọi agent hiểu mục đích và tuân thủ.

## 1. Agent phải biết và làm theo (chuẩn: `docs/AGENT_PROTOCOL.md` mục 4.4)

1. Mục đích: chuyển sang tài khoản còn hạn mức để **tiếp tục Phase**, không phải để lách giới hạn.
2. Đổi tài khoản là việc của chủ dự án, chạy tay (`cc <số|tên>`). Agent KHÔNG tự đổi, KHÔNG tự xoay vòng, KHÔNG chạy
   `cc login/logout/add/rm/set` thay chủ dự án, KHÔNG đọc/sửa `~/.claude-*` hay `.credentials.json`.
3. Phiên có thể bị cắt ngang bất cứ lúc nào khi hết hạn mức: mỗi mốc nhỏ xong ghi ngay vào `docs/PLAN.md` /
   `logs/STATE.md`. Phiên kế tiếp ở tài khoản khác không thấy chat cũ: đọc STATE/PLAN + `git status`/`git log`.
4. Thấy thông báo hết hạn mức: chốt tiến độ, báo một dòng (`⏸ Hết hạn mức... Gõ cc <số khác> rồi "tiếp".`), không thử lại dồn dập.
5. Không ghi tên/email tài khoản vào repo, AKB, commit, phiếu, tin nhắn (thông tin cá nhân): gọi chung "profile `cc`".

## 2. Cơ chế (chỉ trên máy chủ dự án)

`~/.local/bin/cc` + `cc-ls`; mỗi tài khoản một `~/.claude-<tên>` (700), symlink `CLAUDE.md`, `settings.json`, `hooks/`,
`skills/`, `plugins/` từ `~/.claude` (hook bảo mật áp dụng cho mọi profile). Hạn mức lấy từ `rate_limits` trong JSON
status line, ghi cache `~/.cache/tsudev/cc-usage/` (chỉ % và giờ reset); email thật + loại gói từ `claude auth status --json`
(không đụng token). Danh sách: `~/.config/cc/accounts.list`; gói/gia hạn nhập tay: `~/.config/cc/accounts.json`.

## 3. Việc còn lại

- [ ] Chủ dự án merge PR #96 (`v9.1.0`), repo con đồng bộ `sync-standards.sh --ref v9.1.0` (MINOR, không bắt buộc sửa).
- [ ] Chủ dự án chạy `cc N` một lần mỗi tài khoản để có số liệu hạn mức; `cc set N renew=YYYY-MM-DD`.
- Bài học: AKB `LES-20261127-2017-9730`; phiên: `SES-20261127-2017-d3ec`.
