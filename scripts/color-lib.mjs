/**
 * color-lib.mjs - phép đo màu dùng chung cho build-tokens, check-contrast,
 * gen-product-palette và check-products.
 *
 * Tương phản theo WCAG 2.1 (độ chói tương đối sRGB). Sắc độ theo OKLCH
 * (Björn Ottosson 2020) vì khoảng cách sắc độ OKLCH khớp cảm nhận của mắt hơn
 * HSL - hai màu cách 20° OKLCH trông khác nhau thật, HSL thì không chắc.
 */
const HEX = /^#?([0-9a-f]{6})$/i;

export function parseHex(hex) {
  const m = HEX.exec(String(hex).trim());
  if (!m) throw new Error(`Mã màu không hợp lệ: ${hex}`);
  return [0, 2, 4].map((i) => parseInt(m[1].slice(i, i + 2), 16));
}

const wcagLinear = (c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);

export function luminance(hex) {
  const [r, g, b] = parseHex(hex).map((v) => wcagLinear(v / 255));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

export function contrast(a, b) {
  const [la, lb] = [luminance(a), luminance(b)];
  const [hi, lo] = la > lb ? [la, lb] : [lb, la];
  return (hi + 0.05) / (lo + 0.05);
}

const toLinear = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const toGamma = (c) => (c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055);

export function hexToOklch(hex) {
  const [r, g, b] = parseHex(hex).map((v) => toLinear(v / 255));
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  const L = 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s;
  const A = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s;
  const B = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s;
  return { L, C: Math.hypot(A, B), H: ((Math.atan2(B, A) * 180) / Math.PI + 360) % 360 };
}

/** Trả về [r,g,b] tuyến tính, có thể ra ngoài [0,1] nếu màu ngoài gam sRGB. */
function oklchToLinear(L, C, H) {
  const h = (H * Math.PI) / 180;
  const A = C * Math.cos(h);
  const B = C * Math.sin(h);
  const l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3;
  const m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3;
  const s = (L - 0.0894841775 * A - 1.291485548 * B) ** 3;
  return [
    4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s,
  ];
}

/** OKLCH -> HEX chữ HOA, giảm chroma tới khi vào gam sRGB (giữ L và H). */
export function oklchToHex(L, C, H) {
  let c = C;
  let rgb = oklchToLinear(L, c, H);
  while (rgb.some((v) => v < -1e-6 || v > 1 + 1e-6) && c > 0) {
    c = Math.max(0, c - 0.002);
    rgb = oklchToLinear(L, c, H);
  }
  return (
    '#' +
    rgb
      .map((v) => Math.round(Math.min(1, Math.max(0, toGamma(Math.min(1, Math.max(0, v))))) * 255))
      .map((v) => v.toString(16).padStart(2, '0'))
      .join('')
      .toUpperCase()
  );
}

/** Khoảng cách sắc độ trên vòng tròn, 0..180. */
export function hueGap(a, b) {
  const d = Math.abs(a - b) % 360;
  return d > 180 ? 360 - d : d;
}

export function rgba(hex, alpha) {
  const [r, g, b] = parseHex(hex);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

/** Khoảng cách cảm nhận ΔE trong OKLab (0 = trùng; ~0.02 là ngưỡng mắt thường nhận ra). */
export function deltaE(a, b) {
  const p = hexToOklch(a);
  const q = hexToOklch(b);
  const pa = [p.L, p.C * Math.cos((p.H * Math.PI) / 180), p.C * Math.sin((p.H * Math.PI) / 180)];
  const qa = [q.L, q.C * Math.cos((q.H * Math.PI) / 180), q.C * Math.sin((q.H * Math.PI) / 180)];
  return Math.hypot(pa[0] - qa[0], pa[1] - qa[1], pa[2] - qa[2]);
}
