# Defensive Guide: Protecting Against KeyCroc Attacks

## 🛡️ Blue Team Defense Strategies

This guide provides comprehensive defensive measures against physical USB attacks like those demonstrated by KeyCroc payloads.

---

## Table of Contents

1. [Defense-in-Depth Strategy](#defense-in-depth-strategy)
2. [Physical Security Controls](#physical-security-controls)
3. [Endpoint Protection](#endpoint-protection)
4. [Network Security](#network-security)
5. [Detection and Monitoring](#detection-and-monitoring)
6. [User Training](#user-training)
7. [Incident Response](#incident-response)
8. [Payload-Specific Defenses](#payload-specific-defenses)

---

## Defense-in-Depth Strategy

### Layered Security Model

```
┌─────────────────────────────────────┐
│   Physical Security (Layer 1)      │
├─────────────────────────────────────┤
│   USB Device Controls (Layer 2)    │
├─────────────────────────────────────┤
│   Endpoint Protection (Layer 3)    │
├─────────────────────────────────────┤
│   Network Security (Layer 4)       │
├─────────────────────────────────────┤
│   Monitoring & Detection (Layer 5) │
├─────────────────────────────────────┤
│   User Awareness (Layer 6)         │
└─────────────────────────────────────┘
```

**No single control is sufficient. Implement multiple layers.**

---

## Physical Security Controls

### 1. USB Port Management

**Disable Unused Ports:**
- Use BIOS/UEFI settings to disable unused USB ports
- Physically fill ports with USB port locks/blockers
- Document which ports are business-critical

**Port Configuration:**
```powershell
# Disable USB storage via Group Policy
# Computer Configuration > Administrative Templates > System > Removable Storage Access
# Set "All Removable Storage classes: Deny all access" to Enabled
```

### 2. Physical Access Controls

**Workspace Security:**
- ✅ Lock workstations when unattended (Windows+L)
- ✅ Enable automatic screen lock (1-5 minutes idle)
- ✅ Use cable locks for laptops
- ✅ Implement clean desk policy
- ✅ Video surveillance in sensitive areas

**Visitor Management:**
- ✅ Escort all visitors
- ✅ No unattended access to workstations
- ✅ Visitor badge system
- ✅ Sign-in/sign-out logs

### 3. Device Security

**Tamper-Evident Seals:**
- Use security tape on USB ports
- Implement port usage logging
- Regular physical audits

---

## Endpoint Protection

### 1. USB Device Whitelisting

**Allow Only Authorized Devices:**

**Windows (Group Policy):**
```powershell
# Device Installation Restrictions
Computer Configuration > Administrative Templates > System > Device Installation > Device Installation Restrictions

Settings:
- "Prevent installation of devices not described by other policy settings" = Enabled
- "Allow installation of devices that match these device IDs" = [Authorized device IDs]
```

**Commercial Solutions:**
- Device Control Plus (ManageEngine)
- Endpoint Protector (CoSoSys)
- DeviceLock
- Symantec Endpoint Protection

### 2. Antivirus and EDR

**Detection Capabilities:**
- ✅ Behavioral analysis
- ✅ Script execution monitoring
- ✅ Memory analysis
- ✅ Network communication monitoring

**Recommended Solutions:**
- CrowdStrike Falcon
- Microsoft Defender for Endpoint
- SentinelOne
- Carbon Black

**Key Features:**
- PowerShell logging and monitoring
- WMI activity tracking
- Suspicious registry changes
- Credential dumping detection

### 3. Application Whitelisting

**Block Unauthorized Scripts:**

**Windows AppLocker:**
```powershell
# Enable AppLocker
Computer Configuration > Windows Settings > Security Settings > Application Control Policies

Rules:
- Allow only signed PowerShell scripts
- Block scripts from temp directories
- Require administrator approval for new executables
```

### 4. PowerShell Protections

**Security Configuration:**

```powershell
# Enable PowerShell logging
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" -Name "EnableScriptBlockLogging" -Value 1

# Enable transcription
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\Transcription" -Name "EnableTranscripting" -Value 1

# Enable module logging
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ModuleLogging" -Name "EnableModuleLogging" -Value 1

# Constrained Language Mode
$ExecutionContext.SessionState.LanguageMode = "ConstrainedLanguage"
```

**Additional Protections:**
- Require signed scripts (Set-ExecutionPolicy AllSigned)
- Just Enough Administration (JEA)
- PowerShell v5+ with enhanced logging
- Remove PowerShell v2 (used to bypass protections)

---

## Network Security

### 1. Network Segmentation

**Isolate Critical Systems:**
- Separate VLAN for workstations
- Restricted access to file servers
- DMZ for internet-facing systems
- Jump boxes for administrative access

### 2. Egress Filtering

**Block Unauthorized Outbound:**
- Default deny outbound traffic
- Whitelist required destinations
- Block common exfiltration protocols
- Monitor DNS queries

**Suspicious Outbound Indicators:**
- SMB traffic to external IPs
- HTTPS to unusual ports
- DNS tunneling patterns
- Large data transfers

### 3. Internal Firewall Rules

**Restrict Lateral Movement:**
```
Allow: Workstation → Domain Controller (Kerberos, LDAP, DNS)
Allow: Workstation → File Server (SMB)
Deny: Workstation → Workstation (SMB)
Deny: Workstation → External (SMB, RDP, SSH)
```

---

## Detection and Monitoring

### 1. USB Device Logging

**Enable Audit Policies:**

**Windows Event Logs to Monitor:**
- Event ID 6416: New external device recognized
- Event ID 20001/20003: USB device connected/disconnected
- Event ID 1003: USB device installation
- Event ID 4663: Object access attempt
- Event ID 4688: Process creation (with command line)

**Enable Logging:**
```powershell
# Enable USB device audit logging
auditpol /set /subcategory:"Plug and Play Events" /success:enable /failure:enable

# Enable process command line auditing
auditpol /set /subcategory:"Process Creation" /success:enable

# Enable detailed tracking
Computer Configuration > Windows Settings > Security Settings > Advanced Audit Policy Configuration
```

### 2. SIEM Integration

**Log Sources to Collect:**
- Windows Event Logs (Security, System, PowerShell)
- Antivirus/EDR alerts
- Firewall logs
- DNS query logs
- Proxy logs
- Network flow data

**Correlation Rules:**

**Suspicious USB Activity:**
```
USB Device Connected (6416)
  + PowerShell Execution (4688) within 60 seconds
  + Network Connection to External IP within 5 minutes
  = High Priority Alert
```

**Credential Dumping:**
```
LSASS Memory Access (Process: Not System)
  + Registry Access (SAM/SYSTEM hives)
  + SMB Connection to External IP
  = Critical Alert
```

### 3. Behavioral Analytics

**Anomaly Detection:**
- USB device usage outside normal hours
- First-time device connections
- Unusual process trees (explorer.exe → powershell.exe)
- Abnormal data transfer volumes
- Processes accessing sensitive files

### 4. Real-Time Alerting

**Critical Alerts:**
- ⚠️ Unrecognized USB device connected
- ⚠️ PowerShell launched from removable media
- ⚠️ Mimikatz or credential dumping signatures
- ⚠️ SAM/SYSTEM registry hive access
- ⚠️ LSASS memory dump
- ⚠️ Suspicious network connections from user workstation

---

## User Training

### 1. Security Awareness

**Training Topics:**
- USB device risks (malware, data theft)
- Social engineering tactics
- Clean desk policy
- Screen locking discipline
- Recognizing suspicious devices
- Reporting procedures

### 2. USB Threat Scenarios

**Training Examples:**
- "Found USB" drives in parking lot
- Promotional USB drives from unknown sources
- Charging cables that could be malicious
- KeyCroc devices disguised as legitimate cables

### 3. Phishing and Pretexting

**Common Attack Vectors:**
- Attacker poses as IT support
- Requests user to "test" USB device
- Sends malicious USB in mail
- Leaves devices in common areas

### 4. Reporting Culture

**Encourage Reporting:**
- No-blame policy for honest mistakes
- Easy reporting mechanisms
- Rapid response to reports
- Recognition for security vigilance

---

## Incident Response

### 1. USB Security Incident Procedure

**Immediate Actions:**
1. ⚠️ **DO NOT UNPLUG DEVICE** - May destroy evidence
2. ✅ Disconnect network cable or disable WiFi
3. ✅ Take photo of device and connection
4. ✅ Note time of discovery
5. ✅ Contact security team

### 2. Evidence Preservation

**Forensic Collection:**
- Memory dump (capture LSASS, running processes)
- USB device information (VID/PID, serial, files)
- Event logs (Security, System, PowerShell)
- Network traffic capture
- Process list and command lines

**Tools:**
- FTK Imager (memory and disk imaging)
- USB Detective (USB forensics)
- Wireshark (network capture)
- PowerShell Get-Process, Get-NetTCPConnection

### 3. Containment

**Immediate:**
- Isolate affected system from network
- Disable user account
- Block device MAC/IP at switch/firewall
- Alert other teams (SOC, IR, legal)

**Short-term:**
- Identify data accessed/exfiltrated
- Check for persistence mechanisms
- Scan for additional compromised systems
- Revoke credentials if exposed

### 4. Eradication and Recovery

**Remove Threat:**
- Full malware scan
- Remove persistence (scheduled tasks, registry, startup)
- Patch vulnerabilities
- Re-image if necessary

**Credential Reset:**
- Force password reset for affected users
- Invalidate cached credentials
- Reset service account passwords
- Review Kerberos tickets

### 5. Post-Incident

**Analysis:**
- Root cause analysis
- Attack timeline reconstruction
- Data loss assessment
- Control failures identified

**Improvements:**
- Update detection rules
- Enhance monitoring
- Improve controls
- Update training
- Share lessons learned

---

## Payload-Specific Defenses

### System Recon Payload

**Attack:** Enumerates system information, network config, processes

**Defenses:**
- ✅ Monitor for rapid system enumeration commands
- ✅ Restrict WMI access to administrators only
- ✅ Alert on multiple system info queries in short timeframe
- ✅ Limit information available to standard users

**Detection:**
```
Process: systeminfo.exe, ipconfig.exe, whoami.exe, net.exe
Executed from: Removable media
Within: < 60 seconds
= High confidence indicator
```

---

### Credential Exfiltration Payload

**Attack:** Dumps passwords, registry hives, LSASS memory

**Defenses:**
- ✅ Credential Guard (Windows 10/11 Enterprise)
- ✅ Protected Users security group
- ✅ LSA Protection (RunAsPPL)
- ✅ Restrict LSASS memory access
- ✅ Monitor SYSTEM/SAM registry access

**Detection:**
```
Process: reg.exe save HKLM\SAM
OR
Process accessing LSASS memory (not System)
OR
vssadmin.exe create shadow
= Critical Alert
```

**Mitigation:**
```powershell
# Enable LSA Protection
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "RunAsPPL" -Value 1

# Enable Credential Guard
# Requires TPM 2.0 and UEFI
Enable-WindowsOptionalFeature -Online -FeatureName "IsolatedUserMode"
```

---

### Browser Data Exfiltration

**Attack:** Steals browser history, bookmarks, cookies

**Defenses:**
- ✅ Clear browser data on exit (policy)
- ✅ Use credential managers (not browser storage)
- ✅ Enable browser sync encryption
- ✅ Monitor access to browser profile directories
- ✅ Encrypt user profile directories

**Detection:**
```
File Access: %LocalAppData%\Google\Chrome\User Data\*
OR: %AppData%\Mozilla\Firefox\Profiles\*
By: Process on removable media
= Medium Alert
```

---

### Clipboard Monitor

**Attack:** Captures clipboard contents

**Defenses:**
- ✅ Use clipboard managers with encryption
- ✅ Clear clipboard after sensitive operations
- ✅ Don't copy passwords to clipboard
- ✅ Monitor clipboard API access

**Detection:**
```
API Call: GetClipboardData
From: Unsigned executable
OR: Process on removable media
= Low-Medium Alert
```

---

### Network Share Discovery

**Attack:** Enumerates accessible SMB shares

**Defenses:**
- ✅ Principle of least privilege on shares
- ✅ Disable SMBv1
- ✅ Require authentication for all shares
- ✅ Monitor net view, net use commands
- ✅ Network segmentation

**Detection:**
```
Command: net view /domain
OR: net view \\computer
Frequency: > 10 in 5 minutes
= Medium Alert
```

---

## Detection Tool Recommendations

### Commercial SIEM/EDR
- Splunk Enterprise Security
- Microsoft Sentinel
- CrowdStrike Falcon
- Elastic Security
- IBM QRadar

### Open Source
- Wazuh (SIEM/XDR)
- OSSEC (HIDS)
- Sysmon (Windows logging)
- Zeek (Network monitoring)
- TheHive (Incident response)

### USB-Specific
- USBGuard (Linux)
- DeviceFilter (Windows)
- USB Write Blocker (forensics)

---

## Quick Reference: Key Indicators

### Suspicious USB Activity

| Indicator | Severity | Action |
|-----------|----------|--------|
| Unrecognized device VID/PID | Medium | Investigate device |
| Device with keyboard + storage | High | Block and investigate |
| PowerShell from removable media | Critical | Isolate immediately |
| Registry hive access | Critical | Incident response |
| LSASS memory access | Critical | Incident response |
| SMB to external IP | High | Block and investigate |
| Rapid enumeration commands | Medium | Monitor closely |

---

## Compliance Considerations

### Regulatory Requirements

**PCI DSS:**
- Requirement 9: Restrict physical access
- Requirement 10: Track and monitor access

**HIPAA:**
- Physical safeguards (164.310)
- Device and media controls

**NIST 800-53:**
- MP-7: Media Use
- PE-3: Physical Access Control
- SI-4: Information System Monitoring

---

## Testing Your Defenses

### Purple Team Exercises

**Safely Test Controls:**
1. Use isolated test environment
2. Coordinate with blue team
3. Document findings
4. Measure detection time
5. Improve based on results

**Metrics to Track:**
- Time to detect
- Time to alert
- Time to respond
- False positive rate
- Coverage gaps

---

## Additional Resources

### Industry Guidelines
- NIST SP 800-171: Protecting CUI
- CIS Controls: USB Device Control
- SANS: USB Defense-in-Depth

### Tools and Scripts
- Microsoft Attack Surface Analyzer
- Sysinternals Suite
- PowerShell security modules
- YARA rules for USB malware

### Training
- SANS SEC504: Hacker Tools, Techniques, Exploits
- SANS FOR508: Advanced Incident Response
- Offensive Security PEN-200: PWK

---

## Summary

### Defense Checklist

- [ ] Physical security controls in place
- [ ] USB device whitelisting configured
- [ ] Endpoint protection deployed
- [ ] PowerShell logging enabled
- [ ] Network segmentation implemented
- [ ] SIEM collecting relevant logs
- [ ] Alert rules configured
- [ ] User training completed
- [ ] Incident response plan documented
- [ ] Regular testing conducted

---

**Remember: Security is a process, not a product. Continuously monitor, test, and improve your defenses.**

*Last Updated: November 2025*
