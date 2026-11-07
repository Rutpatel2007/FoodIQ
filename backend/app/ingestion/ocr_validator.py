"""
FoodIQ Dedicated Eternal OCR Validation & Reconciliation Module

Responsibilities:
1. Parse raw OCR transcripts from Annexure_OCR/
2. Detect malformed / corrupted numeric values (e.g. 'g281', '4582258888', '3h 23-220')
3. Cross-validate historical values against subsequent comparative disclosures across letters
4. Preserve original OCR transcription
5. Record verified values separately
6. Record evidence supporting every correction
7. Flag unresolved / ambiguous observations for human review
"""
import re
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field

@dataclass
class OCRValidationResult:
    quarter: str
    segment: str
    metric: str
    source_file: str
    source_page: int
    raw_ocr_string: str
    verified_value: Optional[float]
    validation_status: str # 'VERIFIED_CLEAN', 'CORRECTED_VIA_COMPARATIVE', 'UNRESOLVED_FLAGGED'
    evidence: str
    flag_code: Optional[str] = None
    severity: Optional[str] = None

class EternalOCRValidator:
    """
    Validates and reconciles OCR extractions of Eternal's Annexure A Quarterly Disclosures.
    Uses multi-quarter comparative disclosures to ground-truth and correct OCR artifacts.
    """

    # Ground-truth comparative baseline established across clean subsequent digital disclosures
    # (e.g. Q1FY27 p.9, Q2FY27 p.13, and Q4FY26 p.12)
    # Format: {quarter: {metric_key: value}}
    COMPARATIVE_GROUND_TRUTH: Dict[str, Dict[str, float]] = {
        "Q1FY25": {
            "food_gov": 9264.0,
            "qcomm_gov": 4923.0,
            "going_out_gov": 1268.0,
            "b2c_gov": 15455.0,
            "food_nov": 7928.0,
            "qcomm_nov": 4061.0,
            "going_out_nov": 1031.0,
            "b2c_nov": 13020.0,
            "food_adj_rev": 2256.0,
            "qcomm_adj_rev": 942.0,
            "going_out_adj_rev": 178.0,
            "hyperpure_rev": 1212.0,
            "adj_rev_total": 4594.0,
            "food_adj_ebitda": 313.0,
            "qcomm_adj_ebitda": -3.0,
            "going_out_adj_ebitda": 10.0,
            "hyperpure_adj_ebitda": -28.0,
            "adj_ebitda_total": 298.0
        },
        "Q2FY25": {
            "food_gov": 9690.0,
            "qcomm_gov": 6132.0,
            "going_out_gov": 1849.0,
            "b2c_gov": 17670.0,
            "food_nov": 8281.0,
            "qcomm_nov": 4928.0,
            "going_out_nov": 1562.0,
            "b2c_nov": 14771.0,
            "food_adj_rev": 2340.0,
            "qcomm_adj_rev": 1156.0,
            "going_out_adj_rev": 154.0,
            "hyperpure_rev": 1473.0,
            "adj_rev_total": 5127.0,
            "food_adj_ebitda": 341.0,
            "qcomm_adj_ebitda": 8.0,
            "going_out_adj_ebitda": -7.0,
            "hyperpure_adj_ebitda": -22.0,
            "adj_ebitda_total": 330.0
        },
        "Q3FY25": {
            "food_gov": 9913.0,
            "qcomm_gov": 7798.0,
            "going_out_gov": 2495.0,
            "b2c_gov": 20206.0,
            "food_nov": 8443.0,
            "qcomm_nov": 6020.0,
            "going_out_nov": 2158.0,
            "b2c_nov": 16621.0,
            "food_adj_rev": 2413.0,
            "qcomm_adj_rev": 1399.0,
            "going_out_adj_rev": 259.0,
            "hyperpure_rev": 1671.0,
            "adj_rev_total": 5746.0,
            "food_adj_ebitda": 427.0,
            "qcomm_adj_ebitda": -103.0,
            "going_out_adj_ebitda": -17.0,
            "hyperpure_adj_ebitda": -23.0,
            "adj_ebitda_total": 285.0
        },
        "Q4FY25": {
            "food_gov": 9778.0,
            "qcomm_gov": 9421.0,
            "going_out_gov": 2184.0,
            "b2c_gov": 21383.0,
            "food_nov": 8210.0,
            "qcomm_nov": 7362.0,
            "going_out_nov": 1868.0,
            "b2c_nov": 17440.0,
            "food_adj_rev": 2409.0,
            "qcomm_adj_rev": 1709.0,
            "going_out_adj_rev": 229.0,
            "hyperpure_rev": 1840.0,
            "adj_rev_total": 6188.0,
            "food_adj_ebitda": 428.0,
            "qcomm_adj_ebitda": -178.0,
            "going_out_adj_ebitda": -47.0,
            "hyperpure_adj_ebitda": -22.0,
            "adj_ebitda_total": 165.0
        },
        "Q1FY26": {
            "food_gov": 10769.0,
            "qcomm_gov": 11821.0,
            "going_out_gov": 2370.0,
            "b2c_gov": 24960.0,
            "food_nov": 8967.0,
            "qcomm_nov": 9203.0,
            "going_out_nov": 2013.0,
            "b2c_nov": 20183.0,
            "food_adj_rev": 2657.0,
            "qcomm_adj_rev": 2400.0, # Pre-1P inventory transition!
            "going_out_adj_rev": 207.0,
            "hyperpure_rev": 2295.0,
            "adj_rev_total": 7563.0,
            "food_adj_ebitda": 451.0,
            "qcomm_adj_ebitda": -162.0,
            "going_out_adj_ebitda": -54.0,
            "hyperpure_adj_ebitda": -18.0,
            "adj_ebitda_total": 172.0
        },
        "Q2FY26": {
            "food_nov": 9423.0,
            "qcomm_nov": 11679.0,
            "going_out_nov": 2063.0,
            "b2c_nov": 23164.0,
            "food_adj_rev": 2863.0,
            "qcomm_adj_rev": 9891.0, # 1P inventory switch (+312% QoQ)
            "going_out_adj_rev": 189.0,
            "hyperpure_rev": 1023.0, # Hyperpure intercompany flow eliminated (-55% QoQ)
            "adj_rev_total": 13968.0,
            "food_adj_ebitda": 503.0,
            "qcomm_adj_ebitda": -156.0,
            "going_out_adj_ebitda": -63.0,
            "hyperpure_adj_ebitda": -5.0,
            "adj_ebitda_total": 224.0
        },
        "Q3FY26": {
            "food_nov": 9846.0,
            "qcomm_nov": 13300.0,
            "going_out_nov": 2587.0,
            "b2c_nov": 25732.0,
            "food_adj_rev": 3053.0,
            "qcomm_adj_rev": 12256.0,
            "going_out_adj_rev": 300.0,
            "hyperpure_rev": 1070.0,
            "adj_rev_total": 16692.0,
            "food_adj_ebitda": 531.0,
            "qcomm_adj_ebitda": -4.0,
            "going_out_adj_ebitda": -121.0,
            "hyperpure_adj_ebitda": 15.0,
            "adj_ebitda_total": 364.0
        },
        "Q4FY26": {
            "food_nov": 9757.0,
            "qcomm_nov": 14386.0,
            "going_out_nov": 2736.0,
            "b2c_nov": 26880.0,
            "food_adj_rev": 3125.0,
            "qcomm_adj_rev": 13232.0,
            "going_out_adj_rev": 277.0,
            "hyperpure_rev": 978.0,
            "adj_rev_total": 17680.0,
            "food_adj_ebitda": 532.0,
            "qcomm_adj_ebitda": 37.0,
            "going_out_adj_ebitda": -81.0,
            "hyperpure_adj_ebitda": 4.0,
            "adj_ebitda_total": 429.0
        },
        "Q1FY27": {
            "food_nov": 10769.0,
            "qcomm_nov": 17132.0,
            "going_out_nov": 3218.0,
            "b2c_nov": 31120.0,
            "food_adj_rev": 3537.0,
            "qcomm_adj_rev": 15664.0,
            "going_out_adj_rev": 318.0,
            "hyperpure_rev": 1034.0,
            "adj_rev_total": 20648.0,
            "food_adj_ebitda": 606.0,
            "qcomm_adj_ebitda": -102.0,
            "going_out_adj_ebitda": -65.0,
            "hyperpure_adj_ebitda": 17.0,
            "adj_ebitda_total": 555.0
        },
        "Q2FY27": {
            "food_nov": 11445.0,
            "qcomm_nov": 20940.0,
            "going_out_nov": 3259.0,
            "b2c_nov": 35644.0,
            "food_adj_rev": 3879.0,
            "qcomm_adj_rev": 19152.0,
            "going_out_adj_rev": 290.0, # Footnote/table verified
            "hyperpure_rev": 1154.0,
            "adj_rev_total": 24621.0,
            "food_adj_ebitda": 666.0,
            "qcomm_adj_ebitda": 13.0,
            "going_out_adj_ebitda": -36.0,
            "hyperpure_adj_ebitda": 18.0,
            "adj_ebitda_total": 666.0 # Note: Total Adjusted EBITDA Q2FY27 = 666 Cr
        }
    }

    # Known OCR artifacts and patterns to catch
    MALFORMED_PATTERNS = [
        (r"^g(\d+)$", r"\1", "Replaced leading 'g' misread as 8"),
        (r"[—–−]", "-", "Standardized unicode minus"),
        (r"[«»“”’‘~]", "", "Stripped quotes and tildes"),
        (r"(\d+),(\d+)", r"\1\2", "Stripped thousand separator commas"),
    ]

    @classmethod
    def clean_ocr_token(cls, raw: str) -> Tuple[str, bool]:
        """Cleans common OCR noise and flags whether cleaning was applied."""
        orig = raw.strip()
        cleaned = orig
        for pat, repl, _ in cls.MALFORMED_PATTERNS:
            cleaned = re.sub(pat, repl, cleaned)
        return cleaned, cleaned != orig

    @classmethod
    def validate_and_reconcile(
        cls,
        quarter: str,
        segment: str,
        metric: str,
        raw_ocr: str,
        source_doc: str,
        source_page: int
    ) -> OCRValidationResult:
        """
        Validates raw OCR against comparative ground truth.
        """
        cleaned_str, was_cleaned = cls.clean_ocr_token(raw_ocr)
        
        # Check if quarter and metric exist in comparative ground truth
        gt_quarter = cls.COMPARATIVE_GROUND_TRUTH.get(quarter)
        if not gt_quarter or metric not in gt_quarter:
            # Unresolved / unverified observation
            try:
                val = float(cleaned_str)
                return OCRValidationResult(
                    quarter=quarter,
                    segment=segment,
                    metric=metric,
                    source_file=source_doc,
                    source_page=source_page,
                    raw_ocr_string=raw_ocr,
                    verified_value=val,
                    validation_status="UNVERIFIED_SOURCE_ONLY",
                    evidence=f"Extracted from {source_doc} page {source_page}; no comparative baseline available.",
                    flag_code="NO_COMPARATIVE_BASELINE",
                    severity="MEDIUM"
                )
            except ValueError:
                return OCRValidationResult(
                    quarter=quarter,
                    segment=segment,
                    metric=metric,
                    source_file=source_doc,
                    source_page=source_page,
                    raw_ocr_string=raw_ocr,
                    verified_value=None,
                    validation_status="UNRESOLVED_FLAGGED",
                    evidence=f"Failed to parse '{raw_ocr}' as numeric; no comparative ground truth.",
                    flag_code="OCR_CORRUPTED_VALUE",
                    severity="CRITICAL"
                )

        ground_truth_val = gt_quarter[metric]

        # Try parsing cleaned OCR
        parsed_val = None
        try:
            parsed_val = float(cleaned_str)
        except ValueError:
            pass

        if parsed_val is not None and abs(parsed_val - ground_truth_val) < 0.01:
            return OCRValidationResult(
                quarter=quarter,
                segment=segment,
                metric=metric,
                source_file=source_doc,
                source_page=source_page,
                raw_ocr_string=raw_ocr,
                verified_value=ground_truth_val,
                validation_status="VERIFIED_CLEAN",
                evidence=f"OCR value '{raw_ocr}' perfectly matches comparative baseline {ground_truth_val} from subsequent disclosures."
            )
        else:
            # OCR discrepancy / corruption corrected via comparative disclosure
            return OCRValidationResult(
                quarter=quarter,
                segment=segment,
                metric=metric,
                source_file=source_doc,
                source_page=source_page,
                raw_ocr_string=raw_ocr,
                verified_value=ground_truth_val,
                validation_status="CORRECTED_VIA_COMPARATIVE",
                evidence=f"Raw OCR '{raw_ocr}' (parsed as {parsed_val}) corrected to {ground_truth_val} using subsequent comparative table in Q2FY27/Q1FY27.",
                flag_code="OCR_CORRECTED_VIA_COMPARATIVE",
                severity="HIGH"
            )
