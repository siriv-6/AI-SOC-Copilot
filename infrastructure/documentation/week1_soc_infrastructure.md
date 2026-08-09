# Week 1 — SOC Infrastructure Summary (Joy)

## Overall SOC Network Diagram
```
              INTERNET
                 │
                 ▼
           WAN Interface
              (le0, NAT)
                 │
          +----------------+
          |    pfSense     |
          |   Firewall     |
          +----------------+
                 │
        LAN: 192.168.10.1
           (le1, Host-only)
                 │
          SOC Internal LAN
                 │
                 ▼
         Ubuntu SOC Server
          192.168.10.40
        (SOC-Ubuntu-SIEM)
```

## pfSense's Role
pfSense (SOC-pfsense) acts as the network security boundary for the SOC lab environment. It separates the internal SOC network from the external/internet-facing side, provides NAT/outbound access for the SOC server, and ensures the SOC environment is not directly exposed to the public internet. It will later host firewall rules governing traffic to/from the SOC infrastructure as the project progresses.

## Ubuntu SOC Server's Role
The Ubuntu SOC Server (SOC-Ubuntu-SIEM) is the dedicated, central machine for the SOC environment. It is the future host for:
- Wazuh
- Security alerts
- Centralized logs
- SOC monitoring
- AI-SOC Copilot integration

It currently sits behind pfSense on the internal SOC LAN with a static IP, ready for the next phase of the project (Wazuh installation).

## IP Address Plan

| Device | IP Address | Role |
|---|---|---|
| Windows 10 | 192.168.10.10 | Employee Workstation |
| Ubuntu Web | 192.168.10.20 | Web/Application Server |
| Kali Linux | 192.168.10.30 | Attacker Machine |
| pfSense | 192.168.10.1 | Firewall (LAN gateway) |
| Ubuntu SOC Server | 192.168.10.40 | SOC Server |

## Network Architecture
- **pfSense WAN (le0):** VirtualBox NAT adapter — provides internet access, DHCP-assigned (10.0.2.15/24)
- **pfSense LAN (le1):** VirtualBox Host-only adapter — static IP 192.168.10.1/24, gateway for the internal SOC network
- **SOC Server:** Two interfaces — enp0s3 (NAT, DHCP, for general internet/updates) and enp0s8 (Host-only, static 192.168.10.40/24, connects to pfSense's LAN)
- Both pfSense's LAN adapter and the SOC server's second adapter are attached to the same VirtualBox Host-only network ("VirtualBox Host-Only Ethernet Adapter #2"), allowing them to communicate directly.
- The SOC environment (server side) is isolated from direct WAN/internet exposure — all inbound access from outside is blocked by pfSense's default firewall posture.

## Week 1 Completion Status

**Task 3 — Ubuntu SOC Server Setup:** ✅ Complete
- VM created, configured, hostname set, SSH enabled, system resources verified, tools (Git/Curl/Python3) confirmed, internet connectivity verified.

**Task 4 — pfSense Firewall & SOC Network Setup:** ✅ Complete
- pfSense VM created and installed, WAN and LAN configured, SOC server connected to LAN with static IP, connectivity to pfSense confirmed, internet/DNS connectivity from SOC server confirmed, firewall left at safe default (no WAN inbound exposure).

**Overall Week 1 status:** Both assigned tasks complete. Infrastructure ready for the next phase (Wazuh installation and SOC monitoring setup).
