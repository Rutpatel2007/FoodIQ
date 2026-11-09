# FOODIQ — Master Project Intelligence Dossier
**Document Reference:** `FOODIQ-INTEL-MASTER-2026-11`  
**Security & Access Classification:** Institutional Research & Corporate Intelligence  
**Target Universe:** Duopoly Analysis of **Eternal Limited** (Zomato/Blinkit/District/Hyperpure) and **Swiggy Limited** (Food Delivery/Instamart/Dineout/Supply Chain)  
**Verification Standard:** 100% Primary Statutory Filing Anchored (`data/foodiq.db` via SHA-256 Provenance & Coordinate Lineage)

---

## 1. What Exactly is FoodIQ?

### 1.1 Category Definition & Identity
FoodIQ is an **Institutional Corporate Financial Intelligence Platform, Quantitative Econometric Engine, and Research Workstation**. It is not a generic stock screener, a basic web dashboard, or a static financial database. It represents a purpose-built domain intelligence system designed to ingest, normalize, reconcile, and rigorously analyze statutory corporate disclosures from complex platform economies, specifically focusing on the Indian Food Delivery and Quick Commerce duopoly: **Eternal Limited** (NSE: `ETERNAL` / BSE: `543320`) and **Swiggy Limited** (NSE: `SWIGGY` / BSE: `544280`).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FOODIQ PRODUCT IDENTITY                            │
├───────────────────────────┬─────────────────────────────────────────────────┤
│ Software Category         │ Institutional Financial & Competitive Intel     │
├───────────────────────────┼─────────────────────────────────────────────────┤
│ Target Sector             │ Platform Internet, Food Delivery, Quick Commerce│
├───────────────────────────┼─────────────────────────────────────────────────┤
│ Underpinning Philosophy   │ Zero-Synthetic Provenance & Structural Integrity│
├───────────────────────────┼─────────────────────────────────────────────────┤
│ Data Pedigree             │ 14 Primary Filings, 509 Verified Pages, 570 Obs │
├───────────────────────────┼─────────────────────────────────────────────────┤
│ Engine Stack              │ FastAPI REST Core, SQLite RDBMS, Vector Canvas  │
└───────────────────────────┴─────────────────────────────────────────────────┘
```

### 1.2 Multi-Tier Product Explanations

#### In One Sentence:
> **FoodIQ is an institutional financial intelligence workstation that transforms complex, non-standardized statutory corporate disclosures from Eternal and Swiggy into mathematically normalized, structurally consistent, and fully auditable competitive analytics.**

#### In One Paragraph:
> FoodIQ resolves the pervasive asymmetry and comparability breakdown in Indian consumer-internet financial research. While platforms like Eternal and Swiggy disclose non-standard operational and financial metrics (Gross Order Value vs. Net Order Value, 1P gross inventory accounting vs. 3P marketplace take rates, and fluctuating segmental boundaries), FoodIQ ingests primary PDFs with bounding-box OCR coordinate precision, enforces four-tier comparability rules, calculates exact zero-residual waterfall growth decompositions, evaluates forward-looking management guidance delivery, and models unit-economic break-evens through empirical econometric elasticities.

#### The 30-Second Elevator Pitch:
> "If you analyze Zomato and Swiggy today, you are comparing apples to elephants. Blinkit reports gross merchandise value under 1P inventory principles where headline revenue jumped +128% overnight without a single extra order, while Swiggy Instamart reports net marketplace commission. Standard financial dashboards blind-subtract these numbers, generating completely false market share figures. FoodIQ is the only platform that normalizes these accounting structural breaks, links every single number to physical PDF coordinates, and gives institutional research analysts mathematically defensible competitive and econometric models."

#### The Two-Minute Institutional Briefing:
> "Analyzing listed platform duopolies in emerging markets presents three critical institutional bottlenecks:
> 1. **Accounting Incomparability:** Corporate restructuring and Ind AS 115 revenue recognition pivots create artificial surges and distorted spreads. For instance, Swiggy reports Food Delivery GOV while Eternal reports Food Delivery GOV alongside Quick Commerce Net Order Value (NOV). Direct comparison without normalization is invalid under accounting standards.
> 2. **Lack of Provenance:** Financial terminals often display aggregated numbers without identifying whether a metric was a primary statutory filing fact, an analyst projection, or a management conference-call remark.
> 3. **Superficial Metrics:** Most models look at top-line growth without isolating basket size inflation (AOV) from true volume (order expansion).
> 
> FoodIQ eliminates these risks. It establishes an immutable 24-table relational warehouse seeded with 570 audited observations across 14 primary filings from Q1 FY25 to Q2 FY27. It features a strict Four-Tier Comparability Framework that programmatically blocks misleading mathematical operations. It powers 21 specialized analytics modules that calculate exact waterfall volume-price decompositions, track 26 strategic management commitments with objective scoring criteria, execute 10 econometric studies with Benjamini-Hochberg FDR control, and project forward margins via bounded Monte Carlo simulations."

#### The Five-Minute Technical Explanation:
> "FoodIQ is engineered as a zero-dependency, high-throughput financial computing system:
> - **Data Foundation:** SQLite database (`data/foodiq.db`) structured across 24 normalized tables. It enforces referential integrity, check constraints, foreign keys, and strict semantic separation between `NULL` (undisclosed data point) and `0.0` (zero value). Every observation contains a SHA-256 content checksum, physical document identifier, physical PDF page index, table coordinate bounding box, and extraction confidence score.
> - **Backend Micro-Kernel:** Built on Python 3.12 and FastAPI (`backend/app/main.py`), exposing 81 RESTful API endpoints across 17 distinct routers. Core analytics are executed through 21 specialized engine modules in `backend/app/analytics/`.
> - **Financial Decomposition Core:** Employs an exact additive identity:
>   $$\Delta \text{NOV} = (\Delta Q \cdot P_0) + (Q_0 \cdot \Delta P) + (\Delta Q \cdot \Delta P)$$
>   This formula guarantees zero unallocated residual across all historical intervals within publication rounding ($\le \pm ₹1.0\text{ Cr}$).
> - **Econometric & Statistical Engine:** Conducts 10 rigorous relationship studies. It implements first-difference detrending to prevent spurious time-series correlations and applies the Benjamini-Hochberg procedure to enforce False Discovery Rate (FDR) control at $\alpha = 0.05$.
> - **Frontend Research Workstation:** Implemented in pure ES6 Vanilla JavaScript, CSS3, and HTML5. It renders dynamic dual-axis financial charts directly onto vector `<canvas>` elements without external charting libraries, dynamically fetching period-filtered disclosures, enabling cross-metric lineaging, and executing 5 end-to-end analytical workflows across desktop, laptop, tablet, and mobile viewports."

#### The Industry-Professional & Investor Explanation:
> "For buy-side portfolio managers, equity research analysts, and corporate development heads, FoodIQ provides investment-grade signal extraction. It proves, for example, that Swiggy's Food Delivery EBITDA margin spread against Eternal narrowed from 315 bps in Q1 FY25 to 242 bps in Q2 FY27—a +73 bps competitive gain. It proves that Blinkit's blended daily store throughput has reached ₹849,924 / store-day across 2,700 stores, with mature cohorts generating over ₹10–12 lakh/day. Most importantly, it calculates that Swiggy Instamart requires an AOV threshold of exactly ₹813.20 (vs. ₹467 actual) to achieve contribution margin breakeven under current cost structures, enabling investors to underwrite valuation multiples against verifiable operating milestones."

---

## 2. The Core Problem FoodIQ Solves

### 2.1 The Multi-Layer Problem Matrix

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PRIMARY RESEARCH CHALLENGES & RESOLUTIONS                       │
├────────────────────────────┬───────────────────────────────────────────────────────────┤
│ Disclosed Challenge        │ FoodIQ Algorithmic Resolution                             │
├────────────────────────────┼───────────────────────────────────────────────────────────┤
│ Non-standard Top-Line      │ Normalizes GOV, NOV, Gross Revenue, and Net Commission   │
│ Definitions (GOV vs. NOV)  │ into audited comparability tiers (Level 1 to Level 4).    │
├────────────────────────────┼───────────────────────────────────────────────────────────┤
│ Ind AS 115 1P Inventory    │ Identifies structural break in Q2 FY26 (Blinkit); blocks   │
│ Accounting Shift           │ direct historical revenue comparisons; isolates NOV flow. │
├────────────────────────────┼───────────────────────────────────────────────────────────┤
│ M&A Perimeter Shifts       │ Isolates organic vs. inorganic growth (Paytm/District      │
│ (District/Paytm & Lynks)   │ ticketing acquisition; Swiggy Lynks logistics divestment).│
├────────────────────────────┼───────────────────────────────────────────────────────────┤
│ Variable vs. Fixed Loss    │ Reconciles Instamart -1.0% CM (-₹92.3 Cr) vs.             │
│ Conflation in Disclosures  │ Segment Adjusted EBITDA Loss of -9.7% (-₹895.0 Cr).       │
├────────────────────────────┼───────────────────────────────────────────────────────────┤
│ Spurious Correlation in    │ Applies first-difference detrending; proves AOV growth    │
│ Platform Time Series       │ does not synchronously cause contribution margin jumps.   │
├────────────────────────────┼───────────────────────────────────────────────────────────┤
│ Unaudited Forward Guidance │ Scorecard engine tracks 26 forward management commitments │
│ and Narrative Drift        │ with strict denominator isolation for unexpired targets.  │
└────────────────────────────┴───────────────────────────────────────────────────────────┘
```

---

## 3. The Intended Users

1. **Equity Research Analysts (Sell-Side):**
   - Need exact, defensible numbers for quarterly earnings notes and Initiation of Coverage reports.
   - Use FoodIQ to generate instant Waterfall Decompositions and download audit packs with page citations.
2. **Institutional Investors & Fund Managers (Buy-Side):**
   - Underwriting capital allocation between Zomato and Swiggy.
   - Use the Scenario Lab and Monte Carlo simulation to evaluate margin breakeven probabilities.
3. **Strategy Consultants & Corporate Development Teams:**
   - Benchmarking store expansion rates, dark store throughput density, and take rate elasticity.
   - Use the Management Credibility Engine to track corporate execution consistency.
4. **Academic Researchers & Econometricians:**
   - Investigating duopoly platform behavior, network density externalities, and two-sided market pricing power.
   - Use the 10 quantitative research studies with Benjamini-Hochberg FDR corrected outputs.
