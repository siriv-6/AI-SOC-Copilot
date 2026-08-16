from fastapi import FastAPI
from pydantic import BaseModel

from backend.services.alert_prediction_service import AlertPredictionService
from backend.config.settings import settings
from backend.services.ml_service import MLPredictionService


# ============================================================
# PREDICTION REQUEST MODEL
# ============================================================

class NetworkFlowInput(BaseModel):

    packet_length_variance: float

    packet_length_mean: float

    total_length_of_fwd_packets: float

    bwd_packet_length_max: float

    init_win_bytes_backward: float

    max_packet_length: float

    fwd_packet_length_max: float

    init_win_bytes_forward: float

    flow_iat_max: float

    fwd_header_length: float

    flow_duration: float

    fwd_packet_length_mean: float

    fwd_iat_mean: float

    destination_port: float

    flow_bytes_per_second: float

    bwd_header_length: float

    bwd_packets_per_second: float

    flow_packets_per_second: float

    flow_iat_mean: float

    fwd_iat_std: float


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(

    title=settings.app_name,

    description=(
        "Backend API for the AI-powered "
        "SOC Copilot"
    ),

    version=settings.app_version
)


# ============================================================
# INITIALIZE ML PREDICTION SERVICE
# ============================================================

print(
    "Initializing ML Prediction Service..."
)

ml_service = MLPredictionService()
alert_prediction_service = AlertPredictionService()

print(
    "ML Prediction Service initialized successfully!"
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {

        "message":
            f"{settings.app_name} is running",

        "status":
            "success",

        "ml_model_loaded":
            True,

        "number_of_features":
            len(
                ml_service.selected_features
            ),

        "number_of_classes":
            len(
                ml_service.label_mapping
            )

    }


# ============================================================
# HEALTH CHECK ENDPOINT
# ============================================================

@app.get("/health")
def health_check():

    return {

        "status":
            "healthy",

        "ml_model_loaded":
            ml_service.model is not None,

        "number_of_features":
            len(
                ml_service.selected_features
            ),

        "number_of_classes":
            len(
                ml_service.label_mapping
            )

    }


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict_attack(
    data: NetworkFlowInput
):

    print("\n============================================================")
    print("NEW PREDICTION REQUEST")
    print("============================================================")

    # ============================================================
    # CONVERT API INPUT TO FEATURE LIST
    # ============================================================

    # IMPORTANT:
    #
    # This order MUST exactly match the order used
    # when training the Random Forest model.
    #
    # The model expects exactly 20 features.

    feature_values = [

        data.packet_length_variance,

        data.packet_length_mean,

        data.total_length_of_fwd_packets,

        data.bwd_packet_length_max,

        data.init_win_bytes_backward,

        data.max_packet_length,

        data.fwd_packet_length_max,

        data.init_win_bytes_forward,

        data.flow_iat_max,

        data.fwd_header_length,

        data.flow_duration,

        data.fwd_packet_length_mean,

        data.fwd_iat_mean,

        data.destination_port,

        data.flow_bytes_per_second,

        data.bwd_header_length,

        data.bwd_packets_per_second,

        data.flow_packets_per_second,

        data.flow_iat_mean,

        data.fwd_iat_std

    ]
    # ============================================================
# WAZUH ALERT ANALYSIS ENDPOINT
# ============================================================

@app.post("/analyze-alert")
def analyze_alert(alert: dict):

    try:

        result = alert_prediction_service.process_alert(
            alert
        )

        return {
            "status": "success",
            "analysis": result
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
    


    # ============================================================
    # VALIDATE FEATURE COUNT
    # ============================================================

    expected_features = len(
        ml_service.selected_features
    )

    received_features = len(
        feature_values
    )

    if received_features != expected_features:

        raise ValueError(

            f"Feature count mismatch. "

            f"Model expects "
            f"{expected_features} features, "

            f"but received "
            f"{received_features}."

        )


    print(
        f"Received {received_features} "
        f"features."
    )


    # ============================================================
    # SEND FEATURES TO ML SERVICE
    # ============================================================

    # IMPORTANT:
    #
    # Do NOT pass `data` directly.
    #
    # Wrong:
    #
    # ml_service.predict(data)
    #
    # Correct:
    #
    # ml_service.predict(feature_values)

    result = ml_service.predict(
        feature_values
    )


    # ============================================================
    # RETURN PREDICTION RESULT
    # ============================================================

    return result
