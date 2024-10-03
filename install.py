#!/usr/bin/env python3
import os
import shutil
import sys

def main():
    if os.geteuid() != 0:
        print("This script must be run as root!")
        sys.exit(1)

    print("Do you want to install NetSpeed to /usr/local/bin? (y/n)")
    choice = input().lower()

    if choice == 'y':
        source_file = os.path.abspath("Netspeed.py")
        target_file = "/usr/local/bin/netspeed"
        
        try:
            shutil.copyfile(source_file, target_file)
            os.chmod(target_file, 0o755)
            print("NetSpeed has been installed successfully. You can now run 'netspeed' from any terminal.")
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
    else:
        print("Installation cancelled.")
        sys.exit(0)

if __name__ == "__main__":
    main()
