import json


class WazuhAlertParser:

    def __init__(self):
        print("Wazuh Alert Parser initialized")

    # ============================================================
    # PARSE WAZUH ALERT
    # ============================================================

    def parse_alert(self, alert):
        """
        Parse a Wazuh alert JSON object and extract
        relevant SOC alert information and network-flow features.
        """

        if not isinstance(alert, dict):
            raise ValueError(
                "Wazuh alert must be a dictionary"
            )

        # ========================================================
        # BASIC ALERT INFORMATION
        # ========================================================

        alert_id = alert.get("id")
        timestamp = alert.get("timestamp")

        # ========================================================
        # RULE INFORMATION
        # ========================================================

        rule = alert.get("rule", {})

        rule_id = rule.get("id")
        rule_description = rule.get("description")
        rule_level = rule.get("level")

        # ========================================================
        # AGENT INFORMATION
        # ========================================================

        agent = alert.get("agent", {})

        agent_id = agent.get("id")
        agent_name = agent.get("name")

        # ========================================================
        # NETWORK / FLOW INFORMATION
        # ========================================================

        data = alert.get("data", {})

        src_ip = data.get("srcip")
        dst_ip = data.get("dstip")
        src_port = data.get("srcport")
        dst_port = data.get("dstport")
        protocol = data.get("protocol")

        # ========================================================
        # EXTRACT ML FEATURES
        # ========================================================

        ml_feature_names = [
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

        flow_features = {}

        for feature in ml_feature_names:

            if feature in data:

                flow_features[feature] = data[feature]

        # ========================================================
        # STRUCTURED ALERT
        # ========================================================

        parsed_alert = {

            "alert_id": alert_id,

            "timestamp": timestamp,

            "rule": {
                "id": rule_id,
                "description": rule_description,
                "level": rule_level
            },

            "agent": {
                "id": agent_id,
                "name": agent_name
            },

            "network": {

                "source_ip": src_ip,

                "destination_ip": dst_ip,

                "source_port": src_port,

                "destination_port": dst_port,

                "protocol": protocol
            },

            # ====================================================
            # ML NETWORK FLOW FEATURES
            # ====================================================

            "flow_features": flow_features
        }

        return parsed_alert

    # ============================================================
    # PARSE JSON STRING
    # ============================================================

    def parse_json(self, json_string):
        """
        Parse a Wazuh alert from a JSON string.
        """

        try:

            alert = json.loads(json_string)

        except json.JSONDecodeError as e:

            raise ValueError(
                f"Invalid Wazuh JSON: {e}"
            )

        return self.parse_alert(alert)