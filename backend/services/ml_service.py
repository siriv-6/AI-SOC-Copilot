import os
import json
import joblib
import numpy as np


class MLPredictionService:

    def __init__(self):

        # ============================================================
        # PROJECT PATH
        # ============================================================

        PROJECT_ROOT = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )

        MODEL_DIR = os.path.join(
            PROJECT_ROOT,
            "backend",
            "models"
        )

        MODEL_PATH = os.path.join(
            MODEL_DIR,
            "random_forest_class_weighted.pkl"
        )

        FEATURES_PATH = os.path.join(
            MODEL_DIR,
            "selected_features.json"
        )

        LABEL_MAPPING_PATH = os.path.join(
            MODEL_DIR,
            "label_mapping.json"
        )

        # ============================================================
        # PRINT LOADING INFORMATION
        # ============================================================

        print("============================================================")
        print("Loading ML Prediction Service")
        print("============================================================")

        print(
            f"Model path: {MODEL_PATH}"
        )

        print(
            f"Features path: {FEATURES_PATH}"
        )

        print(
            f"Label mapping path: {LABEL_MAPPING_PATH}"
        )

        # ============================================================
        # CHECK MODEL FILES
        # ============================================================

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"ML model not found at: {MODEL_PATH}"
            )

        if not os.path.exists(FEATURES_PATH):
            raise FileNotFoundError(
                f"Selected features file not found at: "
                f"{FEATURES_PATH}"
            )

        if not os.path.exists(LABEL_MAPPING_PATH):
            raise FileNotFoundError(
                f"Label mapping file not found at: "
                f"{LABEL_MAPPING_PATH}"
            )

        # ============================================================
        # LOAD RANDOM FOREST MODEL
        # ============================================================

        self.model = joblib.load(
            MODEL_PATH
        )

        # ============================================================
        # LOAD SELECTED FEATURES
        # ============================================================

        with open(
            FEATURES_PATH,
            "r"
        ) as f:

            self.selected_features = json.load(f)

        # ============================================================
        # LOAD LABEL MAPPING
        # ============================================================

        with open(
            LABEL_MAPPING_PATH,
            "r"
        ) as f:

            label_mapping_data = json.load(f)

        # ============================================================
        # CONVERT LABEL MAPPING
        # ============================================================

        # Your JSON format is:
        #
        # {
        #     "BENIGN": 0,
        #     "Bot": 1,
        #     "DDoS": 2
        # }
        #
        # Convert it to:
        #
        # {
        #     0: "BENIGN",
        #     1: "Bot",
        #     2: "DDoS"
        # }

        self.label_mapping = {
            int(value): key
            for key, value in label_mapping_data.items()
        }

        # ============================================================
        # PRINT MODEL INFORMATION
        # ============================================================

        print(
            "ML Prediction Service loaded successfully!"
        )

        print(
            "Model:",
            type(self.model)
        )

        print(
            "Number of features:",
            len(self.selected_features)
        )

        print(
            "Number of classes:",
            len(self.label_mapping)
        )

        print(
            "Label mapping:"
        )

        for class_id, label in self.label_mapping.items():

            print(
                f"{class_id} -> {label}"
            )

        print("============================================================")


    # ============================================================
    # PREDICT NETWORK FLOW
    # ============================================================

    def predict(
        self,
        feature_values
    ):

        print("\n============================================================")
        print("ML PREDICTION SERVICE")
        print("============================================================")

        # ============================================================
        # VALIDATE INPUT TYPE
        # ============================================================

        if not isinstance(
            feature_values,
            (list, tuple, np.ndarray)
        ):

            raise TypeError(
                "feature_values must be a list, tuple, "
                "or numpy array containing numeric values."
            )

        # ============================================================
        # VALIDATE FEATURE COUNT
        # ============================================================

        if len(feature_values) != len(
            self.selected_features
        ):

            raise ValueError(
                f"Feature count mismatch. "
                f"Model expects "
                f"{len(self.selected_features)} features, "
                f"but received "
                f"{len(feature_values)}."
            )

        # ============================================================
        # CONVERT FEATURES TO NUMPY ARRAY
        # ============================================================

        try:

            features = np.array(
                [feature_values],
                dtype=float
            )

        except Exception as e:

            raise ValueError(
                f"Feature values must contain only numeric "
                f"values. Error: {str(e)}"
            )

        # ============================================================
        # CHECK ARRAY SHAPE
        # ============================================================

        if features.shape[1] != len(
            self.selected_features
        ):

            raise ValueError(
                f"Invalid feature shape. "
                f"Expected "
                f"{len(self.selected_features)} features, "
                f"received {features.shape[1]}."
            )

        print(
            f"Input feature count: "
            f"{features.shape[1]}"
        )

        # ============================================================
        # MAKE CLASS PREDICTION
        # ============================================================

        prediction = self.model.predict(
            features
        )

        predicted_class_id = int(
            prediction[0]
        )

        # ============================================================
        # GET PREDICTED LABEL
        # ============================================================

        predicted_label = self.label_mapping.get(
            predicted_class_id,
            "Unknown"
        )

        # ============================================================
        # GET PREDICTION PROBABILITIES
        # ============================================================

        probabilities = self.model.predict_proba(
            features
        )[0]

        # ============================================================
        # GET CONFIDENCE
        # ============================================================

        confidence = float(
            np.max(probabilities)
        )

        # ============================================================
        # GET TOP 3 PREDICTIONS
        # ============================================================

        top_3_indices = np.argsort(
            probabilities
        )[-3:][::-1]

        top_3_predictions = []

        for class_id in top_3_indices:

            class_id = int(
                class_id
            )

            top_3_predictions.append(
                {
                    "class_id": class_id,

                    "label": self.label_mapping.get(
                        class_id,
                        "Unknown"
                    ),

                    "confidence": round(
                        float(
                            probabilities[class_id]
                        ) * 100,
                        2
                    )
                }
            )

        # ============================================================
        # CREATE RESULT
        # ============================================================

        result = {

            "predicted_class_id":
                predicted_class_id,

            "predicted_label":
                predicted_label,

            "confidence":
                round(
                    confidence * 100,
                    2
                ),

            "top_3_predictions":
                top_3_predictions

        }

        # ============================================================
        # PRINT RESULT
        # ============================================================

        print(
            "Predicted Class ID:",
            predicted_class_id
        )

        print(
            "Predicted Label:",
            predicted_label
        )

        print(
            "Confidence:",
            round(
                confidence * 100,
                2
            ),
            "%"
        )

        print(
            "============================================================"
        )

        # ============================================================
        # RETURN RESULT
        # ============================================================

        return result
    