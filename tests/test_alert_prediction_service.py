from backend.services.alert_prediction_service import (
    AlertPredictionService
)


print("=" * 70)
print("STEP 33 - ALERT PREDICTION SERVICE TEST")
print("=" * 70)


# ============================================================
# SAMPLE WAZUH ALERT
# ============================================================

sample_alert = {

    "id": "step33-test-001",

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
        "srcport": 49152,

        "dstip": "192.168.1.200",
        "dstport": 8080,

        "protocol": "TCP",

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
# INITIALIZE SERVICE
# ============================================================

print("\nInitializing Alert Prediction Service...")

service = AlertPredictionService()

print("Service initialization successful.")


# ============================================================
# PROCESS ALERT
# ============================================================

print("\n" + "-" * 70)
print("PROCESSING WAZUH ALERT")
print("-" * 70)

result = service.process_alert(
    sample_alert
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\nAlert processing completed.")

print("\nAlert ID:")
print(
    result["alert_id"]
)

print("\nRule:")
print(
    result["rule"]
)

print("\nAgent:")
print(
    result["agent"]
)

print("\nNetwork:")
print(
    result["network"]
)


# ============================================================
# DISPLAY ML RESULT
# ============================================================

prediction = result["prediction"]

print("\n" + "-" * 70)
print("ML PREDICTION")
print("-" * 70)

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

print("\nTop 3 Predictions:")

for index, item in enumerate(
    prediction["top_3_predictions"],
    start=1
):

    print(
        f"{index}. "
        f"{item['label']} - "
        f"{item['confidence']}%"
    )


# ============================================================
# VALIDATION
# ============================================================

assert result["alert_id"] == "step33-test-001"

assert "rule" in result

assert "agent" in result

assert "network" in result

assert "prediction" in result

assert "predicted_class_id" in prediction

assert "predicted_label" in prediction

assert "confidence" in prediction

assert "top_3_predictions" in prediction

assert len(
    prediction["top_3_predictions"]
) == 3


print("\n" + "=" * 70)
print("STEP 33 TEST SUCCESSFUL")
print("=" * 70)

print(
    "\nVerified reusable pipeline:"
)

print(
    "Wazuh Alert"
    " -> AlertPredictionService"
    " -> Parser"
    " -> Feature Extraction"
    " -> ML Service"
    " -> Prediction"
)

print("=" * 70)
