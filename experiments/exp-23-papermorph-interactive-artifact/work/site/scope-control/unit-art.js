// Chalk sketches for the unit headers on the contents page, one per unit, drawn in the unit's colour.
// Each entry is the inside of an SVG with viewBox 0 0 600 180; keep the left ~200 px light (the unit title sits there
// on narrow screens). Classes, styled in book.html:
//   d  a stroke that draws itself in when the unit scrolls into view (--k orders the strokes)
//   t  text or a filled shape that fades in
//   a  faint chalk white instead of the unit colour;  faint  even fainter
// A sketch may add one looping motion after it is drawn: give an element a class and add a .seen .unit-art .NAME
// rule with its keyframes in book.html (see the examples there: swap-a, hop, spin, tilt, breathe, ...).
'use strict';
(() => {
  let k = 0;
  const P = (d, cls = '', extra = '') => `<path class="d ${cls}" pathLength="1" style="--k:${k++}" d="${d}" ${extra}/>`;
  const Tx = (x, y, s, size = 24, cls = '', anchor = 'start') => `<text class="t ${cls}" style="--k:${k++}" x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}">${s}</text>`;
  const C = (cx, cy, r, cls = '') => `<circle class="d ${cls}" pathLength="1" style="--k:${k++}" cx="${cx}" cy="${cy}" r="${r}"/>`;
  const reset = s => { k = 0; return s; };

  window.UNIT_ART = [
    // Core discipline: the source-of-truth ladder, a dot climbing to the top rung.
    reset(
      P('M240 132H560', 'faint') + P('M240 88H560') + P('M240 44H560') +
      Tx(252, 140, '3', 20, 'a') + Tx(252, 96, '2', 20, 'a') + Tx(252, 52, '1', 22) +
      `<circle class="t hop" r="8" fill="currentColor" stroke="none" style="--k:${k++};offset-path:path('M270 132Q300 108 330 132Q360 60 420 88Q460 60 500 44')"/>` +
      Tx(380, 170, 'higher wins the conflict', 20)
    ),
  ];
})();
