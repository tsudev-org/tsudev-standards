#!/usr/bin/env node
/**
 * gen-product-palette.mjs - sinh bộ vai trò NHẤN (lớp bản sắc) cho một sản phẩm
 * từ sắc độ OKLCH đã chốt trong tokens/products/<id>.json.
 *
 * Bộ vai trò sinh ra luôn đạt WCAG trên LỚP NỀN CHUNG của design-tokens.json:
 * thuật toán dò độ sáng L theo từng bước nhỏ tới khi mọi cặp đạt, thay vì đoán
 * một L cố định rồi hy vọng (vàng và xanh lục cần L khác hẳn tím để cùng đạt).
 *
 *   node scripts/gen-product-palette.mjs            # sinh lại mọi sản phẩm không "locked"
 *   node scripts/gen-product-palette.mjs cwico      # chỉ một sản phẩm
 *   node scripts/gen-product-palette.mjs --check    # chỉ đối chiếu, không ghi (CI)
 *
 * Sản phẩm "locked": true giữ nguyên bảng màu đã được chủ dự án chốt tay
 * (TsuDEV, TsuFiles) - script bỏ qua, cổng kiểm vẫn đo đủ.
 */
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { contrast, oklchToHex, rgba } from './color-lib.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DIR = join(ROOT, 'tokens', 'products');
const base = JSON.parse(readFileSync(join(ROOT, 'tokens', 'design-tokens.json'), 'utf8')).color;

const TEXT_BGS = ['bg-base', 'bg-surface', 'bg-subtle', 'bg-hover'];
const minOn = (fg, theme, b = base) => Math.min(...TEXT_BGS.map((k) => contrast(fg, b[theme][k])));

/** Dò L từ start theo bước step tới khi ok(hex) đúng. */
function seek(H, C, start, step, ok) {
  for (let L = start; L > 0.2 && L < 0.98; L += step) {
    const hex = oklchToHex(L, C, H);
    if (ok(hex)) return { L, hex };
  }
  throw new Error(`Không tìm được độ sáng đạt WCAG cho H=${H} C=${C}`);
}

/** `b` = lớp nền để đo (mặc định lớp nền chung; chủ đề Pro truyền nền đã ngả sắc). */
export function palette(H, C, b = base) {
  const ink = b.dark['on-primary'];
  const white = b.light['on-primary'];
  // ---- Tối: nút sáng, chữ mực đen. Dò từ tối lên sáng, dừng ở L thấp nhất đạt
  // để màu còn đậm sắc nhất có thể.
  const dP = seek(H, C, 0.6, 0.005, (h) => contrast(ink, h) >= 8.0 && minOn(h, 'dark', b) >= 4.5);
  const dActive = seek(H, C, dP.L - 0.07, 0.005, (h) => contrast(ink, h) >= 6.0);
  const dLink = seek(H, C * 0.85, dP.L + 0.05, 0.005, (h) => minOn(h, 'dark', b) >= 7.0);
  // Nhấn phụ CÙNG sắc độ, sáng hơn (Tối) / đậm hơn (Sáng). Không lệch sắc độ:
  // vòng màu đã chia cho 11 sản phẩm, lệch 25° là đụng màu chính của sản phẩm kế bên.
  const dAccent = seek(H, C * 0.7, dP.L + 0.08, 0.005, (h) => minOn(h, 'dark', b) >= 10.0);
  const dark = {
    'text-link': dLink.hex,
    primary: dP.hex,
    'primary-hover': oklchToHex(Math.min(dP.L + 0.06, 0.95), C * 0.85, H),
    'primary-active': dActive.hex,
    'on-primary': ink,
    'focus-ring': dP.hex,
    accent: dAccent.hex,
    glow: rgba(dP.hex, 0.14),
    'icon-info': dP.hex,
    'icon-nav': dLink.hex,
  };
  // ---- Sáng: nút đậm, chữ trắng. Dò từ sáng xuống tối, dừng ở L cao nhất đạt.
  const lP = seek(H, C, 0.7, -0.005, (h) => contrast(white, h) >= 5.0 && minOn(h, 'light', b) >= 4.5);
  const lHover = oklchToHex(lP.L - 0.06, C, H);
  const light = {
    'text-link': lHover,
    primary: lP.hex,
    'primary-hover': lHover,
    'primary-active': oklchToHex(lP.L - 0.12, C, H),
    'on-primary': white,
    'focus-ring': lP.hex,
    accent: seek(H, C, lP.L - 0.08, -0.005, (h) => minOn(h, 'light', b) >= 7.0).hex,
    glow: rgba(lP.hex, 0.1),
    'icon-info': lP.hex,
    'icon-nav': lHover,
  };
  return { light, dark };
}

const isMain = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (isMain) {
  const check = process.argv.includes('--check');
  const only = process.argv.slice(2).filter((a) => !a.startsWith('--'));
  let drift = 0;
  for (const f of readdirSync(DIR).filter((n) => n.endsWith('.json') && !n.endsWith('.schema.json'))) {
    const path = join(DIR, f);
    const p = JSON.parse(readFileSync(path, 'utf8'));
    if (p.locked || (only.length && !only.includes(p.id))) continue;
    const colors = palette(p.hue, p.chroma);
    if (JSON.stringify(colors) === JSON.stringify(p.colors)) continue;
    if (check) {
      console.error(`LỆCH: ${f} - colors khác bản sinh từ hue=${p.hue} chroma=${p.chroma}`);
      drift++;
      continue;
    }
    p.colors = colors;
    writeFileSync(path, JSON.stringify(p, null, 2) + '\n', 'utf8');
    console.log(`Đã sinh ${f}`);
  }
  if (drift) {
    console.error('Chạy: node scripts/gen-product-palette.mjs');
    process.exit(1);
  }
  if (check) console.log('OK: bảng màu sản phẩm khớp bản sinh');
}
