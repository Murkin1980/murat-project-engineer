# EVIDENCE-019 — Constructor DOM & WebGL Diagnostic Evidence

**Collection date:** 2026-09-29 UTC  
**Source:** `https://privetmaket.ru/shkaf`  
**Method:** Public page DOM extraction (CP-02 anonymous observation)

## Observed Telemetry & Controls

On the public constructor page `/shkaf`, the following interactive diagnostic block and controls are directly rendered in the browser DOM:

### 1. WebGL Telemetry Block
```text
3D perf: 0 fps
FPS avg 0.0 (>= 55)
FPS low 0.0 (>= 30)
Frame ms 0.0 (<= 16.7)
Worst ms 0.0 (<= 50)
Draw calls 0 (<= 300)
Triangles 0 (<= 500k)
Lines 0 (<= 50k)
Points 0 (<= 50k)
Geometries 0 (<= 500)
Textures 1 (<= 100)
Objects 0 (<= 2000)
Meshes visible 0 / 0 (<= 800)
Materials 0 (<= 250)
DPR 1.00 (<= 2)
JS heap 27.1 MB (<= 256 MB)
Run 5s | Reset
```

### 2. Action Controls and Parametric Inputs
- **Preset Modes:** Без ограничений, Гардероб, Гардероб лайт, Купе, Обувница, Тумбочка, Комод, ТВ-тумба.
- **Dimensional Inputs:** Width (`1075`), Height (`1428`), Depth (`300`), Plinth height, Overhangs.
- **Grid Layout:** Columns (`3`), Rows (`4`), cell split / merge options.
- **Interactive Modules:** `+ двери` (single/double), `+ ящики`, `Большие ящики`, `Маленькие ящики`, `Сброс`, `Случайно`.
- **Material Selection:** >50 EGGER / MDF / Plywood swatches; dynamically updates textures.
- **Cart CTA:** `BASKET GO` linking to `/submit/`.

## Architectural Deductions
1. The 3D scene execution is managed entirely client-side via WebGL (geometry instancing/batching, triangle budgets, memory thresholds).
2. The UI does not reload the page when modifying dimensions, materials, or modules.
3. Pricing display is refreshed alongside configuration changes.

**Confidence:** FACT for DOM elements and WebGL metrics; UNKNOWN for async network transport during interaction without CDP DevTools.
