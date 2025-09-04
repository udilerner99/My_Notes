#!/usr/bin/env python3
"""
Simple AWS IAM Security Assessment Tool

A straightforward tool to identify IAM security issues:
- Part A: Users without MFA enabled
- Part B: Users with excessive permissions and old access keys
"""

import json
import boto3
from datetime import datetime
from typing import List, Dict, Any


def get_current_time() -> str:
    """Get current timestamp as string"""
    return datetime.now().isoformat()


def check_mfa_not_enabled(iam_client) -> List[Dict[str, str]]:
    """Part A: Find users without MFA enabled"""
    findings = []
    current_time = get_current_time()
    
    print("Checking for users without MFA...")
    
    try:
        # Get all users
        users = iam_client.list_users()['Users']
        
        # Get all virtual MFA devices once (more efficient)
        virtual_mfa_response = iam_client.list_virtual_mfa_devices()
        all_virtual_mfa = virtual_mfa_response['VirtualMFADevices']
        
        for user in users:
            username = user['UserName']
            
            try:
                # Check hardware MFA devices
                mfa_devices = iam_client.list_mfa_devices(UserName=username)
                hardware_mfa_count = len(mfa_devices['MFADevices'])
                
                # Check virtual MFA devices for this user
                virtual_mfa_count = 0
                for device in all_virtual_mfa:
                    if 'User' in device and 'UserName' in device['User']:
                        if device['User']['UserName'] == username:
                            virtual_mfa_count += 1
                
                has_mfa = hardware_mfa_count > 0 or virtual_mfa_count > 0
                
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


def check_excessive_permissions(iam_client) -> List[Dict[str, str]]:
    """Part B: Find users with excessive permissions"""
    findings = []
    current_time = get_current_time()
    
    dangerous_policies = [
        'arn:aws:iam::aws:policy/AdministratorAccess',
        'arn:aws:iam::aws:policy/PowerUserAccess',
        'arn:aws:iam::aws:policy/IAMFullAccess'
    ]
    
    print("Checking for excessive permissions...")
    
    try:
        users = iam_client.list_users()['Users']
        
        for user in users:
            username = user['UserName']
            
            try:
                # Check attached policies
                policies = iam_client.list_attached_user_policies(UserName=username)
                
                for policy in policies['AttachedPolicies']:
                    if policy['PolicyArn'] in dangerous_policies:
                        findings.append({
                            "time_found": current_time,
                            "identity_name": username,
                            "issue_name": f"Excessive permissions - {policy['PolicyName']} attached"
                        })
                        
            except Exception as e:
                print(f"Warning: Could not check permissions for {username}: {str(e)}")
                
    except Exception as e:
        print(f"Error checking permissions: {str(e)}")
    
    print(f"Found {len(findings)} permission issues")
    return findings


def check_old_access_keys(iam_client) -> List[Dict[str, str]]:
    """Part B: Find old access keys (>90 days)"""
    findings = []
    current_time = get_current_time()
    current_date = datetime.now()
    
    print("Checking for old access keys...")
    
    try:
        users = iam_client.list_users()['Users']
        
        for user in users:
            username = user['UserName']
            
            try:
                keys = iam_client.list_access_keys(UserName=username)
                
                for key in keys['AccessKeyMetadata']:
                    create_date = key['CreateDate'].replace(tzinfo=None)
                    days_old = (current_date - create_date).days
                    
                    if days_old > 90:
                        findings.append({
                            "time_found": current_time,
                            "identity_name": username,
                            "issue_name": f"Old access key ({days_old} days old)"
                        })
                        
            except Exception as e:
                print(f"Warning: Could not check access keys for {username}: {str(e)}")
                
    except Exception as e:
        print(f"Error checking access keys: {str(e)}")
    
    print(f"Found {len(findings)} old access key issues")
    return findings


def run_assessment() -> List[Dict[str, str]]:
    """Run all security checks"""
    print("Starting IAM Security Assessment...")
    
    # Initialize AWS client
    iam_client = boto3.client('iam')
    
    # Run all checks
    all_findings = []
    
    # Part A: MFA check
    mfa_findings = check_mfa_not_enabled(iam_client)
    all_findings.extend(mfa_findings)
    
    # Part B: Permission and key checks
    permission_findings = check_excessive_permissions(iam_client)
    all_findings.extend(permission_findings)
    
    key_findings = check_old_access_keys(iam_client)
    all_findings.extend(key_findings)
    
    print(f"\nAssessment complete. Total findings: {len(all_findings)}")
    return all_findings


def save_report(findings: List[Dict[str, str]], filename: str = "simple_iam_report.json"):
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
        
        print(f"\n🎯 Assessment completed!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
