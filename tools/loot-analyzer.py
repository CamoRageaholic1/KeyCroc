#!/usr/bin/env python3
"""
Loot Analyzer - KeyCroc Payload Analysis Tool
Author: David Osisek (CamoZeroDay)
Description: Automated analysis of captured data from KeyCroc payloads

⚠️ FOR AUTHORIZED PENETRATION TESTING ONLY ⚠️
See LEGAL_DISCLAIMER.md for full details
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict

VERSION = "1.0.0"

class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class LootAnalyzer:
    """Main analysis class"""
    
    def __init__(self, loot_file):
        self.loot_file = loot_file
        self.content = ""
        self.findings = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
            'info': []
        }
        
    def load_file(self):
        """Load loot file"""
        try:
            with open(self.loot_file, 'r', encoding='utf-8', errors='ignore') as f:
                self.content = f.read()
            return True
        except Exception as e:
            print(f"{Colors.RED}Error loading file: {e}{Colors.ENDC}")
            return False
    
    def analyze_system_recon(self):
        """Analyze system reconnaissance output"""
        print(f"\n{Colors.HEADER}{'='*70}")
        print(f"SYSTEM RECONNAISSANCE ANALYSIS")
        print(f"{'='*70}{Colors.ENDC}\n")
        
        # Extract computer name
        comp_match = re.search(r'Host Name:\s+(\S+)', self.content)
        if comp_match:
            print(f"{Colors.CYAN}Computer Name:{Colors.ENDC} {comp_match.group(1)}")
        
        # Extract OS version
        os_match = re.search(r'OS Name:\s+(.+)', self.content)
        if os_match:
            print(f"{Colors.CYAN}Operating System:{Colors.ENDC} {os_match.group(1).strip()}")
        
        # Check for missing patches
        self._check_patches()
        
        # Analyze network config
        self._analyze_network()
        
        # Check running services
        self._analyze_services()
        
        # Check antivirus status
        self._check_antivirus()
        
        # Check firewall status
        self._check_firewall()
        
        # Analyze users and groups
        self._analyze_users()
        
        # Check for shares
        self._check_shares()
        
        # Display findings
        self._display_findings()
    
    def _check_patches(self):
        """Check for missing critical patches"""
        hotfix_section = re.search(r'Hotfix\(s\):(.*?)(?=\n\n|\Z)', self.content, re.DOTALL)
        if hotfix_section:
            hotfixes = re.findall(r'KB\d+', hotfix_section.group(1))
            if len(hotfixes) < 10:
                self.findings['high'].append(f"Only {len(hotfixes)} hotfixes installed - system may be outdated")
        else:
            self.findings['critical'].append("No hotfix information found - system severely outdated")
    
    def _analyze_network(self):
        """Analyze network configuration"""
        print(f"\n{Colors.BLUE}Network Analysis:{Colors.ENDC}")
        
        # Extract IP addresses
        ips = re.findall(r'IPv4 Address[.\s]+:\s+([\d.]+)', self.content)
        for ip in ips:
            if ip != '127.0.0.1':
                print(f"  • IP Address: {ip}")
                if ip.startswith('10.') or ip.startswith('192.168.') or ip.startswith('172.'):
                    self.findings['info'].append(f"Private IP detected: {ip}")
        
        # Check DNS servers
        dns_servers = re.findall(r'DNS Servers[.\s]+:\s+([\d.]+)', self.content)
        for dns in dns_servers:
            print(f"  • DNS Server: {dns}")
            if not dns.startswith(('8.8.', '1.1.', '208.67.')):
                self.findings['medium'].append(f"Non-standard DNS server: {dns} (potential DNS tampering)")
        
        # Check for active connections
        connections = re.findall(r'ESTABLISHED\s+([\d.]+):(\d+)', self.content)
        if len(connections) > 20:
            self.findings['medium'].append(f"{len(connections)} active connections - investigate unusual connections")
    
    def _analyze_services(self):
        """Analyze running services"""
        print(f"\n{Colors.BLUE}Service Analysis:{Colors.ENDC}")
        
        # Look for remote access services
        risky_services = {
            'RemoteRegistry': 'Remote Registry service enabled',
            'RpcSs': 'RPC services running',
            'LanmanServer': 'Server service enabled (file sharing)',
            'TermService': 'Remote Desktop enabled'
        }
        
        for service, description in risky_services.items():
            if re.search(f'{service}.*Running', self.content, re.IGNORECASE):
                print(f"  ⚠ {description}")
                self.findings['medium'].append(description)
    
    def _check_antivirus(self):
        """Check antivirus status"""
        print(f"\n{Colors.BLUE}Security Software:{Colors.ENDC}")
        
        av_section = re.search(r'\[ANTIVIRUS\](.*?)(?=\[|$)', self.content, re.DOTALL)
        if av_section:
            av_products = re.findall(r'displayName\s+:\s+(.+)', av_section.group(1))
            if av_products:
                for av in av_products:
                    print(f"  • {av.strip()}")
                self.findings['info'].append(f"Antivirus detected: {', '.join(av_products)}")
            else:
                print(f"  {Colors.RED}✗ No antivirus products detected{Colors.ENDC}")
                self.findings['critical'].append("No antivirus protection detected")
        
        # Check Windows Defender
        defender_match = re.search(r'RealTimeProtectionEnabled\s+:\s+(\w+)', self.content)
        if defender_match:
            if defender_match.group(1).lower() == 'false':
                print(f"  {Colors.RED}✗ Windows Defender Real-Time Protection: DISABLED{Colors.ENDC}")
                self.findings['high'].append("Windows Defender Real-Time Protection is disabled")
            else:
                print(f"  {Colors.GREEN}✓ Windows Defender Real-Time Protection: ENABLED{Colors.ENDC}")
    
    def _check_firewall(self):
        """Check firewall status"""
        print(f"\n{Colors.BLUE}Firewall Status:{Colors.ENDC}")
        
        firewall_status = re.findall(r'State\s+:\s+(\w+)', self.content)
        disabled_count = firewall_status.count('OFF')
        
        if disabled_count > 0:
            print(f"  {Colors.RED}✗ Firewall disabled on {disabled_count} profile(s){Colors.ENDC}")
            self.findings['critical'].append(f"Firewall disabled on {disabled_count} profile(s)")
        else:
            print(f"  {Colors.GREEN}✓ Firewall enabled on all profiles{Colors.ENDC}")
    
    def _analyze_users(self):
        """Analyze user accounts"""
        print(f"\n{Colors.BLUE}User Analysis:{Colors.ENDC}")
        
        # Check current user privileges
        if re.search(r'BUILTIN\\Administrators', self.content):
            print(f"  {Colors.YELLOW}⚠ Current user has Administrator privileges{Colors.ENDC}")
            self.findings['high'].append("User operating with Administrator privileges")
        
        # Count local users
        user_section = re.search(r'\[LOCAL USERS\](.*?)(?=\[|$)', self.content, re.DOTALL)
        if user_section:
            users = re.findall(r'^(\S+)\s', user_section.group(1), re.MULTILINE)
            print(f"  • Local users: {len(users)}")
            if len(users) > 10:
                self.findings['medium'].append(f"High number of local users ({len(users)}) - review necessary")
    
    def _check_shares(self):
        """Check network shares"""
        print(f"\n{Colors.BLUE}Network Shares:{Colors.ENDC}")
        
        share_section = re.search(r'\[NETWORK SHARES\](.*?)(?=\[|$)', self.content, re.DOTALL)
        if share_section:
            shares = re.findall(r'^(\S+)\s', share_section.group(1), re.MULTILINE)
            shares = [s for s in shares if s not in ['Share', '------', 'The']]
            
            if shares:
                for share in shares:
                    print(f"  • {share}")
                    if share.endswith('$'):
                        self.findings['info'].append(f"Administrative share: {share}")
                    else:
                        self.findings['medium'].append(f"Non-administrative share found: {share}")
    
    def _display_findings(self):
        """Display security findings"""
        print(f"\n{Colors.HEADER}{'='*70}")
        print(f"SECURITY FINDINGS")
        print(f"{'='*70}{Colors.ENDC}\n")
        
        severity_colors = {
            'critical': Colors.RED,
            'high': Colors.YELLOW,
            'medium': Colors.CYAN,
            'low': Colors.BLUE,
            'info': Colors.GREEN
        }
        
        total_findings = 0
        for severity in ['critical', 'high', 'medium', 'low', 'info']:
            if self.findings[severity]:
                color = severity_colors[severity]
                print(f"{color}{severity.upper()}: {len(self.findings[severity])}{Colors.ENDC}")
                for finding in self.findings[severity]:
                    print(f"  • {finding}")
                print()
                total_findings += len(self.findings[severity])
        
        if total_findings == 0:
            print(f"{Colors.GREEN}No significant findings detected.{Colors.ENDC}")
        
        # Risk score
        risk_score = (
            len(self.findings['critical']) * 10 +
            len(self.findings['high']) * 5 +
            len(self.findings['medium']) * 2 +
            len(self.findings['low']) * 1
        )
        
        print(f"\n{Colors.BOLD}Risk Score: {risk_score}{Colors.ENDC}")
        if risk_score >= 20:
            print(f"{Colors.RED}HIGH RISK - Immediate remediation recommended{Colors.ENDC}")
        elif risk_score >= 10:
            print(f"{Colors.YELLOW}MEDIUM RISK - Review and remediate findings{Colors.ENDC}")
        else:
            print(f"{Colors.GREEN}LOW RISK - Maintain current security posture{Colors.ENDC}")
    
    def analyze_cred_exfil(self):
        """Analyze credential exfiltration output"""
        print(f"\n{Colors.HEADER}{'='*70}")
        print(f"CREDENTIAL EXFILTRATION ANALYSIS")
        print(f"{'='*70}{Colors.ENDC}\n")
        
        # Check for Mimikatz output
        if 'mimikatz' in self.content.lower():
            print(f"{Colors.RED}⚠ Mimikatz signatures detected{Colors.ENDC}")
            
            # Look for credentials
            creds = re.findall(r'Username\s*:\s*(\S+).*?Password\s*:\s*(\S+)', self.content, re.DOTALL)
            if creds:
                print(f"\n{Colors.YELLOW}Credentials found: {len(creds)}{Colors.ENDC}")
                self.findings['critical'].append(f"{len(creds)} credentials captured")
        
        # Check for registry hives
        if 'SAM' in self.content or 'SYSTEM' in self.content:
            print(f"{Colors.RED}⚠ Registry hives captured{Colors.ENDC}")
            self.findings['critical'].append("SAM/SYSTEM registry hives captured")
        
        # Check for WiFi passwords
        wifi_matches = re.findall(r'Key Content\s*:\s*(.+)', self.content)
        if wifi_matches:
            print(f"\n{Colors.YELLOW}WiFi passwords found: {len(wifi_matches)}{Colors.ENDC}")
            self.findings['high'].append(f"{len(wifi_matches)} WiFi passwords captured")
        
        self._display_findings()
    
    def export_json(self, output_file):
        """Export findings to JSON"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'loot_file': str(self.loot_file),
            'findings': self.findings,
            'risk_score': (
                len(self.findings['critical']) * 10 +
                len(self.findings['high']) * 5 +
                len(self.findings['medium']) * 2 +
                len(self.findings['low']) * 1
            )
        }
        
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=4)
            print(f"\n{Colors.GREEN}Report exported to: {output_file}{Colors.ENDC}")
        except Exception as e:
            print(f"\n{Colors.RED}Error exporting report: {e}{Colors.ENDC}")

def print_banner():
    """Print tool banner"""
    banner = f"""
{Colors.CYAN}{'='*70}
╔═══════════════════════════════════════════════════════════════════╗
║                    KEYCROC LOOT ANALYZER v{VERSION}                    ║
║                    By David Osisek (CamoZeroDay)                  ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
{Colors.YELLOW}⚠️  FOR AUTHORIZED PENETRATION TESTING ONLY ⚠️{Colors.ENDC}
{Colors.ENDC}"""
    print(banner)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Analyze KeyCroc payload loot files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze system recon output
  python loot-analyzer.py recon-DESKTOP-20251126.txt
  
  # Analyze credential exfiltration
  python loot-analyzer.py -t cred loot-credentials.txt
  
  # Export findings to JSON
  python loot-analyzer.py recon.txt -o report.json
  
  # Batch analyze directory
  python loot-analyzer.py -d /root/loot/system-recon/
        """
    )
    
    parser.add_argument('file', nargs='?', help='Loot file to analyze')
    parser.add_argument('-t', '--type', choices=['auto', 'recon', 'cred'], 
                       default='auto', help='Payload type (default: auto-detect)')
    parser.add_argument('-o', '--output', help='Export findings to JSON file')
    parser.add_argument('-d', '--directory', help='Analyze all files in directory')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}')
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.directory:
        # Batch analysis
        loot_dir = Path(args.directory)
        if not loot_dir.exists():
            print(f"{Colors.RED}Error: Directory not found: {args.directory}{Colors.ENDC}")
            return 1
        
        files = list(loot_dir.glob('*.txt'))
        if not files:
            print(f"{Colors.YELLOW}No .txt files found in directory{Colors.ENDC}")
            return 0
        
        print(f"\n{Colors.CYAN}Analyzing {len(files)} files...{Colors.ENDC}\n")
        
        for loot_file in files:
            print(f"\n{Colors.BOLD}{'='*70}")
            print(f"File: {loot_file.name}")
            print(f"{'='*70}{Colors.ENDC}")
            
            analyzer = LootAnalyzer(loot_file)
            if analyzer.load_file():
                if 'recon' in loot_file.name.lower():
                    analyzer.analyze_system_recon()
                elif 'cred' in loot_file.name.lower():
                    analyzer.analyze_cred_exfil()
                else:
                    analyzer.analyze_system_recon()  # Default
    
    elif args.file:
        # Single file analysis
        loot_file = Path(args.file)
        if not loot_file.exists():
            print(f"{Colors.RED}Error: File not found: {args.file}{Colors.ENDC}")
            return 1
        
        analyzer = LootAnalyzer(loot_file)
        if not analyzer.load_file():
            return 1
        
        # Detect payload type
        payload_type = args.type
        if payload_type == 'auto':
            if 'recon' in loot_file.name.lower() or 'SYSTEM INFORMATION' in analyzer.content:
                payload_type = 'recon'
            elif 'cred' in loot_file.name.lower() or 'mimikatz' in analyzer.content.lower():
                payload_type = 'cred'
            else:
                payload_type = 'recon'  # Default
        
        # Analyze
        if payload_type == 'recon':
            analyzer.analyze_system_recon()
        elif payload_type == 'cred':
            analyzer.analyze_cred_exfil()
        
        # Export if requested
        if args.output:
            analyzer.export_json(args.output)
    
    else:
        parser.print_help()
        return 1
    
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"Analysis complete!")
    print(f"{'='*70}{Colors.ENDC}\n")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Analysis interrupted by user{Colors.ENDC}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)
