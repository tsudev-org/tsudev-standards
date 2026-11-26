# Bộ hook agent (Claude Code) - bản gốc

Bản gốc của các hook cài trên máy phát triển tại `~/.claude/hooks/`. Sửa thì sửa ở đây, chạy kiểm thử, rồi cài lại.

| Tệp | Vai trò | Chuẩn |
| --- | --- | --- |
| `noleaklib.py` | Nhận diện tệp/chuỗi bí mật, đọc siêu dữ liệu an toàn (không bao giờ trả về giá trị) | `SECURITY_BASELINE.md` 12.1 |
| `noleak-guard.py` | Hook `PreToolUse` (chặn lệnh/tệp có thể lộ bí mật) + `PostToolUse` (phát hiện chuỗi dạng khoá thật trong output; tự `chmod 600` tệp bí mật vừa ghi) | 12.1, 12.2 |
| `noleak-inspect.py` | Công cụ cho agent: in tên khoá + độ dài + quyền + định dạng; mã thoát 3 khi tệp không theo `KEY=VALUE`. `--to-env TEN <tệp>`: đổi tệp token thô 1 dòng thành `TEN='...'` (quyền 600, nạp lại so sha256) - chỉ khi chủ dự án ủy quyền | 12.1 mục 4a |
| `phase-context.py` | Hook `SessionStart` (`startup\|clear\|compact\|resume`): nạp lại Phase đang mở của `docs/PLAN.md`, STATE, phiếu mới nhất; rà bảo mật repo (tự `chmod 600`, cảnh báo token thô/tệp bí mật bị theo dõi), nhắc phiếu xoay khoá `*-XK*` còn MỞ | `AGENT_PROTOCOL.md` 4.2, `SECURITY_BASELINE.md` 12.2-12.3 |
| `statusline.py` | Status line: mô hình, repo@nhánh, `ctx %` theo `autoCompactWindow` (vàng 70%, đỏ 90%) | `AGENT_PROTOCOL.md` 4.3 |
| `test-noleak-guard.py` | Kiểm thử bằng dữ liệu giả | - |

## Cài đặt

```bash
python3 scripts/agent-hooks/test-noleak-guard.py          # phải in "N/N dat"
install -d ~/.claude/hooks
install -m 755 scripts/agent-hooks/*.py ~/.claude/hooks/
```

Thêm vào `~/.claude/settings.json` (gộp với khoá đã có, không ghi đè):

```json
{
  "model": "opusplan",
  "autoCompactWindow": 300000,
  "env": {
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-5-5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-5-5",
    "CLAUDE_CODE_SUBAGENT_MODEL": "sonnet"
  },
  "statusLine": { "type": "command", "command": "python3 ~/.claude/hooks/statusline.py" },
  "hooks": {
    "SessionStart": [{ "matcher": "startup|clear|compact|resume",
      "hooks": [{ "type": "command", "command": "python3 ~/.claude/hooks/phase-context.py", "timeout": 10 }] }],
    "PreToolUse": [{ "matcher": "Bash|Read|Grep|Write|Edit|MultiEdit|NotebookEdit",
      "hooks": [{ "type": "command", "command": "python3 ~/.claude/hooks/noleak-guard.py", "timeout": 10 }] }],
    "PostToolUse": [{ "matcher": "*",
      "hooks": [{ "type": "command", "command": "python3 ~/.claude/hooks/noleak-guard.py", "timeout": 10 }] }]
  }
}
```

Kiểm chứng sau khi cài: mở phiên mới, nhờ agent chạy `printenv` - phải bị từ chối với lý do `[Zero Secret Exposure]`.

## Giới hạn đã biết

- Hook phân tích lệnh theo mẫu, không phải trình thông dịch shell: mã python/node viết trong heredoc tự mở tệp bí mật
  không bị chặn trước - lớp `PostToolUse` và quy tắc 12.1 bao phần này.
- `PostToolUse` chỉ báo sau khi output đã vào ngữ cảnh; nó buộc agent dừng, không lặp lại và báo chủ dự án.
- Mẫu chung `TEN_SECRET=gia_tri_dai` chỉ dùng để chặn commit/PR (test giả hay khớp mẫu này).
