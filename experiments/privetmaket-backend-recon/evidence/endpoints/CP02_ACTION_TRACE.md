# CP02 Action Trace

**Experiment:** `privetmaket-backend-recon`  
**Checkpoint:** `CP-02`  
**Execution date:** 2026-09-29 UTC  
**Scope:** Public anonymous interactions observed on `/shkaf` and catalog routes.

---

## Trace Matrix of Public Constructor Actions

| # | Action | UI Trigger / Control | Observed Network Consequence | Network Protocol / Method | Confidence |
|---|---|---|---|---|---|
| 1 | Initial constructor load | Direct navigation to `https://privetmaket.ru/shkaf` | Document load (`GET /shkaf`). Returns HTML document containing the 3D canvas container, WebGL metrics overlay, and parameter controls. | HTTPS GET (HTML) | FACT |
| 2 | Preset / template selection | Links to ready-made examples (e.g. `/877-tumba_pod_vinil/`, `/605-tumba_pod_akvarium_na_zakaz/`) | Document navigation (`GET /[id]-[slug]/`) with option to "открыть в конструкторе". Pre-populates 3D model state. | HTTPS GET (HTML) | FACT |
| 3 | Change dimension (width / height / depth) | Input fields: `Ширина: 1075`, `Высота: 1428`, `Глубина: 300` | Local DOM value update; triggers 3D canvas recalculation and FPS/draw call updates. In the absence of DevTools HAR, whether an async XHR/Fetch to a pricing endpoint is sent is UNVERIFIED. | Unknown (Client calculation or async Fetch) | UNKNOWN |
| 4 | Change material (body / front) | Select dropdown and swatch selector (e.g. `U708 ST9 EGGER 16mm`, `W1000 ST9`, etc.) | Swatch image update (`/uploads/images/minimini/...`). Whether price recalculation calls `/default/index/pricecache` or a client JS formula is UNVERIFIED. | Unknown (Client vs Server) | UNKNOWN |
| 5 | Module addition / layout change | Interactive buttons: `+ двери`, `+ ящики`, `Большие ящики`, `Сброс`, `Случайно` | Interactive 3D scene update. 3D performance stats monitor geometry, meshes, draw calls, and JS heap. No page reload. | Unknown (Likely client-side scene manipulation) | STRONG_INFERENCE |
| 6 | Price recalculation | Triggered by dimension, material, or module change | Price display updates dynamically near canvas (`BASKET GO`, `... ₽`). Client vs server calculation boundary cannot be confirmed without CDP DevTools inspection. | Unknown | UNKNOWN |
| 7 | Add to Basket (`BASKET GO`) | Click `BASKET GO` / `submit` | Target route `/submit/`. Unauthenticated cart page displays empty state or draft state. | HTTPS GET / POST to `/submit/` | STRONG_INFERENCE |

---

## Action-Level Findings

1. **Client-side scene responsiveness:** The constructor interface contains live 3D metrics counters (`Draw calls`, `Triangles`, `Geometries`, `Textures`, `Meshes visible`, `JS heap`), proving extensive client-side JavaScript execution and WebGL state management.
2. **Network detachment of geometric transforms:** Geometry rendering (draw calls, triangle counts, mesh visibility) happens entirely in-browser WebGL context without roundtripping 3D geometry from a remote server for each slider move.
3. **Pricing calculation boundary:** Whether the instant quote is evaluated by an embedded JavaScript formula (as described in the public documentation regarding area × markup) or requires an asynchronous HTTP request cannot be conclusively proven due to the lack of DevTools HAR capture.
