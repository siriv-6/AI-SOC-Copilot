import json


class WazuhAlertParser:

    def __init__(self):
        print("Wazuh Alert Parser initialized")

    def parse_alert(self, alert):
        """
        Parse a Wazuh alert JSON object and extract
        the relevant SOC alert information.
        """

        if not isinstance(alert, dict):
            raise ValueError(
                "Wazuh alert must be a dictionary"
            )

        # Basic alert information
        alert_id = alert.get("id")
        timestamp = alert.get("timestamp")

        # Rule information
        rule = alert.get("rule", {})

        rule_id = rule.get("id")
        rule_description = rule.get("description")
        rule_level = rule.get("level")

        # Agent information
        agent = alert.get("agent", {})

        agent_id = agent.get("id")
        agent_name = agent.get("name")

        # Network information
        data = alert.get("data", {})

        src_ip = data.get("srcip")
        dst_ip = data.get("dstip")
        src_port = data.get("srcport")
        dst_port = data.get("dstport")
        protocol = data.get("protocol")

        # Structured alert
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
            }
        }

        return parsed_alert

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
    