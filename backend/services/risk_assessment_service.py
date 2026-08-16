class RiskAssessmentService:

    # ============================================================
    # INITIALIZE
    # ============================================================

    def __init__(self):

        print("Risk Assessment Service initialized")

    # ============================================================
    # ASSESS SECURITY RISK
    # ============================================================

    def assess_risk(
        self,
        rule_level,
        predicted_label,
        confidence,
        mitre_mapping
    ):

        # --------------------------------------------------------
        # VALIDATE INPUT
        # --------------------------------------------------------

        if not isinstance(rule_level, (int, float)):
            raise ValueError(
                "Wazuh rule level must be numeric."
            )

        if not isinstance(confidence, (int, float)):
            raise ValueError(
                "ML confidence must be numeric."
            )

        # --------------------------------------------------------
        # NORMALIZE VALUES
        # --------------------------------------------------------

        rule_level = float(rule_level)
        confidence = float(confidence)

        # --------------------------------------------------------
        # BENIGN ALERT
        # --------------------------------------------------------

        if predicted_label == "BENIGN":

            risk_level = "LOW"

        # --------------------------------------------------------
        # HIGH CONFIDENCE ATTACK
        # --------------------------------------------------------

        elif confidence >= 80 and rule_level >= 10:

            risk_level = "HIGH"

        # --------------------------------------------------------
        # MEDIUM RISK
        # --------------------------------------------------------

        elif confidence >= 50 or rule_level >= 7:

            risk_level = "MEDIUM"

        # --------------------------------------------------------
        # LOW RISK
        # --------------------------------------------------------

        else:

            risk_level = "LOW"

        # --------------------------------------------------------
        # MITRE MAPPING STATUS
        # --------------------------------------------------------

        mitre_mapped = bool(
            mitre_mapping.get(
                "mapped",
                False
            )
        )

        # --------------------------------------------------------
        # RISK SCORE
        # --------------------------------------------------------

        risk_score = 0

        # Wazuh rule contribution
        risk_score += min(
            rule_level * 5,
            50
        )

        # ML confidence contribution
        if predicted_label != "BENIGN":

            risk_score += min(
                confidence * 0.5,
                40
            )

        # MITRE contribution
        if mitre_mapped:

            risk_score += 10

        risk_score = round(
            min(risk_score, 100),
            2
        )

        # --------------------------------------------------------
        # RISK DESCRIPTION
        # --------------------------------------------------------

        if predicted_label == "BENIGN":

            description = (
                "The machine-learning model classified "
                "the network activity as benign."
            )

        elif risk_level == "HIGH":

            description = (
                "High-risk network activity detected "
                "with strong ML confidence and a "
                "significant Wazuh rule level."
            )

        elif risk_level == "MEDIUM":

            description = (
                "Potentially suspicious network activity "
                "requires further investigation."
            )

        else:

            description = (
                "Low-risk suspicious activity detected."
            )

        # --------------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------------

        return {

            "risk_level": risk_level,

            "risk_score": risk_score,

            "predicted_label": predicted_label,

            "ml_confidence": confidence,

            "wazuh_rule_level": rule_level,

            "mitre_mapped": mitre_mapped,

            "description": description

        }
    