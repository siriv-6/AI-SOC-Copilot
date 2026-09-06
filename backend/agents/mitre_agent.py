MITRE_MAP = {
    "Brute Force Attack": {
        "technique_id": "T1110",
        "technique": "Brute Force",
        "tactic": "Credential Access"
    },

    "Port Scan": {
        "technique_id": "T1046",
        "technique": "Network Service Scanning",
        "tactic": "Discovery"
    },

    "Phishing": {
        "technique_id": "T1566",
        "technique": "Phishing",
        "tactic": "Initial Access"
    },

    "Command and Scripting": {
        "technique_id": "T1059",
        "technique": "Command and Scripting Interpreter",
        "tactic": "Execution"
    }
}


def map_to_mitre(attack_type):

    if attack_type in MITRE_MAP:
        return MITRE_MAP[attack_type]

    return {
        "technique_id": "Unknown",
        "technique": "Unknown",
        "tactic": "Unknown"
    }