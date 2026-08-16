from backend.services.ml_service import MLPredictionService


print("=" * 60)
print("TESTING ML PREDICTION SERVICE")
print("=" * 60)


# Create service

ml_service = MLPredictionService()


# Check model

print("\nModel loaded:")
print(type(ml_service.model))


# Check selected features

print("\nNumber of selected features:")
print(len(ml_service.selected_features))


# Check classes

print("\nNumber of classes:")
print(len(ml_service.label_mapping))


# Display mapping

print("\nLabel mapping:")

for class_id, label in ml_service.label_mapping.items():

    print(
        class_id,
        "->",
        label
    )


print("\nML Prediction Service test completed successfully!")
