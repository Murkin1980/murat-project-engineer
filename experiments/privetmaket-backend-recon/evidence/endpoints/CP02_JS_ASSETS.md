# CP02 JavaScript Assets & Client-Side Engine Analysis

**Experiment:** `privetmaket-backend-recon`  
**Checkpoint:** `CP-02`  
**Execution date:** 2026-09-29 UTC  

---

## 1. Observable Script & Asset Patterns

Direct script bundle names (e.g., hashed webpack/vite chunks like `app.c93f0b.js`) could not be read via raw HTTP response headers or DevTools HAR due to the sandbox execution environment constraints. However, direct DOM and interface analysis on `/shkaf` provides concrete architectural facts:

### 1.1 WebGL / 3D Engine Diagnostics
The constructor page `/shkaf` embeds a live 3D performance diagnostic dashboard directly in the user interface:
```text
3D perf: 0 fps
FPS avg: 0.0 (>= 55)
FPS low: 0.0 (>= 30)
Frame ms: 0.0 (<= 16.7)
Worst ms: 0.0 (<= 50)
Draw calls: 0 (<= 300)
Triangles: 0 (<= 500k)
Lines: 0 (<= 50k)
Points: 0 (<= 50k)
Geometries: 0 (<= 500)
Textures: 1 (<= 100)
Objects: 0 (<= 2000)
Meshes visible: 0 / 0 (<= 800)
Materials: 0 (<= 250)
DPR: 1.00 (<= 2)
JS heap: 27.1 MB (<= 256 MB)
```

**Technical implications:**
- **Engine Signature:** Metrics match standard Three.js / WebGL renderer info (`renderer.info.render.calls`, `renderer.info.memory.geometries`, `renderer.info.render.triangles`).
- **Memory & Draw Call Budgets:** Target thresholds (e.g. Draw calls <= 300, Triangles <= 500k, JS heap <= 256 MB, DPR <= 2) demonstrate production engineering for client-side WebGL performance, consistent with Three.js best practices for parametric furniture configurators.
- **Client Heap Footprint:** Initial JS heap footprint of ~27.1 MB indicates an in-memory scene graph and geometry generation engine running on the client.

### 1.2 Asset Organization
- Dynamic swatches and preview images are loaded from `/uploads/images/minimini/` and `/uploads/images/cropped-square_minimini/`.
- UI icons and control textures are loaded from `/public/images/` (e.g. `canvas-undo.png`, `open-door.png`, `subtype-no-limite.png`, `subtype-storage.png`, `subtype-square.png`, `subtype-wardrobe.png`, `help-door.gif`).

### 1.3 Unknowns
- Exact bundler (Webpack, Vite, Rollup, or legacy script tags).
- Exact script filenames (`/public/js/...`).
- Whether framework is Vanilla JS, React, Vue, or jQuery wrapper around Three.js.
