// Headless smoke test: execute the chapter's BEATS against a stubbed engine API.
// Catches ReferenceErrors / undefined helpers / missing marks without a browser.
// (EXP-23 CP-01 dev tool — the stock e2e is playwright, unavailable in this sandbox.)
'use strict';
class El {
  constructor(tag) {
    this.tag = tag; this.children = []; this.attrs = {}; this.style = {}; this._cls = new Set();
    const s = this;
    this.classList = { add: c => s._cls.add(c), remove: c => s._cls.delete(c), contains: c => s._cls.has(c) };
  }
  setAttribute(k, v) { this.attrs[k] = v; }
  getAttribute(k) { return this.attrs[k]; }
  appendChild(c) { this.children.push(c); return c; }
  insertBefore(c) { this.children.push(c); return c; }
  remove() {}
  addEventListener() {}
  querySelectorAll() { return []; }
}
const scene = new El('svg');
const S = {};
const COL = { nat: '#f4a48c', whole: '#86c9e8', int: '#f3c95c', rat: '#e8a0c8', irr: '#8fd6b0', real: '#bba8ee',
  chalk: '#ece8dc', dim: '#9aaba3', faint: '#5d7068', task: '#f0b45a', good: '#8fd6b0', bad: '#f08c7a', board: '#1d2b27' };
const UI = 'ui', MATH = 'math';
const G = (p, state = {}) => { const e = new El('g'); e._st = Object.assign({ x: 0, y: 0, s: 1, r: 0, o: 1 }, state); if (p && p.appendChild) p.appendChild(e); return e; };
const T = (p, str, attrs = {}) => { const e = new El('text'); e._st = { o: attrs.o ?? 1 }; if (p) p.appendChild(e); return e; };
const M = (p, parts, attrs = {}) => { const e = new El('g'); e._st = { o: attrs.o ?? 1 }; e._w = 100; if (p) p.appendChild(e); return e; };
const path = (p, d, attrs = {}, opts = {}) => { const e = new El('path'); e._st = { o: attrs.o ?? 1, d: opts.d ?? 1 }; if (p) p.appendChild(e); return e; };
const mk = (tag, attrs = {}, parent) => { const e = new El(tag); Object.assign(e.attrs, attrs); if (parent) parent.appendChild(e); return e; };
const F = (a, b) => ({ f: 1 }), R = (x, i) => ({ r: 1 }), E = (x) => ({ e: 1 });
const mathW = () => 100, frac = () => new El('g'), chip = () => new El('g'), tokens = (p, items, o) => items.map(i => { const e = new El('g'); if (p) p.appendChild(e); return e; });
const collapse = () => [], eqLine = () => new El('g'), mathEl = () => new El('g'), rich = (p) => p.join('');
const $m = (p) => [String(p)];
const panel = () => { const e = G(scene); e._isPanel = true; return e; };
const show = (e, t0, dur) => { (e._shows = e._shows || []).push([t0, dur]); return e; };
const hide = (e, t0, dur) => e;
const tw = (e, to, t0, dur, ease) => { (e._tws = e._tws || []).push([t0, dur]); return e; };
const prog = () => {}, draw = (e, t0, dur) => e, pop = (e, t0) => e, pulse = (e, t0, k) => e, stream = () => {};
const fx = () => {}, fxp = () => {}, pulseFx = () => {}, shakeFx = () => {}, floatText = () => {}, qlayer = () => new El('g');
const io = () => {}, out = () => {}, back = () => {}, lin = () => {};
const BAND = { x: 96, y: 686, w: 1408, cls: 'band' };
const TOPR = { x: 960, y: 70, w: 624, cls: 'side' };
const RIGHT = { x: 1258, y: 546, w: 330, cls: 'side' };
const SCREEN = { x: 0, y: 0, w: 1600, cls: 'screen' };
const SORT_SCREEN = { cls: 'screen' };
const quiz = (pos, qs, done, label) => {
  for (const q of qs) if (!q.id || !q.build) throw new Error('bad question ' + JSON.stringify(q).slice(0, 80));
  return { __quiz: true, n: qs.length };
};
const choice = (opts, right, yes, no) => (body, api) => ({ reveal: () => opts[right] });
const blanks = rows => (body, api) => ({ reveal: () => rows });
const grid = (rows, cols, o) => (body, api) => ({ reveal: () => rows });
const tap = (vals, right, yes, no) => (body, api) => ({ reveal: () => right });
const tapEls = (row, idx, right, yes, no) => (body, api) => ({ reveal: () => right });
const pickEls = (items, right, yes, no) => (body, api) => {
  if (right < 0 || right >= items.length) throw new Error('pickEls right out of range');
  for (const it of items) if (!it.el || !it.box || it.box.length !== 4) throw new Error('pickEls bad item');
  return { reveal: () => yes };
};
const finishCard = () => {};
const h = (tag, cls, kids) => new El(tag);
const kbd = k => k;
const boot = () => { console.log('boot() called'); };
globalThis.window = { TIMINGS: null };
