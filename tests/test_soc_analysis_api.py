import requests


print("=" * 70)
print("STEP 50 - MULTI-AGENT SOC COPILOT API INTEGRATION TEST")
print("=" * 70)


API_URL = "http://127.0.0.1:8000/soc-analysis"


# ============================================================
# PORTSCAN INCIDENT
# ============================================================

alert = {

    "id": "step50-test-001",

    "timestamp": "2026-08-28T10:00:00.000+0000",

    "rule": {
        "id": "100002",
        "level": 15,
        "description": "Possible network scanning activity detected"
    },

    "agent": {
        "id": "001",
        "name": "SOC-Test-Agent"
    },

    "data": {

        "srcip": "192.168.1.100",
        "srcport": "49152",

        "dstip": "192.168.1.200",
        "dstport": "80",

        "protocol": "TCP",

        "packet_length_variance": 100787.9015,
        "packet_length_mean": 176.4166667,
        "total_length_of_fwd_packets": 703.0,
        "bwd_packet_length_max": 1050.0,
        "init_win_bytes_backward": 243.0,
        "max_packet_length": 1050.0,
        "fwd_packet_length_max": 356.0,
        "init_win_bytes_forward": 29200.0,
        "flow_iat_max": 4965658.0,
        "fwd_header_length": 200.0,
        "flow_duration": 5021059.0,
        "fwd_packet_length_mean": 117.1666667,
        "fwd_iat_mean": 11080.2,
        "destination_port": 80.0,
        "flow_bytes_per_second": 421.6242032,
        "bwd_header_length": 168.0,
        "bwd_packets_per_second": 0.995805865,
        "flow_packets_per_second": 2.190772903,
        "flow_iat_mean": 502105.9,
        "fwd_iat_std": 17612.66701
    }
}


# ============================================================
# SEND ALERT
# ============================================================

print("\nSending PortScan alert to /soc-analysis...")

response = requests.post(
    API_URL,
    json=alert
)


# ============================================================
# HTTP VALIDATION
# ============================================================

print("\nHTTP Status Code:")
print(response.status_code)

assert response.status_code == 200

print("HTTP response validation: PASSED")


# ============================================================
# PARSE RESPONSE
# ============================================================

result = response.json()

print("\nAPI Response:")
print(result)

assert result["status"] == "success"

print("API status validation: PASSED")


# ============================================================
# EXISTING ML PIPELINE
# ============================================================

incident = result["incident_analysis"]

prediction = incident["prediction"]

print("\n" + "-" * 70)
print("EXISTING SOC PIPELINE")
print("-" * 70)

print(
    "Predicted Label:",
    prediction["predicted_label"]
)

print(
    "Confidence:",
    prediction["confidence"]
)

assert prediction["predicted_label"] == "PortScan"

print("ML prediction validation: PASSED")


# ============================================================
# MULTI-AGENT PIPELINE
# ============================================================

multi_agent = result["multi_agent_analysis"]


# ============================================================
# THREAT HUNTER
# ============================================================

print("\n" + "-" * 70)
print("THREAT HUNTER AGENT")
print("-" * 70)

threat = multi_agent["threat_analysis"]

print(threat)

assert threat is not None

print("Threat Hunter validation: PASSED")


# ============================================================
# MITRE AGENT
# ============================================================

print("\n" + "-" * 70)
print("MITRE ATT&CK AGENT")
print("-" * 70)

mitre = multi_agent["mitre_attack"]

print(mitre)

assert mitre["technique_id"] == "T1046"

assert mitre["technique"] == "Network Service Scanning"

assert mitre["tactic"] == "Discovery"

print("MITRE Agent validation: PASSED")


# ============================================================
# EXPLAINABILITY AGENT
# ============================================================

print("\n" + "-" * 70)
print("EXPLAINABILITY AGENT")
print("-" * 70)

explanation = multi_agent["explainability"]

print(explanation)

assert explanation is not None

assert len(explanation) > 0

print("Explainability Agent validation: PASSED")


# ============================================================
# RESPONSE AGENT
# ============================================================

print("\n" + "-" * 70)
print("RESPONSE AGENT")
print("-" * 70)

response_recommendations = multi_agent[
    "response_recommendations"
]

print(response_recommendations)

assert response_recommendations is not None

assert len(response_recommendations) > 0

print("Response Agent validation: PASSED")


# ============================================================
# FINAL VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("STEP 50 MULTI-AGENT SOC COPILOT API TEST SUCCESSFUL")
print("=" * 70)

print("\nVerified pipeline:")

print(
    "Wazuh Alert"
    " -> FastAPI"
    " -> ML Prediction"
    " -> Threat Hunter Agent"
    " -> MITRE Agent"
    " -> Explainability Agent"
    " -> Response Agent"
)

print("=" * 70)
