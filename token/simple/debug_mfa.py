#!/usr/bin/env python3
"""
Debug script to check MFA detection logic
"""

import json
import boto3
from datetime import datetime
from typing import List, Dict, Any


def debug_mfa_check():
    """Debug MFA checking with detailed output"""
    iam_client = boto3.client('iam')
    
    print("=== DEBUGGING MFA CHECK ===")
    
    try:
        # Get all users
        users = iam_client.list_users()['Users']
        print(f"Found {len(users)} users total")
        
        # Get all virtual MFA devices once (more efficient)
        print("\n--- Getting all virtual MFA devices ---")
        virtual_mfa_response = iam_client.list_virtual_mfa_devices()
        all_virtual_mfa = virtual_mfa_response['VirtualMFADevices']
        print(f"Found {len(all_virtual_mfa)} virtual MFA devices total")
        
        # Debug first few virtual MFA devices
        for i, device in enumerate(all_virtual_mfa[:3]):
            print(f"Virtual MFA {i+1}: {device.get('SerialNumber', 'No serial')}")
            print(f"  - Device keys: {list(device.keys())}")
            if 'User' in device:
                print(f"  - User info: {device['User']}")
                if 'UserName' in device['User']:
                    print(f"  - Assigned to user: {device['User']['UserName']}")
                else:
                    print(f"  - User object missing UserName")
            else:
                print(f"  - Not assigned to any user")
        
        users_without_mfa = 0
        
        print(f"\n--- Checking each user (showing first 5) ---")
        for i, user in enumerate(users[:5]):  # Just check first 5 for debugging
            username = user['UserName']
            print(f"\nUser {i+1}: {username}")
            
            try:
                # Check hardware MFA devices
                mfa_devices = iam_client.list_mfa_devices(UserName=username)
                hardware_mfa_count = len(mfa_devices['MFADevices'])
                print(f"  - Hardware MFA devices: {hardware_mfa_count}")
                
                # Check if this user has any virtual MFA
                user_virtual_mfa = []
                for device in all_virtual_mfa:
                    if 'User' in device:
                        if 'UserName' in device['User'] and device['User']['UserName'] == username:
                            user_virtual_mfa.append(device)
                        else:
                            print(f"    - Virtual MFA device missing UserName: {device['User']}")
                
                print(f"  - Virtual MFA devices: {len(user_virtual_mfa)}")
                
                has_mfa = hardware_mfa_count > 0 or len(user_virtual_mfa) > 0
                print(f"  - Has MFA: {has_mfa}")
                
                if not has_mfa:
                    users_without_mfa += 1
                    print(f"  - ⚠️  NO MFA ENABLED")
                else:
                    print(f"  - ✅ MFA is enabled")
                    
            except Exception as e:
                print(f"  - Error checking {username}: {str(e)}")
        
        print(f"\n=== SUMMARY ===")
        print(f"Users checked: 5 (of {len(users)} total)")
        print(f"Users without MFA in sample: {users_without_mfa}")
        
    except Exception as e:
        print(f"Error in debug: {str(e)}")


if __name__ == "__main__":
    debug_mfa_check()
