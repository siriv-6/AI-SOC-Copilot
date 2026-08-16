import requests


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000/analyze-alert"


# ============================================================
# SAMPLE WAZUH ALERT
# ============================================================

sample_alert = {

    "id": "step35-test-001",

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
# TEST START
# ============================================================

print("=" * 70)
print("STEP 35 - FASTAPI ALERT PREDICTION INTEGRATION TEST")
print("=" * 70)

print("\nSending Wazuh alert to:")
print(API_URL)


# ============================================================
# SEND REQUEST
# ============================================================

try:

    response = requests.post(
        API_URL,
        json=sample_alert,
        timeout=30
    )

except requests.exceptions.ConnectionError:

    print("\nERROR: Could not connect to FastAPI server.")

    print(
        "\nMake sure the server is running with:"
    )

    print(
        "uvicorn backend.api.main:app --reload"
    )

    raise SystemExit(1)


# ============================================================
# HTTP VALIDATION
# ============================================================

print("\nHTTP Status Code:")
print(response.status_code)


assert response.status_code == 200, (
    f"Expected HTTP 200 but received "
    f"{response.status_code}"
)


# ============================================================
# RESPONSE JSON
# ============================================================

result = response.json()

print("\nAPI Response:")
print(result)


# ============================================================
# RESPONSE VALIDATION
# ============================================================

assert result["status"] == "success"

analysis = result["analysis"]

assert analysis["alert_id"] == "step35-test-001"

assert "timestamp" in analysis

assert "rule" in analysis

assert "agent" in analysis

assert "network" in analysis

assert "prediction" in analysis


# ============================================================
# PREDICTION VALIDATION
# ============================================================

prediction = analysis["prediction"]

assert "predicted_class_id" in prediction

assert "predicted_label" in prediction

assert "confidence" in prediction

assert "top_3_predictions" in prediction

assert len(
    prediction["top_3_predictions"]
) == 3


# ============================================================
# DISPLAY PREDICTION
# ============================================================

print("\n" + "-" * 70)
print("PREDICTION RESULT")
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
# SUCCESS
# ============================================================

print("\n" + "=" * 70)
print("STEP 35 API INTEGRATION TEST SUCCESSFUL")
print("=" * 70)

print("\nVerified pipeline:")

print(
    "Wazuh Alert"
    " -> FastAPI"
    " -> AlertPredictionService"
    " -> Wazuh Parser"
    " -> Feature Extractor"
    " -> ML Service"
    " -> Random Forest"
    " -> Attack Prediction"
)

print("=" * 70)
