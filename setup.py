"""
Setup script for Mushaf Hafid application
Run this to install dependencies and start the application
"""

import subprocess
import sys
import os

def install_python_deps():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        print("Please install pip first:")
        print("curl https://bootstrap.pypa.io/get-pip.py | python3")
        return False
    return True

def install_frontend_deps():
    """Install frontend dependencies"""
    print("Installing frontend dependencies...")
    try:
        os.chdir("frontend")
        subprocess.check_call(["npm", "install"])
        os.chdir("..")
        print("✅ Frontend dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install frontend dependencies: {e}")
        return False
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("Starting backend server...")
    try:
        subprocess.Popen([sys.executable, "main.py"])
        print("✅ Backend server started at http://localhost:8000")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    return True

def start_frontend():
    """Start the React frontend"""
    print("Starting frontend development server...")
    try:
        os.chdir("frontend")
        subprocess.Popen(["npm", "run", "dev"])
        os.chdir("..")
        print("✅ Frontend started at http://localhost:5173")
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return False
    return True

if __name__ == "__main__":
    print("🕌 Setting up Mushaf Hafid Application")
    print("=" * 50)
    
    # Check if database exists
    if not os.path.exists("app/database/quran.db"):
        print("Initializing database...")
        subprocess.call([sys.executable, "init_db.py"])
        subprocess.call([sys.executable, "sample_data.py"])
    
    # Install dependencies
    if len(sys.argv) > 1 and sys.argv[1] == "--install-deps":
        if not install_python_deps():
            sys.exit(1)
        if not install_frontend_deps():
            sys.exit(1)
    
    print("\n🚀 Application Setup Complete!")
    print("\nTo start the application:")
    print("1. Backend: python3 main.py")
    print("2. Frontend: cd frontend && npm run dev")
    print("\nThen visit: http://localhost:5173")