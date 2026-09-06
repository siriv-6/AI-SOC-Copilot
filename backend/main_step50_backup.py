from fastapi import FastAPI
from pydantic import BaseModel

from backend.config.settings import settings
from backend.services.ml_service import MLPredictionService
from backend.services.alert_prediction_service import AlertPredictionService
from backend.services.analysis_response_service import AnalysisResponseService
from backend.services.investigation_service import InvestigationService

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
        "Backend API for the AI-powered SOC Copilot"
    ),
    version=settings.app_version
)


# ============================================================
# INITIALIZE SERVICES
# ============================================================

print("Initializing ML Prediction Service...")

ml_service = MLPredictionService()

alert_prediction_service = AlertPredictionService()

analysis_response_service = AnalysisResponseService()

investigation_service = InvestigationService()

print("ML Prediction Service initialized successfully!")


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": f"{settings.app_name} is running",
        "status": "success",
        "ml_model_loaded": ml_service.model is not None,
        "number_of_features": len(
            ml_service.selected_features
        ),
        "number_of_classes": len(
            ml_service.label_mapping
        )
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "ml_model_loaded": ml_service.model is not None,
        "number_of_features": len(
            ml_service.selected_features
        ),
        "number_of_classes": len(
            ml_service.label_mapping
        )
    }


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict_attack(data: NetworkFlowInput):

    print("\n============================================================")
    print("NEW PREDICTION REQUEST")
    print("============================================================")

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

    expected_features = len(
        ml_service.selected_features
    )

    received_features = len(
        feature_values
    )

    if received_features != expected_features:

        raise ValueError(
            f"Feature count mismatch. "
            f"Model expects {expected_features} features, "
            f"but received {received_features}."
        )

    print(
        f"Received {received_features} features."
    )

    result = ml_service.predict(
        feature_values
    )

    return result


# ============================================================
# WAZUH ALERT ANALYSIS ENDPOINT
# ============================================================

@app.post("/analyze-alert")
def analyze_alert(alert: dict):

    try:

        print("\n============================================================")
        print("NEW WAZUH ALERT ANALYSIS REQUEST")
        print("============================================================")

        # --------------------------------------------------------
        # STEP 1 - ML + MITRE + RISK ANALYSIS
        # --------------------------------------------------------

        result = alert_prediction_service.process_alert(
            alert
        )

        # --------------------------------------------------------
        # STEP 2 - BUILD STANDARDIZED SOC RESPONSE
        # --------------------------------------------------------

        standardized_response = (
            analysis_response_service.build_response(
                result
            )
        )

        # --------------------------------------------------------
        # STEP 3 - INVESTIGATION
        # --------------------------------------------------------

        investigation = investigation_service.investigate(
            standardized_response
        )

        # --------------------------------------------------------
        # STEP 4 - ADD INVESTIGATION TO RESPONSE
        # --------------------------------------------------------

        standardized_response["investigation"] = investigation

        # --------------------------------------------------------
        # STEP 5 - FINAL API RESPONSE
        # --------------------------------------------------------

        return {
            "status": "success",
            "analysis": standardized_response
        }

    except Exception as e:

        print("\n============================================================")
        print("ALERT ANALYSIS ERROR")
        print("============================================================")

        print(f"Error: {str(e)}")

        return {
            "status": "error",
            "analysis_status": "error",
            "message": str(e)
        }
