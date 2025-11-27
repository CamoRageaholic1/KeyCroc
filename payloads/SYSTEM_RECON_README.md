# System Reconnaissance Payload

## ⚠️ CRITICAL LEGAL WARNING

**This payload is for AUTHORIZED PENETRATION TESTING ONLY.**

### Required Before Use:
- ✅ Written authorization from system owner
- ✅ Clearly defined scope
- ✅ Documented test plan
- ✅ Appropriate legal agreements

### Illegal Without Authorization:
- Computer Fraud and Abuse Act (CFAA) - 18 U.S.C. § 1030
- Electronic Communications Privacy Act (ECPA)
- **⚠️ CHECK YOUR LOCAL AND STATE LAWS** - Penalties vary by jurisdiction

### Consequences of Unauthorized Use:
- Federal imprisonment (up to 10 years)
- Fines up to $250,000
- Civil liability
- Professional license revocation
- Permanent criminal record

**See [LEGAL_DISCLAIMER.md](../../LEGAL_DISCLAIMER.md) for complete details.**

---

## Overview

**System Reconnaissance** is a comprehensive enumeration payload that rapidly gathers system information for authorized security assessments.

### Purpose
- Understand target system configuration
- Identify potential security gaps
- Establish baseline for further testing
- Document system state

### Educational Value
- Teaches attackers' initial enumeration techniques
- Shows defenders what information is exposed
- Demonstrates importance of least privilege
- Highlights critical system information to protect

---

## Technical Details

### Target Systems
- Windows 8, 8.1
- Windows 10 (all versions)
- Windows 11
- Windows Server 2012 R2, 2016, 2019, 2022

### Attack Modes
- **HID:** Keyboard emulation for command execution
- **Storage:** Mass storage for loot exfiltration

### Execution Time
- **Average:** 45-90 seconds
- **Depends on:** System performance, antivirus scanning, network latency

### Stealth Level
- **Low:** PowerShell window briefly visible
- **High process activity:** Multiple enumeration commands
- **Network traffic:** DNS queries, domain checks (if domain-joined)

---

## Information Gathered

### System Information
- ✅ OS version, build, architecture
- ✅ Computer name and domain
- ✅ Installed hotfixes and patches
- ✅ System manufacturer and model
- ✅ Boot time and uptime
- ✅ Time zone

### Network Configuration
- ✅ IP addresses (IPv4/IPv6)
- ✅ MAC addresses
- ✅ Default gateway
- ✅ DNS servers
- ✅ DHCP status
- ✅ Network adapters (enabled/disabled)
- ✅ Routing table
- ✅ ARP cache
- ✅ Active connections (netstat)
- ✅ DNS cache

### User Information
- ✅ Current user (username, SID, privileges)
- ✅ User groups and memberships
- ✅ Local user accounts
- ✅ Local groups
- ✅ Domain information (if domain-joined)
- ✅ Domain trusts

### Software and Services
- ✅ Installed applications (name, version, publisher)
- ✅ Running processes (top 50 by CPU)
- ✅ Running services
- ✅ Startup programs
- ✅ Scheduled tasks
- ✅ Antivirus products
- ✅ Windows Defender status

### Security Configuration
- ✅ Firewall status (all profiles)
- ✅ Firewall rules
- ✅ Network shares
- ✅ Share permissions
- ✅ PowerShell execution policy
- ✅ PowerShell command history

### Recent Activity
- ✅ Recent documents
- ✅ USB device history
- ✅ Connected devices (current and historical)

### Environment
- ✅ Environment variables
- ✅ PATH variable
- ✅ System directories

---

## Output Format

### File Naming
```
recon-[COMPUTERNAME]-[YYYYMMDD-HHMMSS].txt
```

**Example:**
```
recon-DESKTOP-ABC123-20251126-143022.txt
```

### File Structure
```
==============================================
SYSTEM RECONNAISSANCE REPORT
Generated: 11/26/2025 2:30:22 PM
==============================================

[SYSTEM INFORMATION]
Host Name:                 DESKTOP-ABC123
OS Name:                   Microsoft Windows 10 Pro
OS Version:                10.0.19045 N/A Build 19045
...

[NETWORK CONFIGURATION]
Ethernet adapter Ethernet:
   Connection-specific DNS Suffix  . : home.local
   IPv4 Address. . . . . . . . . . . : 192.168.1.100
   ...

[RUNNING PROCESSES]
ProcessName       CPU(s)     PM(M)      Id
-----------       ------     -----      --
chrome            45.2       512.4      1234
...

[INSTALLED SOFTWARE]
DisplayName              DisplayVersion    Publisher
-----------              --------------    ---------
Google Chrome            120.0.6099.129   Google LLC
...
```

---

## Usage

### Basic Execution

1. **Prepare KeyCroc:**
   ```bash
   # Copy payload to KeyCroc
   scp system-recon.croc root@172.16.64.1:/root/payloads/
   
   # SSH into KeyCroc
   ssh root@172.16.64.1
   
   # Set as active payload
   cp /root/payloads/system-recon.croc /root/payload.croc
   ```

2. **Deploy:**
   - Connect KeyCroc inline between target keyboard and computer
   - Or temporarily disconnect keyboard and insert KeyCroc
   - Payload executes automatically on insertion

3. **Retrieve Loot:**
   ```bash
   # Via SCP
   scp root@172.16.64.1:/root/loot/system-recon/* ./
   
   # Or mount storage and copy files
   ```

### LED Status Indicators

| LED Pattern | Meaning |
|-------------|---------|
| Green/Blue slow | Setup phase |
| Blue fast | Attack in progress |
| Green solid | Success - loot captured |
| Red slow | Failure - check logs |

---

## Defensive Countermeasures

### Prevention

**1. Physical Security**
- ✅ Lock workstations when unattended (Windows+L)
- ✅ Disable unused USB ports in BIOS
- ✅ Use USB port locks/blockers
- ✅ Implement clean desk policy
- ✅ Video surveillance in sensitive areas

**2. USB Device Controls**
- ✅ Enable USB device whitelisting (Group Policy)
- ✅ Block HID devices from executing commands
- ✅ Require administrator approval for new devices
- ✅ Use Device Guard / AppLocker

**3. PowerShell Protections**
- ✅ Enable PowerShell logging (Script Block, Module, Transcription)
- ✅ Set execution policy to AllSigned
- ✅ Enable Constrained Language Mode
- ✅ Remove PowerShell v2 (legacy, no logging)
- ✅ Implement Just Enough Administration (JEA)

**4. Least Privilege**
- ✅ Standard users cannot access sensitive registry keys
- ✅ Limit WMI access to administrators
- ✅ Restrict systeminfo, net, and ipconfig commands
- ✅ Use Protected Users security group

### Detection

**Windows Event Logs to Monitor:**

| Event ID | Description | Severity |
|----------|-------------|----------|
| 4688 | Process Creation (with command line) | Medium |
| 4663 | Object Access Attempt | Low |
| 6416 | New External Device | Medium |
| 4103 | PowerShell Module Logging | Medium |
| 4104 | PowerShell Script Block Logging | High |

**Suspicious Indicators:**
```
Alert: Multiple enumeration commands in < 60 seconds
- systeminfo.exe
- ipconfig.exe /all
- whoami.exe /all
- net.exe user
- net.exe localgroup
- netstat.exe -ano
- Get-Process, Get-Service, Get-CimInstance

Source: powershell.exe
Parent: rundll32.exe or explorer.exe
= HIGH CONFIDENCE INDICATOR
```

**SIEM Correlation Rule:**
```
USB Device Connected (Event 6416)
  + PowerShell Execution (Event 4688) within 30 seconds
  + Multiple System Commands (systeminfo, ipconfig, net) within 60 seconds
  + File Created on Removable Media
= CRITICAL ALERT: Possible KeyCroc Attack
```

**Behavioral Analytics:**
- Unusual process tree (explorer.exe → powershell.exe)
- Rapid succession of system enumeration commands
- File writes to recently connected USB device
- PowerShell accessing multiple registry hives
- Network enumeration from user workstation

### Response

**Immediate Actions:**
1. ⚠️ **DO NOT UNPLUG DEVICE** - Preserve evidence
2. ✅ Disconnect network cable
3. ✅ Take photo of device
4. ✅ Note connection time
5. ✅ Contact security team

**Forensic Collection:**
- Memory dump (before disconnection)
- USB device info (VID/PID, serial, files)
- Event logs (Security, System, PowerShell)
- Process list with command lines
- Network connections

**Containment:**
- Isolate system from network
- Disable user account
- Block device at network layer
- Alert SOC/IR team

---

## Payload Customization

### Modify Information Gathered

**Add Custom Checks:**
```bash
# In system-recon.croc, add before Phase 4:

# Check for specific software
Q STRING "Write-Section ''; Write-Section '[CUSTOM CHECK]'; "
Q STRING "Get-ItemProperty 'HKLM:\\Software\\CompanyName\\Product' | Out-File -Append -FilePath \$outPath;"
Q ENTER
```

### Adjust Timing
```bash
# Increase delays for slower systems
Q DELAY 3000  # Default: 1000-2000ms

# Decrease for faster execution (higher detection risk)
Q DELAY 500
```

### Stealth Modifications
```bash
# Hide PowerShell window better
Q STRING "powershell -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass"

# Obfuscate commands (not recommended - focus on authorized testing)
```

---

## Analysis of Captured Data

### Quick Analysis

**Look for:**
- Unpatched systems (systeminfo output)
- Weak firewall rules (firewall status)
- Exposed shares (net share)
- Privileged users (whoami /all)
- Installed security products (antivirus)
- Network topology (routing table, ARP)

**Security Gaps:**
- Missing patches
- Disabled antivirus
- Firewall disabled
- Weak passwords (if credentials captured)
- Unnecessary services running
- Overly permissive shares

### Automated Analysis

See [tools/loot-analyzer.py](../../tools/loot-analyzer.py) for automated parsing and reporting.

---

## Comparison to Other Payloads

| Payload | Focus | Stealth | Speed | Complexity |
|---------|-------|---------|-------|------------|
| System Recon | Enumeration | Low | Fast | Low |
| Cred Exfil | Credentials | Medium | Slow | High |
| Browser Exfil | Browser data | Medium | Medium | Medium |

---

## Educational Resources

### Learn More About Enumeration

**Training:**
- SANS SEC560: Network Penetration Testing
- Offensive Security PEN-200: PWK
- eLearnSecurity eCPPT

**Tools:**
- PowerSploit (PowerShell post-exploitation)
- Empire (PowerShell post-exploitation framework)
- BloodHound (Active Directory mapping)

**Reading:**
- "The Hacker Playbook" by Peter Kim
- "Red Team Field Manual" by Ben Clark
- MITRE ATT&CK: Discovery tactics (TA0007)

### Blue Team Resources

**Detection:**
- SANS SEC504: Hacker Tools, Techniques, Exploits
- SANS FOR508: Advanced Incident Response
- Splunk for Security
- ELK Stack for SIEM

**Hardening:**
- CIS Benchmarks for Windows
- Microsoft Security Baselines
- NIST 800-53 Controls

---

## MITRE ATT&CK Mapping

This payload demonstrates techniques from:

| Tactic | Technique | ID |
|--------|-----------|-----|
| Discovery | System Information Discovery | T1082 |
| Discovery | System Network Configuration Discovery | T1016 |
| Discovery | System Network Connections Discovery | T1049 |
| Discovery | Process Discovery | T1057 |
| Discovery | Software Discovery | T1518 |
| Discovery | Permission Groups Discovery | T1069 |
| Discovery | System Owner/User Discovery | T1033 |
| Discovery | Account Discovery | T1087 |
| Discovery | Network Share Discovery | T1135 |
| Discovery | Peripheral Device Discovery | T1120 |
| Execution | PowerShell | T1059.001 |
| Collection | Data from Local System | T1005 |
| Exfiltration | Exfiltration Over Physical Medium | T1052 |

---

## Troubleshooting

### Payload Doesn't Execute
- Check USB connection
- Verify payload.croc is in correct location
- Check KeyCroc logs: `cat /tmp/payload.log`
- Ensure target is unlocked

### No Output File Created
- Antivirus may be blocking
- PowerShell execution policy may be restricted
- User may not have write permissions
- Check Windows Event Logs for errors

### Partial Output
- System may be too slow (increase delays)
- Antivirus interrupted execution
- PowerShell constrained language mode
- Network timeout for domain queries

### Device Not Recognized
- Driver installation may be required (first use)
- USB port may be disabled
- Device Control policy blocking
- Try different USB port

---

## Changelog

### Version 1.0 (November 2025)
- Initial release
- Comprehensive system enumeration
- 25+ information categories
- Educational defensive guidance

---

## Contributing

Improvements welcome! Consider:
- Additional enumeration techniques
- Better stealth methods
- Enhanced parsing scripts
- Detection rule improvements

---

## License

MIT License - See [LICENSE](../../LICENSE)

---

## Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED TESTING PURPOSES ONLY**

The author is not responsible for misuse of this payload. Users are solely responsible for:
- Obtaining proper authorization
- Complying with all applicable laws
- Consequences of their actions
- Ensuring ethical use

---

**Author:** David Osisek (CamoZeroDay)  
**Version:** 1.0  
**Last Updated:** November 2025

**Remember: Authorized testing only. Always get written permission.**
