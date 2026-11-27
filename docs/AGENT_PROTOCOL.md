# GIAO THỨC LÀM VIỆC CỦA AGENT (v2.5.0)

> Tài liệu này mô tả **cách vận hành một phiên làm việc** cho cả lập trình viên
> và agent AI: mở phiên, khóa file, bàn giao, đóng phiên. Quy ước nội dung nằm ở
> các tài liệu khác; đây là quy trình.

## 1. Ba file điều phối

| File | Vai trò | Ai ghi |
| --- | --- | --- |
| `logs/STATE.md` | Hàng đợi việc, việc đang làm, việc đã xong, quyết định quan trọng | Mọi phiên, đầu và cuối |
| `logs/LOCKS.md` | File nào đang bị ai khóa | Người/agent trước khi sửa file |
| `logs/handover/` | Phiếu bàn giao giữa các phiên | Phiên sắp kết thúc |

Cả ba `MUST` được commit vào repo. Chúng là bộ nhớ chung của dự án, không phải
file tạm.

## 2. Mở phiên

Dán nguyên khối này vào đầu **mọi** phiên terminal mới:

```
Đọc AGENTS.md, logs/STATE.md và phiếu bàn giao mới nhất trong logs/handover/.
Tuân thủ toàn bộ quy ước. Nhận task tiếp theo trong hàng đợi của STATE.md,
khóa file mình sẽ sửa vào logs/LOCKS.md rồi mới bắt đầu. Trả lời ngắn gọn,
tiết kiệm token, không lặp lại nội dung đã có trong file quy ước.
```

Agent `MUST` thực hiện đúng thứ tự: đọc quy ước -> đọc trạng thái -> đọc phiếu
bàn giao -> nhận việc -> khóa file -> mới bắt đầu sửa.

Repo sản phẩm chưa có phiếu `RA_SOAT_DANG_NHAP` cho bộ quy ước MAJOR hiện hành: `MUST` làm bước tự kiểm một cổng đăng
nhập ở [`AUTH_AND_ACCOUNT.md`](AUTH_AND_ACCOUNT.md) mục 2.1.

Trên máy phát triển có kho tri thức AKB ([`KNOWLEDGE_BASE.md`](KNOWLEDGE_BASE.md)), ngay sau khi nhận việc agent
`MUST` chạy `akb start "<mục tiêu phiên>"` (đọc phần liên quan trong danh sách in ra) và, với việc cụ thể (lỗi, thư
viện, CI, deploy, nộp duyệt), `akb search "<từ khoá>"` để dùng lại cách sửa mà dự án khác đã kiểm chứng.

## 3. Khóa file (chống giẫm chân)

Trước khi sửa **bất kỳ** file nào:

1. Đọc `logs/LOCKS.md`.
2. File chưa ai khóa: thêm dòng theo đúng định dạng, rồi mới sửa.
   ```
   src/features/search/index.ts | agent-2 / tìm kiếm không dấu | 14:30 24/08/2026
   ```
3. Sửa xong: **xóa dòng khóa của mình ngay**, không đợi cuối phiên.

**File đang bị người khác khóa: TUYỆT ĐỐI không sửa.** Thay vào đó tạo phiếu bàn
giao tại `logs/handover/` theo mẫu `docs/templates/HANDOVER.md`, ghi rõ cần thay
đổi gì, vì sao, và tiêu chí thế nào là xong.

Người đang giữ khóa `MUST` đọc phiếu gửi đến mình **trước khi** nhả khóa, thực
hiện hoặc từ chối có lý do, và ghi kết quả vào chính phiếu đó.

`MUST NOT` can thiệp vào nhiệm vụ, nhánh git, hay file của người khác đang làm.

## 4. Tiết kiệm token và ngữ cảnh

- Không đọc lại file đã nắm nội dung trong cùng phiên.
- Không in toàn bộ file dài ra hội thoại - chỉ trích phần liên quan.
- Trả lời và ghi log **ngắn gọn, gạch đầu dòng, không văn mẫu**.
- Tri thức dùng lại được (quyết định kiến trúc, cách chạy build, lỗi đã gặp) ghi
  vào file markdown tương ứng **một lần duy nhất**; các phiên sau chỉ tham chiếu
  đường dẫn.
- Task lớn `MUST` chia nhỏ. Làm xong phần nào chốt phần đó vào log ngay, để mất
  phiên không mất công.

### 4.1. Chọn mô hình theo độ khó (MUST - chủ dự án 26/11/2026)

Máy phát triển chạy Claude Code với `opusplan`: **Plan Mode dùng Opus, thực thi dùng Sonnet**; subagent mặc định
Sonnet. Mục tiêu: chi phí thấp nhất mà **không hạ chất lượng** - đúng mô hình cho đúng việc.

| Việc | Mô hình |
| --- | --- |
| Thực thi Phase đã có kế hoạch, lỗi rõ nguyên nhân, test, tài liệu | Sonnet (mặc định) |
| Kiến trúc, ADR, lập hoặc sửa `docs/PLAN.md` | **Opus** |
| Lỗi sửa 2 lần chưa được, hoặc chưa rõ nguyên nhân | **Opus** |
| Xung đột merge, race, đồng thời; bảo mật, mật mã, xác thực, phân quyền | **Opus** |
| Migration hay thao tác dữ liệu production; thay đổi chạm nhiều module; rà soát trước phát hành | **Opus** |
| Tìm kiếm rộng trong mã | subagent `Explore` (Sonnet) |
| Việc máy móc: đổi tên hàng loạt, định dạng, sinh dữ liệu mẫu | subagent `haiku` |

Agent **không tự gõ được** `/model`, `/clear`, `/compact`. Cách lên Opus (chủ dự án đã ủy quyền chung):

1. Gọi công cụ `EnterPlanMode` - phiên chuyển sang Opus để điều tra và lập phương án; `ExitPlanMode` xin duyệt, sau
   đó Sonnet thực thi.
2. Giao subagent `model: "opus"` phần phân tích hoặc rà soát cụ thể; nhận kết luận rồi thực thi bằng Sonnet.
3. Cả phiên cần Opus: đề nghị chủ dự án gõ `/model opus`.

Nghi ngờ thì lên Opus. `MUST NOT` hạ mô hình hay bỏ bước kiểm chứng để tiết kiệm.

### 4.2. Chu trình Phase (MUST)

Nguồn sự thật của tiến độ là **tệp**, không phải lịch sử hội thoại. Nhờ đó `/clear` lúc nào cũng an toàn.

1. Kế hoạch nhiều bước nằm ở `docs/PLAN.md` theo mẫu [`templates/PLAN.md`](templates/PLAN.md): mỗi Phase là
   `## Phase <id> - <tên>` + checklist `- [ ]` + tiêu chí nghiệm thu đo được. Kế hoạch do Opus lập (mục 4.1).
2. Một ngữ cảnh làm **một** Phase. Xong Phase = đạt tiêu chí nghiệm thu (build, test, cổng kiểm) -> đánh `[x]` ->
   cập nhật `logs/STATE.md` kèm bước tiếp -> commit -> AKB nếu có -> **dừng** và báo đúng một dòng:
   `✅ Phase <id> xong. Gõ /clear rồi "tiếp" để sang Phase <id kế>.`
   `MUST NOT` tự bắt đầu Phase kế trong cùng ngữ cảnh.
3. Phase dài: mỗi mốc nhỏ xong ghi tiến độ vào PLAN/STATE ngay, để nén ngữ cảnh lúc nào cũng không mất gì.
4. Sau `/clear` hoặc nén: đọc khối ngữ cảnh do hook `SessionStart` chèn (Phase đang mở, STATE, phiếu mới nhất), đọc lại
   phần liên quan của PLAN/STATE, làm tiếp - không hỏi lại điều đã ghi.

Kế hoạch cũ dạng bảng hoặc emoji vẫn dùng được; khi sửa kế hoạch `SHOULD` chuyển sang mẫu checklist.

### 4.3. Quản lý ngữ cảnh (MUST)

- Ngưỡng tự nén của máy là **300K token** (`autoCompactWindow`), không phải cửa sổ 1M của mô hình: mỗi lượt gửi lại
  toàn bộ ngữ cảnh, ngữ cảnh lớn nhân chi phí của mọi lượt sau và làm giảm mức tuân thủ quy ước. 300K = chi phí cố
  định của phiên (prompt hệ thống, công cụ, `CLAUDE.md`/`AGENTS.md`, khoảng 30-60K) + đủ chỗ cho một Phase lớn.
- Status line hiện `ctx %` theo ngưỡng tự nén: **vàng >= 70%**, **đỏ >= 90%**, trên 100% = phiên mở trước khi đổi cấu hình. Vàng/đỏ giữa Phase: chốt tiến độ vào tệp
  rồi đề nghị `/compact giữ Phase <id>, tệp đang sửa, lỗi chưa xử lý`. Xong Phase: `/clear` (không tốn token).
- Việc không liên quan tới việc đang làm: `/clear` trước.
- Đọc tệp theo đoạn cần thiết; lọc output dài (`tail`, `grep`); tìm kiếm rộng giao subagent để chỉ kết luận vào ngữ
  cảnh chính.
- `CLAUDE.md`/`AGENTS.md` của repo nạp vào **mọi** lượt của **mọi** phiên: `SHOULD` dưới 200 dòng; phần chỉ cần cho
  một vùng mã chuyển sang `.claude/rules/*.md` có `paths:`, quy trình dùng thỉnh thoảng chuyển thành skill, ghi chú
  cho người bảo trì đặt trong `<!-- -->` (không tốn token).
- `CLAUDE.md` có mục `# Compact instructions` nói rõ cần giữ gì khi nén.
- **Tiết kiệm chỉ cắt lãng phí, không cắt mục tiêu**: `MUST NOT` bỏ bớt phạm vi, mục checklist, tiêu chí nghiệm thu,
  test, cổng kiểm hay bước bảo mật của task/Phase để đỡ token. Ngữ cảnh sắp đầy thì chốt tiến độ vào tệp và đề nghị
  `/compact`, không vội kết thúc Phase.

### 4.4. Nhiều tài khoản Claude trên một máy: lệnh `cc` (MUST - chủ dự án 27/11/2026)

**Mục đích.** Chủ dự án dùng nhiều tài khoản Claude (gói thuê bao riêng, mỗi tài khoản một hạn mức giờ/tuần) trên cùng
một máy và chạy 2-6 terminal song song cho nhiều dự án. Khi một tài khoản hết hạn mức, cách cũ (`/logout` rồi `/login`
kèm dán mã qua trình duyệt) tốn thời gian, tốn RAM/CPU và làm đứt việc của agent. Cách mới: mỗi tài khoản một thư mục
cấu hình riêng (`CLAUDE_CONFIG_DIR`), đăng nhập **đúng một lần**, sau đó chuyển tức thì. Mục tiêu là **tiếp tục Phase
không mất ngữ cảnh làm việc**, không phải tăng hạn mức bằng thủ thuật.

**Cơ chế (chỉ trên máy của chủ dự án, repo con không phụ thuộc).**

- Lệnh `cc <số|tên>` (`~/.local/bin/cc`) chạy `claude` với `CLAUDE_CONFIG_DIR=~/.claude-<tên>`; `cc ls` liệt kê tài khoản
  và trạng thái đăng nhập (chỉ kiểm tệp có tồn tại, không đọc nội dung); `cc init` tạo lại liên kết dùng chung.
- `cc ls` hiện hạn mức 5 giờ/tuần (% đã dùng + giờ reset) và gói/gia hạn của từng tài khoản để chủ dự án chọn tài
  khoản còn hạn mức. Nguồn hạn mức là trường `rate_limits` mà Claude Code đưa vào status line (không dùng token OAuth,
  không gọi API không công khai); status line ghi cache `~/.cache/tsudev/cc-usage/<profile>.json` (chỉ % và giờ reset,
  `600`). Số liệu chỉ mới khi tài khoản đó có phiên chạy. Gói/gia hạn do chủ dự án nhập tay (`cc set`) vào
  `~/.config/cc/accounts.json`. Agent `MUST NOT` lấy hạn mức bằng cách đọc token hay gọi API ngoài đường này.
- Quản lý tài khoản: `cc login <số|tên>` (đăng nhập một lần, điền sẵn email), `cc logout <số|tên>` (hỏi xác nhận, chỉ
  xoá đăng nhập của profile đó), `cc add <email>` / `cc rm <số|tên>` (sửa `~/.config/cc/accounts.list`, `rm` không xoá
  thư mục profile). `cc ls` gọi `claude auth status --json` để đối chiếu email thật của từng profile với danh sách và
  báo `SAI` khi đăng nhập nhầm; loại gói lấy từ đây, ngày gia hạn vẫn nhập tay. Các lệnh này do chủ dự án chạy, agent
  không chạy thay.
- Mỗi profile liên kết (symlink) `CLAUDE.md`, `settings.json`, `hooks/`, `skills/`, `plugins/` về `~/.claude` để hook
  bảo mật (`noleak-guard`), quy ước Phase và status line **áp dụng như nhau cho mọi tài khoản**. Token
  (`.credentials.json`), lịch sử và `projects/` (kèm memory) **riêng từng tài khoản**.
- Tên thư mục profile là định danh tài khoản của chủ dự án: `MUST NOT` ghi vào repo, tài liệu, AKB, commit, phiếu
  bàn giao hay tin nhắn cho phiên khác (thông tin cá nhân); chỉ gọi chung là "profile `cc`".

**Quy tắc cho agent.**

1. Việc đổi tài khoản là **việc của chủ dự án, chạy tay**. Agent `MUST NOT` tự đổi tài khoản, tự viết công cụ phát hiện
   hết hạn mức rồi xoay vòng, hay đề xuất cách né/lách giới hạn (nằm ngoài ý định và có rủi ro vi phạm điều khoản của
   nhà cung cấp). Cần thêm hạn mức: đề xuất kênh chính thống (nâng gói, API key theo lượng dùng).
2. `MUST NOT` đọc, in, sao chép, sửa, chuyển `.credentials.json` hay tệp trong `~/.claude-*` (mục Zero Secret Exposure);
   `MUST NOT` chạy `/logout`, `/login` hay đổi `CLAUDE_CONFIG_DIR` thay chủ dự án, và `MUST NOT` nới quyền thư mục
   profile (giữ `700`).
3. **Phiên có thể bị cắt ngang bất cứ lúc nào vì hết hạn mức**, nên nguồn sự thật phải nằm trong tệp (mục 4.2): mỗi mốc
   nhỏ xong ghi ngay vào `docs/PLAN.md`/`logs/STATE.md` (Phase đang làm, tệp đang sửa, lỗi chưa xử lý, bước tiếp). Phiên
   kế tiếp ở tài khoản khác không thấy lịch sử chat của phiên trước: đọc `STATE.md`/`PLAN.md`, `git status`/`git log`
   để làm tiếp, không đoán.
4. Gặp thông báo hết hạn mức/`rate limit`: chốt tiến độ vào tệp theo mục 4.2 rồi báo chủ dự án một dòng (ví dụ
   `⏸ Hết hạn mức tài khoản này. Tiến độ đã ghi STATE.md. Gõ cc <số khác> rồi "tiếp".`); không thử lại dồn dập.
5. Nhiều phiên song song ở các profile khác nhau vẫn tuân thủ mục 3 và 7 (khóa file, nhánh riêng, một nhiệm vụ mỗi
   phiên); tài khoản khác nhau **không** làm hai phiên được phép sửa cùng một tệp.

## 5. Đóng phiên và bàn giao

Kích hoạt khi: (a) hàng đợi trong `STATE.md` cạn, (b) được yêu cầu bàn giao,
hoặc (c) ngữ cảnh sắp cạn.

1. Ghi vào `logs/STATE.md`: việc đã làm, việc dang dở **kèm bước tiếp theo cụ
   thể**, quyết định quan trọng.
2. Tạo phiếu `logs/handover/YYYYMMDD-NN_<chủ-đề>.md` theo mẫu. Tiêu chuẩn: phiên
   sau đọc xong làm tiếp được **không cần hỏi lại**, kể cả khi máy tắt đột ngột.
3. Nhả toàn bộ khóa của mình trong `logs/LOCKS.md`.
4. Dọn tàn dư: xóa file tạm, không để thay đổi chưa commit nằm ngoài phạm vi bàn
   giao. Cây làm việc sạch để phiên sau không tốn "chi phí chết".
5. **AKB** (`KNOWLEDGE_BASE.md` mục 7): lỗi/bài học/quyết định dùng lại được đã ghi thành `ISS`/`LES`/`DEC`;
   điền `SES`, `akb close <SES-ID> "<tóm tắt>"`, `akb sync --project <slug>`. Phiếu bàn giao trỏ tới ID AKB thay vì
   chép lại tri thức.
6. Đề xuất chủ project đóng terminal và mở phiên mới cho task kế tiếp.

## 6. Ranh giới của agent AI

Ngoài các mục ở `SECURITY_BASELINE.md` mục 12, agent `MUST NOT`:

- Sửa file quy ước (`AGENTS.md`, `.standards/**`, `docs/*` được đánh dấu KHÔNG
  SỬA, `tokens/*`, `.gitignore`) trừ khi chủ project yêu cầu trực tiếp.
- Tự ý `git push`, mở PR, hay merge khi chưa được yêu cầu.
- Tự ý xóa file hay thư mục ngoài phạm vi task.
- Chạy lệnh phá hủy (`rm -rf`, `git reset --hard`, `DROP TABLE`) mà không hỏi trước.
- Thêm phụ thuộc mới mà không khai báo theo `SECURITY_BASELINE.md` mục 5.

Và `MUST`:

- Báo cáo trung thực: test trượt thì nói là trượt kèm output; bỏ qua bước nào thì
  nói rõ bước đó.
- Khi phát hiện quy ước tự mâu thuẫn hoặc sai, báo cho chủ project và đề xuất qua
  `proposals/`, không tự sửa theo ý mình.

### 6.1. Sản phẩm đứng tên chủ dự án (MUST - chủ dự án 20/11/2026)

Mọi dự án trong hệ TsuDEV do chủ dự án xây dựng, sở hữu và quản lý; agent là công cụ. Mọi thứ agent tạo ra cho dự án
`MUST NOT` ghi "do AI thực hiện" hay tương đương:

- Nội dung và dữ liệu sản phẩm: README, tài liệu, giao diện, mô tả, ghi chú phát hành, website, hồ sơ cửa hàng - tác
  giả là chủ dự án.
- Git: commit và PR **không** thêm dòng `Co-Authored-By:` của AI, "Generated with ...", hay chữ ký agent. Tác giả
  commit là cấu hình git của máy.
- Biểu mẫu nền tảng (Google Play Console, Partner Center, App Store Connect, cổng báo nhầm antivirus...): điền như chủ
  dự án tự điền, không chọn "do AI thực hiện"; chi tiết và ngoại lệ câu hỏi về tính năng thật của app ở
  `STORE_SUBMISSION.md` mục 0.1.
- Không áp dụng cho chỗ AI LÀ đối tượng của nội dung (ví dụ tài liệu cách dùng agent, `AGENTS.md`, AKB, `logs/`): các
  tệp điều phối nội bộ vẫn gọi đúng tên agent.

## 7. Nhiều agent làm song song

- Mỗi agent nhận **một nhiệm vụ duy nhất** tại một thời điểm, ghi trong
  `STATE.md` mục "Đang thực hiện".
- Mỗi agent làm trên **nhánh riêng**.
- Phân chia theo **ranh giới file**, không theo ranh giới tính năng - vì hai
  tính năng có thể đụng cùng một file.
- Khi hai nhiệm vụ buộc phải đụng cùng file: một agent làm, agent kia gửi phiếu
  bàn giao. Không có ngoại lệ.
