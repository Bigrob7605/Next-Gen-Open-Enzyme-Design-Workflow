#!/usr/bin/env python3
"""
Setup Script for Next-Gen Open Enzyme Design Workflow
Local Test Environment Setup

This script helps set up the local environment for testing the workflow.
"""

import os
import sys
import subprocess
import platform

def check_python():
    """Check if Python is available and get version info."""
    print("🔍 Checking Python installation...")
    
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Python found but version check failed")
            return False
    except Exception as e:
        print(f"❌ Python not found or not accessible: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        'numpy', 'scipy', 'pandas', 'matplotlib', 'seaborn',
        'biopython', 'pyyaml', 'requests', 'tqdm'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies(missing_packages):
    """Install missing dependencies."""
    if not missing_packages:
        print("\n✅ All dependencies are installed!")
        return True
    
    print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages, 
                      check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_system_resources():
    """Check system resources for optimal performance."""
    print("\n🔍 Checking system resources...")
    
    # Check available memory
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(f"💾 RAM: {memory.total / (1024**3):.1f} GB total, "
              f"{memory.available / (1024**3):.1f} GB available")
        
        if memory.total >= 16 * (1024**3):  # 16GB
            print("✅ Sufficient RAM for local AlphaFold")
        else:
            print("⚠️  Limited RAM - consider using ColabFold")
            
    except ImportError:
        print("⚠️  psutil not available - cannot check memory")
    
    # Check disk space
    try:
        disk = psutil.disk_usage('.')
        print(f"💿 Disk: {disk.free / (1024**3):.1f} GB available")
        
        if disk.free >= 50 * (1024**3):  # 50GB
            print("✅ Sufficient disk space")
        else:
            print("⚠️  Limited disk space - AlphaFold models can be large")
            
    except:
        print("⚠️  Cannot check disk space")

def create_test_environment():
    """Create test environment and files."""
    print("\n🔧 Setting up test environment...")
    
    # Create directories if they don't exist
    directories = ['designs', 'models', 'design_notes', 'viz']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Copy example file if it exists
    example_file = "examples/PETase_S238F_example.fasta"
    target_file = "designs/PETase_S238F.fasta"
    
    if os.path.exists(example_file) and not os.path.exists(target_file):
        import shutil
        shutil.copy2(example_file, target_file)
        print(f"✅ Copied example file: {target_file}")
    
    print("✅ Test environment ready!")

def main():
    """Main setup function."""
    print("🚀 Next-Gen Open Enzyme Design Workflow")
    print("🔧 Local Test Environment Setup")
    print("=" * 50)
    
    # Check Python
    if not check_python():
        print("\n❌ Python is required but not found!")
        print("\n📋 Installation Instructions:")
        print("1. Download Python from: https://www.python.org/downloads/")
        print("2. Install with 'Add to PATH' option checked")
        print("3. Restart your terminal/PowerShell")
        print("4. Run this script again")
        return False
    
    # Check system resources
    check_system_resources()
    
    # Check dependencies
    missing_packages = check_dependencies()
    
    # Install missing dependencies
    if missing_packages:
        if not install_dependencies(missing_packages):
            print("\n❌ Failed to install dependencies!")
            print("Try running: pip install -r requirements.txt")
            return False
    
    # Create test environment
    create_test_environment()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next Steps:")
    print("1. Install AlphaFold (see docs/AlphaFold_setup.md)")
    print("2. Install Rosetta (see docs/Rosetta_setup.md)")
    print("3. Run test: python scripts/run_alphafold.py designs/PETase_S238F.fasta")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 