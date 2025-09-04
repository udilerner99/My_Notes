#!/usr/bin/env python3
"""
Example usage and testing of the IAM Security Assessment tool
"""

from iam_security_assessment import IAMSecurityAssessment, SecurityFinding
import json

def demo_assessment():
    """Demonstrate the security assessment tool"""
    print("🔍 Starting IAM Security Assessment Demo")
    print("=" * 50)
    
    try:
        # Initialize the assessment tool
        assessment = IAMSecurityAssessment()
        
        # Run the full assessment
        findings = assessment.run_assessment()
        
        # Generate the report
        assessment.generate_report(findings, 'demo_iam_security_report.json')
        
        # Show some example findings
        if findings:
            print(f"\n📋 Sample Findings:")
            for i, finding in enumerate(findings[:3], 1):
                print(f"\n{i}. {finding.issue_name}")
                print(f"   Identity: {finding.identity_name}")
                print(f"   Severity: {finding.severity}")
                print(f"   Description: {finding.description[:100]}...")
        
        return findings
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return []

def analyze_report(report_file: str = 'demo_iam_security_report.json'):
    """Analyze the generated report"""
    try:
        with open(report_file, 'r') as f:
            report = json.load(f)
        
        print(f"\n📊 Report Analysis")
        print(f"=" * 30)
        print(f"Assessment Time: {report['assessment_metadata']['timestamp']}")
        print(f"Total Findings: {report['assessment_metadata']['total_findings']}")
        
        # Group findings by issue type
        issue_types = {}
        for finding in report['findings']:
            issue_name = finding['issue_name']
            if issue_name not in issue_types:
                issue_types[issue_name] = []
            issue_types[issue_name].append(finding)
        
        print(f"\n📈 Issues by Type:")
        for issue_type, findings in sorted(issue_types.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  {issue_type}: {len(findings)} occurrences")
        
    except FileNotFoundError:
        print(f"Report file {report_file} not found. Run the assessment first.")
    except Exception as e:
        print(f"Error analyzing report: {str(e)}")

if __name__ == "__main__":
    # Run the demo
    findings = demo_assessment()
    
    if findings:
        # Analyze the report
        analyze_report()
        
        print(f"\n✅ Demo completed successfully!")
        print(f"📄 Check 'demo_iam_security_report.json' for full results")
    else:
        print(f"\n⚠️  No findings to analyze")
