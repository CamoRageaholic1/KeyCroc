# KeyCroc Payloads

![Security](https://img.shields.io/badge/Security-Penetration_Testing-red?style=for-the-badge&logo=hackaday&logoColor=white)
![KeyCroc](https://img.shields.io/badge/Hak5-KeyCroc-000000?style=for-the-badge&logo=hackaday&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Educational-yellow?style=for-the-badge)

Custom payloads for Hak5 KeyCroc device - Educational security research and authorized penetration testing.

---

## ⚠️ LEGAL DISCLAIMER - READ BEFORE USE

**🚨 AUTHORIZED USE ONLY 🚨**

This repository contains security research tools intended **EXCLUSIVELY** for:
- ✅ Authorized penetration testing with written permission
- ✅ Educational purposes in controlled lab environments
- ✅ Security research on systems you own
- ✅ Professional security assessments with client authorization

**UNAUTHORIZED USE IS ILLEGAL AND UNETHICAL**

The tools in this repository can be used for credential harvesting and system exploitation. Unauthorized access to computer systems, credential theft, and unauthorized security testing are **FEDERAL CRIMES** under:
- Computer Fraud and Abuse Act (CFAA) - 18 U.S.C. § 1030
- Electronic Communications Privacy Act (ECPA)
- State and international cyber crime laws

**VIOLATION OF THESE LAWS CAN RESULT IN:**
- Criminal prosecution
- Civil lawsuits
- Substantial fines
- Imprisonment
- Permanent criminal record

**BY USING THESE TOOLS YOU AGREE:**
- You have explicit written authorization from system owners
- You understand applicable laws and regulations
- You accept full responsibility for your actions
- The author assumes NO LIABILITY for misuse

---

## 🎯 Purpose

Educational repository demonstrating security research techniques for the Hak5 KeyCroc device. These payloads are designed to help security professionals understand credential exfiltration techniques and develop defensive strategies.

## 📦 Available Payloads

### Credential Exfiltration on Screen Lock

**File:** `payloads/cred-exfil-on-screenlock.croc`

**Description:** Advanced credential harvesting payload that:
- Captures Windows login credentials
- Waits for screen lock event (Win + L)
- Automatically logs back in using captured credentials
- Exfiltrates sensitive data from multiple sources
- Performs cleanup and re-locks screen for stealth

**Capabilities:**
- ✅ Chrome browser credentials
- ✅ Firefox browser credentials
- ✅ Windows Vault passwords
- ✅ Wi-Fi credentials
- ✅ SAM/SECURITY/SYSTEM registry hives (admin required)
- ✅ LSASS memory dump (admin required)
- ✅ System information

**Target:** Windows 8/10/11  
**Version:** 1.4  
**Author:** David Osisek (CamoZeroDay)

## 🔧 Requirements

### Hardware
- Hak5 KeyCroc device
- USB-C cable
- Target Windows system

### Software Dependencies
- **Go** - HTTP server functionality
- **Python 3** with pip3
- **Impacket** - SMB server functionality
- **gohttp** - HTTP server

### PowerShell Scripts (Auto-downloaded)
- `Get-ChromeDump.ps1` - Chrome credential extraction
- `Get-FoxDump.ps1` - Firefox credential extraction
- `Out-Minidump.ps1` - LSASS memory dumping

## 🚀 Setup & Installation

### 1. Prepare KeyCroc Device

```bash
# SSH into your KeyCroc
ssh root@keycroc.lan

# Clone this repository
git clone https://github.com/CamoRageaholic1/KeyCroc.git
cd KeyCroc

# Copy payload to KeyCroc
cp payloads/cred-exfil-on-screenlock.croc /root/udisk/payloads/
```

### 2. Configure Payload

The payload automatically installs dependencies on first run:
- Go
- pip3
- Impacket
- gohttp
- Required PowerShell scripts

### 3. Deploy Payload

1. Insert KeyCroc into target system
2. Payload triggers on match condition: `__dumpcreds`
3. Follow execution flow in logs: `/root/loot/dumpcreds/execution_log.txt`

## 📖 How It Works

### Execution Flow

```
1. Credential Capture
   └─> Captures username and password from target

2. Lock Detection
   └─> Waits for Windows lock screen (Win + L)

3. Automatic Login
   └─> Logs back in using captured credentials

4. Network Setup
   └─> Establishes RNDIS Ethernet connection
   └─> Starts HTTP server (port 80)
   └─> Starts SMB server

5. Data Exfiltration
   └─> Browser credentials (Chrome, Firefox)
   └─> Windows Vault credentials
   └─> Wi-Fi passwords
   └─> SAM/SECURITY/SYSTEM hives (if admin)
   └─> LSASS memory dump (if admin)
   └─> System information

6. Cleanup & Stealth
   └─> Removes execution traces
   └─> Stops HTTP/SMB servers
   └─> Moves data to loot directory
   └─> Re-locks screen

7. Complete
   └─> Data stored in: /root/loot/dumpcreds/<timestamp>/
```

## 🔒 Security Considerations

### Defensive Strategies

Organizations can defend against these attacks by:

1. **Endpoint Security**
   - Deploy EDR (Endpoint Detection & Response)
   - Enable real-time anti-malware
   - Implement application whitelisting
   - Use Device Guard / Credential Guard

2. **USB Security**
   - Disable unauthorized USB devices via Group Policy
   - Use USB port locks physically
   - Implement Device Control policies
   - Monitor USB device connections

3. **Credential Protection**
   - Enable Windows Credential Guard
   - Use Windows Hello for Business
   - Implement MFA/2FA on all accounts
   - Use LAPS for local admin passwords

4. **Network Security**
   - Segment network traffic
   - Monitor for unusual SMB/HTTP traffic
   - Block unauthorized network interfaces
   - Implement NAC (Network Access Control)

5. **User Training**
   - Security awareness training
   - Report suspicious USB devices
   - Never leave workstations unlocked
   - Use screen locks with short timeouts

## 📊 Captured Data

### Data Storage

Exfiltrated data is stored in:
```
/root/loot/dumpcreds/<timestamp>/
├── DumpCreds_systeminfo.txt      # System information
├── DumpCreds_ChromeDump.txt      # Chrome credentials
├── DumpCreds_FoxDump.txt         # Firefox credentials
├── DumpCreds_WiFiDump.txt        # Wi-Fi passwords
├── DumpCreds_VaultDump.txt       # Windows Vault creds
├── DumpCreds_WinLogon.txt        # WinLogon registry
├── lsass_<pid>.dmp               # LSASS memory (if admin)
├── sam                           # SAM registry (if admin)
├── security                      # SECURITY registry (if admin)
└── system                        # SYSTEM registry (if admin)
```

### Data Analysis

LSASS dumps can be analyzed with:
- **Mimikatz** - `sekurlsa::minidump lsass.dmp`
- **pypykatz** - `pypykatz lsa minidump lsass.dmp`

SAM hives can be analyzed with:
- **samdump2** - `samdump2 system sam`
- **impacket-secretsdump** - `secretsdump.py -sam sam -security security -system system LOCAL`

## 📁 Project Structure

```
KeyCroc/
├── payloads/
│   └── cred-exfil-on-screenlock.croc    # Main payload
├── README.md                             # This file
├── LICENSE                               # MIT License
└── .gitignore                            # Ignore loot files
```

## 🛠️ Troubleshooting

### Payload Not Triggering
- Verify match condition: `__dumpcreds`
- Check KeyCroc LED status
- Review logs: `/var/log/croc`

### Dependencies Failing
```bash
# Manually install dependencies
apt-get update
apt-get install -y golang python3-pip
pip3 install impacket
go get github.com/blmayer/gohttp
```

### SMB Server Issues
- Ensure no firewall blocking port 445
- Verify Impacket installation
- Check SMB logs in payload execution log

### Exfiltration Incomplete
- Increase delay values in payload
- Check target system performance
- Verify network connectivity

## 🤝 Contributing

Contributions to defensive research are welcome:

- Improved stealth techniques (for testing detection)
- Additional data sources for exfiltration testing
- Better cleanup mechanisms
- Cross-platform compatibility
- Detection signatures for defensive tools

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Ethical Use Statement

The author of this repository:
- Condemns all unauthorized use of these tools
- Provides these tools for EDUCATIONAL PURPOSES ONLY
- Assumes NO RESPONSIBILITY for misuse
- Encourages ethical security research
- Supports defensive security improvements

**Use these tools responsibly and legally.**

## 📚 Additional Resources

### Learning Resources
- [Hak5 KeyCroc Documentation](https://docs.hak5.org/keycroc/)
- [MITRE ATT&CK - Credential Access](https://attack.mitre.org/tactics/TA0006/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### Detection & Defense
- [Windows Defender ATP](https://www.microsoft.com/en-us/security/business/threat-protection/endpoint-defender)
- [YARA Rules for USB Device Detection](https://github.com/Neo23x0/signature-base)
- [Sysmon for Endpoint Monitoring](https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon)

## 📫 Support

- 🐛 **Bug Reports:** Open an issue on GitHub
- 💡 **Feature Requests:** Educational improvements only
- 📧 **Contact:** For responsible disclosure and ethical inquiries

---

**Author:** David Osisek (CamoZeroDay)  
**Purpose:** Educational security research and authorized penetration testing  
**Reminder:** ALWAYS obtain written authorization before testing

**🔐 Stay Legal. Stay Ethical. Stay Professional. 🔐**
