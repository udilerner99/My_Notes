# Simple IAM Security Assessment Tool

A straightforward AWS IAM security assessment tool that identifies key security issues.

## What it does

### Part A: MFA Not Enabled
- Finds IAM users without Multi-Factor Authentication
- Checks both hardware and virtual MFA devices

### Part B: Security Issues
1. **Excessive Permissions**: Users with dangerous policies (AdminAccess, PowerUser, IAMFullAccess)
2. **Old Access Keys**: Access keys older than 90 days

## Usage

```bash
# Install dependencies
pip install -r simple_requirements.txt

# Run assessment
python simple_iam_assessment.py
```

## Output

Creates `simple_iam_report.json` with findings in this format:

```json
{
  "assessment_time": "2025-09-04T10:30:00",
  "total_findings": 5,
  "findings": [
    {
      "time_found": "2025-09-04T10:30:00",
      "identity_name": "user-name",
      "issue_name": "MFA not enabled"
    }
  ]
}
```

## Code Structure

- **Simple functions**: Each check is a single function
- **No classes**: Straightforward procedural approach  
- **Minimal dependencies**: Just boto3 and datetime
- **Easy to read**: Clear function names and comments
