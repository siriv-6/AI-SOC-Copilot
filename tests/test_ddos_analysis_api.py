import requests

API_URL = "http://127.0.0.1:8000/soc-analysis"

alert = {
    "id": "ddos-test-001",

    "timestamp": "2026-09-06T10:00:00.000+0000",

    "rule": {
        "id": "100003",
        "level": 15,
        "description": "Possible DDoS network activity detected"
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

        "packet_length_variance": 3435230.673,
        "packet_length_mean": 1057.545455,
        "total_length_of_fwd_packets": 26.0,
        "bwd_packet_length_max": 5840.0,
        "init_win_bytes_backward": 229.0,
        "max_packet_length": 5840.0,
        "fwd_packet_length_max": 20.0,
        "init_win_bytes_forward": 8192.0,
        "flow_iat_max": 1292730.0,
        "fwd_header_length": 72.0,
        "flow_duration": 1293792.0,
        "fwd_packet_length_mean": 8.666666667,
        "fwd_iat_mean": 373.5,
        "destination_port": 80.0,
        "flow_bytes_per_second": 8991.398927,
        "bwd_header_length": 152.0,
        "bwd_packets_per_second": 5.410452376,
        "flow_packets_per_second": 7.72921768,
        "flow_iat_mean": 143754.6667,
        "fwd_iat_std": 523.9661249
    }
}


print("=" * 70)
print("DDOS MULTI-AGENT SOC COPILOT TEST")
print("=" * 70)

print("\nSending DDoS alert...")

response = requests.post(
    API_URL,
    json=alert,
    timeout=300
)

print("\nHTTP Status:", response.status_code)

assert response.status_code == 200

result = response.json()

print("\nAPI Response:")
print(result)

assert result["status"] == "success"

incident = result["incident_analysis"]
prediction = incident["prediction"]

print("\n" + "-" * 70)
print("ML PREDICTION")
print("-" * 70)

print("Predicted Label:", prediction["predicted_label"])
print("Confidence:", prediction["confidence"])

print("\n" + "-" * 70)
print("MULTI-AGENT ANALYSIS")
print("-" * 70)

multi_agent = result["multi_agent_analysis"]

print("\nThreat Hunter:")
print(multi_agent["threat_analysis"])

print("\nMITRE ATT&CK:")
print(multi_agent["mitre_attack"])

print("\nExplainability:")
print(multi_agent["explainability"])

print("\nResponse Recommendations:")
print(multi_agent["response_recommendations"])

print("\n" + "=" * 70)
print("DDOS TEST COMPLETED")
print("=" * 70)
