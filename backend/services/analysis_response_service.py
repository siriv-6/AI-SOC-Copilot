class AnalysisResponseService:

    def __init__(self):
        print("Analysis Response Service initialized")

    # ============================================================
    # BUILD STANDARDIZED SOC RESPONSE
    # ============================================================

    def build_response(self, analysis):

        if not isinstance(analysis, dict):
            raise ValueError(
                "Security analysis must be a dictionary."
            )

        # --------------------------------------------------------
        # EXTRACT COMPONENTS
        # --------------------------------------------------------

        prediction = analysis.get(
            "prediction",
            {}
        )

        mitre = analysis.get(
            "mitre_attack",
            analysis.get(
                "mitre",
                {}
            )
        )

        risk = analysis.get(
            "risk_assessment",
            {}
        )

        # --------------------------------------------------------
        # PREDICTION INFORMATION
        # --------------------------------------------------------

        predicted_label = prediction.get(
            "predicted_label",
            "Unknown"
        )

        confidence = prediction.get(
            "confidence",
            0
        )

        # --------------------------------------------------------
        # RISK INFORMATION
        # --------------------------------------------------------

        risk_level = risk.get(
            "risk_level",
            "UNKNOWN"
        )

        risk_score = risk.get(
            "risk_score",
            0
        )

        # --------------------------------------------------------
        # MITRE INFORMATION
        # --------------------------------------------------------

        mitre_mapped = mitre.get(
            "mapped",
            False
        )

        # --------------------------------------------------------
        # GENERATE EXPLANATION
        # --------------------------------------------------------

        if predicted_label == "BENIGN":

            explanation = (
                "The machine-learning model classified "
                "the network activity as benign."
            )

            investigation_priority = "LOW"

        elif risk_level == "HIGH":

            explanation = (
                f"The network activity was classified as "
                f"{predicted_label} with {confidence}% confidence. "
                "The activity represents a high-priority security "
                "event requiring immediate investigation."
            )

            investigation_priority = "HIGH"

        elif risk_level == "MEDIUM":

            explanation = (
                f"The network activity was classified as "
                f"{predicted_label} with {confidence}% confidence. "
                "The activity is potentially suspicious and "
                "requires further investigation."
            )

            investigation_priority = "MEDIUM"

        else:

            explanation = (
                f"The network activity was classified as "
                f"{predicted_label}."
            )

            investigation_priority = "LOW"

        # --------------------------------------------------------
        # BUILD STANDARDIZED RESPONSE
        # --------------------------------------------------------

        response = {

            "analysis_status": "success",

            # ----------------------------------------------------
            # ALERT INFORMATION
            # ----------------------------------------------------

            "alert_id": analysis.get(
                "alert_id"
            ),

            "timestamp": analysis.get(
                "timestamp"
            ),

            "rule": analysis.get(
                "rule",
                {}
            ),

            "agent": analysis.get(
                "agent",
                {}
            ),

            "network": analysis.get(
                "network",
                {}
            ),

            # ----------------------------------------------------
            # ML PREDICTION
            # ----------------------------------------------------

            "prediction": {

                "predicted_class_id":
                    prediction.get(
                        "predicted_class_id"
                    ),

                "predicted_label":
                    predicted_label,

                "confidence":
                    confidence,

                "top_3_predictions":
                    prediction.get(
                        "top_3_predictions",
                        []
                    )
            },

            # ----------------------------------------------------
            # MITRE ATT&CK
            # ----------------------------------------------------

            "mitre_attack": {

                "mapped":
                    mitre_mapped,

                "tactic":
                    mitre.get(
                        "tactic"
                    ),

                "technique_id":
                    mitre.get(
                        "technique_id"
                    ),

                "technique":
                    mitre.get(
                        "technique"
                    ),

                "description":
                    mitre.get(
                        "description"
                    )
            },

            # ----------------------------------------------------
            # RISK ASSESSMENT
            # ----------------------------------------------------

            "risk_assessment": {

                "risk_level":
                    risk_level,

                "risk_score":
                    risk_score
            },

            # ----------------------------------------------------
            # EXPLAINABILITY
            # ----------------------------------------------------

            "explainability": {

                "summary":
                    explanation,

                "investigation_priority":
                    investigation_priority
            }
        }

        return response