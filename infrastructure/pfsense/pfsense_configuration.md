# pfSense Configuration — Task 4

## pfSense VM Specifications
- **VM Name:** SOC-pfsense
- **Software:** pfSense CE 2.7.2-RELEASE (amd64)
- **Hypervisor:** Oracle VirtualBox
- **OS Type (VirtualBox):** BSD / FreeBSD (64-bit)
- **CPU:** 2 cores
- **RAM:** 2048 MB
- **Storage:** 20 GB (VDI, dynamically allocated)
- **Partitioning:** Auto (UFS), entire disk, MBR partition scheme

## WAN Configuration
- **Interface:** le0
- **VirtualBox Adapter:** Adapter 1 — NAT
- **Assignment method:** Manual (via console "Assign Interfaces")
- **IPv4:** DHCP4 — 10.0.2.15/24 (assigned by VirtualBox NAT)
- **IPv6:** DHCP6 — fd17:625c:f037:2:a00:27ff:feff:900b:64 (auto-assigned)

## LAN Configuration
- **Interface:** le1
- **VirtualBox Adapter:** Adapter 2 — Host-only Adapter (VirtualBox Host-Only Ethernet Adapter #2)
- **Assignment method:** Manual (via console "Assign Interfaces")
- **LAN IP:** 192.168.10.1
- **Subnet:** /24 (255.255.255.0)
- **DHCP Server on LAN:** Disabled (static IP assignment used for SOC server instead)
- **webConfigurator URL:** http://192.168.10.1/

## Firewall Rules
- Default pfSense LAN → any rule left in place, allowing the internal SOC LAN to reach the internet through pfSense (NAT/outbound).
- No WAN → LAN inbound rule created — the SOC environment remains isolated from external/public access, as required by the project plan.

## Connectivity Testing
**Test 1 — SOC Server → pfSense LAN gateway**
```
ping -c 4 192.168.10.1
```
Result: Successful — 4/4 packets received, 0% packet loss.

**Test 2 — Routing confirmation**
```
ip route
```
Result:
```
default via 10.0.2.2 dev enp0s3 proto dhcp src 10.0.2.15 metric 100
192.168.10.0/24 dev enp0s8 proto kernel scope link src 192.168.10.40
```
Confirms the SOC server correctly routes traffic for the 192.168.10.0/24 subnet through its LAN-facing interface (enp0s8), while internet-bound traffic continues via the NAT interface (enp0s3).

## Internet Testing
**Test 1 — Internet reachability (IP)**
```
ping -c 4 8.8.8.8
```
Result: [FILL IN — confirm packets sent/received and packet loss %]

**Test 2 — DNS resolution**
```
ping -c 4 google.com
```
Result: [FILL IN — confirm DNS resolved and packets sent/received]

## Problems Encountered & Troubleshooting

1. **"CPU doesn't support long mode" boot error**
   - Cause: VM was created with OS type set to "Other/Unknown" (32-bit), which disables 64-bit long mode regardless of host CPU capability.
   - Fix: Changed VM Settings → General → OS to BSD → FreeBSD (64-bit). VM booted correctly afterward.

2. **Corrupted virtual disk after install (`vm_fault: pager read error, pid 1 (init)`)**
   - Cause: Likely caused by ejecting the install ISO / force-unmounting while the system was still finalizing a shell/write step during the first reboot cycle.
   - Fix: Removed and deleted the corrupted virtual disk, created a fresh 20 GB VDI, reinstalled pfSense from scratch. On the second attempt, the ISO was only ejected while the VM was idle at the installer welcome screen (not mid-transition), followed by a clean `Machine → Reset` — this avoided the issue.

3. **LAN interface (Adapter 2) not detected by pfSense**
   - Cause: Adapter 2 reverted to "Not attached" in VirtualBox network settings (likely during the storage/disk recreation process).
   - Fix: Re-enabled Adapter 2, re-attached it to "VirtualBox Host-Only Ethernet Adapter #2" (matching the SOC server's adapter), then rebooted the VM — pfSense correctly detected both le0 and le1 afterward.

4. **SOC server's LAN interface pulling a DHCP IP (192.168.56.x) instead of the static IP**
   - Cause: Netplan config for enp0s8 did not explicitly disable DHCP.
   - Fix: Added `dhcp4: false` alongside the static `addresses:` entry in `/etc/netplan/50-cloud-init.yaml`, then ran `sudo netplan apply`. Interface correctly showed 192.168.10.40/24 afterward.

## Final Status
✅ pfSense VM installed and running (pfSense CE 2.7.2-RELEASE)
✅ WAN configured (le0, NAT, DHCP)
✅ LAN configured (le1, Host-only, static 192.168.10.1/24)
✅ SOC Server connected to LAN with static IP 192.168.10.40/24
✅ pfSense connectivity test successful (0% packet loss)
✅ Routing confirmed via `ip route`
✅ Firewall left at safe default (LAN isolated from WAN inbound)
✅ **pfSense and SOC network ready for Wazuh integration in the next phase**
