# EXP-S2C-01 — Frozen Reference Fixture

## Source Metadata
- **Source Project**: `Murkin1980/salamat-projects-dashboard`
- **Route / URL Class**: `/` (Main portfolio/dashboard screen at root route `http://localhost:4173/`, Triage view)
- **Capture Timestamp**: `2026-10-10T08:46:00Z`
- **Capture Environment**: Headless Chromium (`@sparticuz/chromium` v153.0.0 via Puppeteer Core)

## Viewport Definitions
1. **Desktop Viewport**:
   - Resolution: `1280 × 800` px
   - Device Scale Factor: `1.0`
   - Path: `experiments/exp-s2c-01/reference/desktop.png`
   - SHA256: `534979a87ca7445a1c4c1c10debf133b1971a2a9ed9e568eee913cbc2e86fb7f`

2. **Mobile Viewport**:
   - Resolution: `390 × 844` px (iPhone 12/13/14 form factor, touch enabled)
   - Device Scale Factor: `1.0`
   - Path: `experiments/exp-s2c-01/reference/mobile.png`
   - SHA256: `380ffe157b6889860ed9b369df3423c79fabf58db4ca9335815fba06898db810`

## Dynamic / Variable Content Notice
- Time badge ("Обновлено 08:46"): timestamp indicates render/poll time. The numerical string may vary with clock or remain static fixture time; reconstruction targets the visual layout and text.
- No third-party network assets or auth required.
- Excluded regions: None. Entire screen viewport captured.

## Anti-Cheating Boundary Verification
- The target repository was used solely to start the production preview build (`npm run preview` on port 4173) to capture these two screenshots.
- No component source files, CSS rules, Tailwind configs, DOM structures, or design tokens from `salamat-projects-dashboard` were inspected or copied.
- Both reconstruction arms (Arm A baseline and Arm B candidate) will be constructed strictly from these reference screenshots.
