#!/usr/bin/env node
// build.mjs - dây chuyền sinh bộ nhận diện TsuMIND từ ĐÚNG MỘT bộ nguồn (bộ logo chính thức chủ dự án giao 27/11/2026).
//
// Nguồn (sửa ở đây, không sửa dist/):
//   source/tsumind-logo-primary.png     huy hiệu chính (cú + dải chữ), nền trong suốt, 1024x1024
//   source/tsumind-symbol.png           biểu tượng thu gọn (cú, không chữ), nền trong suốt, 1024x667
//   source/tsumind-wordmark.png         dải chữ, nền trong suốt, 995x223
//   source/tsumind-logo-horizontal.png  logo ngang (cú + dải chữ), nền trong suốt, 2141x620
//   source/tsumind-app-icon-1024.png    biểu tượng ứng dụng, nền Midnight Navy liền, 1024x1024
//   source/tsumind-tagline-vi.svg       tuyên ngôn "Công cụ thông minh cho mọi nền tảng" (path từ Be Vietnam Pro)
//   source/tsumind-domain.svg           "tsumind.com" (path)
//
// Lệnh:
//   npm ci && node build.mjs     sinh lại toàn bộ dist/ + MANIFEST.json
//   node build.mjs --check       KHÔNG cần sharp: đối chiếu SHA-256 nguồn + dist với MANIFEST.json (CI)
//
// Nguyên tắc: chỉ THU NHỎ, không phóng to quá kích thước nguồn; ảnh giao diện xuất AVIF → WebP → PNG để
// <picture>/srcset chọn bản sắc nét nhất cho mật độ điểm ảnh 1x/2x/3x. Ảnh vẽ chi tiết KHÔNG vector hoá tự động
// (thử vtracer 27/11/2026: mất viền đậm và độ sâu - xem BRAND_ASSETS.md mục 16).
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, mkdirSync, readdirSync, statSync, rmSync, existsSync } from 'node:fs';
import { join, relative, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = dirname(fileURLToPath(import.meta.url));
const SRC = join(ROOT, 'source');
const DIST = join(ROOT, 'dist');
const MANIFEST = join(ROOT, 'MANIFEST.json');
const src = (f) => join(SRC, f);

// Hệ màu chuẩn (Sổ tay nhận diện TSUMIND mục 5).
const MIDNIGHT_NAVY = '#0A1B3D';
const DEEP_CIRCUIT_BLUE = '#13408A';

const sha = (buf) => createHash('sha256').update(buf).digest('hex');
const walk = (d) =>
  existsSync(d)
    ? readdirSync(d).flatMap((n) => {
        const p = join(d, n);
        return statSync(p).isDirectory() ? walk(p) : [p];
      })
    : [];

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
  const listed = new Set([...Object.keys(m.outputs), ...Object.keys(m.sources)]);
  for (const f of [...walk(DIST), ...walk(SRC)]) {
    const rel = relative(ROOT, f);
    if (!listed.has(rel)) errs.push(`thừa ${rel} (chưa ghi vào MANIFEST - chạy lại build.mjs)`);
  }
  if (errs.length) {
    console.error('Bộ nhận diện TsuMIND LỆCH nguồn:\n  ' + errs.join('\n  '));
    console.error('Sửa nguồn ở source/, rồi: npm ci && node build.mjs');
    process.exit(1);
  }
  console.log(`OK - ${Object.keys(m.sources).length} nguồn, ${Object.keys(m.outputs).length} tệp sinh khớp MANIFEST.json`);
}

// Xoá đốm alpha mồ côi (cụm điểm ảnh không trong suốt < minArea, tách rời hình chính) - ảnh nguồn có vài đốm 1-3px.
async function despeckle(sharp, file, minArea = 400) {
  const { data, info } = await sharp(file).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const { width: w, height: h, channels } = info;
  if (channels !== 4) throw new Error(`despeckle: cần 4 kênh, nhận ${channels}`);
  const n = w * h;
  const seen = new Uint8Array(n);
  const q = new Int32Array(n);
  for (let s = 0; s < n; s++) {
    if (seen[s] || data[s * 4 + 3] === 0) continue;
    let qh = 0, qt = 0;
    q[qt++] = s; seen[s] = 1;
    while (qh < qt) {
      const i = q[qh++], x = i % w, y = (i / w) | 0;
      for (let dy = -1; dy <= 1; dy++)
        for (let dx = -1; dx <= 1; dx++) {
          const nx = x + dx, ny = y + dy;
          if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
          const j = ny * w + nx;
          if (!seen[j] && data[j * 4 + 3] !== 0) { seen[j] = 1; q[qt++] = j; }
        }
    }
    if (qt < minArea) for (let k = 0; k < qt; k++) data[q[k] * 4 + 3] = 0;
  }
  return sharp(data, { raw: { width: w, height: h, channels: 4 } }).png().toBuffer();
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
  const png = (s) => s.png({ compressionLevel: 9, adaptiveFiltering: true });
  // Ba định dạng cho giao diện web: AVIF (nhỏ nhất) → WebP → PNG (dự phòng).
  const triple = async (base, img) => {
    out(`${base}.avif`, await img.clone().avif({ quality: 72, effort: 4 }).toBuffer());
    out(`${base}.webp`, await img.clone().webp({ quality: 90, alphaQuality: 100, effort: 6 }).toBuffer());
    out(`${base}.png`, await png(img.clone()).toBuffer());
  };
  const fit = (buf, w, h) =>
    sharp(buf).resize(w, h, { kernel: 'lanczos3', fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } });

  const primary = await despeckle(sharp, src('tsumind-logo-primary.png'));
  const symbol = await despeckle(sharp, src('tsumind-symbol.png'));
  const wordmark = await despeckle(sharp, src('tsumind-wordmark.png'));
  const horizontal = await despeckle(sharp, src('tsumind-logo-horizontal.png'));
  const appIcon = readFileSync(src('tsumind-app-icon-1024.png'));

  // 1. Logo chính (huy hiệu + dải chữ) - vuông.
  for (const s of [1024, 512, 384, 256, 192, 128]) await triple(`logo/tsumind-logo-primary-${s}`, fit(primary, s, s));
  // 2. Biểu tượng thu gọn (không chữ) - tỷ lệ 1024:667, đặt tên theo chiều rộng.
  for (const wd of [1024, 512, 256, 128, 64]) await triple(`symbol/tsumind-symbol-${wd}w`, fit(symbol, wd));
  // 3. Dải chữ.
  for (const wd of [995, 480, 240]) await triple(`wordmark/tsumind-wordmark-${wd}w`, fit(wordmark, wd));
  // 4. Logo ngang - header website cao 28-48px ⇒ bản 360/720/1440 phủ 1x-3x.
  for (const wd of [2141, 1440, 720, 360]) await triple(`horizontal/tsumind-logo-horizontal-${wd}w`, fit(horizontal, wd));

  // 5. Favicon + PWA từ biểu tượng ứng dụng (đã giản lược, nền liền - đọc rõ ở 16px).
  const icon = (s) => png(sharp(appIcon).resize(s, s, { kernel: 'lanczos3' })).toBuffer();
  const icoLayers = await Promise.all([16, 24, 32, 48, 64, 128, 256].map(icon));
  out('favicon/favicon.ico', await pngToIco(icoLayers));
  for (const s of [16, 32, 48, 96]) out(`favicon/favicon-${s}x${s}.png`, await icon(s));
  out('favicon/apple-touch-icon.png', await icon(180));
  for (const s of [192, 512]) {
    out(`favicon/android-chrome-${s}x${s}.png`, await icon(s));
    // maskable: thu cú vào vùng an toàn 80%, viền kéo dài bằng phản chiếu mép nền để không lộ khung.
    const inner = Math.round(s * 0.8), pad = Math.floor((s - inner) / 2);
    const small = await sharp(appIcon).resize(inner, inner, { kernel: 'lanczos3' }).png().toBuffer();
    out(
      `favicon/maskable-${s}x${s}.png`,
      await png(
        sharp(small).extend({ top: pad, left: pad, bottom: s - inner - pad, right: s - inner - pad, extendWith: 'mirror' }),
      ).toBuffer(),
    );
  }

  // 6. Biểu tượng ứng dụng theo nền tảng.
  out('app-icon/tsumind-app.ico', await pngToIco(icoLayers));
  for (const s of [1024, 512, 256]) out(`app-icon/tsumind-app-icon-${s}.png`, await icon(s));
  out('app-icon/google-play-icon-512.png', await icon(512));
  // Android adaptive icon: lớp nền liền Midnight Navy + lớp trước là biểu tượng cú trong vùng an toàn 66/108.
  out(
    'app-icon/android-adaptive-background-1024.png',
    await png(sharp({ create: { width: 1024, height: 1024, channels: 4, background: MIDNIGHT_NAVY } })).toBuffer(),
  );
  out(
    'app-icon/android-adaptive-foreground-1024.png',
    await png(
      sharp({ create: { width: 1024, height: 1024, channels: 4, background: { r: 0, g: 0, b: 0, alpha: 0 } } }).composite([
        { input: await fit(symbol, 620).png().toBuffer(), gravity: 'center' },
      ]),
    ).toBuffer(),
  );

  // 7. Ảnh chia sẻ (Open Graph 1200x630) + ảnh đại diện.
  const bg = (w, h) =>
    Buffer.from(
      `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><defs>` +
        `<radialGradient id="g" cx="0.3" cy="0.45" r="0.9"><stop offset="0" stop-color="${DEEP_CIRCUIT_BLUE}"/>` +
        `<stop offset="0.55" stop-color="${MIDNIGHT_NAVY}"/><stop offset="1" stop-color="#050D20"/></radialGradient></defs>` +
        `<rect width="100%" height="100%" fill="url(#g)"/></svg>`,
    );
  const svgImg = (f, wd) => sharp(readFileSync(src(f)), { density: 300 }).resize({ width: wd }).png().toBuffer();
  const ogPng = await png(
    sharp(bg(1200, 630)).composite([
      { input: await fit(primary, 500, 500).png().toBuffer(), left: 64, top: 65 },
      { input: await fit(wordmark, 560).png().toBuffer(), left: 600, top: 198 },
      { input: await svgImg('tsumind-tagline-vi.svg', 560), left: 604, top: 350 },
      { input: await svgImg('tsumind-domain.svg', 190), left: 604, top: 430 },
    ]),
  ).toBuffer();
  out('social/og-image-1200x630.png', ogPng);
  out('social/og-image-1200x630.webp', await sharp(ogPng).webp({ quality: 90 }).toBuffer());
  out('social/avatar-app-icon-500.png', await icon(500));
  out(
    'social/avatar-logo-primary-500.png',
    await png(
      sharp(bg(500, 500)).composite([{ input: await fit(primary, 450, 450).png().toBuffer(), gravity: 'center' }]),
    ).toBuffer(),
  );

  const manifest = { generator: 'assets/brand/tsumind/build.mjs', sources: {}, outputs: {} };
  for (const f of walk(SRC).sort()) manifest.sources[relative(ROOT, f)] = sha(readFileSync(f));
  for (const f of walk(DIST).sort()) manifest.outputs[relative(ROOT, f)] = sha(readFileSync(f));
  writeFileSync(MANIFEST, JSON.stringify(manifest, null, 2) + '\n');
  console.log(`Đã sinh ${Object.keys(manifest.outputs).length} tệp vào dist/`);
}

if (process.argv.includes('--check')) check();
else await build();
