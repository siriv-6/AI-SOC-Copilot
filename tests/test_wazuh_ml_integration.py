import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from backend.parser.wazuh_parser import WazuhAlertParser
from backend.parser.feature_extractor import NetworkFeatureExtractor
from backend.services.ml_service import MLPredictionService


print("=" * 70)
print("STEP 32 - WAZUH TO ML PREDICTION INTEGRATION")
print("=" * 70)


# ============================================================
# SAMPLE WAZUH ALERT
# ============================================================

sample_alert = {
    "id": "step32-test-001",
    "timestamp": "2026-08-13T10:00:00Z",

    "rule": {
        "id": "100001",
        "description": "Suspicious network activity",
        "level": 10
    },

    "agent": {
        "id": "001",
        "name": "SOC-Windows10"
    },

    "data": {
        "srcip": "192.168.1.100",
        "dstip": "192.168.1.200",
        "srcport": 49152,
        "dstport": 8080,
        "protocol": "TCP"
    },

    # Network-flow information
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
# INITIALIZE COMPONENTS
# ============================================================

print("\nInitializing Wazuh Alert Parser...")

parser = WazuhAlertParser()

print("Parser initialized successfully.")


print("\nInitializing Feature Extractor...")

extractor = NetworkFeatureExtractor()

print("Feature extractor initialized successfully.")


print("\nInitializing ML Prediction Service...")

ml_service = MLPredictionService()

print("ML Prediction Service initialized successfully.")


# ============================================================
# STEP 1 - PARSE WAZUH ALERT
# ============================================================

print("\n" + "-" * 70)
print("STEP 1 - PARSING WAZUH ALERT")
print("-" * 70)

parsed_alert = parser.parse_alert(sample_alert)

print("Wazuh alert parsed successfully.")

assert parsed_alert["alert_id"] == "step32-test-001"
assert parsed_alert["rule"]["id"] == "100001"

print("Parsed alert validation: PASSED")


# ============================================================
# STEP 2 - GET NETWORK FLOW
# ============================================================

print("\n" + "-" * 70)
print("STEP 2 - RETRIEVING NETWORK FLOW")
print("-" * 70)

flow = sample_alert["flow"]

print(
    f"Flow features available: {len(flow)}"
)

assert len(flow) == 20

print("20-feature availability validation: PASSED")


# ============================================================
# STEP 3 - EXTRACT ML FEATURES
# ============================================================

print("\n" + "-" * 70)
print("STEP 3 - EXTRACTING ML FEATURES")
print("-" * 70)

features = extractor.extract_from_flow(flow)

print(
    f"ML feature vector length: {len(features)}"
)

assert len(features) == 20

extractor.validate(features)

print("Feature vector validation: PASSED")


# ============================================================
# STEP 4 - SEND FEATURES TO ML MODEL
# ============================================================

print("\n" + "-" * 70)
print("STEP 4 - ML PREDICTION")
print("-" * 70)

result = ml_service.predict(features)

print("\nML Prediction Result:")
print("-" * 40)

print(
    "Predicted Class ID:",
    result["predicted_class_id"]
)

print(
    "Predicted Label:",
    result["predicted_label"]
)

print(
    "Confidence:",
    result["confidence"],
    "%"
)


# ============================================================
# STEP 5 - TOP 3 PREDICTIONS
# ============================================================

print("\nTop 3 Predictions:")

for index, prediction in enumerate(
    result["top_3_predictions"],
    start=1
):

    print(
        f"{index}. "
        f"{prediction['label']} - "
        f"{prediction['confidence']}%"
    )


# ============================================================
# VALIDATION
# ============================================================

assert "predicted_class_id" in result
assert "predicted_label" in result
assert "confidence" in result
assert "top_3_predictions" in result

assert len(result["top_3_predictions"]) == 3

print("\nML prediction validation: PASSED")


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("STEP 32 INTEGRATION TEST SUCCESSFUL")
print("=" * 70)

print(
    "\nVerified pipeline:"
)

print(
    "Wazuh Alert"
    " -> Wazuh Parser"
    " -> Network Flow"
    " -> Feature Extractor"
    " -> 20 ML Features"
    " -> Random Forest"
    " -> Attack Prediction"
)

print("=" * 70)
