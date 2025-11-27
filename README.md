# KeyCroc Security Research Payloads

![Security](https://img.shields.io/badge/Security-Research-red?style=for-the-badge&logo=security&logoColor=white)
![Hak5](https://img.shields.io/badge/Hak5-KeyCroc-blue?style=for-the-badge&logo=hackthebox&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Educational-yellow?style=for-the-badge)

**Educational security research payloads for Hak5 KeyCroc USB keystroke injection and data exfiltration device.**

**Author:** David Osisek (CamoZeroDay)  
**Purpose:** Authorized penetration testing and security education

---

## ⚠️ CRITICAL LEGAL WARNING

### READ THIS BEFORE ACCESSING ANY FILES

**ALL payloads in this repository are for AUTHORIZED PENETRATION TESTING ONLY.**

### Illegal Without Authorization:
- **Computer Fraud and Abuse Act (CFAA)** - 18 U.S.C. § 1030
- **Electronic Communications Privacy Act (ECPA)** - 18 U.S.C. § 2510-2523
- **Wiretap Act** - 18 U.S.C. § 2511
- **⚠️ CHECK YOUR LOCAL AND STATE LAWS** - Penalties vary significantly by jurisdiction

### Consequences of Unauthorized Use:
- Federal imprisonment (up to 10 years)
- Fines up to $250,000
- Civil liability for damages
- Professional license revocation
- Permanent criminal record

### Required Before Use:
- ✅ Written authorization from system owner
- ✅ Clearly defined scope of testing
- ✅ Documented test plan
- ✅ Appropriate legal agreements

**📖 [READ FULL LEGAL DISCLAIMER](LEGAL_DISCLAIMER.md)** - Comprehensive legal information

**🛡️ [READ DEFENSIVE GUIDE](DEFENSIVE_GUIDE.md)** - How to protect against these attacks

---

## 📚 Repository Contents

### 📄 Core Documentation
- **[LEGAL_DISCLAIMER.md](LEGAL_DISCLAIMER.md)** - Complete legal framework and warnings
- **[DEFENSIVE_GUIDE.md](DEFENSIVE_GUIDE.md)** - Blue team defense strategies
- **[README.md](README.md)** - This file
- **[LICENSE](LICENSE)** - MIT License
- **[.gitignore](.gitignore)** - Protects sensitive loot data

### 🎯 Payloads

#### 1. System Reconnaissance
**File:** `payloads/system-recon.croc`  
**Documentation:** `payloads/SYSTEM_RECON_README.md`  
**Purpose:** Comprehensive system enumeration

**Capabilities:**
- System information (OS, patches, hardware)
- Network configuration (IP, DNS, routing, ARP)
- User accounts and groups
- Installed software
- Running processes and services
- Security products (AV, firewall)
- Recent activity and USB history

**Execution Time:** 45-90 seconds  
**Stealth Level:** Low (visible PowerShell window)

**[Read Full Documentation →](payloads/SYSTEM_RECON_README.md)**

---

#### 2. Credential Exfiltration on Screenlock
**File:** `payloads/cred-exfil-on-screenlock.croc`  
**Purpose:** Credential harvesting when system locks

**Capabilities:**
- Chrome/Firefox credentials
- Windows Vault passwords
- WiFi passwords
- SAM/SECURITY/SYSTEM registry hives
- LSASS memory dumps

**Execution Flow:**
1. Monitor for screenlock (user logs out)
2. Auto-login as user
3. Execute credential capture
4. Network setup and exfiltration
5. Cleanup traces
6. Re-lock system

**Execution Time:** 2-5 minutes  
**Stealth Level:** Medium (requires screenlock)

**⚠️ Advanced Payload** - Requires deep understanding of Windows authentication

---

### 🛠️ Tools

#### Loot Analyzer
**File:** `tools/loot-analyzer.py`  
**Purpose:** Automated analysis of captured data

**Features:**
- Parses system recon output
- Identifies security gaps
- Risk scoring (Critical/High/Medium/Low)
- JSON export for reporting
- Batch analysis support

**Usage:**
```bash
# Analyze single file
python loot-analyzer.py recon-DESKTOP-20251126.txt

# Batch analyze directory
python loot-analyzer.py -d /root/loot/system-recon/

# Export to JSON
python loot-analyzer.py recon.txt -o report.json
```

**Analysis Includes:**
- Missing patches
- Weak firewall configuration
- Disabled antivirus
- Exposed network shares
- Privileged user accounts
- Unusual network connections

---

## 🎓 Educational Purpose

### For Red Teams (Offense)
- Learn USB attack techniques
- Understand credential exfiltration
- Practice enumeration methods
- Study post-exploitation tactics

### For Blue Teams (Defense)
- Understand attacker methodologies
- Implement detection mechanisms
- Test defensive controls
- Improve security posture

### MITRE ATT&CK Mapping

Payloads demonstrate techniques from:
- **TA0001** - Initial Access
- **TA0002** - Execution (PowerShell)
- **TA0003** - Persistence
- **TA0004** - Privilege Escalation
- **TA0005** - Defense Evasion
- **TA0006** - Credential Access
- **TA0007** - Discovery
- **TA0009** - Collection
- **TA0010** - Exfiltration

---

## 🛡️ Defensive Strategies

### Quick Defense Checklist

**Physical Security:**
- [ ] Lock workstations when unattended (Windows+L)
- [ ] Disable unused USB ports in BIOS
- [ ] Implement clean desk policy
- [ ] Use cable locks for laptops
- [ ] Video surveillance in sensitive areas

**USB Device Controls:**
- [ ] Enable USB device whitelisting
- [ ] Block unauthorized HID devices
- [ ] Require admin approval for new devices
- [ ] Implement Device Guard/AppLocker

**Endpoint Protection:**
- [ ] Deploy EDR solution
- [ ] Enable PowerShell logging (all modules)
- [ ] Set execution policy to AllSigned
- [ ] Remove PowerShell v2
- [ ] Enable Credential Guard

**Network Security:**
- [ ] Network segmentation
- [ ] Egress filtering
- [ ] Block SMB to external IPs
- [ ] Monitor DNS queries

**Monitoring & Detection:**
- [ ] SIEM with USB device correlation
- [ ] Alert on PowerShell from removable media
- [ ] Monitor LSASS memory access
- [ ] Track registry hive access

**📖 [READ FULL DEFENSIVE GUIDE](DEFENSIVE_GUIDE.md)**

---

## 🔍 Detection Methods

### Windows Event Logs

| Event ID | Description | Severity |
|----------|-------------|----------|
| 6416 | New external device recognized | Medium |
| 4688 | Process creation (with command line) | Medium |
| 4103 | PowerShell module logging | Medium |
| 4104 | PowerShell script block logging | High |
| 4663 | Object access attempt | Low |

### SIEM Correlation Rule

```
USB Device Connected (Event 6416)
  + PowerShell Execution (Event 4688) within 30 seconds
  + Multiple System Commands within 60 seconds
  + File Created on Removable Media
= CRITICAL ALERT: Possible KeyCroc Attack
```

### Behavioral Indicators

**High Confidence:**
- PowerShell launched from removable media
- LSASS memory access by non-system process
- SAM/SYSTEM registry hive access
- Multiple enumeration commands in < 60 seconds

**Medium Confidence:**
- Unusual process tree (explorer.exe → powershell.exe)
- Rapid file writes to USB device
- Network connections from user workstation to external IPs
- Registry modifications from removable media

---

## 🚀 Quick Start (Authorized Testing Only)

### Prerequisites
- Hak5 KeyCroc device
- Target system with physical access
- **Written authorization**
- SSH client

### Setup

```bash
# 1. Connect to KeyCroc
ssh root@172.16.64.1
# Default password: hak5croc

# 2. Copy payload to KeyCroc
scp payloads/system-recon.croc root@172.16.64.1:/root/payloads/

# 3. Set as active payload
cp /root/payloads/system-recon.croc /root/payload.croc

# 4. Deploy KeyCroc
# Insert inline between keyboard and computer
# OR temporarily replace keyboard

# 5. Retrieve loot
scp root@172.16.64.1:/root/loot/system-recon/* ./

# 6. Analyze
python tools/loot-analyzer.py recon-*.txt
```

### LED Status Indicators

| LED Pattern | Meaning |
|-------------|----------|
| Green/Blue slow | Setup phase |
| Blue fast | Attack in progress |
| Green solid | Success - loot captured |
| Red slow | Failure - check logs |

---

## 📊 Data Analysis

### Using Loot Analyzer

The included `loot-analyzer.py` tool provides:

**Automated Analysis:**
- Missing security patches
- Firewall configuration issues
- Disabled antivirus
- Weak network security
- Exposed shares
- Privileged user accounts

**Risk Scoring:**
- Critical findings (10 points each)
- High findings (5 points)
- Medium findings (2 points)
- Low findings (1 point)

**Reporting:**
- Console output with color coding
- JSON export for documentation
- Integration with ticketing systems

### Manual Analysis

For credential exfiltration payloads:

```bash
# Extract password hashes
samdump2 SYSTEM SAM

# Analyze LSASS dump
mimikatz
> sekurlsa::minidump lsass.dmp
> sekurlsa::logonpasswords

# Parse Chrome credentials
python chrome-password-decrypt.py

# Analyze registry hives
impacket-secretsdump -sam SAM -system SYSTEM LOCAL
```

---

## 🔐 Payload Security

### Best Practices

**Payload Development:**
- Minimize execution time
- Clean up traces
- Handle errors gracefully
- Test in isolated environment
- Document thoroughly

**Loot Protection:**
- Encrypt captured data
- Use secure transport (SCP/SFTP)
- Delete from KeyCroc after retrieval
- Store securely with access controls
- Follow data retention policies

**Operational Security:**
- Use dedicated KeyCroc per engagement
- Maintain chain of custody
- Document all access
- Sanitize device after use
- Secure physical storage

---

## 🤝 Contributing

### We Welcome Contributions!

**Ideas for contributions:**
- Additional payloads
- Detection improvements
- Analysis tools
- Documentation enhancements
- Defensive strategies

**Contribution Guidelines:**

1. **Fork the repository**
2. **Create feature branch:** `git checkout -b feature/new-payload`
3. **Follow existing structure:**
   - Payload in `/payloads/`
   - Documentation (README.md)
   - Legal disclaimers
   - Defensive countermeasures
4. **Test thoroughly** in isolated environment
5. **Submit pull request** with detailed description

**All contributions must:**
- Include legal disclaimers
- Document defensive countermeasures
- Provide detection methods
- Be educational in nature
- Follow ethical guidelines

---

## 📖 Additional Resources

### Training & Certifications
- **SANS SEC560:** Network Penetration Testing
- **SANS SEC504:** Hacker Tools, Techniques, Exploits
- **SANS FOR508:** Advanced Incident Response
- **Offensive Security PEN-200:** PWK
- **eLearnSecurity eCPPT**

### Tools
- **Mimikatz:** Credential extraction
- **Impacket:** Network protocol toolkit
- **PowerSploit:** PowerShell post-exploitation
- **BloodHound:** Active Directory analysis
- **Sysinternals:** Windows troubleshooting

### Reading
- "The Hacker Playbook" by Peter Kim
- "Red Team Field Manual" by Ben Clark
- "RTFM" by Ben Clark
- MITRE ATT&CK Framework
- NIST 800-53 Security Controls

### Communities
- **Hak5 Forums:** https://forums.hak5.org
- **Reddit /r/netsec:** Security discussions
- **Discord:** Hak5 community server
- **GitHub:** Security tool development

---

## ⚖️ Responsible Disclosure

### If You Discover Vulnerabilities

1. **Report to system owner immediately**
2. **Do NOT exploit beyond proof-of-concept**
3. **Allow reasonable time for patching** (typically 90 days)
4. **Follow coordinated disclosure practices**
5. **Document findings professionally**

**Resources:**
- **HackerOne:** https://www.hackerone.com
- **Bugcrowd:** https://www.bugcrowd.com
- **CERT/CC:** https://www.kb.cert.org/vuls/report/

---

## 📋 Repository Structure

```
KeyCroc/
├── README.md                      # This file
├── LEGAL_DISCLAIMER.md            # Comprehensive legal warnings
├── DEFENSIVE_GUIDE.md             # Blue team strategies
├── LICENSE                        # MIT License
├── .gitignore                     # Protects sensitive data
├── payloads/
│   ├── system-recon.croc          # System enumeration
│   ├── SYSTEM_RECON_README.md     # Full documentation
│   └── cred-exfil-on-screenlock.croc  # Credential harvesting
└── tools/
    └── loot-analyzer.py           # Automated analysis tool
```

---

## 📊 Statistics

- **Payloads:** 2
- **Tools:** 1
- **Documentation Pages:** 5
- **MITRE Techniques:** 15+
- **Detection Methods:** 10+
- **Defensive Controls:** 30+

---

## 🙏 Acknowledgments

### Credit Where Due

- **Hak5:** For creating the KeyCroc platform
- **Security Community:** For knowledge sharing
- **Red Teams:** For offensive techniques
- **Blue Teams:** For defensive strategies
- **MITRE:** For ATT&CK framework

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

**Copyright © 2025 David Osisek**

---

## 📬 Contact

**Author:** David Osisek (CamoZeroDay)  
**GitHub:** [@CamoRageaholic1](https://github.com/CamoRageaholic1)  
**LinkedIn:** [linkedin.com/in/davidosisek](https://linkedin.com/in/davidosisek)

**For questions about:**
- Payload usage → Read documentation
- Legal concerns → Consult attorney
- Defensive strategies → See DEFENSIVE_GUIDE.md
- Contributions → Submit pull request

---

## ⚠️ Final Warning

**UNAUTHORIZED ACCESS IS A FEDERAL CRIME**

- These tools are for **AUTHORIZED TESTING ONLY**
- Violations will result in **CRIMINAL PROSECUTION**
- You are **SOLELY RESPONSIBLE** for your actions
- **CHECK LOCAL LAWS** before use

**If there is ANY doubt about authorization, DO NOT PROCEED.**

---

**🔒 Use Responsibly. Test Ethically. Defend Proactively. 🔒**

*Last Updated: November 2025*
