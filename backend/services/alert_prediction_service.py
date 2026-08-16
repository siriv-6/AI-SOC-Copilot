from backend.parser.wazuh_parser import WazuhAlertParser
from backend.parser.feature_extractor import NetworkFeatureExtractor
from backend.services.ml_service import MLPredictionService


class AlertPredictionService:

    def __init__(self):

        print("Loading Alert Prediction Service...")

        # --------------------------------------------------------
        # Initialize Wazuh parser
        # --------------------------------------------------------

        self.parser = WazuhAlertParser()

        # --------------------------------------------------------
        # Initialize feature extractor
        # --------------------------------------------------------

        self.feature_extractor = NetworkFeatureExtractor()

        # --------------------------------------------------------
        # Initialize ML prediction service
        # --------------------------------------------------------

        self.ml_service = MLPredictionService()

        print("Alert Prediction Service loaded successfully!")

    # ============================================================
    # PROCESS WAZUH ALERT
    # ============================================================

    def process_alert(self, alert):
        if not isinstance(alert, dict):
            raise ValueError(
        "Wazuh alert must be a dictionary."
    )

        # --------------------------------------------------------
        # STEP 1 - Parse Wazuh alert
        # --------------------------------------------------------

        parsed_alert = self.parser.parse_alert(alert)

        # --------------------------------------------------------
        # STEP 2 - Get network-flow features
        # --------------------------------------------------------

        flow_features = parsed_alert.get(
            "flow_features",
            {}
        )

        if not flow_features:

            raise ValueError(
                "No network-flow features found in Wazuh alert."
            )

        # --------------------------------------------------------
        # STEP 3 - Extract features in ML model order
        # --------------------------------------------------------

        features = self.feature_extractor.extract_from_flow(
            flow_features
        )

        # --------------------------------------------------------
        # STEP 4 - Validate feature vector
        # --------------------------------------------------------

        self.feature_extractor.validate(
            features
        )

        # --------------------------------------------------------
        # STEP 5 - Run ML prediction
        # --------------------------------------------------------

        prediction = self.ml_service.predict(
            features
        )

        # --------------------------------------------------------
        # STEP 6 - Build standardized result
        # --------------------------------------------------------

        result = {

            "alert_id": parsed_alert.get(
                "alert_id"
            ),

            "timestamp": parsed_alert.get(
                "timestamp"
            ),

            "rule": parsed_alert.get(
                "rule"
            ),

            "agent": parsed_alert.get(
                "agent"
            ),

            "network": parsed_alert.get(
                "network"
            ),

            "prediction": prediction

        }

        return result
    