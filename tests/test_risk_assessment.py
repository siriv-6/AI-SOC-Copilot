import sys

sys.path.insert(0, ".")

from backend.services.risk_assessment_service import (
    RiskAssessmentService
)


print("=" * 70)
print("STEP 40 - SECURITY RISK ASSESSMENT TEST")
print("=" * 70)


# ============================================================
# INITIALIZE SERVICE
# ============================================================

print("\nInitializing Risk Assessment Service...")

risk_service = RiskAssessmentService()

print("Risk Assessment Service initialized successfully.")


# ============================================================
# TEST 1 - BENIGN ALERT
# ============================================================

print("\n" + "-" * 70)
print("TEST 1 - BENIGN ALERT")
print("-" * 70)

benign_mitre = {
    "mapped": False,
    "tactic": None,
    "technique_id": None,
    "technique": "No MITRE ATT&CK technique"
}

benign_result = risk_service.assess_risk(
    rule_level=5,
    predicted_label="BENIGN",
    confidence=100.0,
    mitre_mapping=benign_mitre
)

print("Predicted Label:", benign_result["predicted_label"])
print("Confidence:", benign_result["ml_confidence"], "%")
print("Risk Level:", benign_result["risk_level"])
print("Risk Score:", benign_result["risk_score"])
print("MITRE Mapped:", benign_result["mitre_mapped"])
print("Description:", benign_result["description"])

assert benign_result["risk_level"] == "LOW"

print("Benign risk assessment validation: PASSED")


# ============================================================
# TEST 2 - HIGH-RISK ATTACK
# ============================================================

print("\n" + "-" * 70)
print("TEST 2 - HIGH-RISK ATTACK")
print("-" * 70)

attack_mitre = {
    "mapped": True,
    "tactic": "Discovery",
    "technique_id": "T1046",
    "technique": "Network Service Scanning"
}

attack_result = risk_service.assess_risk(
    rule_level=12,
    predicted_label="PortScan",
    confidence=95.0,
    mitre_mapping=attack_mitre
)

print("Predicted Label:", attack_result["predicted_label"])
print("Confidence:", attack_result["ml_confidence"], "%")
print("Risk Level:", attack_result["risk_level"])
print("Risk Score:", attack_result["risk_score"])
print("MITRE Mapped:", attack_result["mitre_mapped"])
print("Description:", attack_result["description"])

assert attack_result["risk_level"] == "HIGH"

assert attack_result["mitre_mapped"] is True

assert attack_result["risk_score"] > 0

print("High-risk assessment validation: PASSED")


# ============================================================
# TEST 3 - MEDIUM-RISK ACTIVITY
# ============================================================

print("\n" + "-" * 70)
print("TEST 3 - MEDIUM-RISK ACTIVITY")
print("-" * 70)

medium_mitre = {
    "mapped": True,
    "tactic": "Discovery",
    "technique_id": "T1046",
    "technique": "Network Service Scanning"
}

medium_result = risk_service.assess_risk(
    rule_level=7,
    predicted_label="PortScan",
    confidence=55.0,
    mitre_mapping=medium_mitre
)

print("Predicted Label:", medium_result["predicted_label"])
print("Confidence:", medium_result["ml_confidence"], "%")
print("Risk Level:", medium_result["risk_level"])
print("Risk Score:", medium_result["risk_score"])
print("MITRE Mapped:", medium_result["mitre_mapped"])
print("Description:", medium_result["description"])

assert medium_result["risk_level"] == "MEDIUM"

print("Medium-risk assessment validation: PASSED")


# ============================================================
# FINAL VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("STEP 40 RISK ASSESSMENT TEST SUCCESSFUL")
print("=" * 70)

print("\nVerified:")

print("BENIGN activity -> LOW risk")

print("High-confidence attack -> HIGH risk")

print("Moderate suspicious activity -> MEDIUM risk")

print("MITRE mapping included in risk assessment")

print("Risk score generated successfully")

print("=" * 70)
