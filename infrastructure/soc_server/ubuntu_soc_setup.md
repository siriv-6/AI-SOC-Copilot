Ubuntu SOC Server Setup 



## VM Specifications
- **VM Name:** SOC-Ubuntu-SIEM
- **Operating System:** Ubuntu 26.04 LTS
- **Kernel:** Linux 7.0.0-28-generic
- **CPU:** 4 cores (AMD Ryzen 5 5600H host, KVM virtualization)
- **RAM:** 8192 MB allocated (8 GB) — ~5.3GB visible to OS
- **Storage:** 80 GB (resized from default 25GB during creation)
- **Hypervisor:** Oracle VirtualBox

## Hostname Configuration
- **Command used:** `sudo hostnamectl set-hostname SOC-Ubuntu-SIEM`
- **Verified via:** `hostnamectl`
- **Result:** Static hostname: SOC-Ubuntu-SIEM (persists across reboots)

## Network Configuration
- **Commands used:** `ip addr`, `ip route`
- **Interface:** enp0s3
- **IP Address:** 10.0.2.15/24 (VirtualBox NAT network)
- **MAC Address:** 08:00:27:fa:be:12
- **Gateway:** 10.0.2.2
- **Note:** Temporary NAT-based IP for Week 1 standalone testing (working independently per project plan). Final planned architecture IP: 192.168.10.40 — to be configured during network/pfSense integration phase.

## SSH Configuration
- **Status check:** `sudo systemctl status ssh` → initially inactive (dead)
- **Enabled via:** `sudo systemctl enable ssh`
- **Started via:** `sudo systemctl start ssh`
- **Result:** Active: active (running), listening on port 22 (IPv4 & IPv6)

## System Resource Verification
- **df -h:** Root (/) = 39G total, 7.3G used, 29G available (20% used); /boot = 2.0G total, 183M used
- **free -h:** Total RAM = 5.3Gi, Used = 511Mi, Available = 4.8Gi, Swap = 4.0Gi (0B used)
- **lscpu:** AMD Ryzen 5 5600H, 4 cores / 4 threads, KVM virtualization (full)
- **ping -c 4 8.8.8.8:** 4/4 packets received, 0% packet loss, avg RTT 70.3ms — Internet connectivity confirmed

## Tools Verified (for future Wazuh readiness)
- **Git version:** 2.53.0
- **Curl version:** 8.18.0
- **Python3 version:** 3.14.4
- **System status:** Fully updated (`sudo apt update && sudo apt upgrade -y`)

## Commands Used (Full List)
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install net-tools curl wget git vim openssh-server -y
sudo hostnamectl set-hostname SOC-Ubuntu-SIEM
hostnamectl
ip addr
ip route
sudo systemctl status ssh
sudo systemctl enable ssh
sudo systemctl start ssh
df -h
free -h
lscpu
ping -c 4 8.8.8.8
git --version
curl --version
python3 --version
```

## Server Readiness Status
✅ VM created and running (SOC-Ubuntu-SIEM, Ubuntu 26.04 LTS)
✅ CPU: 4 cores, RAM: 8GB allocated, Storage: 80GB
✅ Hostname configured: SOC-Ubuntu-SIEM
✅ IP address documented: 10.0.2.15/24 (NAT, temporary — final planned IP 192.168.10.40)
✅ MAC address documented: 08:00:27:fa:be:12
✅ SSH enabled and running (port 22)
✅ Internet connectivity verified (0% packet loss)
✅ System resources confirmed sufficient
✅ Git, Curl, Python3 verified
✅ **Server is ready for Wazuh installation in the next phase**