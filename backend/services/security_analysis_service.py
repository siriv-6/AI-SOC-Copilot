from backend.parser.wazuh_parser import WazuhAlertParser
from backend.parser.feature_extractor import NetworkFeatureExtractor
from backend.services.ml_service import MLPredictionService
from backend.services.mitre_mapper import MITREAttackMapper
from backend.services.risk_assessment_service import RiskAssessmentService


class SecurityAnalysisService:

    # ============================================================
    # INITIALIZE SERVICES
    # ============================================================

    def __init__(self):

        print("Loading Security Analysis Service...")

        self.alert_parser = WazuhAlertParser()
        self.feature_extractor = NetworkFeatureExtractor()
        self.ml_service = MLPredictionService()
        self.mitre_mapper = MITREAttackMapper()
        self.risk_service = RiskAssessmentService()

        print("Security Analysis Service loaded successfully!")

    # ============================================================
    # ANALYZE WAZUH ALERT
    # ============================================================

    def analyze_alert(self, alert):

        # --------------------------------------------------------
        # VALIDATE ALERT
        # --------------------------------------------------------

        if not isinstance(alert, dict):

            raise ValueError(
                "Wazuh alert must be a dictionary."
            )

        # --------------------------------------------------------
        # PARSE WAZUH ALERT
        # --------------------------------------------------------

        parsed_alert = self.alert_parser.parse_alert(
            alert
        )

        # --------------------------------------------------------
        # RETRIEVE NETWORK FLOW
        # --------------------------------------------------------

        flow = alert.get("flow")

        if not isinstance(flow, dict):

            raise ValueError(
                "No network-flow features found in Wazuh alert."
            )

        # --------------------------------------------------------
        # EXTRACT ML FEATURES
        # --------------------------------------------------------

        feature_vector = (
            self.feature_extractor.extract_from_flow(
                flow
            )
        )

        # --------------------------------------------------------
        # VALIDATE FEATURE VECTOR
        # --------------------------------------------------------

        self.feature_extractor.validate(
            feature_vector
        )

        # --------------------------------------------------------
        # ML PREDICTION
        # --------------------------------------------------------

        prediction = self.ml_service.predict(
            feature_vector
        )

        # --------------------------------------------------------
        # MITRE ATT&CK MAPPING
        # --------------------------------------------------------

        mitre_mapping = (
            self.mitre_mapper.map_prediction(
                prediction["predicted_label"]
            )
        )

        # --------------------------------------------------------
        # WAZUH RULE LEVEL
        # --------------------------------------------------------

        rule_level = parsed_alert.get(
            "rule",
            {}
        ).get(
            "level"
        )

        if rule_level is None:

            rule_level = 0

        # --------------------------------------------------------
        # RISK ASSESSMENT
        # --------------------------------------------------------

        risk_assessment = (
            self.risk_service.assess_risk(
                rule_level=rule_level,
                predicted_label=prediction[
                    "predicted_label"
                ],
                confidence=prediction[
                    "confidence"
                ],
                mitre_mapping=mitre_mapping
            )
        )

        # --------------------------------------------------------
        # BUILD COMPLETE SECURITY ANALYSIS
        # --------------------------------------------------------

        analysis = {

            "alert": parsed_alert,

            "prediction": prediction,

            "mitre_attack": mitre_mapping,

            "risk_assessment": risk_assessment

        }

        return analysis
    