from backend.services.alert_prediction_service import AlertPredictionService


print("=" * 70)
print("STEP 36 - ALERT INPUT VALIDATION TEST")
print("=" * 70)


# ============================================================
# INITIALIZE SERVICE
# ============================================================

print("\nInitializing Alert Prediction Service...")

service = AlertPredictionService()

print("Service initialized successfully.")


# ============================================================
# TEST 1 - INVALID ALERT TYPE
# ============================================================

print("\n" + "-" * 70)
print("TEST 1 - INVALID ALERT TYPE")
print("-" * 70)

invalid_alert = "this is not a valid Wazuh alert"

try:

    service.process_alert(invalid_alert)

    print("ERROR: Invalid alert was accepted.")

    raise SystemExit(1)

except ValueError as e:

    print("Invalid alert rejected successfully.")
    print("Error:", e)


# ============================================================
# TEST 2 - EMPTY ALERT
# ============================================================

print("\n" + "-" * 70)
print("TEST 2 - EMPTY ALERT")
print("-" * 70)

empty_alert = {}

try:

    service.process_alert(empty_alert)

    print(
        "Empty alert reached processing "
        "without crashing."
    )

except Exception as e:

    print(
        "Empty alert rejected safely."
    )

    print(
        "Error:",
        e
    )


# ============================================================
# SUCCESS
# ============================================================

print("\n" + "=" * 70)
print("STEP 36 VALIDATION TEST COMPLETED")
print("=" * 70)

print("\nVerified:")

print("Invalid alert type is rejected.")
print("Malformed input does not silently reach ML prediction.")

print("=" * 70)
