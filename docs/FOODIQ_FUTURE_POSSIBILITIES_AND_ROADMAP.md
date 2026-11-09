# FOODIQ — Future Possibilities & Strategic Product Roadmap
**Document Reference:** `FOODIQ-ROADMAP-2026-11`  
**Planning Horizons:** Horizon 1 (Months 1–6), Horizon 2 (Months 6–18), Horizon 3 (Years 2–5)  
**Product Strategy Focus:** Scaling from a Specialized Duopoly Research Workstation into an Enterprise Consumer-Internet Financial Intelligence Platform

---

## 1. Product Evolution Vision (1, 3, and 5 Years)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               FOODIQ FIVE-YEAR ROADMAP                                 │
├─────────────────────┬────────────────────────────────┬─────────────────────────────────┤
│ Year 1 (Current +)  │ Year 3 (Expansion)             │ Year 5 (Institutional Standard) │
├─────────────────────┼────────────────────────────────┼─────────────────────────────────┤
│ Indian Platform     │ Multi-Sector Platform Economy  │ Global Platform Terminal        │
│ Duopoly Engine      │ (Ride-Hailing, FinTech, E-Com) │ (India, SEA, MENA, LatAm)       │
│ Eternal vs. Swiggy  │ + Zepto, Ola, Uber, Nykaa      │ Cross-Border Benchmarking       │
│ Zero-Residual Decomp│ Automated SEBI/BSE Ingestion   │ Real-Time Delivery Tracking     │
│ Workstation UI      │ Multi-User Team Collaboration  │ Enterprise Quantitative API     │
└─────────────────────┴────────────────────────────────┴─────────────────────────────────┘
```

---

## 2. Structured Feature Opportunity Matrix (30 Enhancements)

| ID | Enhancement Name | Category | User Problem Solved | Priority | Complexity | Effort |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **OPP-01** | Global Search Keyword Highlight | Quick Win | Enhances visibility of matches in data tables. | HIGH | LOW | 1 day |
| **OPP-02** | CSV Raw Table Export Button | Quick Win | Analysts require immediate Excel tabular exports. | HIGH | LOW | 2 days |
| **OPP-03** | Canvas PNG Download Pill | Quick Win | Allows copying high-res charts into presentations. | MEDIUM | LOW | 1 day |
| **OPP-04** | Tooltip Pinning & Snapshot | Quick Win | Freezes hover tooltips for side-by-side reading. | LOW | LOW | 1 day |
| **OPP-05** | Filter State in URL Query Params | Quick Win | Enables bookmarking and sharing filtered views. | HIGH | LOW | 2 days |
| **OPP-06** | Dark/Light Terminal Theme Toggle | Quick Win | Accommodates varied lighting environments. | LOW | LOW | 2 days |
| **OPP-07** | Keyboard Shortcuts (Alt+1..0) | Quick Win | Speeds up power-analyst workspace switching. | MEDIUM | LOW | 1 day |
| **OPP-08** | In-Browser PDF Coordinate Viewer | High-Value | Displays physical PDF page with bounding box box. | HIGH | MEDIUM | 1 week |
| **OPP-09** | Zepto IPO Ingestion Engine | High-Value | Incorporates upcoming Zepto disclosures into QComm. | CRITICAL | MEDIUM | 2 weeks |
| **OPP-10** | Free Cash Flow & Working Capital | High-Value | Models payables to restaurants and inventory float. | HIGH | MEDIUM | 1.5 weeks |
| **OPP-11** | ESOP Dilution & Normalized EPS | High-Value | Adjusts headline EBITDA for share-based payments. | HIGH | MEDIUM | 1 week |
| **OPP-12** | Interactive Waterfall Builder | High-Value | Allows custom multi-quarter starting and end dates. | HIGH | MEDIUM | 1.5 weeks |
| **OPP-13** | Multi-Scenario Comparison Overlay| High-Value | Plots Base vs. Conservative vs. Optimistic lines. | HIGH | MEDIUM | 1 week |
| **OPP-14** | Automated PDF Ingestion Watcher | High-Value | Automatically parses new filings dropped into dir. | HIGH | MEDIUM | 2 weeks |
| **OPP-15** | Role-Based Access Control (RBAC)| High-Value | Multi-user authentication for buy-side firms. | HIGH | MEDIUM | 2 weeks |
| **OPP-16** | Vector-Embedded Natural Language | Major Capability| Ask questions with strict citation gating. | HIGH | HIGH | 3 weeks |
| **OPP-17** | Automated Quarterly Result Alerts| Major Capability| Slack/Email webhook notifications on new filing. | MEDIUM | MEDIUM | 1.5 weeks |
| **OPP-18** | Dineout vs. District Deep Dive | Major Capability| Dedicated entertainment and ticketing analytics. | MEDIUM | MEDIUM | 2 weeks |
| **OPP-19** | Hyperpure B2B Economics Core | Major Capability| Gross margin tracking for B2B supply logistics. | MEDIUM | MEDIUM | 2 weeks |
| **OPP-20** | Forward Guidance Consensus Deck | Major Capability| Blends management targets with sell-side estimates. | MEDIUM | HIGH | 3 weeks |
| **OPP-21** | Structural Break Auto-Chow Test | Major Capability| Continuously scans time series for regime breaks. | MEDIUM | MEDIUM | 2 weeks |
| **OPP-22** | Monte Carlo Volatility Estimator| Major Capability| Auto-calibrates bounds from historical variance. | MEDIUM | MEDIUM | 1.5 weeks |
| **OPP-23** | Enterprise API Gateway (GraphQL)| Major Capability| Provides programmatic query access for quant funds. | HIGH | HIGH | 4 weeks |
| **OPP-24** | Automated Docx Research Note | Major Capability| 1-click export formatted to broker research style. | HIGH | MEDIUM | 2 weeks |
| **OPP-25** | Ride-Hailing Module (Ola/Uber) | Long-Term | Extends platform architecture to mobility sector. | LOW | HIGH | 8 weeks |
| **OPP-26** | SEA Duopoly (Grab vs. GoTo) | Long-Term | Replicates FoodIQ model in Southeast Asia. | LOW | HIGH | 10 weeks |
| **OPP-27** | Real-Time Delivery Fleet Tracker| Long-Term | Ingests app telemetry to track wait times. | LOW | VERY HIGH| 12 weeks |
| **OPP-28** | Collaborative Annotations System| Long-Term | Analysts leave shared margin notes on data cells. | MEDIUM | MEDIUM | 3 weeks |
| **OPP-29** | Micro-Market City Level Matrix | Experimental | Synthetic decomposition of Tier 1 vs 2 cities. | LOW | HIGH | 6 weeks |
| **OPP-30** | Algorithmic Guidance Bull/Bear | Experimental | Automated NLP tone analysis of earnings transcripts. | LOW | MEDIUM | 3 weeks |

---

## 3. What Should NOT Be Built (Anti-Roadmap & Discipline)

To preserve FoodIQ's institutional authority, the following features are **explicitly rejected**:
1. **Unverified Web-Scraped Store Counts:** Third-party web scraping of consumer apps generates high noise and phantom store counts. FoodIQ must remain anchored to audited statutory disclosures.
2. **Arbitrary Algorithmic "Health" Scores:** Single aggregated "Scores" (e.g. 78/100) that blend unrelated ratios without mathematical definitions undermine credibility with institutional investors.
3. **Black-Box AI Price Predictors:** AI models predicting daily stock prices create legal liability and violate quantitative research standards.
4. **Direct Level-4 Incomparable Operations:** Direct subtraction of Blinkit 1P gross revenue from Swiggy 3P net commissions must remain permanently blocked.
