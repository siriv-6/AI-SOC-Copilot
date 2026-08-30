# Week 2 — End-to-End SOC Integration Validation

## Objective
Prove that the full pipeline works:
Nithin's Endpoints → Wazuh Agents → Secure Network (Tailscale) → Joy's Wazuh Manager → Wazuh Indexer → Wazuh Dashboard

---

## Step 1 — Wazuh Dashboard Access
- Dashboard loads: SUCCESS
- Login works:SUCCESS
- No major service errors observed

## Step 2 — Agent Visibility
| Agent Name | ID | OS | IP Address | Status |
|---|---|---|---|---|
| DESKTOP-ISFGJMC | 002 | Windows 10 Pro 10.0.19045.3803 | 10.0.2.4 | active |
| soc-ubuntu-web | 003 | Ubuntu 24.04.4 LTS | 10.0.2.5 | active |

Wazuh Manager: **SOC-Ubuntu-SIEM**
Wazuh Manager Address (from `ossec.conf`): **100.78.147.127**, port **1514**

## Step 3 — Test Events Generated (Nithin)
| Endpoint | Event | Time Generated |
|---|---|---|
| soc-ubuntu-web | `sudo systemctl restart ssh` | Aug 30, 2026 @ 14:57:21 UTC (= 20:27 IST) |
| DESKTOP-ISFGJMC | Logout | Aug 30, 2026 @ 20:30 IST |
| DESKTOP-ISFGJMC | Login | Aug 30, 2026 @ 20:32 IST |

## Step 4 — Events Verified in Wazuh Dashboard (Joy)
| Agent Name | Timestamp (Wazuh) | Rule Description | Rule ID | Severity |
|---|---|---|---|---|
| soc-ubuntu-web | Aug 30, 2026 @ 20:27:22.813 | Successful sudo to ROOT executed | 5402 | 3 |
| soc-ubuntu-web | Aug 30, 2026 @ 20:27:22.812 | PAM: Login session opened | 5501 | 3 |
| soc-ubuntu-web | Aug 30, 2026 @ 20:27:22.813 | PAM: Login session closed | 5502 | 3 |
| DESKTOP-ISFGJMC | Aug 30, 2026 @ 20:31:37.618 | Non service account logged off | 67023 | 3 |
| DESKTOP-ISFGJMC | Aug 30, 2026 @ 20:31:40.861 | Windows Workstation Logon Success | 60118 | 3 |
| DESKTOP-ISFGJMC | Aug 30, 2026 @ 20:31:40.967 | Special privileges assigned to new logon | 67028 | 3 |

All events correspond directly to Nithin's test activities — confirmed by matching timestamps (within ~1-2 minutes, accounting for normal ingestion delay).

## Step 5 — End-to-End Integration Test
| Machine | Event Type | Time Generated (Nithin) | Time Received (Joy, Wazuh) | Match |
|---|---|---|---|---|
| soc-ubuntu-web | SSH service restart | 14:57:21 UTC (20:27 IST) | 20:27:22 IST | SUCCESS |
| DESKTOP-ISFGJMC | Logout | 20:30 IST | 20:31:37 IST | SUCCESS |
| DESKTOP-ISFGJMC | Login | 20:32 IST | 20:31:40 IST | SUCCESS |

**End-to-End Integration: SUCCESS** — events traveled successfully through the full pipeline (Agent → Manager → Indexer → Dashboard) for both endpoints.

## Step 6 — Integration Evidence
Screenshots captured:
1. Nithin's Windows/Ubuntu event generation (Event Viewer / terminal + journalctl output)
2. Wazuh Agent running (`wazuh-agentd: Connected to the server` log line)
3. Joy's Wazuh Dashboard (Overview: 480+ total events, authentication success/failure counts)
4. Agent visible in Wazuh (Endpoints page — both agents listed, active status)
5. Corresponding event/alert (Events tab, filtered by agent name, matching rule/timestamp)
6. End-to-end successful integration (side-by-side: Nithin's recorded time vs Wazuh's received time)

---


Task 4 Deliverables 

1. Functional Wazuh Dashboard
Dashboard loads: SUCCESS
Login works: SUCCESS
No major service errors observed

2. Nithin's Windows Agent visible
Agent Name: DESKTOP-ISFGJMC
ID: 002
OS: Windows 10 Pro 10.0.19045.3803
IP Address: 10.0.2.4
Status: active

3. Nithin's Ubuntu Agent visible
Agent Name: soc-ubuntu-web
ID: 003
OS: Ubuntu 24.04.4 LTS
IP Address: 10.0.2.5
Status: active

4. Test event received / 5. Alert/event visible in Dashboard

Endpoint: SOC-Ubuntu-Web
Event Generated: SSH service restart (sudo systemctl restart ssh)
Time Generated: Aug 30, 2026 @ 14:57:21 UTC (= 20:27 IST)
Wazuh Agent: soc-ubuntu-web
Wazuh Manager: SOC-Ubuntu-SIEM (100.78.147.127:1514)
Alert/Rule: Successful sudo to ROOT executed (Rule ID 5402); PAM: Login session opened (5501); PAM: Login session closed (5502)
Severity: 3
Dashboard Verification: SUCCESS
End-to-End Integration: SUCCESS

Endpoint: SOC-Windows10
Event Generated: Logout
Time Generated: Aug 30, 2026 @ 20:30 IST
Wazuh Agent: DESKTOP-ISFGJMC
Wazuh Manager: SOC-Ubuntu-SIEM (100.78.147.127:1514)
Alert/Rule: Non service account logged off (Rule ID 67023)
Severity: 3
Dashboard Verification: SUCCESS
End-to-End Integration: SUCCESS

Endpoint: SOC-Windows10
Event Generated: Login
Time Generated: Aug 30, 2026 @ 20:32 IST
Wazuh Agent: DESKTOP-ISFGJMC
Wazuh Manager: SOC-Ubuntu-SIEM (100.78.147.127:1514)
Alert/Rule: Windows Workstation Logon Success (Rule ID 60118); Special privileges assigned to new logon (Rule ID 67028)
Severity: 3
Dashboard Verification: SUCCESS
End-to-End Integration: SUCCESS

6. End-to-end integration 
DONE

7. Integration test results
Machine: soc-ubuntu-web | Event: SSH service restart | Time Generated: 14:57:21 UTC (20:27 IST) | Time Received: 20:27:22 IST | Result: SUCCESS
Machine: DESKTOP-ISFGJMC | Event: Logout | Time Generated: 20:30 IST | Time Received: 20:31:37 IST | Result: SUCCESS
Machine: DESKTOP-ISFGJMC | Event: Login | Time Generated: 20:32 IST | Time Received: 20:31:40 IST | Result: SUCCESS
End-to-End Integration: SUCCESS

8. Problems and solutions
**Problem 1 — Device registered on wrong Tailscale network**
Joy's laptop initially joined Nithin's invite as a *user*, but the *device* itself remained registered to Joy's own personal Tailscale network, so it never appeared on Nithin's tailnet Machines list despite showing "Connected" locally.
**Solution:** Logged out of the Tailscale app, re-accepted Nithin's invite link, and explicitly selected `nithin2006july@gmail.com` as the tailnet when reconnecting the device. Device now shows correctly under Nithin's tailnet with IP 100.78.147.127.

**Problem 2 — VM system clocks were out of sync**
Both the Windows and Ubuntu VMs had incorrect system time (Windows off by ~1 day at one point; Ubuntu clock reporting UTC instead of IST), causing generated event timestamps to appear mismatched against what Wazuh displayed.
**Solution:** Forced clock resync — `w32tm /resync /force` on Windows, `sudo timedatectl set-ntp true` on Ubuntu. Also identified that Ubuntu's clock was correctly synced but displaying in **UTC**, while the Wazuh Dashboard displays in **IST** — a 5.5 hour offset, not an actual error. Documented this so future comparisons account for the timezone difference rather than assuming a fault.

**Recommendation for future runs:** Before any test event generation, run a quick clock pre-check (`w32tm /resync /force` on Windows, `timedatectl` on Ubuntu) to avoid re-encountering Problem 2.

9. Final Week 2 SOC status
Wazuh Dashboard functional: SUCCESS
Nithin's Windows Agent visible and active: SUCCESS
Nithin's Ubuntu Agent visible and active: SUCCESS
Test events received from both endpoints: SUCCESS
Alerts/events visible and correctly attributed in Dashboard: SUCCESS
End-to-end integration confirmed successful: SUCCESS
Secure connectivity (Tailscale) issue identified and resolved: SUCCESS
VM clock sync issue identified and resolved: SUCCESS

---

## Final Week 2 SOC Status
- ✅ Wazuh Dashboard functional
- ✅ Nithin's Windows Agent visible and active
- ✅ Nithin's Ubuntu Agent visible and active
- ✅ Test events received from both endpoints
- ✅ Alerts/events visible and correctly attributed in Dashboard
- ✅ End-to-end integration confirmed successful
- ✅ Secure connectivity (Tailscale) issue identified and resolved
- ✅ VM clock sync issue identified and resolved

**Overall Task 4 Status: COMPLETE**
