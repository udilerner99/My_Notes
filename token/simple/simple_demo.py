#!/usr/bin/env python3
"""
Simple demo of the IAM security assessment tool
"""

from simple_iam_assessment import run_assessment, save_report, print_summary
import json

def demo():
    print("🔍 Simple IAM Security Assessment Demo")
    print("=" * 40)
    
    # Run the assessment
    findings = run_assessment()
    
    # Save to demo file
    save_report(findings, "demo_simple_report.json")
    
    # Show summary
    print_summary(findings)
    
    # Show a few sample findings
    if findings:
        print(f"\n📋 Sample Findings:")
        for i, finding in enumerate(findings[:3], 1):
            print(f"{i}. {finding['identity_name']}: {finding['issue_name']}")
    
    print(f"\n✅ Demo completed!")

if __name__ == "__main__":
    demo()
