import sys

sys.path.insert(0, ".")

from backend.services.security_analysis_service import (
    SecurityAnalysisService
)


print("=" * 70)
print("STEP 41 - SECURITY ANALYSIS SERVICE TEST")
print("=" * 70)


# ============================================================
# INITIALIZE SERVICE
# ============================================================

print("\nInitializing Security Analysis Service...")

service = SecurityAnalysisService()

print("Security Analysis Service initialized successfully.")


# ============================================================
# SAMPLE WAZUH ALERT
# ============================================================

sample_alert = {

    "id": "step39-test-001",

    "timestamp": "2026-08-16T10:00:00Z",

    "rule": {
        "id": "100001",
        "description": "Suspicious network activity",
        "level": 10
    },

    "agent": {
        "id": "001",
        "name": "SOC-Test-Agent"
    },

    "data": {
        "srcip": "192.168.1.100",
        "dstip": "192.168.1.200",
        "srcport": 49152,
        "dstport": 8080,
        "protocol": "TCP"
    },

    "flow": {

        "packet_length_variance": 8424.25731,

        "packet_length_mean": 30.42105263,

        "total_length_of_fwd_packets": 322.0,

        "bwd_packet_length_max": 256.0,

        "init_win_bytes_backward": 110.0,

        "max_packet_length": 322.0,

        "fwd_packet_length_max": 322.0,

        "init_win_bytes_forward": 29200.0,

        "flow_iat_max": 10200000.0,

        "fwd_header_length": 296.0,

        "flow_duration": 60202640.0,

        "fwd_packet_length_mean": 35.77777778,

        "fwd_iat_mean": 6396441.875,

        "destination_port": 8080.0,

        "flow_bytes_per_second": 9.600907867,

        "bwd_header_length": 296.0,

        "bwd_packets_per_second": 0.149495105,

        "flow_packets_per_second": 0.29899021,

        "flow_iat_mean": 3541331.765,

        "fwd_iat_std": 5268489.909
    }
}


# ============================================================
# RUN SECURITY ANALYSIS
# ============================================================

print("\n" + "-" * 70)
print("RUNNING SECURITY ANALYSIS")
print("-" * 70)

result = service.analyze_alert(
    sample_alert
)


# ============================================================
# DISPLAY ALERT INFORMATION
# ============================================================

print("\n" + "-" * 70)
print("ALERT INFORMATION")
print("-" * 70)

print(
    "Alert ID:",
    result["alert"]["alert_id"]
)

print(
    "Rule:",
    result["alert"]["rule"]
)

print(
    "Agent:",
    result["alert"]["agent"]
)

print(
    "Network:",
    result["alert"]["network"]
)


# ============================================================
# DISPLAY ML PREDICTION
# ============================================================

print("\n" + "-" * 70)
print("ML PREDICTION")
print("-" * 70)

prediction = result["prediction"]

print(
    "Predicted Class ID:",
    prediction["predicted_class_id"]
)

print(
    "Predicted Label:",
    prediction["predicted_label"]
)

print(
    "Confidence:",
    prediction["confidence"],
    "%"
)


# ============================================================
# DISPLAY MITRE MAPPING
# ============================================================

print("\n" + "-" * 70)
print("MITRE ATT&CK MAPPING")
print("-" * 70)

mitre = result["mitre_attack"]

print(
    "Mapped:",
    mitre["mapped"]
)

print(
    "Tactic:",
    mitre["tactic"]
)

print(
    "Technique ID:",
    mitre["technique_id"]
)

print(
    "Technique:",
    mitre["technique"]
)
# ============================================================
# DISPLAY RISK ASSESSMENT
# ============================================================

print("\n" + "-" * 70)
print("RISK ASSESSMENT")
print("-" * 70)

risk = result["risk_assessment"]

print(
    "Risk Level:",
    risk["risk_level"]
)

print(
    "Risk Score:",
    risk["risk_score"]
)

print(
    "ML Confidence:",
    risk["ml_confidence"],
    "%"
)

print(
    "Wazuh Rule Level:",
    risk["wazuh_rule_level"]
)

print(
    "MITRE Mapped:",
    risk["mitre_mapped"]
)

print(
    "Description:",
    risk["description"]
)

# ============================================================
# VALIDATION
# ============================================================

print("\n" + "-" * 70)
print("VALIDATING COMBINED ANALYSIS")
print("-" * 70)

assert "alert" in result

assert "prediction" in result

assert "mitre_attack" in result

assert "risk_assessment" in result

assert (
    result["alert"]["alert_id"]
    == "step39-test-001"
)

assert (
    result["prediction"]["predicted_label"]
    is not None
)

assert "mapped" in result["mitre_attack"]

assert "technique_id" in result["mitre_attack"]

print("Alert analysis validation: PASSED")

print("ML prediction validation: PASSED")

print("MITRE mapping validation: PASSED")

print("MITRE mapping validation: PASSED")

print("Risk assessment validation: PASSED")

print("Combined analysis validation: PASSED")


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("STEP 41 SECURITY ANALYSIS SERVICE INTEGRATION TEST SUCCESSFUL")
print("=" * 70)

print("\nVerified pipeline:")

print(
    "Wazuh Alert -> "
    "Parser -> "
    "Feature Extraction -> "
    "ML Prediction -> "
    "MITRE ATT&CK Mapping -> "
    "Security Analysis"
)

print("=" * 70)
