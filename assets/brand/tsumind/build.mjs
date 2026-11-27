#!/usr/bin/env node
// build.mjs - dây chuyền sinh bộ nhận diện TsuMIND từ ĐÚNG MỘT bộ nguồn.
//
// Nguồn (sửa ở đây, không sửa dist/):
//   source/tsumind-emblem-source.png  ảnh gốc huy hiệu (nền xám giả + watermark - script tự xoá)
//   svg/tsumind-*.svg                 dấu hiệu thu gọn, wordmark, logo ngang (vector vẽ tay)
//
// Lệnh:
//   npm ci && node build.mjs          sinh lại toàn bộ dist/ + MANIFEST.json
//   node build.mjs --check            KHÔNG cần sharp: đối chiếu SHA-256 nguồn + dist với MANIFEST.json
//                                     (chạy trong CI - bắt sửa tay dist/ hoặc đổi nguồn mà quên sinh lại)
//
// Quy chuẩn: docs/BRAND_GUIDELINES.md (TsuMIND) + docs/BRAND_ASSETS.md mục 12 (bộ tài sản bắt buộc).
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, mkdirSync, readdirSync, statSync, rmSync, existsSync } from 'node:fs';
import { join, relative, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = dirname(fileURLToPath(import.meta.url));
const SRC_PNG = join(ROOT, 'source/tsumind-emblem-source.png');
const SVG_DIR = join(ROOT, 'svg');
const DIST = join(ROOT, 'dist');
const MANIFEST = join(ROOT, 'MANIFEST.json');

// Màu nền ô icon nền đặc (apple-touch, maskable, icon app) = Ink Navy của bảng màu thương hiệu.
const TILE_BG = '#021023';
const PAGE_BG_DARK = '#0A0A0A';

const sha = (buf) => createHash('sha256').update(buf).digest('hex');
const walk = (d) =>
  readdirSync(d).flatMap((n) => {
    const p = join(d, n);
    return statSync(p).isDirectory() ? walk(p) : [p];
  });
const sources = () => [SRC_PNG, ...walk(SVG_DIR).filter((f) => f.endsWith('.svg'))].sort();

function check() {
  if (!existsSync(MANIFEST)) {
    console.error('THIẾU MANIFEST.json - chạy: npm ci && node build.mjs');
    process.exit(1);
  }
  const m = JSON.parse(readFileSync(MANIFEST, 'utf8'));
  const errs = [];
  for (const [rel, h] of Object.entries({ ...m.sources, ...m.outputs })) {
    const p = join(ROOT, rel);
    if (!existsSync(p)) errs.push(`thiếu ${rel}`);
    else if (sha(readFileSync(p)) !== h) errs.push(`lệch ${rel}`);
  }
  const listed = new Set(Object.keys(m.outputs));
  for (const f of existsSync(DIST) ? walk(DIST) : []) {
    const rel = relative(ROOT, f);
    if (!listed.has(rel)) errs.push(`thừa ${rel} (không do build.mjs sinh)`);
  }
  if (errs.length) {
    console.error('Bộ nhận diện TsuMIND LỆCH nguồn:\n  ' + errs.join('\n  '));
    console.error('Sửa nguồn ở source/ hoặc svg/, rồi: npm ci && node build.mjs');
    process.exit(1);
  }
  console.log(`OK - ${Object.keys(m.sources).length} nguồn, ${listed.size} tệp sinh khớp MANIFEST.json`);
}

// Tách nền giả: vùng xám ít bão hoà NỐI LIỀN mép ảnh (flood fill từ mép), bỏ đảo nhỏ, mép mềm 1px.
// Watermark ✦ góc dưới nằm trong vùng nền nên bị xoá cùng.
async function cutEmblem(sharp) {
  const { data, info } = await sharp(SRC_PNG).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  const { width: w, height: h } = info;
  const n = w * h;
  const bgish = new Uint8Array(n);
  for (let i = 0; i < n; i++) {
    const r = data[i * 3], g = data[i * 3 + 1], b = data[i * 3 + 2];
    const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
    const sat = mx ? (mx - mn) / mx : 0;
    const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    bgish[i] = sat < 0.16 && lum > 95 ? 1 : 0;
  }
  const bg = new Uint8Array(n);
  const q = new Int32Array(n);
  let qh = 0, qt = 0;
  const push = (i) => {
    if (bgish[i] && !bg[i]) { bg[i] = 1; q[qt++] = i; }
  };
  for (let x = 0; x < w; x++) { push(x); push((h - 1) * w + x); }
  for (let y = 0; y < h; y++) { push(y * w); push(y * w + w - 1); }
  while (qh < qt) {
    const i = q[qh++], x = i % w, y = (i / w) | 0;
    if (x > 0) push(i - 1);
    if (x < w - 1) push(i + 1);
    if (y > 0) push(i - w);
    if (y < h - 1) push(i + w);
  }
  // Đóng hình thái 2 vòng (giãn rồi co, kernel chữ thập, mép coi như nền): nối các vệt xám tối
  // của nền giả vào vùng nền để chúng không thành đảo tiền cảnh lớn.
  const morph = (m, grow) => {
    const r = new Uint8Array(n);
    for (let y = 0; y < h; y++)
      for (let x = 0; x < w; x++) {
        const i = y * w + x;
        const nb = [m[i], x > 0 ? m[i - 1] : 1, x < w - 1 ? m[i + 1] : 1, y > 0 ? m[i - w] : 1, y < h - 1 ? m[i + w] : 1];
        r[i] = grow ? (nb.some((v) => v) ? 1 : 0) : nb.every((v) => v) ? 1 : 0;
      }
    return r;
  };
  let closed = morph(morph(bg, true), true);
  closed = morph(morph(closed, false), false);
  bg.set(closed);
  // Bỏ đảo tiền cảnh nhỏ (đốm nhiễu trong nền) < 5000 px.
  const lab = new Int32Array(n).fill(-1);
  for (let s = 0; s < n; s++) {
    if (bg[s] || lab[s] !== -1) continue;
    qh = 0; qt = 0; q[qt++] = s; lab[s] = s;
    while (qh < qt) {
      const i = q[qh++], x = i % w, y = (i / w) | 0;
      for (const j of [x > 0 ? i - 1 : -1, x < w - 1 ? i + 1 : -1, y > 0 ? i - w : -1, y < h - 1 ? i + w : -1]) {
        if (j >= 0 && !bg[j] && lab[j] === -1) { lab[j] = s; q[qt++] = j; }
      }
    }
    if (qt < 5000) for (let k = 0; k < qt; k++) bg[q[k]] = 1;
  }
  const mask = Buffer.alloc(n);
  for (let i = 0; i < n; i++) mask[i] = bg[i] ? 0 : 255;
  const soft = await sharp(mask, { raw: { width: w, height: h, channels: 1 } }).blur(0.7).extractChannel(0).raw().toBuffer();
  const rgba = Buffer.alloc(n * 4);
  for (let i = 0; i < n; i++) {
    rgba[i * 4] = data[i * 3]; rgba[i * 4 + 1] = data[i * 3 + 1]; rgba[i * 4 + 2] = data[i * 3 + 2];
    rgba[i * 4 + 3] = soft[i];
  }
  // Cắt sát khung + đệm 8px, đặt vào ô vuông trong suốt.
  const trimmed = await sharp(rgba, { raw: { width: w, height: h, channels: 4 } })
    .trim({ threshold: 1 })
    .extend({ top: 8, bottom: 8, left: 8, right: 8, background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .png()
    .toBuffer({ resolveWithObject: true });
  const side = Math.max(trimmed.info.width, trimmed.info.height);
  return sharp(trimmed.data)
    .resize(side, side, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .png()
    .toBuffer();
}

async function build() {
  const sharp = (await import('sharp')).default;
  const pngToIco = (await import('png-to-ico')).default;
  rmSync(DIST, { recursive: true, force: true });
  const out = (rel, buf) => {
    const p = join(DIST, rel);
    mkdirSync(dirname(p), { recursive: true });
    writeFileSync(p, buf);
  };
  const png = (s) => s.png({ compressionLevel: 9, adaptiveFiltering: true, palette: false });
  const svg = (name) => readFileSync(join(SVG_DIR, name));
  const raster = (name, size) =>
    png(sharp(svg(name), { density: Math.max(72, Math.ceil((size / 256) * 72 * 1.5)) }).resize(size, size)).toBuffer();

  // 1. Huy hiệu đầy đủ (cú + chữ) - nền trong suốt, AVIF → WebP → PNG.
  const emblem = await cutEmblem(sharp);
  for (const s of [1024, 512, 256, 192, 128, 96, 48]) {
    const r = sharp(emblem).resize(s, s, { kernel: 'lanczos3' });
    out(`emblem/tsumind-emblem-${s}.png`, await png(r.clone()).toBuffer());
    out(`emblem/tsumind-emblem-${s}.webp`, await r.clone().webp({ quality: 90, alphaQuality: 100, effort: 6 }).toBuffer());
    out(`emblem/tsumind-emblem-${s}.avif`, await r.clone().avif({ quality: 70, effort: 4 }).toBuffer());
  }

  // 2. SVG giao diện (đã tối giản sẵn - chép nguyên).
  for (const f of readdirSync(SVG_DIR).filter((f) => f.endsWith('.svg'))) out(`svg/${f}`, svg(f));

  // 3. Dấu hiệu thu gọn PNG (khay hệ thống, Linux hicolor, tài liệu).
  for (const s of [16, 24, 32, 48, 64, 128, 256, 512, 1024]) out(`mark/tsumind-mark-${s}.png`, await raster('tsumind-mark.svg', s));

  // 4. Favicon + PWA (BRAND_ASSETS mục 12.1).
  out('favicon/favicon.svg', svg('tsumind-mark.svg'));
  const icoLayers = await Promise.all([16, 24, 32, 48, 64, 128, 256].map((s) => raster('tsumind-mark.svg', s)));
  out('favicon/favicon.ico', await pngToIco(icoLayers));
  out('favicon/favicon-96x96.png', await raster('tsumind-mark.svg', 96));
  const tile = async (size, inner) =>
    png(
      sharp({ create: { width: size, height: size, channels: 4, background: TILE_BG } }).composite([
        { input: await raster('tsumind-mark.svg', Math.round(size * inner)), gravity: 'center' },
      ]),
    ).toBuffer();
  out('favicon/apple-touch-icon.png', await tile(180, 0.84));
  for (const s of [192, 512]) {
    out(`favicon/android-chrome-${s}x${s}.png`, await raster('tsumind-mark.svg', s));
    out(`favicon/maskable-${s}x${s}.png`, await tile(s, 0.72)); // vùng an toàn maskable = 80% đường kính
  }

  // 5. Icon ứng dụng (ô nền đặc theo quy ước hệ điều hành).
  const appLayers = await Promise.all([16, 24, 32, 48, 64, 128, 256].map((s) => tile(s, 0.9)));
  out('app/tsumind-app.ico', await pngToIco(appLayers));
  for (const s of [256, 512, 1024]) out(`app/tsumind-app-${s}.png`, await tile(s, 0.86));

  // 6. Ảnh chia sẻ + ảnh đại diện mạng xã hội/GitHub.
  const og = sharp({ create: { width: 1200, height: 630, channels: 4, background: PAGE_BG_DARK } }).composite([
    { input: await sharp(emblem).resize(470, 470).png().toBuffer(), left: 70, top: 80 },
    { input: await sharp(svg('tsumind-wordmark.svg'), { density: 300 }).resize({ width: 560 }).png().toBuffer(), left: 590, top: 262 },
  ]);
  out('social/og-image.png', await png(og).toBuffer());
  out('social/avatar-500.png', await tile(500, 0.86));
  out(
    'social/avatar-emblem-500.png',
    await png(
      sharp({ create: { width: 500, height: 500, channels: 4, background: PAGE_BG_DARK } }).composite([
        { input: await sharp(emblem).resize(460, 460).png().toBuffer(), gravity: 'center' },
      ]),
    ).toBuffer(),
  );

  const manifest = { generator: 'assets/brand/tsumind/build.mjs', sources: {}, outputs: {} };
  for (const f of sources()) manifest.sources[relative(ROOT, f)] = sha(readFileSync(f));
  for (const f of walk(DIST).sort()) manifest.outputs[relative(ROOT, f)] = sha(readFileSync(f));
  writeFileSync(MANIFEST, JSON.stringify(manifest, null, 2) + '\n');
  console.log(`Đã sinh ${Object.keys(manifest.outputs).length} tệp vào dist/`);
}

if (process.argv.includes('--check')) check();
else await build();
