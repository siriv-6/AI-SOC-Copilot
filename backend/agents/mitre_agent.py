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
    },

    # DDoS / Network Denial of Service
    "DDoS": {
        "technique_id": "T1498",
        "technique": "Network Denial of Service",
        "tactic": "Impact"
    },

    "DoS": {
        "technique_id": "T1498",
        "technique": "Network Denial of Service",
        "tactic": "Impact"
    },

    "DoS Hulk": {
        "technique_id": "T1498",
        "technique": "Network Denial of Service",
        "tactic": "Impact"
    },

    "DoS GoldenEye": {
        "technique_id": "T1498",
        "technique": "Network Denial of Service",
        "tactic": "Impact"
    },

    "DoS Slowhttptest": {
        "technique_id": "T1498",
        "technique": "Network Denial of Service",
        "tactic": "Impact"
    },

    "DoS slowloris": {
        "technique_id": "T1498",
        "technique": "Network Denial of Service",
        "tactic": "Impact"
    }
}


def map_to_mitre(attack_type):

    if not attack_type:
        return {
            "technique_id": "Unknown",
            "technique": "Unknown",
            "tactic": "Unknown"
        }

    # Convert to string and normalize
    attack = str(attack_type).strip()

    # Exact match
    if attack in MITRE_MAP:
        return MITRE_MAP[attack]

    # Case-insensitive exact match
    for key, value in MITRE_MAP.items():
        if attack.lower() == key.lower():
            return value

    # Handle verbose DDoS descriptions
    attack_lower = attack.lower()

    if (
        "ddos" in attack_lower
        or "distributed denial of service" in attack_lower
    ):
        return MITRE_MAP["DDoS"]

    # Handle DoS variants
    if "dos hulk" in attack_lower:
        return MITRE_MAP["DoS Hulk"]

    if "dos goldeneye" in attack_lower:
        return MITRE_MAP["DoS GoldenEye"]

    if "slowhttptest" in attack_lower:
        return MITRE_MAP["DoS Slowhttptest"]

    if "slowloris" in attack_lower:
        return MITRE_MAP["DoS slowloris"]

    if attack_lower.startswith("dos"):
        return MITRE_MAP["DoS"]

    # Unknown attack
    return {
        "technique_id": "Unknown",
        "technique": "Unknown",
        "tactic": "Unknown"
    }
