# FoodIQ — Source-to-Insight Provenance & Lineage Specification

## 1. Provenance Architecture
In traditional dashboards, financial numbers appear in isolated charts without verifiable source citations. In FoodIQ, **every single observation must be traceable to its original corporate disclosure**.

The provenance chain guarantees:
$$\text{Insight} \longrightarrow \text{MetricObservation} \longrightarrow \text{SourcePage} \longrightarrow \text{SourceDocument} \longrightarrow \text{SHA-256 Checksum}$$

---

## 2. Granular Provenance Model

Every row in `metric_observations` stores:
1. `source_document_id`: The authoritative filing key (e.g., `SWIGGY-Q2FY26`, `ETERNAL-Q1FY27`).
2. `source_page_id`: Physical PDF page identifier (e.g., `SWIGGY-Q2FY26-P05`).
3. `raw_source_value`: The unparsed string extracted directly from the PDF or OCR transcript (`"g281"`, `"27.5m"`, `"14797"`).
4. `verified_value`: The normalized numeric value after unit conversion and comparative cross-checking (`8281.0`, `27.5`, `14797.0`).
5. `observation_type`: Classification of data origin:
   - `REPORTED`: Explicitly stated in a primary financial table or statutory report.
   - `OCR_VERIFIED`: Extracted from raster images and verified against comparative disclosures.
   - `MANAGEMENT_ESTIMATE`: Cited in executive commentary or investor presentation charts.
   - `RESTATED`: Replaced or reconciled by subsequent filings.
6. `file_checksum_sha256`: 64-character SHA-256 cryptographic digest of the source PDF.

---

## 3. Provenance API & Inspection Endpoint

Lineage is accessible programmatically via:
```
GET /api/v1/observations/{observation_id}/lineage
```

### Sample Lineage Response:
```json
{
  "observation_id": "OBS-ETERNAL-Q2FY25-ETERNAL_FOOD-food_nov-v1",
  "company": {
    "id": "ETERNAL",
    "name": "Eternal Limited",
    "ticker": "ZOMATO"
  },
  "segment": {
    "id": "ETERNAL_FOOD",
    "name": "Food Delivery",
    "brand": "Zomato",
    "scope": "SEGMENT"
  },
  "metric": {
    "id": "eternal_food_nov",
    "value": 8281.0,
    "raw_source_value": "g281",
    "verified_value": 8281.0,
    "unit": "INR crore",
    "denominator_basis": "Reported in Annexure A",
    "observation_type": "OCR_VERIFIED",
    "validation_status": "RESTATED"
  },
  "time_period": {
    "fiscal_year": "FY25",
    "fiscal_quarter": "Q2",
    "period_end_date": "2024-09-30"
  },
  "provenance": {
    "source_document_id": "ETERNAL-Q2FY26",
    "original_file_name": "60824ca7-d07d-40a8-9e5d-5298e8eb5c4c.pdf",
    "file_checksum_sha256": "4b6842849e798f3bba5f2dd3e27a13dff608c0ef7343e74b33df5a6104e7fe9c",
    "total_pages": 38,
    "source_page_id": "ETERNAL-Q2FY26-P12",
    "pdf_page_number": 12,
    "printed_page_number": "10",
    "section_hint": "Annexure A",
    "has_raster_tables": true
  },
  "quality_flags": [
    {
      "flag_id": "DQ-ETERNAL-OCR-Q2FY25-food_nov",
      "issue_code": "OCR_CORRECTED_VIA_COMPARATIVE",
      "severity": "HIGH",
      "description": "Raw OCR 'g281' corrected to 8281.0",
      "audit_trail": "Raw OCR 'g281' (parsed as 281.0) corrected to 8281.0 using subsequent comparative table in Q2FY27/Q1FY27.",
      "is_resolved": true
    }
  ]
}
```
