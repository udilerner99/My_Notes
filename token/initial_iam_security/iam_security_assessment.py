#!/usr/bin/env python3
"""
AWS IAM Security Assessment Tool

This tool performs comprehensive security assessments on AWS IAM configurations
to identify potential vulnerabilities and security issues.

Author: Security Assessment Team
Date: September 4, 2025
"""

import json
import boto3
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SecurityFinding:
    """Data class representing a security finding"""
    time_found: str
    identity_name: str
    issue_name: str
    severity: str = "Medium"
    description: str = ""
    recommendation: str = ""


class SecurityCheck(ABC):
    """Abstract base class for security checks"""
    
    @abstractmethod
    def check_name(self) -> str:
        """Return the name of this security check"""
        pass
    
    @abstractmethod
    def perform_check(self, iam_client: Any) -> List[SecurityFinding]:
        """Perform the security check and return findings"""
        pass


class MFANotEnabledCheck(SecurityCheck):
    """Check for IAM users without MFA enabled"""
    
    def check_name(self) -> str:
        return "MFA Not Enabled Check"
    
    def perform_check(self, iam_client: Any) -> List[SecurityFinding]:
        """Identify IAM users without MFA enabled"""
        findings: List[SecurityFinding] = []
        current_time = datetime.now().isoformat()
        
        try:
            logger.info("Checking for users without MFA enabled...")
            
            # Get all users
            paginator = iam_client.get_paginator('list_users')
            
            for page in paginator.paginate():
                for user in page['Users']:
                    username = user['UserName']
                    
                    try:
                        # Check if user has MFA devices
                        mfa_devices = iam_client.list_mfa_devices(UserName=username)
                        virtual_mfa_devices = iam_client.list_virtual_mfa_devices()
                        
                        user_has_mfa = False
                        
                        # Check hardware MFA devices
                        if mfa_devices['MFADevices']:
                            user_has_mfa = True
                        
                        # Check virtual MFA devices
                        for virtual_device in virtual_mfa_devices['VirtualMFADevices']:
                            if 'User' in virtual_device and virtual_device['User']['UserName'] == username:
                                user_has_mfa = True
                                break
                        
                        if not user_has_mfa:
                            finding = SecurityFinding(
                                time_found=current_time,
                                identity_name=username,
                                issue_name="MFA not enabled",
                                severity="High",
                                description=f"User {username} does not have MFA enabled, making the account vulnerable to credential compromise.",
                                recommendation="Enable MFA for this user account to add an additional layer of security."
                            )
                            findings.append(finding)
                            
                    except Exception as e:
                        logger.warning(f"Error checking MFA for user {username}: {str(e)}")
                        
        except Exception as e:
            logger.error(f"Error in MFA check: {str(e)}")
        
        logger.info(f"Found {len(findings)} users without MFA enabled")
        return findings


class ExcessivePermissionsCheck(SecurityCheck):
    """Check for IAM users with potentially excessive permissions"""
    
    DANGEROUS_POLICIES = [
        'arn:aws:iam::aws:policy/AdministratorAccess',
        'arn:aws:iam::aws:policy/PowerUserAccess',
        'arn:aws:iam::aws:policy/IAMFullAccess'
    ]
    
    def check_name(self) -> str:
        return "Excessive Permissions Check"
    
    def perform_check(self, iam_client: Any) -> List[SecurityFinding]:
        """Identify IAM users with potentially excessive permissions"""
        findings: List[SecurityFinding] = []
        current_time = datetime.now().isoformat()
        
        try:
            logger.info("Checking for users with excessive permissions...")
            
            # Get all users
            paginator = iam_client.get_paginator('list_users')
            
            for page in paginator.paginate():
                for user in page['Users']:
                    username = user['UserName']
                    
                    try:
                        # Check attached user policies
                        attached_policies = iam_client.list_attached_user_policies(UserName=username)
                        
                        for policy in attached_policies['AttachedPolicies']:
                            if policy['PolicyArn'] in self.DANGEROUS_POLICIES:
                                finding = SecurityFinding(
                                    time_found=current_time,
                                    identity_name=username,
                                    issue_name="Excessive permissions - High privilege policy attached",
                                    severity="High",
                                    description=f"User {username} has the high-privilege policy '{policy['PolicyName']}' directly attached.",
                                    recommendation="Review if this user requires such broad permissions. Consider using groups or more specific policies."
                                )
                                findings.append(finding)
                        
                        # Check user groups for dangerous policies
                        user_groups = iam_client.get_groups_for_user(UserName=username)
                        
                        for group in user_groups['Groups']:
                            group_name = group['GroupName']
                            group_policies = iam_client.list_attached_group_policies(GroupName=group_name)
                            
                            for policy in group_policies['AttachedPolicies']:
                                if policy['PolicyArn'] in self.DANGEROUS_POLICIES:
                                    finding = SecurityFinding(
                                        time_found=current_time,
                                        identity_name=username,
                                        issue_name="Excessive permissions - High privilege policy via group",
                                        severity="Medium",
                                        description=f"User {username} inherits high-privilege policy '{policy['PolicyName']}' through group '{group_name}'.",
                                        recommendation="Review group memberships and consider if this level of access is necessary."
                                    )
                                    findings.append(finding)
                        
                        # Check for inline policies (generally not recommended)
                        inline_policies = iam_client.list_user_policies(UserName=username)
                        if inline_policies['PolicyNames']:
                            finding = SecurityFinding(
                                time_found=current_time,
                                identity_name=username,
                                issue_name="Inline policies detected",
                                severity="Low",
                                description=f"User {username} has {len(inline_policies['PolicyNames'])} inline policies attached.",
                                recommendation="Consider converting inline policies to managed policies for better governance and reusability."
                            )
                            findings.append(finding)
                            
                    except Exception as e:
                        logger.warning(f"Error checking permissions for user {username}: {str(e)}")
                        
        except Exception as e:
            logger.error(f"Error in excessive permissions check: {str(e)}")
        
        logger.info(f"Found {len(findings)} permission-related issues")
        return findings


class AccessKeySecurityCheck(SecurityCheck):
    """Check for access key security issues"""
    
    def check_name(self) -> str:
        return "Access Key Security Check"
    
    def perform_check(self, iam_client: Any) -> List[SecurityFinding]:
        """Check for old or unused access keys"""
        findings: List[SecurityFinding] = []
        current_time = datetime.now().isoformat()
        current_datetime = datetime.now()
        
        try:
            logger.info("Checking access key security...")
            
            # Get all users
            paginator = iam_client.get_paginator('list_users')
            
            for page in paginator.paginate():
                for user in page['Users']:
                    username = user['UserName']
                    
                    try:
                        # Get access keys for user
                        access_keys = iam_client.list_access_keys(UserName=username)
                        
                        for key in access_keys['AccessKeyMetadata']:
                            key_id = key['AccessKeyId']
                            create_date = key['CreateDate'].replace(tzinfo=None)
                            status = key['Status']
                            
                            # Check for old keys (> 90 days)
                            days_old = (current_datetime - create_date).days
                            if days_old > 90:
                                finding = SecurityFinding(
                                    time_found=current_time,
                                    identity_name=username,
                                    issue_name="Old access key",
                                    severity="Medium",
                                    description=f"Access key {key_id} for user {username} is {days_old} days old.",
                                    recommendation="Consider rotating access keys regularly (every 90 days) as a security best practice."
                                )
                                findings.append(finding)
                            
                            # Check for inactive but not deleted keys
                            if status == 'Inactive':
                                finding = SecurityFinding(
                                    time_found=current_time,
                                    identity_name=username,
                                    issue_name="Inactive access key not deleted",
                                    severity="Low",
                                    description=f"Access key {key_id} for user {username} is inactive but not deleted.",
                                    recommendation="Delete unused access keys to reduce potential attack surface."
                                )
                                findings.append(finding)
                            
                            # Check for multiple access keys
                            if len(access_keys['AccessKeyMetadata']) > 1:
                                finding = SecurityFinding(
                                    time_found=current_time,
                                    identity_name=username,
                                    issue_name="Multiple access keys",
                                    severity="Low",
                                    description=f"User {username} has {len(access_keys['AccessKeyMetadata'])} access keys.",
                                    recommendation="Consider if multiple access keys are necessary. Use key rotation instead of creating multiple keys."
                                )
                                findings.append(finding)
                                break  # Only report this once per user
                                
                    except Exception as e:
                        logger.warning(f"Error checking access keys for user {username}: {str(e)}")
                        
        except Exception as e:
            logger.error(f"Error in access key security check: {str(e)}")
        
        logger.info(f"Found {len(findings)} access key related issues")
        return findings


class IAMSecurityAssessment:
    """Main class for performing IAM security assessments"""
    
    def __init__(self, profile_name: Optional[str] = None, region_name: str = 'us-east-1'):
        """Initialize the security assessment tool"""
        self.profile_name = profile_name
        self.region_name = region_name
        self.security_checks: List[SecurityCheck] = []
        
        # Initialize AWS session
        if profile_name:
            self.session = boto3.Session(profile_name=profile_name)
        else:
            self.session = boto3.Session()
        
        self.iam_client = self.session.client('iam', region_name=region_name)
        
        # Register security checks
        self.register_security_checks()
    
    def register_security_checks(self) -> None:
        """Register all available security checks"""
        self.security_checks = [
            MFANotEnabledCheck(),
            ExcessivePermissionsCheck(),
            AccessKeySecurityCheck()
        ]
        logger.info(f"Registered {len(self.security_checks)} security checks")
    
    def run_assessment(self) -> List[SecurityFinding]:
        """Run all security checks and return combined findings"""
        all_findings: List[SecurityFinding] = []
        
        logger.info("Starting IAM security assessment...")
        
        for check in self.security_checks:
            logger.info(f"Running {check.check_name()}...")
            try:
                findings = check.perform_check(self.iam_client)
                all_findings.extend(findings)
                logger.info(f"Completed {check.check_name()}: {len(findings)} findings")
            except Exception as e:
                logger.error(f"Error running {check.check_name()}: {str(e)}")
        
        logger.info(f"Assessment complete. Total findings: {len(all_findings)}")
        return all_findings
    
    def generate_report(self, findings: List[SecurityFinding], output_file: str = 'iam_security_report.json') -> None:
        """Generate JSON report from findings"""
        report_data = {
            'assessment_metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_findings': len(findings),
                'aws_region': self.region_name,
                'profile_used': self.profile_name or 'default'
            },
            'findings': []
        }
        
        # Convert findings to dictionaries
        for finding in findings:
            report_data['findings'].append({
                'time_found': finding.time_found,
                'identity_name': finding.identity_name,
                'issue_name': finding.issue_name,
                'severity': finding.severity,
                'description': finding.description,
                'recommendation': finding.recommendation
            })
        
        # Sort findings by severity and identity name
        severity_order = {'High': 0, 'Medium': 1, 'Low': 2}
        report_data['findings'].sort(key=lambda x: (severity_order.get(x['severity'], 3), x['identity_name']))
        
        # Write report to file
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"Report saved to {output_file}")
        
        # Print summary
        self.print_summary(findings)
    
    def print_summary(self, findings: List[SecurityFinding]) -> None:
        """Print a summary of findings to console"""
        if not findings:
            print("\n✅ No security issues found!")
            return
        
        severity_counts = {'High': 0, 'Medium': 0, 'Low': 0}
        for finding in findings:
            severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1
        
        print(f"\n📊 Security Assessment Summary")
        print(f"=" * 40)
        print(f"Total Issues Found: {len(findings)}")
        print(f"🔴 High Severity: {severity_counts['High']}")
        print(f"🟡 Medium Severity: {severity_counts['Medium']}")
        print(f"🟢 Low Severity: {severity_counts['Low']}")
        
        print(f"\n📝 Top Issues by Identity:")
        identity_counts = {}
        for finding in findings:
            identity_counts[finding.identity_name] = identity_counts.get(finding.identity_name, 0) + 1
        
        for identity, count in sorted(identity_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {identity}: {count} issues")


def main():
    """Main function to run the IAM security assessment"""
    try:
        # Initialize assessment tool
        assessment = IAMSecurityAssessment()
        
        # Run the assessment
        findings = assessment.run_assessment()
        
        # Generate report
        assessment.generate_report(findings, 'iam_security_report.json')
        
        print(f"\n🎯 Assessment completed successfully!")
        print(f"📄 Full report saved to: iam_security_report.json")
        
    except Exception as e:
        logger.error(f"Assessment failed: {str(e)}")
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
