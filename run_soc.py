import json

from graph.soc_graph import soc_graph


with open("data/incidents.json", "r") as file:
    incident = json.load(file)


initial_state = {
    "incident": incident
}


result = soc_graph.invoke(initial_state)


print("\n==============================")
print("AI SOC COPILOT ANALYSIS")
print("==============================")


print("\n--- THREAT ANALYSIS ---")
print(result["threat"])


print("\n--- MITRE ATT&CK ---")
print(result["mitre"])


print("\n--- EXPLANATION ---")
print(result["explanation"])


print("\n--- RESPONSE RECOMMENDATIONS ---")
print(result["response"])