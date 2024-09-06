# KeyCroc Cred Exfil on Screenlock Payload
Works with KeyCroc and Ducky

Author: David Osisek
Version: 1.4
Overview

This script captures credentials (username and password) from a Windows machine, waits for a lock screen event, and automatically logs back in to deliver a payload. The payload dumps various credentials and system information from browsers, Windows Vault, Wi-Fi profiles, SAM files, and LSASS memory. After executing the payload, the script cleans up and locks the screen again to maintain stealth.

The payload is designed to run on Windows 8/10/11 and is optimized for use with Hak5's KeyCroc device for penetration testing.

Features

Credential Capture: Captures the username and password entered by the target before the system locks.
Lock Screen Detection: Waits for the user to lock the system (via Win + L), then detects the next login attempt.
Automatic Login: Logs back into the system using the captured credentials.
Payload Execution: Once logged in, the script runs the payload to gather sensitive data (browsers, Wi-Fi, system info, SAM hashes, LSASS memory dump).
Stealth Cleanup: Deletes traces of the payload, stops the SMB and HTTP servers, and removes temporary files.
Final Lock: Re-locks the screen after executing the payload to avoid suspicion.
Requirements

Hak5 KeyCroc
Go (for HTTP server functionality)
pip3 (for installing Impacket)
Impacket (for SMB server functionality)
gohttp (for HTTP server)
PowerShell scripts:
Get-ChromeDump.ps1
Get-FoxDump.ps1
Out-Minidump.ps1
The script automatically installs and downloads these dependencies if they are not already installed.

Installation

Clone or copy the script to your KeyCroc device or another environment where it will be executed.
Ensure that the KeyCroc is set up properly with an internet connection, and that it is connected to the target machine.
Verify prerequisites: Make sure the following tools are available on the system:
Go
pip3
Impacket
gohttp
PowerShell
If these are not available, the script will automatically install them.
Place the required PowerShell scripts (Get-ChromeDump.ps1, Get-FoxDump.ps1, Out-Minidump.ps1) in the /tools/DumpCreds directory, or the script will download them automatically.
Usage

Run the Payload
Start the script on the KeyCroc device.
The script will run in the background, capturing credentials and waiting for a lock event (Win + L) on the target system.
When the target system locks and unlocks:
The KeyCroc logs back in using the captured credentials.
The script runs the payload to extract the following:
Chrome and Firefox usernames and passwords.
Windows Vault credentials.
Wi-Fi credentials.
SAM, LSASS memory dumps (if admin rights are available).
The script cleans up temporary files and re-locks the system.
Captured data will be exfiltrated to the SMB share set up by the script.
Cleanup

After the script completes:

All temporary files (including exfiltrated data) are moved to a safe directory (/root/loot/dumpcreds).
The temporary SMB and HTTP servers are stopped.
The system is re-locked for stealth.
Legal Disclaimer

This script is intended for educational purposes only and should only be used for legal, authorized security testing with explicit permission from the system owner. Unauthorized access to computer systems, theft of credentials, and any form of unauthorized exploitation are illegal and unethical. The author and distributor of this script are not responsible for any misuse or illegal activity performed with this tool.

Additional Notes

This script assumes admin privileges on the target system. If admin privileges are not available, certain data dumps (such as SAM and LSASS) may not succeed.
Timing Considerations: Depending on the system's resources and network connection, delays might be needed between certain steps (e.g., file downloads and exfiltration).
Script Customization: You may need to adjust the MATCH patterns for capturing the username and password based on the target environment (e.g., if the system requires a specific login format or process).
