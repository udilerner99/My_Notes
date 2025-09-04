#!/usr/bin/env python3
"""
Demo of the refactored IAM security assessment tool
"""

from refactored_iam_assessment import run_assessment, save_report, print_summary, IAMSecurityChecker
import boto3

def demo_class_usage():
    """Demonstrate individual class method usage"""
    print("🔍 Demonstrating Class-based Security Checker")
    print("=" * 50)
    
    try:
        # Initialize IAM client and security checker
        iam_client = boto3.client('iam')
        checker = IAMSecurityChecker(iam_client)
        
        print("📋 Running individual security checks:")
        
        # Run each check individually
        print("\n1️⃣ Excessive Permissions Check:")
        perm_findings = checker.check_excessive_permissions()
        print(f"   Found: {len(perm_findings)} issues")
        
        print("\n2️⃣ Old Access Keys Check:")
        key_findings = checker.check_old_access_keys(max_age_days=90)
        print(f"   Found: {len(key_findings)} issues")
        
        print("\n3️⃣ Inactive Users Check:")
        inactive_findings = checker.check_inactive_users(max_inactive_days=180)
        print(f"   Found: {len(inactive_findings)} issues")
        
        print("\n🏃 Running all checks together:")
        all_class_findings = checker.run_all_checks()
        print(f"   Total from class: {len(all_class_findings)} issues")
        
        return all_class_findings
        
    except Exception as e:
        print(f"❌ Error in class demo: {str(e)}")
        return []

def demo_full_assessment():
    """Demonstrate the full assessment"""
    print("\n🔍 Full Assessment Demo (Function + Class)")
    print("=" * 50)
    
    # Run the full assessment
    findings = run_assessment()
    
    # Save to demo file
    save_report(findings, "demo_refactored_report.json")
    
    # Show summary
    print_summary(findings)
    
    return findings

def main():
    """Run both demos"""
    print("🚀 REFACTORED IAM SECURITY ASSESSMENT DEMO")
    print("=" * 60)
    
    # Demo 1: Class usage
    class_findings = demo_class_usage()
    
    # Demo 2: Full assessment
    full_findings = demo_full_assessment()
    
    # Compare results
    print(f"\n📊 COMPARISON:")
    print(f"Class-only findings: {len(class_findings)}")
    print(f"Full assessment findings: {len(full_findings)}")
    print(f"Function-based MFA findings: {len(full_findings) - len(class_findings)}")
    
    print(f"\n✅ Demo completed!")
    print(f"📄 Files created:")
    print(f"  • refactored_iam_report.json - Full assessment report")
    print(f"  • demo_refactored_report.json - Demo report")

if __name__ == "__main__":
    main()
