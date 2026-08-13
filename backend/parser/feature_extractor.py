class NetworkFeatureExtractor:

    # ============================================================
    # FEATURES REQUIRED BY THE ML MODEL
    # ============================================================

    REQUIRED_FEATURES = [
        "packet_length_variance",
        "packet_length_mean",
        "total_length_of_fwd_packets",
        "bwd_packet_length_max",
        "init_win_bytes_backward",
        "max_packet_length",
        "fwd_packet_length_max",
        "init_win_bytes_forward",
        "flow_iat_max",
        "fwd_header_length",
        "flow_duration",
        "fwd_packet_length_mean",
        "fwd_iat_mean",
        "destination_port",
        "flow_bytes_per_second",
        "bwd_header_length",
        "bwd_packets_per_second",
        "flow_packets_per_second",
        "flow_iat_mean",
        "fwd_iat_std"
    ]

    # ============================================================
    # INITIALIZE
    # ============================================================

    def __init__(self):

        self.feature_names = self.REQUIRED_FEATURES.copy()

    # ============================================================
    # EXTRACT FEATURES FROM NETWORK FLOW
    # ============================================================

    def extract_from_flow(self, flow):

        missing_features = [
            feature
            for feature in self.REQUIRED_FEATURES
            if feature not in flow
        ]

        if missing_features:

            raise ValueError(
                "Missing required network-flow features: "
                + ", ".join(missing_features)
            )

        features = [
            float(flow[feature])
            for feature in self.REQUIRED_FEATURES
        ]

        return features

    # ============================================================
    # RETURN FEATURE DICTIONARY
    # ============================================================

    def extract_feature_dict(self, flow):

        features = self.extract_from_flow(flow)

        return dict(
            zip(
                self.REQUIRED_FEATURES,
                features
            )
        )

    # ============================================================
    # VALIDATE FEATURE VECTOR
    # ============================================================

    def validate(self, features):

        if len(features) != len(self.REQUIRED_FEATURES):

            raise ValueError(
                f"Expected {len(self.REQUIRED_FEATURES)} features, "
                f"but received {len(features)}."
            )

        return True