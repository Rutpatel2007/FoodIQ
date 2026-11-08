# FoodIQ Phase 6 — UI/UX Design System Specification

## 1. Design Philosophy

The FoodIQ Research Workstation is built for institutional buy-side and sell-side equity analysts, quantitative researchers, and corporate strategy teams. Its interface prioritizes:
- **Maximum Information Density:** Efficient multi-column grids, compact tabular rows, and clear data hierarchy.
- **Visual Ergonomics:** Deep dark-slate backgrounds reduce eye strain during prolonged financial modeling sessions.
- **Epistemic Clarity:** Rigorous visual distinction between reported facts, derived calculations, management explanations, and analyst assumptions.
- **Audit-First UX:** Every number displays its pedigree, formula, and source document citation upon click or hover.

---

## 2. Color System & Semantic Tokens

| Token | Hex Value | Semantic Usage |
| :--- | :--- | :--- |
| `--bg-base` | `#080b11` | Primary workstation background canvas |
| `--bg-surface` | `#0f172a` | Card containers, navigation headers, modal dialogs |
| `--bg-elevated` | `#1e293b` | Interactive controls, inputs, selected tabs, table headers |
| `--border-color` | `#334155` | Dividers, card boundaries, table cell borders |
| `--accent-cyan` | `#0ea5e9` | Primary focus accents, active tabs, metric highlights, primary series |
| `--accent-emerald` | `#10b981` | Positive delta, `DELIVERED` status, statistically significant badges |
| `--accent-amber` | `#f59e0b` | `PARTIALLY_DELIVERED`, Level 3 comparability, warnings |
| `--accent-rose` | `#f43f5e` | Negative delta, `MISSED` status, Level 4 blocked comparisons |
| `--accent-purple` | `#a855f7` | Secondary series (Swiggy), Monte Carlo distributions |
| `--text-primary` | `#f8fafc` | Primary titles, critical financial figures, active labels |
| `--text-secondary` | `#94a3b8` | Subheaders, metric units, descriptive body copy |
| `--text-muted` | `#64748b` | Footnotes, source page numbers, table metadata |

---

## 3. Typography & Numerical Formatting

- **Data Elements:** Monospace font stack (`'JetBrains Mono', 'Consolas', 'Menlo', monospace`) ensures vertical digit alignment across quarters and financial statements.
- **Header Elements:** Clean geometric sans-serif (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`).
- **Formatting Standards:**
  - Currency: Indian Rupee formatted with commas (e.g., `₹20,940 Cr`, `₹849,924 / store-day`).
  - Basis Points: Explicitly annotated with `bps` (e.g., `+242 bps`, `-54 bps`).
  - Percentages: Single decimal precision for standard metrics (`+22.0%`, `75.0%`); two decimal places for statistical significance (`p = 0.0482`).

---

## 4. UI Components

### 4.1 Global Command Header & Navigation Bar
- Workstation title, live clock, backend API health badge (`SYSTEM ONLINE`).
- 10 tab buttons with keyboard accessibility and active state indicators.
- Quick Workflow Bar with 5 one-click acceptance testing workflows (A through E).

### 4.2 Interactive Head-to-Head KPI Grid
- 5 comparative KPI cards (Food GOV, QC GOV, Dark Stores, Food Margin, QC Margin).
- Real-time delta calculation, winner badge, and comparability status badge.

### 4.3 Native HTML5 Vector Canvas Charting
- High-performance 2D canvas supporting multi-series line and bar plotting.
- Dynamic dual-axis auto-scaling, gridlines, quarter tick formatting, and interactive crosshair hover inspection.

### 4.4 Scenario Simulation Cockpit
- Multi-segment parameter input sliders and numeric controls.
- Parameter pedigree badges (`OLS`, `GUIDANCE`, `ASSUMPTION`).
- Base, Bull, and Bear preset loaders.
- Real-time financial output recomputation (<10ms).
- Monte Carlo distribution summary and persistent scenario save modal.

### 4.5 Audit Citation Modal & Sidecar Panels
- Clickable citation pills throughout all tables and findings.
- Inspects primary source document metadata, filing date, reporting quarter, physical page index, and extracted text snippet.
