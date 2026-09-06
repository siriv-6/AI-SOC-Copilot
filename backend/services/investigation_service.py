class InvestigationService:

    def __init__(self):
        print("Investigation Service initialized")

    def investigate(self, analysis):

        if not isinstance(analysis, dict):
            raise ValueError(
                "Analysis must be a dictionary."
            )

        prediction = analysis.get(
            "prediction",
            {}
        )

        mitre = analysis.get(
            "mitre_attack",
            {}
        )

        risk = analysis.get(
            "risk_assessment",
            {}
        )

        alert = analysis.get(
            "alert",
            {}
        )

        label = prediction.get(
            "predicted_label",
            "Unknown"
        )

        confidence = prediction.get(
            "confidence",
            0
        )

        risk_level = risk.get(
            "risk_level",
            "UNKNOWN"
        )

        risk_score = risk.get(
            "risk_score",
            0
        )

        mitre_mapped = mitre.get(
            "mapped",
            False
        )

        findings = []

        # --------------------------------------------------------
        # BENIGN TRAFFIC
        # --------------------------------------------------------

        if label == "BENIGN":

            findings.append(
                "The machine-learning model classified "
                "the observed network activity as benign."
            )

            findings.append(
                f"The model confidence for the benign "
                f"classification was {confidence}%."
            )

            investigation_status = "NO_IMMEDIATE_THREAT"

            recommendation = (
                "No immediate containment action is required. "
                "Continue monitoring the source activity."
            )

        # --------------------------------------------------------
        # MALICIOUS / SUSPICIOUS TRAFFIC
        # --------------------------------------------------------

        else:

            findings.append(
                f"The machine-learning model classified "
                f"the network activity as {label}."
            )

            findings.append(
                f"The model produced a confidence score "
                f"of {confidence}%."
            )

            if mitre_mapped:

                findings.append(
                    f"The activity was mapped to MITRE ATT&CK "
                    f"technique {mitre.get('technique_id')}: "
                    f"{mitre.get('technique')}."
                )

            findings.append(
                f"The calculated security risk is "
                f"{risk_level} with a risk score of "
                f"{risk_score}."
            )

            if risk_level == "HIGH":

                investigation_status = "HIGH_PRIORITY"

                recommendation = (
                    "Immediately investigate the source IP, "
                    "review related network activity, and "
                    "consider containment if malicious activity "
                    "is confirmed."
                )

            elif risk_level == "MEDIUM":

                investigation_status = "INVESTIGATE"

                recommendation = (
                    "Perform additional investigation of the "
                    "source activity and review related alerts."
                )

            else:

                investigation_status = "MONITOR"

                recommendation = (
                    "Continue monitoring the activity for "
                    "additional suspicious behavior."
                )

        # --------------------------------------------------------
        # RETURN INVESTIGATION RESULT
        # --------------------------------------------------------

        return {

            "investigation_status":
                investigation_status,

            "finding_count":
                len(findings),

            "findings":
                findings,

            "recommendation":
                recommendation,

            "alert_context": {

                "alert_id":
                    analysis.get(
                        "alert_id"
                    ),

                "source_ip":
                    alert.get(
                        "network",
                        {}
                    ).get(
                        "source_ip"
                    ),

                "destination_ip":
                    alert.get(
                        "network",
                        {}
                    ).get(
                        "destination_ip"
                    ),

                "predicted_label":
                    label,

                "confidence":
                    confidence,

                "risk_level":
                    risk_level,

                "risk_score":
                    risk_score

            }

        }
