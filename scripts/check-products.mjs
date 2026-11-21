#!/usr/bin/env node
/**
 * check-products.mjs - cổng kiểm LỚP BẢN SẮC (tokens/products/*.json),
 * DESIGN_SYSTEM.md mục 1.2.
 *
 * Bắt bốn lỗi mà mắt người dễ bỏ sót khi hệ sinh thái có thêm sản phẩm:
 *   1. Khai thiếu/sai trường (bố cục, bo góc, hoạ tiết, font ngoài danh sách).
 *   2. Bảng nhấn trượt WCAG trên lớp nền chung.
 *   3. Hai sản phẩm trông như một (trước 21/11/2026 Lotus Share và TsuFiles dùng
 *      chung #A970FF, chín sản phẩm khác dùng chung một màu xanh).
 *   4. Màu chính trông như nút "Xoá" (quá gần sắc độ danger).
 */
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { contrast, hexToOklch, hueGap, deltaE } from './color-lib.mjs';
import { palette } from './gen-product-palette.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DIR = join(ROOT, 'tokens', 'products');
const base = JSON.parse(readFileSync(join(ROOT, 'tokens', 'design-tokens.json'), 'utf8')).color;
const schema = JSON.parse(readFileSync(join(DIR, 'product.schema.json'), 'utf8'));
const ENUM = (k) => schema.properties[k].enum;

/** Ngưỡng - đổi ở đây thì MUST đổi cùng DESIGN_SYSTEM.md mục 1.2. */
const MIN_HUE_GAP = 20; // độ OKLCH giữa màu chính của hai sản phẩm, ở CẢ hai chế độ
const MIN_DELTA_E = 0.045; // ΔE OKLab tối thiểu giữa màu chính hai sản phẩm
const NEAR_DELTA_E = 0.08; // dưới ngưỡng này: hai sản phẩm MUST khác cả layout lẫn shape
const DANGER_GAP = 15; // độ OKLCH tối thiểu giữa màu chính và danger

const ROLES = ['text-link', 'primary', 'primary-hover', 'primary-active', 'on-primary', 'focus-ring', 'accent', 'glow', 'icon-info', 'icon-nav'];
const TEXT_BGS = ['bg-base', 'bg-surface', 'bg-subtle', 'bg-hover'];
const STABLE_BGS = ['bg-base', 'bg-surface', 'bg-subtle'];

const errors = [];
const err = (m) => errors.push(m);

const products = readdirSync(DIR)
  .filter((f) => f.endsWith('.json') && !f.endsWith('.schema.json'))
  .map((f) => ({ file: f, ...JSON.parse(readFileSync(join(DIR, f), 'utf8')) }));

for (const p of products) {
  const at = `${p.file}:`;
  if (p.file !== `${p.id}.json`) err(`${at} tên tệp phải là ${p.id}.json`);
  if (!/^[a-z][a-z0-9-]*$/.test(p.id || '')) err(`${at} id "${p.id}" phải chữ thường a-z0-9-`);
  for (const k of schema.required) if (p[k] === undefined) err(`${at} thiếu trường ${k}`);
  for (const k of ['layout', 'shape', 'motif', 'fontDisplay']) {
    if (p[k] !== undefined && !ENUM(k).includes(p[k])) err(`${at} ${k}="${p[k]}" ngoài danh sách: ${ENUM(k).join(', ')}`);
  }
  for (const theme of ['light', 'dark']) {
    const c = p.colors?.[theme] || {};
    const keys = Object.keys(c);
    if (keys.join('|') !== ROLES.join('|')) err(`${at} colors.${theme} phải đủ và đúng thứ tự: ${ROLES.join(', ')}`);
    if (keys.length !== ROLES.length) continue;
    const m = { ...base[theme], ...c };
    const need = (fg, bgs, min, what) => {
      const worst = Math.min(...bgs.map((b) => contrast(m[fg], m[b])));
      if (worst < min) err(`${at} ${theme} ${fg} ${worst.toFixed(2)} < ${min} (${what})`);
    };
    need('text-link', TEXT_BGS, 4.5, 'liên kết');
    need('accent', TEXT_BGS, 4.5, 'nhấn phụ dùng cả cho chữ');
    need('focus-ring', STABLE_BGS, 3.0, 'WCAG 1.4.11');
    need('icon-info', STABLE_BGS, 3.0, 'biểu tượng, WCAG 1.4.11');
    need('icon-nav', STABLE_BGS, 3.0, 'biểu tượng, WCAG 1.4.11');
    for (const bg of ['primary', 'primary-hover', 'primary-active']) {
      const r = contrast(m['on-primary'], m[bg]);
      if (r < 4.5) err(`${at} ${theme} on-primary/${bg} ${r.toFixed(2)} < 4.5`);
    }
    const g = hueGap(hexToOklch(m.primary).H, hexToOklch(m.danger).H);
    if (g < DANGER_GAP) err(`${at} ${theme} primary cách danger ${g.toFixed(0)}° < ${DANGER_GAP}° - nút chính sẽ trông như nút Xoá`);
  }
  if (!p.locked && p.colors?.light) {
    const want = palette(p.hue, p.chroma);
    if (JSON.stringify(want) !== JSON.stringify(p.colors)) err(`${at} colors lệch bản sinh - chạy: node scripts/gen-product-palette.mjs ${p.id}`);
  }
}

const seenMotif = new Map();
for (const p of products) {
  if (seenMotif.has(p.motif)) err(`${p.file}: hoạ tiết "${p.motif}" đã thuộc ${seenMotif.get(p.motif)} - mỗi sản phẩm một hoạ tiết riêng`);
  else seenMotif.set(p.motif, p.id);
}

let minGap = [Infinity];
let minDE = [Infinity];
for (let i = 0; i < products.length; i++) {
  for (let j = i + 1; j < products.length; j++) {
    const [a, b] = [products[i], products[j]];
    if (!a.colors?.light || !b.colors?.light) continue;
    let near = false;
    for (const theme of ['light', 'dark']) {
      const [x, y] = [a.colors[theme].primary, b.colors[theme].primary];
      const gap = hueGap(hexToOklch(x).H, hexToOklch(y).H);
      const dE = deltaE(x, y);
      if (gap < minGap[0]) minGap = [gap, `${a.id}/${b.id} ${theme}`];
      if (dE < minDE[0]) minDE = [dE, `${a.id}/${b.id} ${theme}`];
      if (gap < MIN_HUE_GAP) err(`${a.id} và ${b.id}: màu chính ${theme} cách ${gap.toFixed(0)}° < ${MIN_HUE_GAP}°`);
      if (dE < MIN_DELTA_E) err(`${a.id} và ${b.id}: màu chính ${theme} ΔE ${dE.toFixed(3)} < ${MIN_DELTA_E}`);
      if (dE < NEAR_DELTA_E) near = true;
    }
    if (near && (a.layout === b.layout || a.shape === b.shape)) {
      err(`${a.id} và ${b.id}: màu gần nhau (ΔE < ${NEAR_DELTA_E}) nên MUST khác cả layout lẫn shape (đang ${a.layout}/${a.shape} và ${b.layout}/${b.shape})`);
    }
  }
}

// Danh bạ ở DESIGN_SYSTEM.md mục 1.2 là bản người đọc - lệch JSON là tài liệu nói sai.
const doc = readFileSync(join(ROOT, 'docs', 'DESIGN_SYSTEM.md'), 'utf8');
for (const p of products) {
  const row = doc.split('\n').find((l) => l.startsWith(`| \`${p.id}\` |`));
  const want = `\`${p.colors?.dark?.primary}\` / \`${p.colors?.light?.primary}\` | ${p.layout} | ${p.shape} | ${p.motif} | ${p.fontDisplay} |`;
  if (!row || !row.includes(` | ${p.hue} | `) || !row.endsWith(want)) err(`DESIGN_SYSTEM.md mục 1.2 thiếu hoặc lệch dòng của ${p.id} (cần: ...| ${p.hue} | ${want})`);
}

if (errors.length) {
  for (const e of errors) console.error(`LỖI: ${e}`);
  console.error(`\n${errors.length} lỗi ở lớp bản sắc sản phẩm (DESIGN_SYSTEM.md mục 1.2).`);
  process.exit(1);
}
console.log(
  `OK: ${products.length} sản phẩm - đạt WCAG, hoạ tiết không trùng, sắc độ gần nhất ${minGap[0].toFixed(1)}° (${minGap[1]}), ΔE gần nhất ${minDE[0].toFixed(3)} (${minDE[1]}).`,
);
