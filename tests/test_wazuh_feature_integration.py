from backend.parser.wazuh_parser import WazuhAlertParser
from backend.parser.feature_extractor import NetworkFeatureExtractor


print("=" * 70)
print("STEP 31 - WAZUH ALERT TO FEATURE EXTRACTION INTEGRATION")
print("=" * 70)


# ============================================================
# SAMPLE WAZUH ALERT
# ============================================================

sample_alert = {

    "id": "alert-001",

    "timestamp": "2026-08-13T08:30:00.000+0000",

    "rule": {
        "id": "100001",
        "level": 10,
        "description": "Suspicious network activity detected"
    },

    "agent": {
        "id": "001",
        "name": "SOC-Ubuntu-Web"
    },

    "data": {

        "srcip": "192.168.1.100",
        "srcport": "54321",

        "dstip": "192.168.1.20",
        "dstport": "8080",

        "protocol": "TCP",

        # ====================================================
        # 20 ML FEATURES
        # ====================================================

        "packet_length_variance": 8424.25731,

        "packet_length_mean": 30.42105263,

        "total_length_of_fwd_packets": 322.0,

        "bwd_packet_length_max": 256.0,

        "init_win_bytes_backward": 110.0,

        "max_packet_length": 322.0,

        "fwd_packet_length_max": 322.0,

        "init_win_bytes_forward": 29200.0,

        "flow_iat_max": 10200000.0,

        "fwd_header_length": 296.0,

        "flow_duration": 60202640.0,

        "fwd_packet_length_mean": 35.77777778,

        "fwd_iat_mean": 6396441.875,

        "destination_port": 8080.0,

        "flow_bytes_per_second": 9.600907867,

        "bwd_header_length": 296.0,

        "bwd_packets_per_second": 0.149495105,

        "flow_packets_per_second": 0.29899021,

        "flow_iat_mean": 3541331.765,

        "fwd_iat_std": 5268489.909
    }
}


# ============================================================
# INITIALIZE COMPONENTS
# ============================================================

print("\nInitializing Wazuh Alert Parser...")

parser = WazuhAlertParser()

print("Parser initialized successfully.")


print("\nInitializing Feature Extractor...")

extractor = NetworkFeatureExtractor()

print("Feature extractor initialized successfully.")


# ============================================================
# STEP 1
# PARSE WAZUH ALERT
# ============================================================

print("\n" + "-" * 70)
print("STEP 1 - PARSING WAZUH ALERT")
print("-" * 70)

parsed_alert = parser.parse_alert(sample_alert)

print("Wazuh alert parsed successfully.")


# ============================================================
# VALIDATE PARSED ALERT
# ============================================================

assert "alert_id" in parsed_alert

assert "rule" in parsed_alert

assert "agent" in parsed_alert

assert "network" in parsed_alert

assert "flow_features" in parsed_alert

print("Parsed alert structure validation: PASSED")


# ============================================================
# STEP 2
# EXTRACT FLOW FEATURES
# ============================================================

print("\n" + "-" * 70)
print("STEP 2 - EXTRACTING NETWORK FEATURES")
print("-" * 70)


flow_features = parsed_alert["flow_features"]


print(
    f"Flow features available: "
    f"{len(flow_features)}"
)


# ============================================================
# VALIDATE FEATURE COUNT
# ============================================================

assert len(flow_features) == 20

print(
    "20-feature availability validation: PASSED"
)


# ============================================================
# STEP 3
# FEATURE EXTRACTION
# ============================================================

print("\n" + "-" * 70)
print("STEP 3 - BUILDING ML FEATURE VECTOR")
print("-" * 70)


features = extractor.extract_from_flow(
    flow_features
)


# ============================================================
# VALIDATE FEATURE VECTOR
# ============================================================

assert len(features) == 20

print(
    "ML feature vector length: "
    f"{len(features)}"
)

print(
    "Feature vector validation: PASSED"
)


# ============================================================
# DISPLAY FEATURES
# ============================================================

print("\nExtracted ML features:")

for index, (name, value) in enumerate(
    zip(
        extractor.REQUIRED_FEATURES,
        features
    ),
    start=1
):

    print(
        f"{index:02d}. "
        f"{name}: "
        f"{value}"
    )


# ============================================================
# VALIDATE NUMERIC VALUES
# ============================================================

for value in features:

    assert isinstance(
        value,
        (int, float)
    )


print(
    "\nNumeric feature validation: PASSED"
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("STEP 31 INTEGRATION TEST SUCCESSFUL")
print("=" * 70)

print(
    "\nVerified pipeline:"
)

print(
    "Wazuh Alert"
    " -> Wazuh Parser"
    " -> Flow Features"
    " -> Feature Extractor"
    " -> 20 ML Features"
)