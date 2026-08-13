from backend.parser.feature_extractor import NetworkFeatureExtractor
from backend.services.ml_service import MLPredictionService


print("=" * 70)
print("STEP 30 - FEATURE EXTRACTION + ML SERVICE INTEGRATION TEST")
print("=" * 70)


# ============================================================
# INITIALIZE COMPONENTS
# ============================================================

print("\nLoading Feature Extractor...")

extractor = NetworkFeatureExtractor()

print("Feature Extractor loaded successfully.")


print("\nLoading ML Prediction Service...")

ml_service = MLPredictionService()

print("ML Prediction Service loaded successfully.")


# ============================================================
# SAMPLE NETWORK FLOW
# ============================================================

sample_flow = {

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


# ============================================================
# STEP 1 - EXTRACT FEATURES
# ============================================================

print("\n" + "-" * 70)
print("STEP 1 - EXTRACTING FEATURES")
print("-" * 70)


features = extractor.extract_from_flow(
    sample_flow
)


print(
    f"Number of extracted features: {len(features)}"
)


# ============================================================
# VALIDATE FEATURE COUNT
# ============================================================

assert len(features) == 20

print("Feature count validation: PASSED")


# ============================================================
# DISPLAY FEATURES
# ============================================================

print("\nExtracted feature vector:")

for index, (name, value) in enumerate(
    zip(
        extractor.REQUIRED_FEATURES,
        features
    ),
    start=1
):

    print(
        f"{index:02d}. {name}: {value}"
    )


# ============================================================
# STEP 2 - SEND FEATURES TO ML SERVICE
# ============================================================

print("\n" + "-" * 70)
print("STEP 2 - SENDING FEATURES TO ML SERVICE")
print("-" * 70)


result = ml_service.predict(
    features
)


# ============================================================
# DISPLAY ML RESULT
# ============================================================

print("\nML Prediction Result:")

print(
    f"Predicted Class ID : "
    f"{result['predicted_class_id']}"
)

print(
    f"Predicted Label    : "
    f"{result['predicted_label']}"
)

print(
    f"Confidence         : "
    f"{result['confidence']}%"
)


# ============================================================
# TOP 3 PREDICTIONS
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
# VALIDATE RESULT STRUCTURE
# ============================================================

print("\n" + "-" * 70)
print("STEP 3 - VALIDATING ML RESULT")
print("-" * 70)


assert "predicted_class_id" in result

assert "predicted_label" in result

assert "confidence" in result

assert "top_3_predictions" in result


assert len(
    result["top_3_predictions"]
) == 3


print("Prediction result structure: PASSED")


# ============================================================
# VALIDATE CONFIDENCE
# ============================================================

assert (
    0 <= result["confidence"] <= 100
)

print("Confidence validation: PASSED")


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("STEP 30 INTEGRATION TEST SUCCESSFUL")
print("=" * 70)

print(
    "\nPipeline verified successfully:"
)

print(
    "Network Flow"
    " -> Feature Extractor"
    " -> 20 Features"
    " -> ML Prediction Service"
    " -> Random Forest"
    " -> Prediction"
)