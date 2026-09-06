from backend.graph.soc_graph import soc_graph


incident = {
    "alert_id": "step49-test-001",

    "network": {
        "source_ip": "192.168.1.100",
        "destination_ip": "192.168.1.200",
        "source_port": "49152",
        "destination_port": "80",
        "protocol": "TCP"
    },

    "prediction": {
        "predicted_label": "Port Scan",
        "confidence": 0.86
    },

    "risk_assessment": {
        "risk_level": "HIGH",
        "risk_score": 100
    }
}


print("=" * 70)
print("STEP 49 - MULTI-AGENT SOC GRAPH TEST")
print("=" * 70)

print("\nRunning LangGraph...\n")

result = soc_graph.invoke({
    "incident": incident
})


print("=" * 70)
print("THREAT ANALYSIS")
print("=" * 70)

print(result["threat"])


print("\n" + "=" * 70)
print("MITRE ATT&CK")
print("=" * 70)

print(result["mitre"])


print("\n" + "=" * 70)
print("EXPLAINABILITY")
print("=" * 70)

print(result["explanation"])


print("\n" + "=" * 70)
print("RESPONSE RECOMMENDATIONS")
print("=" * 70)

print(result["response"])


print("\n" + "=" * 70)
print("STEP 49 SUCCESSFUL")
print("=" * 70)
