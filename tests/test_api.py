import requests


URL = "http://127.0.0.1:8000/predict"


# Sample network flow
payload = {
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


response = requests.post(
    URL,
    json=payload
)


print("HTTP Status Code:", response.status_code)

if response.status_code == 200:

    result = response.json()

    print("\n===== API TEST SUCCESSFUL =====")

    print(
        "Predicted Label:",
        result["predicted_label"]
    )

    print(
        "Confidence:",
        result["confidence"],
        "%"
    )

    print("\nTop 3 Predictions:")

    for prediction in result["top_3_predictions"]:

        print(
            f"{prediction['label']} - "
            f"{prediction['confidence']}%"
        )

else:

    print("\n===== API TEST FAILED =====")
    print(response.text)
    