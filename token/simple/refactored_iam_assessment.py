#!/usr/bin/env python3
"""
Refactored AWS IAM Security Assessment Tool

A straightforward tool to identify IAM security issues:
- Part A: Users without MFA enabled (function-based)
- Part B: Security issues using class-based approach
"""

import json
import boto3
from datetime import datetime
from typing import List, Dict, Any


def get_current_time() -> str:
    """Get current timestamp as string"""
    return datetime.now().isoformat()


def check_mfa_not_enabled(iam_client) -> List[Dict[str, str]]:
    """Part A: Find users without MFA enabled (kept as function)"""
    findings = []
    current_time = get_current_time()
    
    print("Checking for users without MFA...")
    
    try:
        # Get all users
        users = iam_client.list_users()['Users']
        
        for user in users:
            username = user['UserName']
            
            try:
                # Check MFA devices
                mfa_devices = iam_client.list_mfa_devices(UserName=username)
                virtual_mfa = iam_client.list_virtual_mfa_devices()
                
                has_mfa = False
                
                # Check hardware MFA
                if mfa_devices['MFADevices']:
                    has_mfa = True
                
                # Check virtual MFA
                for device in virtual_mfa['VirtualMFADevices']:
                    if 'User' in device and device['User']['UserName'] == username:
                        has_mfa = True
                        break
                
                if not has_mfa:
                    findings.append({
                        "time_found": current_time,
                        "identity_name": username,
                        "issue_name": "MFA not enabled"
                    })
                    
            except Exception as e:
                print(f"Warning: Could not check MFA for {username}: {str(e)}")
                
    except Exception as e:
        print(f"Error checking MFA: {str(e)}")
    
    print(f"Found {len(findings)} users without MFA")
    return findings


class IAMSecurityChecker:
    """Part B: Class-based security checker for candidate-identified issues"""
    
    def __init__(self, iam_client):
        """Initialize the security checker with IAM client"""
        self.iam_client = iam_client
        self.current_time = get_current_time()
        
        # Define dangerous policies for excessive permissions check
        self.dangerous_policies = [
            'arn:aws:iam::aws:policy/AdministratorAccess',
            'arn:aws:iam::aws:policy/PowerUserAccess',
            'arn:aws:iam::aws:policy/IAMFullAccess'
        ]
    
    def get_all_users(self) -> List[Dict]:
        """Get all IAM users"""
        try:
            return self.iam_client.list_users()['Users']
        except Exception as e:
            print(f"Error getting users: {str(e)}")
            return []
    
    def check_excessive_permissions(self) -> List[Dict[str, str]]:
        """Check for users with excessive permissions"""
        findings = []
        
        print("Checking for excessive permissions...")
        
        try:
            users = self.get_all_users()
            
            for user in users:
                username = user['UserName']
                
                try:
                    # Check attached policies
                    policies = self.iam_client.list_attached_user_policies(UserName=username)
                    
                    for policy in policies['AttachedPolicies']:
                        if policy['PolicyArn'] in self.dangerous_policies:
                            findings.append({
                                "time_found": self.current_time,
                                "identity_name": username,
                                "issue_name": f"Excessive permissions - {policy['PolicyName']} attached"
                            })
                            
                except Exception as e:
                    print(f"Warning: Could not check permissions for {username}: {str(e)}")
                    
        except Exception as e:
            print(f"Error checking permissions: {str(e)}")
        
        print(f"Found {len(findings)} permission issues")
        return findings
    
    def check_old_access_keys(self, max_age_days: int = 90) -> List[Dict[str, str]]:
        """Check for old access keys"""
        findings = []
        current_date = datetime.now()
        
        print(f"Checking for access keys older than {max_age_days} days...")
        
        try:
            users = self.get_all_users()
            
            for user in users:
                username = user['UserName']
                
                try:
                    keys = self.iam_client.list_access_keys(UserName=username)
                    
                    for key in keys['AccessKeyMetadata']:
                        create_date = key['CreateDate'].replace(tzinfo=None)
                        days_old = (current_date - create_date).days
                        
                        if days_old > max_age_days:
                            findings.append({
                                "time_found": self.current_time,
                                "identity_name": username,
                                "issue_name": f"Old access key ({days_old} days old)"
                            })
                            
                except Exception as e:
                    print(f"Warning: Could not check access keys for {username}: {str(e)}")
                    
        except Exception as e:
            print(f"Error checking access keys: {str(e)}")
        
        print(f"Found {len(findings)} old access key issues")
        return findings
    
    def check_inactive_users(self, max_inactive_days: int = 180) -> List[Dict[str, str]]:
        """Additional check: Find users who haven't been active recently"""
        findings = []
        current_date = datetime.now()
        
        print(f"Checking for users inactive for more than {max_inactive_days} days...")
        
        try:
            users = self.get_all_users()
            
            for user in users:
                username = user['UserName']
                
                try:
                    # Check password last used
                    if 'PasswordLastUsed' in user:
                        last_used = user['PasswordLastUsed'].replace(tzinfo=None)
                        days_inactive = (current_date - last_used).days
                        
                        if days_inactive > max_inactive_days:
                            findings.append({
                                "time_found": self.current_time,
                                "identity_name": username,
                                "issue_name": f"Inactive user ({days_inactive} days since last password use)"
                            })
                    else:
                        # User never used password (console access)
                        create_date = user['CreateDate'].replace(tzinfo=None)
                        days_since_creation = (current_date - create_date).days
                        
                        if days_since_creation > 30:  # If user created >30 days ago but never used password
                            findings.append({
                                "time_found": self.current_time,
                                "identity_name": username,
                                "issue_name": "User never used password (potential unused account)"
                            })
                            
                except Exception as e:
                    print(f"Warning: Could not check activity for {username}: {str(e)}")
                    
        except Exception as e:
            print(f"Error checking user activity: {str(e)}")
        
        print(f"Found {len(findings)} inactive user issues")
        return findings
    
    def run_all_checks(self) -> List[Dict[str, str]]:
        """Run all security checks in this class"""
        all_findings = []
        
        # Run excessive permissions check
        permission_findings = self.check_excessive_permissions()
        all_findings.extend(permission_findings)
        
        # Run old access keys check
        key_findings = self.check_old_access_keys()
        all_findings.extend(key_findings)
        
        # Run inactive users check (additional security issue)
        inactive_findings = self.check_inactive_users()
        all_findings.extend(inactive_findings)
        
        return all_findings


def run_assessment() -> List[Dict[str, str]]:
    """Run all security checks using both function and class approaches"""
    print("Starting IAM Security Assessment...")
    
    # Initialize AWS client
    iam_client = boto3.client('iam')
    
    # Run all checks
    all_findings = []
    
    # Part A: MFA check (function-based)
    print("\n=== PART A: MFA CHECK (Function-based) ===")
    mfa_findings = check_mfa_not_enabled(iam_client)
    all_findings.extend(mfa_findings)
    
    # Part B: Other security checks (class-based)
    print("\n=== PART B: SECURITY CHECKS (Class-based) ===")
    security_checker = IAMSecurityChecker(iam_client)
    class_findings = security_checker.run_all_checks()
    all_findings.extend(class_findings)
    
    print(f"\nAssessment complete. Total findings: {len(all_findings)}")
    return all_findings


def save_report(findings: List[Dict[str, str]], filename: str = "refactored_iam_report.json"):
    """Save findings to JSON report"""
    report = {
        "assessment_time": get_current_time(),
        "total_findings": len(findings),
        "findings": findings
    }
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to {filename}")


def print_summary(findings: List[Dict[str, str]]):
    """Print simple summary"""
    if not findings:
        print("\n✅ No security issues found!")
        return
    
    print(f"\n📊 Summary:")
    print(f"Total Issues: {len(findings)}")
    
    # Count issue types
    issue_types = {}
    for finding in findings:
        issue = finding['issue_name']
        if issue not in issue_types:
            issue_types[issue] = 0
        issue_types[issue] += 1
    
    print("\nIssues by type:")
    for issue, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {issue}: {count}")
    
    # Show affected users
    users = {}
    for finding in findings:
        user = finding['identity_name']
        if user not in users:
            users[user] = 0
        users[user] += 1
    
    print("\nMost affected users:")
    for user, count in sorted(users.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  • {user}: {count} issues")


def main():
    """Main function"""
    try:
        # Run assessment
        findings = run_assessment()
        
        # Save report
        save_report(findings)
        
        # Show summary
        print_summary(findings)
        
        print(f"\n🎯 Assessment completed using hybrid approach!")
        print(f"📄 Part A (MFA): Function-based")
        print(f"📄 Part B (Security Issues): Class-based")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
