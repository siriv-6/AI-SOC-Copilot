# Week 2 — Wazuh SOC Server Setup Summary (Joy)

## Overall SOC Monitoring Architecture
```
        Windows 10 ───────┐
                           │
        Ubuntu Web ───────┼──→ Wazuh Manager
                           │
        Future Endpoints ─┘
                           │
                           ▼
                    Wazuh Indexer
                           │
                           ▼
                   Wazuh Dashboard
                           │
                           ▼
                   Security Alerts
```

## Wazuh Server's Role
The Ubuntu SOC Server (SOC-Ubuntu-SIEM) has been converted into the central Wazuh SOC server. It now runs all three core Wazuh components — Manager, Indexer, and Dashboard — and is ready to receive and process telemetry from Nithin's endpoints (SOC-Windows10, SOC-Ubuntu-Web) once their agents are connected in Task 2/4.

## Server Details

| Item | Value |
|---|---|
| Hostname | SOC-Ubuntu-SIEM |
| OS | Ubuntu 26.04 LTS |
| Wazuh version | 4.14.7 |
| Local IP (NAT) | 10.0.2.15 |
| CPU | AMD Ryzen 5 5600H, 4 cores |
| RAM | 5.3 GiB total |
| Disk | 39 GB total, ~29 GB free |

## Installation Method
Installed using Wazuh's official all-in-one installation assistant (`wazuh-install.sh -a`) from `packages.wazuh.com`, appropriate for a single-node deployment given the VM's available resources.

```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
chmod +x wazuh-install.sh
sudo ./wazuh-install.sh -a
```

## Components & Service Status

| Component | Status |
|---|---|
| Wazuh Manager | ✅ active (running), enabled |
| Wazuh Indexer | ✅ active (running), enabled |
| Wazuh Dashboard | ✅ active (running), enabled |

All three services are set to start automatically on boot and survived a VM restart cleanly.

## Ports in Use

| Port | Service | Purpose |
|---|---|---|
| 443 | wazuh-dashboard | Web dashboard UI |
| 1514 | wazuh-remoted | Agent event/log collection |
| 1515 | wazuh-authd | Agent enrollment/registration |
| 9200 | wazuh-indexer | Indexer API (localhost-bound) |
| 22 | sshd | SSH management access |

No services are exposed beyond what Wazuh requires; the server is not exposed to the public internet.

## Dashboard Access
- Local (VM): `https://10.0.2.15`
- Host access: `https://localhost:8443` via VirtualBox NAT port forwarding (Host IP restricted to `127.0.0.1`, host-only access)
- Login verified successful — dashboard shows Agents Summary, Alerts, and all standard SOC modules (Threat Hunting, Vulnerability Detection, MITRE ATT&CK, File Integrity Monitoring, etc.)
- Agents registered: 0 (expected — pending Nithin's agent installation in Task 2)

## Connectivity for Nithin

| Item | Value |
|---|---|
| Wazuh version | 4.14.7 |
| SOC server local IP | 10.0.2.15 |
| Public exposure | None |
| Connectivity method | Tailscale (overlay VPN) — pending setup |
| Tailscale IP | *pending* |

