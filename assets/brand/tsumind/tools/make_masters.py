#!/usr/bin/env python3
"""make_masters.py - dựng BẢN GỐC CHUẨN (master) của bộ nhận diện TsuMIND từ 5 hình chủ dự án giao.

    source/original/  (bất biến, nguyên văn chủ dự án giao 27/11/2026)
        0-logo-tsumind.png        huy hiệu 1024x1024, alpha thật + dấu ✦ bán trong suốt
        1-primary-emblem.png      bản 255px của hình 0 (chỉ để đối chiếu, không dùng sinh)
        2-horizontal-lockup.jpg   logo ngang 255x143 trên nền đen
        3-brand-mark.jpg          biểu tượng cú trong vòng tròn 255x255 trên nền đen
        4-app-icon-squircle.jpg   icon squircle 255x255 trên nền navy đậm
              |
              v  (script này - chạy tay khi đổi hình gốc)
    source/master/    PNG RGBA nền trong suốt, độ phân giải đủ cho icon 1024px
        tsumind-emblem.png        từ hình 0: xoá ✦, cắt sát + vuông
        tsumind-mark.png          từ hình 3: Real-ESRGAN x4, tách nền đen (giữ quầng sáng), vuông
        tsumind-wordmark.png      phần chữ của hình 2: Real-ESRGAN x4, tách nền đen, tách theo khoảng trống alpha
        tsumind-lockup.png        cú master (hình 3) + wordmark, đúng tỷ lệ/khoảng cách của hình 2
        tsumind-lockup-light.png  như trên, chữ Midnight Navy cho nền sáng (+ tsumind-wordmark-light.png)
        tsumind-squircle.png      từ hình 4: Real-ESRGAN x4, khớp siêu elip, 1024px, cú master ghép đè cho nét sắc
              |
              v  build.mjs (Node, sharp) -> dist/ AVIF/WebP/PNG/ICO/ICNS

Phóng to: Real-ESRGAN (Wang và cộng sự, ICCVW 2021, BSD-3), trọng số chính thức
github.com/xinntao/Real-ESRGAN releases, kiểm SHA-256 trước khi nạp, nạp bằng torch.load(weights_only=True)
(không thực thi mã trong tệp trọng số). Chạy CPU, ~1-3 phút.

Môi trường (ngoài repo, 0 đồng):
    python3 -m venv ~/.cache/tsumind-brand/venv
    ~/.cache/tsumind-brand/venv/bin/pip install -r tools/requirements.txt \
        --extra-index-url https://download.pytorch.org/whl/cpu
    ~/.cache/tsumind-brand/venv/bin/python -I tools/make_masters.py

Kết quả có tính tất định trên cùng phiên bản thư viện + CPU; khác máy có thể lệch vài mức xám, nên master được
COMMIT và build.mjs chỉ đọc master (không chạy lại AI trong CI).
"""
from __future__ import annotations

import hashlib
import os
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / 'source' / 'original'
MASTER = ROOT / 'source' / 'master'
CACHE = Path(os.environ.get('TSUMIND_BRAND_CACHE', Path.home() / '.cache' / 'tsumind-brand' / 'models'))

MODELS = {
    # tên: (URL, SHA-256, số khối RRDB)
    'x4plus': (
        'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth',
        '4fa0d38905f75ac06eb49a7951b426670021be3018265fd191d2125df9d682f1',
        23,
    ),
    'anime6b': (
        'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth',
        'f872d837d3c90ed2e05227bed711af5671a6fd1c9f7d7e91c911a61f155e99da',
        6,
    ),
}
MODEL = os.environ.get('TSUMIND_SR_MODEL', 'anime6b')  # nét logo minh hoạ gọn hơn x4plus (so 28/11/2026)


# ---------------------------------------------------------------- Real-ESRGAN (RRDBNet, kiến trúc gốc)
def build_net(num_block: int):
    import torch
    from torch import nn
    import torch.nn.functional as F

    class RDB(nn.Module):
        def __init__(self, nf=64, gc=32):
            super().__init__()
            self.conv1 = nn.Conv2d(nf, gc, 3, 1, 1)
            self.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1)
            self.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1)
            self.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1)
            self.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1)
            self.lrelu = nn.LeakyReLU(0.2, inplace=True)

        def forward(self, x):
            x1 = self.lrelu(self.conv1(x))
            x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
            x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
            x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
            x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
            return x5 * 0.2 + x

    class RRDB(nn.Module):
        def __init__(self, nf=64, gc=32):
            super().__init__()
            self.rdb1, self.rdb2, self.rdb3 = RDB(nf, gc), RDB(nf, gc), RDB(nf, gc)

        def forward(self, x):
            return self.rdb3(self.rdb2(self.rdb1(x))) * 0.2 + x

    class RRDBNet(nn.Module):
        def __init__(self, nb, nf=64, gc=32):
            super().__init__()
            self.conv_first = nn.Conv2d(3, nf, 3, 1, 1)
            self.body = nn.Sequential(*[RRDB(nf, gc) for _ in range(nb)])
            self.conv_body = nn.Conv2d(nf, nf, 3, 1, 1)
            self.conv_up1 = nn.Conv2d(nf, nf, 3, 1, 1)
            self.conv_up2 = nn.Conv2d(nf, nf, 3, 1, 1)
            self.conv_hr = nn.Conv2d(nf, nf, 3, 1, 1)
            self.conv_last = nn.Conv2d(nf, 3, 3, 1, 1)
            self.lrelu = nn.LeakyReLU(0.2, inplace=True)

        def forward(self, x):
            feat = self.conv_first(x)
            feat = feat + self.conv_body(self.body(feat))
            feat = self.lrelu(self.conv_up1(F.interpolate(feat, scale_factor=2, mode='nearest')))
            feat = self.lrelu(self.conv_up2(F.interpolate(feat, scale_factor=2, mode='nearest')))
            return self.conv_last(self.lrelu(self.conv_hr(feat)))

    return RRDBNet(num_block)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def load_model():
    import torch

    url, want, nb = MODELS[MODEL]
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / url.rsplit('/', 1)[1]
    if not path.exists():
        print(f'tải trọng số {path.name} ...')
        urllib.request.urlretrieve(url, path)
    got = sha256(path)
    if got != want:
        sys.exit(f'LỖI: SHA-256 {path.name} = {got}, cần {want} - từ chối nạp')
    state = torch.load(path, map_location='cpu', weights_only=True)
    state = state.get('params_ema', state.get('params', state))
    net = build_net(nb)
    net.load_state_dict(state, strict=True)
    net.eval()
    torch.set_num_threads(max(1, os.cpu_count() or 1))
    return net


_NET = None


def upscale4(rgb: np.ndarray) -> np.ndarray:
    """rgb float32 HxWx3 0..1 -> 4H x 4W x 3. Đệm phản chiếu 8px để mép không méo."""
    import torch

    global _NET
    if _NET is None:
        _NET = load_model()
    pad = 8
    x = np.pad(rgb, ((pad, pad), (pad, pad), (0, 0)), mode='reflect')
    t = torch.from_numpy(x.transpose(2, 0, 1).copy()).unsqueeze(0)
    with torch.inference_mode():
        y = _NET(t).squeeze(0).clamp_(0, 1).numpy().transpose(1, 2, 0)
    return y[pad * 4 : -pad * 4, pad * 4 : -pad * 4]


# ---------------------------------------------------------------- tách nền
def unblend(rgb: np.ndarray, bg: np.ndarray, t_core: float, t_glow: float, hole_t: float, hole_min: int) -> np.ndarray:
    """Tách nền màu đơn `bg`, GIỮ quầng sáng: vùng nền (nối mép ảnh, khác bg < t_core) nhận alpha theo độ lệch
    so với bg rồi khử pha trộn F = (C - (1-a)·bg)/a. Lỗ kín gần như đúng màu nền (lòng chữ) diện tích >= hole_min
    cũng là nền."""
    d = np.abs(rgb - bg).max(axis=2)
    lab, _ = ndimage.label(d < t_core)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    outside = np.isin(lab, border[border > 0])
    hl, n = ndimage.label(d < hole_t)
    if n:
        sizes = ndimage.sum(np.ones_like(d), hl, index=np.arange(1, n + 1))
        big = np.arange(1, n + 1)[sizes >= hole_min]
        outside |= np.isin(hl, big)
    a = np.ones_like(d)
    a[outside] = np.clip((d[outside] - 0.012) / (t_glow - 0.012), 0, 1)
    safe = np.maximum(a, 1e-4)[..., None]
    fg = np.clip((rgb - (1 - a[..., None]) * bg) / safe, 0, 1)
    fg[a == 0] = 0
    return np.dstack([fg, a])


def keep_main(rgba: np.ndarray, min_frac: float = 0.002) -> np.ndarray:
    """Bỏ đốm/vết rời (dấu ✦, nhiễu JPEG): giữ các thành phần alpha > 0 có diện tích >= min_frac thành phần lớn nhất."""
    lab, n = ndimage.label(rgba[..., 3] > 0.02, structure=np.ones((3, 3)))
    if n <= 1:
        return rgba
    sizes = ndimage.sum(np.ones(lab.shape), lab, index=np.arange(1, n + 1))
    keep = np.isin(lab, np.arange(1, n + 1)[sizes >= sizes.max() * min_frac])
    out = rgba.copy()
    out[~keep] = 0
    return out


def trim(rgba: np.ndarray, pad: int, square: bool) -> np.ndarray:
    ys, xs = np.nonzero(rgba[..., 3] > 0.01)
    c = rgba[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]
    h, w = c.shape[:2]
    H, W = (max(h, w),) * 2 if square else (h, w)
    H, W = H + 2 * pad, W + 2 * pad
    out = np.zeros((H, W, 4), np.float32)
    y0, x0 = (H - h) // 2, (W - w) // 2
    out[y0 : y0 + h, x0 : x0 + w] = c
    return out


def superellipse_fit(core: np.ndarray, ss: int = 4) -> np.ndarray:
    """Khớp |x/a|^n + |y/b|^n <= 1 vào mặt nạ nhị phân: biên trái/phải/trên/dưới lấy TRUNG VỊ trên dải giữa 25-75%
    (bền với u lồi cục bộ), số mũ n chọn theo sai khác XOR nhỏ nhất; trả alpha khử răng cưa bằng siêu lấy mẫu ss x ss."""
    h, w = core.shape
    rows = [np.nonzero(core[y])[0] for y in range(int(h * 0.25), int(h * 0.75))]
    cols = [np.nonzero(core[:, x])[0] for x in range(int(w * 0.25), int(w * 0.75))]
    left = np.median([r[0] for r in rows if len(r)]); right = np.median([r[-1] for r in rows if len(r)])
    top = np.median([c[0] for c in cols if len(c)]); bottom = np.median([c[-1] for c in cols if len(c)])
    # Icon nền tảng là hình VUÔNG: lấy bán kính theo chiều ngang (ảnh gốc có bóng đổ ở đáy làm cao giả), neo mép trên.
    a = b = (right - left) / 2 + 0.5
    cx, cy = (left + right) / 2, top - 0.5 + b
    yy, xx = np.mgrid[0:h, 0:w]
    best = min(
        (np.count_nonzero(((np.abs((xx - cx) / a) ** n + np.abs((yy - cy) / b) ** n) <= 1) ^ core), n)
        for n in np.arange(3.0, 10.01, 0.25)
    )[1]
    o = (np.arange(ss) + 0.5) / ss - 0.5
    acc = np.zeros((h, w), np.float32)
    for dy in o:
        for dx in o:
            acc += (np.abs((xx + dx - cx) / a) ** best + np.abs((yy + dy - cy) / b) ** best) <= 1
    print(f'  squircle: n={best:.2f}, {2 * a:.0f}x{2 * b:.0f}px')
    return acc / (ss * ss)


def squircle_1024(sqm: np.ndarray, size: int = 1024, pad: int = 0) -> np.ndarray:
    """Squircle master đủ 1024px cho icon nền tảng: nền (họa tiết mạch mờ) phóng Lanczos, rồi ghép đè cú master
    (hình 3, 820px, nét sắc) đúng vị trí/cỡ của cú trong hình 4 - tìm bằng tương quan chéo chuẩn hoá trên lưới
    cỡ x độ lệch. Tránh cú bị nhoè khi phóng squircle 746px lên 1024px."""
    S = Image.fromarray(np.round(sqm * 255).astype(np.uint8), 'RGBA').resize((size, size), Image.LANCZOS)
    sq = np.asarray(S, np.float32) / 255.0
    mk = trim(np.asarray(Image.open(MASTER / 'tsumind-mark.png'), np.float32) / 255.0, 0, True)
    lum = lambda x: x[..., 0] * 0.2126 + x[..., 1] * 0.7152 + x[..., 2] * 0.0722
    q = 4
    base = lum(sq[::q, ::q])
    best = (-2.0, 0, 0, 0)
    for frac in np.arange(0.70, 0.95, 0.005):
        d = int(round(size * frac / q))
        m = np.asarray(Image.fromarray(np.round(mk * 255).astype(np.uint8), 'RGBA').resize((d, d), Image.LANCZOS), np.float32) / 255.0
        w = m[..., 3] > 0.9
        t = lum(m)[w]
        t = (t - t.mean()) / (t.std() + 1e-6)
        c0 = (base.shape[0] - d) // 2
        for oy in range(c0 - 6, c0 + 7):
            for ox in range(c0 - 6, c0 + 7):
                v = base[oy : oy + d, ox : ox + d][w]
                r = float(((v - v.mean()) / (v.std() + 1e-6) * t).mean())
                if r > best[0]:
                    best = (r, d * q, oy * q, ox * q)
    r, d, oy, ox = best
    print(f'  squircle: cú master ghép cỡ {d}px tại ({ox},{oy}), tương quan {r:.3f}')
    if r < 0.5:
        sys.exit('LỖI: không khớp được cú master vào squircle (tương quan < 0.5) - kiểm lại hình 3/4')
    m = np.asarray(Image.fromarray(np.round(mk * 255).astype(np.uint8), 'RGBA').resize((d, d), Image.LANCZOS), np.float32) / 255.0
    out = sq.copy()
    a = m[..., 3:4]
    region = out[oy : oy + d, ox : ox + d]
    region[..., :3] = m[..., :3] * a + region[..., :3] * (1 - a)
    return out


def load(name: str) -> np.ndarray:
    im = Image.open(ORIG / name)
    im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
    return np.asarray(im, np.float32) / 255.0


def save(arr: np.ndarray, name: str) -> None:
    MASTER.mkdir(parents=True, exist_ok=True)
    img = Image.fromarray(np.round(np.clip(arr, 0, 1) * 255).astype(np.uint8), 'RGBA')
    img.save(MASTER / name, optimize=True)
    print(f'  {name}: {img.width}x{img.height}')


def border_color(rgb: np.ndarray) -> np.ndarray:
    e = np.concatenate([rgb[:4].reshape(-1, 3), rgb[-4:].reshape(-1, 3), rgb[:, :4].reshape(-1, 3), rgb[:, -4:].reshape(-1, 3)])
    return np.median(e, axis=0)


def main() -> None:
    print(f'Mô hình phóng to: Real-ESRGAN {MODEL}')

    # 0 -> huy hiệu: alpha thật sẵn có; chỉ xoá ✦ (thành phần rời) và cắt sát.
    # Dấu ✦ (alpha ~0,3) chạm viền mờ của huy hiệu nên lọc thành phần rời thường bỏ sót: lấy THÂN = khối alpha > 0,5
    # lớn nhất, chỉ giữ điểm ảnh cách thân <= 3px (đủ cho viền khử răng cưa), mọi thứ xa hơn bị xoá.
    e = load('0-logo-tsumind.png')
    e[..., 3][e[..., 3] < 8 / 255] = 0
    lab, n = ndimage.label(e[..., 3] > 0.5)
    body = lab == (1 + int(np.argmax(ndimage.sum(np.ones(lab.shape), lab, index=np.arange(1, n + 1)))))
    near = ndimage.binary_dilation(ndimage.binary_fill_holes(body), iterations=3)
    e[~near] = 0
    save(trim(e, 8, True), 'tsumind-emblem.png')

    # 3 -> biểu tượng cú trong vòng tròn, nền đen.
    m = load('3-brand-mark.jpg')[..., :3]
    m4 = upscale4(m)
    save(trim(keep_main(unblend(m4, np.zeros(3, np.float32), 0.10, 0.30, 0.03, 4000)), 12, True), 'tsumind-mark.png')

    # 2 -> logo ngang. Thân cú trong hình 2 có mảng gần đen trùng màu nền (tách nền sẽ khoét thủng), nên chỉ lấy
    # PHẦN CHỮ từ hình 2; phần cú ghép lại bằng master của hình 3 (cùng thiết kế, nét sạch hơn) đúng vị trí, cỡ.
    lk = load('2-horizontal-lockup.jpg')[..., :3]
    lk4 = trim(keep_main(unblend(upscale4(lk), np.zeros(3, np.float32), 0.10, 0.30, 0.03, 1500)), 0, False)
    cols = lk4[..., 3].max(axis=0) > 0.05
    gaps, x, w = [], 0, len(cols)
    while x < w:
        if not cols[x]:
            s0 = x
            while x < w and not cols[x]:
                x += 1
            if s0 > 0 and x < w:
                gaps.append((x - s0, s0, x))
        x += 1
    if not gaps:
        sys.exit('LỖI: không tìm được khoảng trống giữa cú và chữ ở hình 2')
    _, gap_l, gap_r = max(gaps)
    word = trim(lk4[:, gap_r:], 0, False)
    save(trim(word, 12, False), 'tsumind-wordmark.png')
    mark_h = int(np.ptp(np.nonzero(lk4[:, :gap_l, 3].max(axis=1) > 0.05)[0])) + 1
    mk = Image.open(MASTER / 'tsumind-mark.png')
    inner = trim(np.asarray(mk, np.float32) / 255.0, 0, True)
    mk_small = Image.fromarray(np.round(inner * 255).astype(np.uint8), 'RGBA').resize((mark_h, mark_h), Image.LANCZOS)
    H = max(mark_h, word.shape[0])
    canvas = np.zeros((H, mark_h + (gap_r - gap_l) + word.shape[1], 4), np.float32)
    canvas[(H - mark_h) // 2 : (H - mark_h) // 2 + mark_h, :mark_h] = np.asarray(mk_small, np.float32) / 255.0
    canvas[(H - word.shape[0]) // 2 : (H - word.shape[0]) // 2 + word.shape[0], mark_h + gap_r - gap_l :] = word
    save(trim(canvas, 12, False), 'tsumind-lockup.png')
    # Bản cho NỀN SÁNG: chữ bạc kim chỉ đọc được trên nền tối - đổi phần chữ sang Midnight Navy #0A1B3D, giữ alpha.
    light = canvas.copy()
    light[:, mark_h:, :3] = np.array([10, 27, 61], np.float32) / 255.0
    save(trim(light, 12, False), 'tsumind-lockup-light.png')
    wl = word.copy()
    wl[..., :3] = np.array([10, 27, 61], np.float32) / 255.0
    save(trim(wl, 12, False), 'tsumind-wordmark-light.png')

    # 4 -> icon squircle. Mặt nạ HÌNH HỌC: ngưỡng khác nền -> lấp lỗ -> mở hình thái -> giữ khối lớn nhất ->
    # KHỚP SIÊU ELIP (dạng squircle của iOS/macOS) rồi vẽ lại mặt nạ siêu lấy mẫu - bóng đổ, u lồi của ảnh gốc biến mất.
    sq = load('4-app-icon-squircle.jpg')[..., :3]
    sq4 = upscale4(sq)
    bg = border_color(sq4)
    core = np.abs(sq4 - bg).max(axis=2) > 0.07
    core = ndimage.binary_fill_holes(core)
    yy, xx = np.mgrid[-6:7, -6:7]
    disk = xx**2 + yy**2 <= 36
    core = ndimage.binary_opening(core, structure=disk)
    lab, n = ndimage.label(core)
    if n > 1:
        sizes = ndimage.sum(core, lab, index=np.arange(1, n + 1))
        core = lab == (1 + int(np.argmax(sizes)))
    core = ndimage.binary_fill_holes(core)
    alpha = superellipse_fit(core)
    sqm = trim(np.dstack([sq4, alpha]), 0, True)
    save(squircle_1024(sqm), 'tsumind-squircle.png')

if __name__ == '__main__':
    main()
