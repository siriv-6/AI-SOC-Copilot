import json
import os

from backend.parser.wazuh_parser import WazuhAlertParser


print("=" * 60)
print("TESTING WAZUH ALERT PARSER")
print("=" * 60)


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ============================================================
# SAMPLE ALERT PATH
# ============================================================

ALERT_PATH = os.path.join(
    PROJECT_ROOT,
    "tests",
    "sample_data",
    "wazuh_alert.json"
)


# ============================================================
# CHECK SAMPLE FILE
# ============================================================

if not os.path.exists(ALERT_PATH):
    raise FileNotFoundError(
        f"Sample Wazuh alert not found at: {ALERT_PATH}"
    )


# ============================================================
# LOAD SAMPLE ALERT AS JSON
# ============================================================

with open(
    ALERT_PATH,
    "r",
    encoding="utf-8"
) as f:

    alert = json.load(f)


print("\nSample Wazuh alert loaded successfully.")


# ============================================================
# CREATE PARSER
# ============================================================

parser = WazuhAlertParser()


# ============================================================
# TEST 1 — PARSE JSON OBJECT
# ============================================================

print("\nTesting JSON object parsing...")

parsed_alert = parser.parse_alert(alert)


print("\nParsed Wazuh Alert:")

print(
    json.dumps(
        parsed_alert,
        indent=4
    )
)


# ============================================================
# VALIDATE JSON OBJECT PARSING
# ============================================================

assert (
    parsed_alert["alert_id"]
    == "1764860000.123456"
)

assert (
    parsed_alert["agent"]["name"]
    == "windows-endpoint"
)

assert (
    parsed_alert["rule"]["id"]
    == "100002"
)

assert (
    parsed_alert["rule"]["level"]
    == 10
)

assert (
    parsed_alert["network"]["source_ip"]
    == "192.168.1.100"
)

assert (
    parsed_alert["network"]["destination_ip"]
    == "10.0.0.50"
)

assert (
    parsed_alert["network"]["source_port"]
    == "49152"
)

assert (
    parsed_alert["network"]["destination_port"]
    == "8080"
)

assert (
    parsed_alert["network"]["protocol"]
    == "TCP"
)


print("\nJSON object parsing successful.")


# ============================================================
# TEST 2 — PARSE JSON STRING
# ============================================================

print("\nTesting JSON string parsing...")


with open(
    ALERT_PATH,
    "r",
    encoding="utf-8"
) as f:

    json_string = f.read()


parsed_from_string = parser.parse_json(
    json_string
)


# ============================================================
# VALIDATE JSON STRING PARSING
# ============================================================

assert (
    parsed_from_string["alert_id"]
    == "1764860000.123456"
)

assert (
    parsed_from_string["network"]["protocol"]
    == "TCP"
)

assert (
    parsed_from_string["network"]["destination_port"]
    == "8080"
)


print("JSON string parsing successful.")


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 60)
print("WAZUH ALERT PARSER TEST SUCCESSFUL")
print("=" * 60)