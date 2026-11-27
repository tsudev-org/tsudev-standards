#!/usr/bin/env node
// build.mjs - dây chuyền sinh bộ nhận diện TsuMIND từ ĐÚNG MỘT bộ nguồn.
//
// Ba tầng nguồn (sửa ở đây, không sửa dist/):
//   source/original/  5 hình chủ dự án giao 28/11/2026 - BẤT BIẾN, giữ làm bằng chứng gốc
//   source/master/    PNG RGBA nền trong suốt sinh từ original bằng tools/make_masters.py (Real-ESRGAN + tách nền)
//                     tsumind-emblem (huy hiệu + chữ), tsumind-mark (cú trong vòng tròn), tsumind-lockup(-light)
//                     (logo ngang), tsumind-wordmark(-light), tsumind-squircle (icon 1024)
//   source/text/      tuyên ngôn + tên miền dạng path SVG (ảnh chia sẻ)
//
// Lệnh:
//   npm ci && node build.mjs     sinh lại toàn bộ dist/ + MANIFEST.json (~1 phút)
//   node build.mjs --check       KHÔNG cần sharp: đối chiếu SHA-256 nguồn + dist với MANIFEST.json (CI)
//
// Nguyên tắc: chỉ THU NHỎ từ master (không phóng to); ảnh giao diện xuất AVIF → WebP → PNG cho <picture>/srcset
// 1x/2x/3x; cỡ nhỏ (<= 64px) làm nét nhẹ sau khi thu; icon theo đúng lưới từng nền tảng (BRAND_GUIDELINES.md mục 10).
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, mkdirSync, readdirSync, statSync, rmSync, existsSync } from 'node:fs';
import { join, relative, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = dirname(fileURLToPath(import.meta.url));
const SRC = join(ROOT, 'source');
const DIST = join(ROOT, 'dist');
const MANIFEST = join(ROOT, 'MANIFEST.json');
const TOOLS = join(ROOT, 'tools'); // make_masters.py + requirements.txt cũng được băm: đổi công cụ = đổi nguồn
const master = (f) => join(SRC, 'master', f);

// Hệ màu chuẩn (BRAND_GUIDELINES.md mục 5).
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
  for (const f of [...walk(DIST), ...walk(SRC), ...walk(TOOLS)]) {
    const rel = relative(ROOT, f);
    if (!listed.has(rel)) errs.push(`thừa ${rel} (chưa ghi vào MANIFEST - chạy lại build.mjs)`);
  }
  for (const f of walk(DIST)) if (statSync(f).size === 0) errs.push(`rỗng ${relative(ROOT, f)} (build bị cắt ngang?)`);
  if (errs.length) {
    console.error('Bộ nhận diện TsuMIND LỆCH nguồn:\n  ' + errs.join('\n  '));
    console.error('Sửa nguồn ở source/, rồi: npm ci && node build.mjs');
    process.exit(1);
  }
  console.log(`OK - ${Object.keys(m.sources).length} nguồn, ${Object.keys(m.outputs).length} tệp sinh khớp MANIFEST.json`);
}

// ICNS (macOS): đầu 'icns' + tổng độ dài, rồi từng mục <loại 4 byte><độ dài 4 byte gồm đầu mục><PNG>.
function icns(entries) {
  const parts = entries.map(([type, png]) => {
    const head = Buffer.alloc(8);
    head.write(type, 0, 'ascii');
    head.writeUInt32BE(png.length + 8, 4);
    return Buffer.concat([head, png]);
  });
  const body = Buffer.concat(parts);
  const head = Buffer.alloc(8);
  head.write('icns', 0, 'ascii');
  head.writeUInt32BE(body.length + 8, 4);
  return Buffer.concat([head, body]);
}

async function build() {
  const sharp = (await import('sharp')).default;
  const pngToIco = (await import('png-to-ico')).default;
  rmSync(DIST, { recursive: true, force: true });
  const files = new Map();
  const out = (rel, buf) => {
    if (!buf?.length) throw new Error(`tệp sinh rỗng: ${rel}`);
    const p = join(DIST, rel);
    mkdirSync(dirname(p), { recursive: true });
    writeFileSync(p, buf);
    files.set(rel, buf.length);
  };
  const png = (s) => s.png({ compressionLevel: 9, adaptiveFiltering: true, palette: false });
  const T = { r: 0, g: 0, b: 0, alpha: 0 };
  // Thu nhỏ Lanczos3 (sharp tự xử lý alpha nhân trước); <= 64px làm nét nhẹ bù độ mềm của phép thu.
  const fit = (src, w, h = w) => {
    let s = sharp(src).resize(w, h, { kernel: 'lanczos3', fit: 'contain', background: T });
    if (Math.max(w, h) <= 64) s = s.sharpen({ sigma: 0.5 });
    return s;
  };
  const fitW = (src, w) => sharp(src).resize({ width: w, kernel: 'lanczos3' });
  // Ba định dạng cho giao diện web: AVIF (nhỏ nhất) → WebP → PNG (dự phòng mọi trình duyệt/hệ điều hành).
  const triple = async (base, img) => {
    const buf = await img.png().toBuffer();
    // sharp 0.35 (aom 3.15) chấm `quality` khác 0.34: 88 (92 cho cạnh <= 128px) mới >= độ trung thực của q70 cũ
    // ở MỌI tệp (PSNR nhân alpha so với PNG, đo 28/11/2026). Đổi mức thì đo lại, không hạ.
    const { width: aw, height: ah } = await sharp(buf).metadata();
    const aq = Math.max(aw, ah) <= 128 ? 92 : 88;
    out(`${base}.avif`, await sharp(buf).avif({ quality: aq, effort: 6, chromaSubsampling: '4:4:4' }).toBuffer());
    out(`${base}.webp`, await sharp(buf).webp({ quality: 90, alphaQuality: 100, effort: 6, smartSubsample: true }).toBuffer());
    out(`${base}.png`, await png(sharp(buf)).toBuffer());
  };
  const bg = (w, h) =>
    Buffer.from(
      `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><defs>` +
        `<radialGradient id="g" cx="0.5" cy="0.42" r="0.75"><stop offset="0" stop-color="${DEEP_CIRCUIT_BLUE}"/>` +
        `<stop offset="0.6" stop-color="${MIDNIGHT_NAVY}"/><stop offset="1" stop-color="#050D20"/></radialGradient></defs>` +
        `<rect width="100%" height="100%" fill="url(#g)"/></svg>`,
    );
  // Ô nền liền (iOS, Android cũ, cửa hàng, apple-touch): gradient Midnight Navy + cú chiếm `frac` cạnh, căn giữa.
  const tile = async (s, frac) =>
    sharp(await sharp(bg(s, s)).png().toBuffer())
      .composite([{ input: await fit(master('tsumind-mark.png'), Math.round(s * frac)).png().toBuffer(), gravity: 'center' }])
      .flatten({ background: MIDNIGHT_NAVY });
  // Squircle (macOS, Windows, Linux, PWA "any") đã có nền trong suốt quanh khối.
  const squircle = (s) => fit(master('tsumind-squircle.png'), s);
  // macOS: theo lưới Apple, khối squircle 824/1024 căn giữa ô trong suốt.
  const macTile = async (s) => {
    const inner = Math.round((s * 824) / 1024);
    return sharp({ create: { width: s, height: s, channels: 4, background: T } }).composite([
      { input: await squircle(inner).png().toBuffer(), gravity: 'center' },
    ]);
  };
  const buf = async (s) => png(s).toBuffer();

  // 1. Logo chính (huy hiệu + dải chữ) - vuông. Master 1040px.
  for (const s of [1024, 512, 384, 256, 192, 128])
    await triple(`logo/tsumind-logo-primary-${s}`, fit(master('tsumind-emblem.png'), s));
  // 2. Biểu tượng (cú trong vòng tròn, không chữ) - vuông. Master 820px ⇒ tối đa 768.
  for (const s of [768, 512, 256, 128, 64, 32])
    await triple(`symbol/tsumind-symbol-${s}`, fit(master('tsumind-mark.png'), s));
  // 3. Logo ngang: bản nền tối (chữ bạc kim) và bản nền sáng (chữ Midnight Navy). Master 910x409.
  for (const v of ['', '-light'])
    for (const w of [910, 720, 480, 360, 240])
      await triple(`horizontal/tsumind-logo-horizontal${v}-${w}w`, fitW(master(`tsumind-lockup${v}.png`), w));
  // 4. Dải chữ. Master 499x126.
  for (const v of ['', '-light'])
    for (const w of [499, 360, 240])
      await triple(`wordmark/tsumind-wordmark${v}-${w}w`, fitW(master(`tsumind-wordmark${v}.png`), w));

  // 5. Favicon + PWA. Cỡ tab (16-48) dùng biểu tượng tròn (đọc rõ hơn squircle tối ở 16px).
  const mark = (s) => buf(fit(master('tsumind-mark.png'), s));
  const fav = await Promise.all([16, 32, 48].map(mark));
  out('favicon/favicon.ico', await pngToIco(fav));
  for (const s of [16, 32, 48, 96]) out(`favicon/favicon-${s}x${s}.png`, await mark(s));
  out('favicon/apple-touch-icon.png', await buf(await tile(180, 0.8)));
  for (const s of [192, 512]) {
    out(`favicon/android-chrome-${s}x${s}.png`, await buf(squircle(s)));
    // maskable: vùng an toàn là vòng tròn đường kính 80% ⇒ cú 70% trên nền liền.
    out(`favicon/maskable-${s}x${s}.png`, await buf(await tile(s, 0.7)));
  }
  out(
    'favicon/site.webmanifest',
    Buffer.from(
      JSON.stringify(
        {
          name: 'TsuMIND',
          short_name: 'TsuMIND',
          icons: [
            { src: '/android-chrome-192x192.png', sizes: '192x192', type: 'image/png', purpose: 'any' },
            { src: '/android-chrome-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'any' },
            { src: '/maskable-192x192.png', sizes: '192x192', type: 'image/png', purpose: 'maskable' },
            { src: '/maskable-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
          ],
          theme_color: MIDNIGHT_NAVY,
          background_color: MIDNIGHT_NAVY,
          display: 'standalone',
        },
        null,
        2,
      ) + '\n',
    ),
  );
  out(
    'favicon/head-snippet.html',
    Buffer.from(
      [
        '<!-- TsuMIND - chép vào <head>; tệp nằm ở gốc web (BRAND_GUIDELINES.md mục 10) -->',
        '<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">',
        '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">',
        '<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">',
        '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">',
        '<link rel="manifest" href="/site.webmanifest">',
        `<meta name="theme-color" content="${MIDNIGHT_NAVY}">`,
        '<meta property="og:image" content="https://tsumind.com/og-image-1200x630.png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '',
      ].join('\n'),
    ),
  );

  // 6. Biểu tượng ứng dụng theo nền tảng.
  // iOS / App Store / Google Play / Android cũ: vuông, KHÔNG trong suốt, không tự bo góc.
  for (const s of [1024, 512, 256]) out(`app-icon/tsumind-app-icon-${s}.png`, await buf((await tile(s, 0.8)).removeAlpha()));
  out('app-icon/google-play-icon-512.png', await buf((await tile(512, 0.8)).removeAlpha()));
  // Squircle nền trong suốt: Linux, Windows Store, ảnh minh hoạ.
  for (const s of [1024, 512, 256, 128]) out(`app-icon/tsumind-app-icon-squircle-${s}.png`, await buf(squircle(s)));
  // Windows .ico: 16-32 dùng biểu tượng tròn (giản lược), 48-256 dùng squircle.
  const winLayers = [
    ...(await Promise.all([16, 24, 32].map(mark))),
    ...(await Promise.all([48, 64, 128, 256].map((s) => buf(squircle(s))))),
  ];
  out('app-icon/tsumind-app.ico', await pngToIco(winLayers));
  // macOS .icns theo lưới Apple (squircle 824/1024).
  const mac = async (s) => buf(await macTile(s));
  out(
    'app-icon/tsumind.icns',
    icns([
      ['icp4', await mac(16)], ['icp5', await mac(32)], ['icp6', await mac(64)], ['ic07', await mac(128)],
      ['ic08', await mac(256)], ['ic09', await mac(512)], ['ic10', await mac(1024)], ['ic11', await mac(32)],
      ['ic12', await mac(64)], ['ic13', await mac(256)], ['ic14', await mac(512)],
    ]),
  );
  out('app-icon/tsumind-macos-1024.png', await mac(1024));
  // Linux hicolor: PNG 16-512.
  for (const s of [16, 32, 48, 64, 128, 256, 512])
    out(`app-icon/linux/hicolor/${s}x${s}/apps/tsumind.png`, s <= 32 ? await mark(s) : await buf(squircle(s)));
  // Android adaptive 108dp (432px @4x, xuất 1024 để Android Studio tự thu): nền liền + cú trong vùng 66/108,
  // bản đơn sắc (themed icon) là bóng trắng của cú.
  out('app-icon/android-adaptive-background-1024.png', await buf(sharp(bg(1024, 1024)).flatten({ background: MIDNIGHT_NAVY })));
  const fg = await fit(master('tsumind-mark.png'), Math.round((1024 * 62) / 108)).png().toBuffer();
  const blank = () => sharp({ create: { width: 1024, height: 1024, channels: 4, background: T } });
  out('app-icon/android-adaptive-foreground-1024.png', await buf(blank().composite([{ input: fg, gravity: 'center' }])));
  // Themed icon: Android tô một màu theo alpha. Bóng của cú là đĩa tròn đặc (vô nghĩa) ⇒ alpha = alpha × độ sáng
  // (mắt, viền, mạch sáng thành nét; thân tối trong suốt).
  const { data: fd, info: fi } = await sharp(fg).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const mono = Buffer.alloc(fi.width * fi.height * 4, 255);
  for (let i = 0; i < fi.width * fi.height; i++) {
    const l = (0.2126 * fd[i * 4] + 0.7152 * fd[i * 4 + 1] + 0.0722 * fd[i * 4 + 2]) / 255;
    mono[i * 4 + 3] = Math.round(fd[i * 4 + 3] * Math.min(1, Math.max(0, (l - 0.22) / 0.45)));
  }
  const white = await sharp(mono, { raw: { width: fi.width, height: fi.height, channels: 4 } }).png().toBuffer();
  out('app-icon/android-adaptive-monochrome-1024.png', await buf(blank().composite([{ input: white, gravity: 'center' }])));

  // 7. Ảnh chia sẻ (Open Graph 1200x630) + ảnh đại diện.
  const svgImg = (f, wd) => sharp(readFileSync(join(SRC, 'text', f)), { density: 300 }).resize({ width: wd }).png().toBuffer();
  const og = await png(
    sharp(bg(1200, 630)).composite([
      { input: await fit(master('tsumind-emblem.png'), 500).png().toBuffer(), left: 64, top: 65 },
      { input: await fitW(master('tsumind-wordmark.png'), 499).png().toBuffer(), left: 620, top: 190 },
      { input: await svgImg('tsumind-tagline-vi.svg', 540), left: 624, top: 360 },
      { input: await svgImg('tsumind-domain.svg', 190), left: 624, top: 440 },
    ]),
  ).toBuffer();
  out('social/og-image-1200x630.png', og);
  out('social/og-image-1200x630.webp', await sharp(og).webp({ quality: 90 }).toBuffer());
  out('social/og-image-1200x630.avif', await sharp(og).avif({ quality: 80, effort: 6 }).toBuffer());
  out('social/avatar-app-icon-500.png', await buf(await tile(500, 0.8)));
  out(
    'social/avatar-logo-primary-500.png',
    await buf(sharp(bg(500, 500)).composite([{ input: await fit(master('tsumind-emblem.png'), 450).png().toBuffer(), gravity: 'center' }])),
  );

  const manifest = { generator: 'assets/brand/tsumind/build.mjs', sources: {}, outputs: {} };
  for (const f of [...walk(SRC), ...walk(TOOLS)].sort()) manifest.sources[relative(ROOT, f)] = sha(readFileSync(f));
  for (const f of walk(DIST).sort()) manifest.outputs[relative(ROOT, f)] = sha(readFileSync(f));
  writeFileSync(MANIFEST, JSON.stringify(manifest, null, 2) + '\n');
  const total = [...files.values()].reduce((a, b) => a + b, 0);
  console.log(`Đã sinh ${files.size} tệp vào dist/ (${(total / 1024 / 1024).toFixed(1)} MB)`);
}

if (process.argv.includes('--check')) check();
else await build();
