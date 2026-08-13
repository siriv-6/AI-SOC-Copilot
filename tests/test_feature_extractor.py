from backend.parser.feature_extractor import NetworkFeatureExtractor


print("=" * 60)
print("TESTING NETWORK FEATURE EXTRACTOR")
print("=" * 60)


# ============================================================
# CREATE EXTRACTOR
# ============================================================

extractor = NetworkFeatureExtractor()


print("\nNumber of required features:")
print(len(extractor.REQUIRED_FEATURES))


# ============================================================
# SAMPLE NETWORK FLOW
# ============================================================

sample_flow = {

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


# ============================================================
# EXTRACT FEATURE VECTOR
# ============================================================

features = extractor.extract_from_flow(
    sample_flow
)


print("\nExtracted feature vector:")

for name, value in zip(
    extractor.REQUIRED_FEATURES,
    features
):

    print(
        f"{name}: {value}"
    )


# ============================================================
# VALIDATE
# ============================================================

assert len(features) == 20

assert extractor.validate(
    features
)


# ============================================================
# TEST FEATURE DICTIONARY
# ============================================================

feature_dict = extractor.extract_feature_dict(
    sample_flow
)


assert len(feature_dict) == 20

assert (
    feature_dict["destination_port"]
    == 8080.0
)


print("\nFeature extraction successful.")


print("\n" + "=" * 60)
print("NETWORK FEATURE EXTRACTOR TEST SUCCESSFUL")
print("=" * 60)
