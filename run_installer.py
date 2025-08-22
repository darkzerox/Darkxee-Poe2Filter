#!/usr/bin/env python3
"""
POE2 Filter Installer - Main Runner
รัน installer ในโหมด GUI หรือ CLI
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main entry point"""
    try:
        from installer import main as installer_main
        installer_main()
    except ImportError as e:
        print(f"ข้อผิดพลาดในการ import: {e}")
        print("กรุณาติดตั้ง dependencies ด้วย: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"ข้อผิดพลาด: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
