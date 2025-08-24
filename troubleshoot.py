#!/usr/bin/env python3
"""
Quick CLI launcher for the AgentHack 2025 Networking Troubleshooter
"""

import sys
import os
sys.path.append('/workspace/backend')

from app.networking_troubleshooter import NetworkingTroubleshooter

def main():
    print("🚀 AgentHack 2025 Networking Troubleshooter")
    print("=" * 50)
    
    # Create troubleshooter instance
    troubleshooter = NetworkingTroubleshooter()
    
    # Run diagnosis
    results = troubleshooter.run_full_diagnosis()
    
    # Print results
    troubleshooter.print_results(results)
    
    # Generate fix script if there are failures
    failures = [r for r in results if r.status == "FAIL"]
    if failures:
        print("\n🔧 Generating fix script...")
        script_content = troubleshooter.generate_fix_script(results)
        with open("/workspace/fix_networking.sh", "w") as f:
            f.write(script_content)
        print("✅ Fix script saved to: fix_networking.sh")
        print("Run with: bash fix_networking.sh")
    
    print("\n🎯 Troubleshooting complete!")

if __name__ == "__main__":
    main()