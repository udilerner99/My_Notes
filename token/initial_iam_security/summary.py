#!/usr/bin/env python3
"""
Summary script to show key findings from the IAM Security Assessment
"""

import json
from collections import defaultdict

def summarize_report(filename='iam_security_report.json'):
    """Generate a summary of the security assessment report"""
    
    try:
        with open(filename, 'r') as f:
            report = json.load(f)
        
        print("🔍 IAM Security Assessment - Executive Summary")
        print("=" * 55)
        
        metadata = report['assessment_metadata']
        print(f"📅 Assessment Date: {metadata['timestamp'][:10]}")
        print(f"🌐 AWS Region: {metadata['aws_region']}")
        print(f"👤 Profile Used: {metadata['profile_used']}")
        print(f"📊 Total Findings: {metadata['total_findings']}")
        
        findings = report['findings']
        
        # Group by severity
        severity_groups = defaultdict(list)
        for finding in findings:
            severity_groups[finding['severity']].append(finding)
        
        print(f"\n🚨 Findings by Severity:")
        for severity in ['High', 'Medium', 'Low']:
            count = len(severity_groups[severity])
            if count > 0:
                emoji = '🔴' if severity == 'High' else '🟡' if severity == 'Medium' else '🟢'
                print(f"   {emoji} {severity}: {count} issues")
        
        # Top issues by type
        issue_types = defaultdict(int)
        for finding in findings:
            issue_types[finding['issue_name']] += 1
        
        print(f"\n📈 Most Common Issues:")
        for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {issue_type}: {count} occurrences")
        
        # Critical findings (High severity)
        high_severity = severity_groups['High']
        if high_severity:
            print(f"\n🚨 Critical Issues Requiring Immediate Attention:")
            for finding in high_severity[:5]:  # Show top 5
                print(f"   • {finding['identity_name']}: {finding['issue_name']}")
        
        # Users with most issues
        user_issues = defaultdict(int)
        for finding in findings:
            user_issues[finding['identity_name']] += 1
        
        print(f"\n👥 Users with Most Issues:")
        for user, count in sorted(user_issues.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   • {user}: {count} issues")
        
        print(f"\n💡 Key Recommendations:")
        print(f"   1. Review and reduce excessive permissions for high-privilege users")
        print(f"   2. Implement regular access key rotation (90-day cycle)")
        print(f"   3. Remove or delete inactive access keys")
        print(f"   4. Enable MFA for all users (if not already done)")
        print(f"   5. Use IAM groups instead of direct user policy attachments")
        
        print(f"\n📄 Full detailed report available in: {filename}")
        
    except FileNotFoundError:
        print(f"❌ Report file '{filename}' not found. Please run the assessment first.")
    except json.JSONDecodeError:
        print(f"❌ Error reading JSON from '{filename}'. File may be corrupted.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    summarize_report()
