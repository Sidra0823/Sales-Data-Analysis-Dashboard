"""
Sales Dashboard Setup Script
Run this to verify installation and setup
"""

import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. You have Python {}.{}".format(version.major, version.minor))
        return False
    print("✅ Python {}.{} detected".format(version.major, version.minor))
    return True

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def verify_data():
    """Verify data file exists"""
    import os
    if os.path.exists('data/sales_data.csv'):
        print("✅ Sales data found")
        return True
    else:
        print("⚠️  Sales data not found. Generating...")
        try:
            subprocess.check_call([sys.executable, "data/generate_data.py"])
            print("✅ Sales data generated successfully")
            return True
        except:
            print("❌ Failed to generate data")
            return False

def main():
    """Main setup function"""
    print("🚀 Sales Dashboard Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Verify data
    if not verify_data():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✨ Setup complete! You're ready to go!")
    print("\n📊 To start the dashboard, run:")
    print("   streamlit run dashboard/app.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
