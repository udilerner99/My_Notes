# IAM Security Assessment Tool

A comprehensive Python tool for assessing AWS IAM security configurations and identifying potential vulnerabilities.

## Features

### Part A: MFA Not Enabled Check
- Identifies IAM users without Multi-Factor Authentication (MFA) enabled
- Checks both hardware and virtual MFA devices
- High severity findings for users without MFA

### Part B: Additional Security Checks
1. **Excessive Permissions Check**: Identifies users with potentially dangerous high-privilege policies
2. **Access Key Security Check**: Finds old, unused, or multiple access keys

## Architecture

The tool follows a modular, object-oriented design:

- **Abstract Base Class**: `SecurityCheck` provides the interface for all security checks
- **Concrete Implementations**: Each security issue is implemented as a separate class
- **Main Controller**: `IAMSecurityAssessment` orchestrates all checks and report generation
- **Type Safety**: Full type hints using Python's typing module
- **Extensible**: Easy to add new security checks by implementing the `SecurityCheck` interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python iam_security_assessment.py
```

### With AWS Profile
```python
from iam_security_assessment import IAMSecurityAssessment

# Initialize with specific profile
assessment = IAMSecurityAssessment(profile_name='your-profile')

# Run assessment
findings = assessment.run_assessment()

# Generate report
assessment.generate_report(findings)
```

## Output

The tool generates a JSON report (`iam_security_report.json`) with the following structure:

```json
{
  "assessment_metadata": {
    "timestamp": "2025-09-04T10:30:00",
    "total_findings": 15,
    "aws_region": "us-east-1",
    "profile_used": "default"
  },
  "findings": [
    {
      "time_found": "2025-09-04T10:30:00",
      "identity_name": "user-name",
      "issue_name": "MFA not enabled",
      "severity": "High",
      "description": "User does not have MFA enabled...",
      "recommendation": "Enable MFA for this user account..."
    }
  ]
}
```

## Security Checks Implemented

### 1. MFA Not Enabled Check (Part A)
- **Purpose**: Identifies users without MFA protection
- **Severity**: High
- **Method**: Checks both hardware and virtual MFA devices for each user

### 2. Excessive Permissions Check (Part B)
- **Purpose**: Finds users with dangerous high-privilege policies
- **Severity**: High/Medium
- **Policies Checked**: AdministratorAccess, PowerUserAccess, IAMFullAccess
- **Scope**: Direct user policies and inherited group policies

### 3. Access Key Security Check (Part B - Additional)
- **Purpose**: Identifies access key security issues
- **Checks**:
  - Keys older than 90 days
  - Inactive keys not deleted
  - Users with multiple access keys
- **Severity**: Medium/Low

## Extensibility

To add a new security check:

```python
class NewSecurityCheck(SecurityCheck):
    def check_name(self) -> str:
        return "New Security Check"
    
    def perform_check(self, iam_client: Any) -> List[SecurityFinding]:
        findings = []
        # Implement your check logic here
        return findings
```

Then register it in the `IAMSecurityAssessment.register_security_checks()` method.

## Best Practices Implemented

- **Type Safety**: Full type annotations for better code maintainability
- **Error Handling**: Comprehensive exception handling with logging
- **Modular Design**: Each check is independent and can be run separately
- **Scalable Architecture**: Easy to add new checks without modifying existing code
- **Detailed Reporting**: Rich JSON output with metadata and recommendations
- **Logging**: Proper logging for debugging and monitoring
