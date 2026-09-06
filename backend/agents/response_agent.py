def generate_response(incident, threat, mitre):

    attack_type = threat.get("attack_type", "Unknown")
    severity = threat.get("severity", "MEDIUM")
    technique = mitre.get("technique", "Unknown")
    technique_id = mitre.get("technique_id", "Unknown")

    # ---------------------------------------------------------
    # DDoS / DoS response
    # ---------------------------------------------------------

    if attack_type in [
        "DDoS",
        "DoS",
        "DoS Hulk",
        "DoS GoldenEye",
        "DoS Slowhttptest",
        "DoS slowloris"
    ]:

        return {
            "immediate_actions": [
                "Notify the SOC/incident response team.",
                "Increase monitoring of inbound network traffic.",
                "Identify the affected destination system or service.",
                "Review firewall and IDS/IPS alerts for related activity."
            ],

            "investigation_actions": [
                "Analyze network and firewall logs.",
                "Identify source IP addresses and traffic patterns.",
                "Determine the protocol and attack characteristics.",
                "Check whether other systems are experiencing abnormal traffic."
            ],

            "containment_recommendations": [
                "Apply rate limiting where appropriate.",
                "Filter or block confirmed malicious traffic.",
                "Use firewall/IPS controls to reduce attack traffic.",
                "Contact the ISP or DDoS mitigation provider if required."
            ],

            "prevention_recommendations": [
                "Implement DDoS protection mechanisms.",
                "Strengthen network monitoring and alerting.",
                "Review firewall and traffic-filtering policies.",
                "Maintain an incident response procedure for denial-of-service attacks."
            ],

            "mitre_reference": {
                "technique_id": technique_id,
                "technique": technique,
                "tactic": mitre.get("tactic", "Unknown")
            },

            "severity": severity
        }

    # ---------------------------------------------------------
    # Port Scan
    # ---------------------------------------------------------

    if attack_type == "Port Scan":

        return {
            "immediate_actions": [
                "Notify the SOC analyst.",
                "Review the source IP and affected destination.",
                "Increase monitoring for additional reconnaissance activity."
            ],

            "investigation_actions": [
                "Review network and firewall logs.",
                "Identify scanned ports and services.",
                "Determine whether the source IP is known or suspicious."
            ],

            "containment_recommendations": [
                "Restrict unnecessary exposed services.",
                "Block or rate-limit confirmed malicious scanning sources."
            ],

            "prevention_recommendations": [
                "Minimize externally exposed services.",
                "Strengthen network segmentation.",
                "Maintain network scanning detection rules."
            ],

            "mitre_reference": {
                "technique_id": technique_id,
                "technique": technique,
                "tactic": mitre.get("tactic", "Unknown")
            },

            "severity": severity
        }

    # ---------------------------------------------------------
    # Generic fallback
    # ---------------------------------------------------------

    return {
        "immediate_actions": [
            "Notify the SOC analyst.",
            "Review the alert and associated evidence.",
            "Increase monitoring for related activity."
        ],

        "investigation_actions": [
            "Review relevant security logs.",
            "Identify affected systems and network entities.",
            "Look for related alerts or suspicious activity."
        ],

        "containment_recommendations": [
            "Apply appropriate access-control or network controls.",
            "Isolate affected systems if evidence indicates compromise."
        ],

        "prevention_recommendations": [
            "Strengthen monitoring and detection rules.",
            "Review security controls associated with the incident."
        ],

        "mitre_reference": {
            "technique_id": technique_id,
            "technique": technique,
            "tactic": mitre.get("tactic", "Unknown")
        },

        "severity": severity
    }
