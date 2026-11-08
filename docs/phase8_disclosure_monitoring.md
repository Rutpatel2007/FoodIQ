# FoodIQ Phase 8 — Corporate Disclosure Monitoring Specification

## 1. Monitoring Purpose & Operating Scope

FoodIQ's Corporate Disclosure Monitoring System transforms the platform from a static historical database into an active, controlled financial intelligence system. It monitors official disclosures from:
- **BSE / NSE Statutory Announcements:** Quarterly financial results, board meeting outcomes, shareholding patterns.
- **Investor Relations Websites:** Eternal Limited (`blinkit.com/investor-relations`, `zomato.com/investor-relations`) and Swiggy Limited (`swiggy.com/investor-relations`).
- **Official Shareholder Letters & Earnings Presentations:** Quarterly letters, management commentary, call transcripts.
- **SEBI Regulatory Filings:** Red Herring Prospectus (RHP), Draft RHP (DRHP), Scheme of Amalgamation / Demerger filings.

---

## 2. Persistent Disclosure Register

Every discovered disclosure is indexed into the `disclosure_register` table in `data/foodiq.db`:

| Field | Type | Description |
| :--- | :--- | :--- |
| `disclosure_id` | TEXT PRIMARY KEY | Unique ID (e.g. `DISC-ETERNAL-Q2FY27-A1B2`) |
| `company_id` | TEXT NOT NULL | `ETERNAL` or `SWIGGY` |
| `document_title` | TEXT NOT NULL | Full title as disclosed |
| `document_category` | TEXT NOT NULL | `Shareholder Letter`, `Financial Results`, `Investor Presentation`, `IPO Prospectus` |
| `reporting_period` | TEXT NOT NULL | Standardized period (e.g. `Q2 FY27`, `FY26`) |
| `publication_date` | DATE | Official publication / release date |
| `source_url` | TEXT | Official BSE/NSE or IR URL |
| `original_file_location` | TEXT | Local archive path |
| `sha256_checksum` | TEXT NOT NULL | Cryptographic hash for deduplication |
| `processing_status` | TEXT NOT NULL | `DISCOVERED`, `RETRIEVED`, `EXTRACTED`, `PENDING_REVIEW`, `APPROVED`, `REJECTED` |
| `validation_status` | TEXT NOT NULL | `VALIDATED`, `WARNING`, `FAILED` |

---

## 3. Anticipated Filing Horizon & Missing Period Alerts

The monitoring dashboard tracks filing calendars and surfaces missing historical quarters or upcoming filings:
- **Quarterly Calendar:** Indian listed internet companies disclose quarterly results within 45 days of quarter end (Q1: mid-August, Q2: mid-November, Q3: mid-February, Q4: late May).
- **Upcoming Filings:** Tracks anticipated releases (e.g., Q3 FY27 anticipated February 2027) with readiness status `AWAITING_PUBLICATION`.
