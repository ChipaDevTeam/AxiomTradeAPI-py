#!/usr/bin/env python3
"""
Build and publish script for AxiomTradeAPI-py
This script helps build and publish the package to PyPI
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description, capture=False):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}")
    print(f"Running: {command}")
    
    if capture:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} failed")
            print(f"Error: {result.stderr}")
            return False
    else:
        # Don't capture output for interactive commands (like twine upload)
        # or when we want to see output in real-time
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
        else:
            print(f"❌ {description} failed")
            return False
    
    return True

def clean_build():
    """Clean previous build artifacts"""
    print("\n🧹 Cleaning previous build artifacts...")
    
    dirs_to_clean = ['build', 'dist', 'axiomtradeapi.egg-info']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed {dir_name}/")
    
    print("✅ Build artifacts cleaned")

def check_requirements():
    """Check if required tools are installed"""
    print("\n🔍 Checking requirements...")
    
    required_packages = ['build', 'twine']
    missing_packages = []
    
    for package in required_packages:
        result = subprocess.run(f"pip show {package}", shell=True, capture_output=True)
        if result.returncode != 0:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {missing_packages}")
        print("Installing missing packages...")
        for package in missing_packages:
            if not run_command(f"pip install {package}", f"Installing {package}"):
                return False
    
    print("✅ All requirements satisfied")
    return True

def build_package():
    """Build the package"""
    return run_command("python -m build", "Building package")

def check_package():
    """Check the package with twine"""
    return run_command("python -m twine check dist/*", "Checking package")

def upload_test():
    """Upload to Test PyPI"""
    print("\n🚀 Uploading to Test PyPI...")
    print("Note: You'll need to enter your Test PyPI credentials")
    return run_command("python -m twine upload --repository testpypi dist/*", "Uploading to Test PyPI")

def upload_production():
    """Upload to Production PyPI"""
    print("\n🚀 Uploading to Production PyPI...")
    print("Note: You'll need to enter your PyPI credentials")
    return run_command("python -m twine upload dist/*", "Uploading to Production PyPI")

def main():
    """Main build and publish workflow"""
    print("🎉 AxiomTradeAPI-py Build & Publish Script")
    print("=" * 50)
    
    # Check current directory
    if not os.path.exists("setup.py"):
        print("❌ setup.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Step 1: Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Step 2: Clean previous builds
    clean_build()
    
    # Step 3: Build package
    if not build_package():
        sys.exit(1)
    
    # Step 4: Check package
    if not check_package():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Package built successfully!")
    print("\nNext steps:")
    print("1. Test upload: python build_and_publish.py --test")
    print("2. Production upload: python build_and_publish.py --prod")
    print("\nOr run individual commands:")
    print("  Test PyPI: python -m twine upload --repository testpypi dist/*")
    print("  Prod PyPI: python -m twine upload dist/*")
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        if "--test" in sys.argv:
            upload_test()
        elif "--prod" in sys.argv:
            upload_production()
        elif "--help" in sys.argv:
            print("\nUsage:")
            print("  python build_and_publish.py         # Build only")
            print("  python build_and_publish.py --test  # Build and upload to Test PyPI")
            print("  python build_and_publish.py --prod  # Build and upload to Production PyPI")

if __name__ == "__main__":
    main()
