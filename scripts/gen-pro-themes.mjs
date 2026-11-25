#!/usr/bin/env node
/**
 * gen-pro-themes.mjs - sinh bộ CHỦ ĐỀ PRO (quyền lợi Q2, PRODUCT_POLICY 3.7.1)
 * từ sắc độ OKLCH khai trong tokens/pro-themes.json - DESIGN_SYSTEM.md mục 1.3.
 *
 * Mỗi chủ đề = (1) lớp nền NGẢ SẮC nhẹ (giữ nguyên độ sáng L của lớp nền chung, chỉ
 * thêm chroma `tint` theo `hue`) + (2) 10 vai trò nhấn sinh bằng CHÍNH thuật toán
 * dò WCAG của gen-product-palette.mjs, đo trên nền đã ngả + (3) cặp màu khung ảnh
 * đại diện. Không màu nào chọn tay; trượt WCAG thì giảm `tint` từng bước tới khi đạt.
 *
 *   node scripts/gen-pro-themes.mjs           # sinh lại colors trong pro-themes.json
 *   node scripts/gen-pro-themes.mjs --check   # chỉ đối chiếu + đo (CI, check-standards.sh)
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { contrast, hexToOklch, oklchToHex, hueGap } from './color-lib.mjs';
import { palette } from './gen-product-palette.mjs';
import { auditColors, STABLE_BACKGROUNDS } from './check-contrast.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const PATH = join(ROOT, 'tokens', 'pro-themes.json');
const base = JSON.parse(readFileSync(join(ROOT, 'tokens', 'design-tokens.json'), 'utf8')).color;

/** Vai trò nền được ngả sắc. Chữ, trạng thái, lớp phủ giữ nguyên lớp nền chung. */
const TINTED = ['bg-base', 'bg-surface', 'bg-subtle', 'bg-hover', 'border', 'border-strong'];
const DANGER_GAP = 15; // như check-products.mjs
const MIN_THEME_GAP = 20; // hai chủ đề có màu (chroma >= 0.05) cách nhau >= 20°
const RING_HUE_SHIFT = 40; // khung ảnh: chuyển sắc primary -> primary lệch 40° (theme.ringShift ghi đè)
const RING_MIN = 3.0; // WCAG 1.4.11 - khung là thành phần đồ hoạ

function tintPalette(H, tint) {
  const out = {};
  for (const mode of ['light', 'dark']) {
    out[mode] = { ...base[mode] };
    for (const k of TINTED) {
      const { L } = hexToOklch(base[mode][k]);
      out[mode][k] = oklchToHex(L, tint, H);
    }
  }
  return out;
}

function ringEnd(hex, mode, b, shift = RING_HUE_SHIFT) {
  const { L, C, H } = hexToOklch(hex);
  const H2 = (H + shift + 360) % 360;
  const step = mode === 'dark' ? 0.005 : -0.005;
  for (let l = L; l > 0.2 && l < 0.98; l += step) {
    const h = oklchToHex(l, C, H2);
    if (Math.min(...STABLE_BACKGROUNDS.map((k) => contrast(h, b[mode][k]))) >= RING_MIN) return h;
  }
  throw new Error(`Không tìm được màu khung đạt ${RING_MIN}:1 cho ${hex}`);
}

/** Sinh một chủ đề; trả về { colors, tintUsed }. */
export function build(theme) {
  for (let tint = theme.tint; tint >= 0; tint = +(tint - 0.002).toFixed(3)) {
    const b = tintPalette(theme.hue, tint);
    const accents = palette(theme.hue, theme.chroma, b);
    const colors = {};
    let ok = true;
    for (const mode of ['light', 'dark']) {
      const merged = { ...b[mode], ...accents[mode] };
      if (!auditColors(merged).every((r) => r.ok)) ok = false;
      colors[mode] = {};
      for (const k of TINTED) colors[mode][k] = b[mode][k];
      Object.assign(colors[mode], accents[mode]);
      colors[mode]['pro-ring-start'] = accents[mode].primary;
      colors[mode]['pro-ring-end'] = ringEnd(accents[mode].primary, mode, b, theme.ringShift ?? RING_HUE_SHIFT);
    }
    if (ok) return { colors, tintUsed: tint };
  }
  throw new Error(`Chủ đề ${theme.id}: không đạt WCAG kể cả khi bỏ ngả sắc`);
}

/** Đo lại một bộ đã ghi (không tin vào bản sinh) - dùng cho --check. */
export function audit(data) {
  const errors = [];
  const ids = new Set();
  for (const t of data.themes) {
    if (ids.has(t.id)) errors.push(`${t.id}: trùng id`);
    ids.add(t.id);
    if (!/^[a-z][a-z0-9-]*$/.test(t.id)) errors.push(`${t.id}: id chỉ gồm a-z, 0-9, -`);
    if (!t.name?.vi || !t.name?.en) errors.push(`${t.id}: thiếu name.vi / name.en`);
    for (const mode of ['light', 'dark']) {
      const merged = { ...base[mode], ...t.colors[mode] };
      for (const r of auditColors(merged)) {
        if (!r.ok) errors.push(`${t.id} ${mode}: ${r.pair} = ${r.ratio.toFixed(2)} < ${r.min} (${r.note})`);
      }
      for (const k of ['pro-ring-start', 'pro-ring-end']) {
        const m = Math.min(...STABLE_BACKGROUNDS.map((bg) => contrast(t.colors[mode][k], merged[bg])));
        if (m < RING_MIN) errors.push(`${t.id} ${mode}: ${k} = ${m.toFixed(2)} < ${RING_MIN}`);
      }
      if (t.chroma >= 0.05) {
        const gap = hueGap(hexToOklch(t.colors[mode].primary).H, hexToOklch(base[mode].danger).H);
        if (gap < DANGER_GAP) errors.push(`${t.id} ${mode}: primary cách danger ${gap.toFixed(1)}° < ${DANGER_GAP}°`);
      }
    }
  }
  const colored = data.themes.filter((t) => t.chroma >= 0.05);
  for (let i = 0; i < colored.length; i++) {
    for (let j = i + 1; j < colored.length; j++) {
      const g = hueGap(colored[i].hue, colored[j].hue);
      if (g < MIN_THEME_GAP) errors.push(`${colored[i].id}/${colored[j].id}: sắc độ cách ${g}° < ${MIN_THEME_GAP}°`);
    }
  }
  return errors;
}

const isMain = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (isMain) {
  const check = process.argv.includes('--check');
  const data = JSON.parse(readFileSync(PATH, 'utf8'));
  let drift = 0;
  for (const t of data.themes) {
    const { colors, tintUsed } = build(t);
    if (JSON.stringify(colors) !== JSON.stringify(t.colors)) {
      if (check) {
        console.error(`LỆCH: ${t.id} - colors khác bản sinh từ hue=${t.hue} chroma=${t.chroma} tint=${t.tint}`);
        drift++;
      }
      if (!check) t.colors = colors;
    }
    if (tintUsed !== t.tint) console.log(`${t.id}: tint ${t.tint} -> ${tintUsed} để đạt WCAG`);
  }
  if (!check) writeFileSync(PATH, JSON.stringify(data, null, 2) + '\n', 'utf8');
  const errors = audit(data);
  for (const e of errors) console.error(`LỖI: ${e}`);
  if (drift) console.error('Chạy: node scripts/gen-pro-themes.mjs');
  if (drift || errors.length) process.exit(1);
  console.log(`OK: ${data.themes.length} chủ đề Pro - khớp bản sinh, đạt WCAG trên nền ngả sắc của chính nó`);
}
