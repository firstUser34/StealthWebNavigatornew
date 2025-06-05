#!/usr/bin/env python3
"""
Dependency Installer for Ultimate Stealth Bot System
Automatically installs all required packages and browsers
"""

import subprocess
import sys
import os
import platform

def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"Installing: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ Success: {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {description}")
        print(f"Error: {e.stderr}")
        return False

def install_python_packages():
    """Install required Python packages"""
    packages = [
        "requests",
        "fake-useragent", 
        "python-dotenv",
        "selenium"
    ]
    
    for package in packages:
        run_command(f"{sys.executable} -m pip install {package}", f"Python package: {package}")

def install_browsers():
    """Install browsers based on the operating system"""
    system = platform.system().lower()
    
    if system == "linux":
        # Install Firefox
        run_command("sudo apt-get update", "Updating package list")
        run_command("sudo apt-get install -y firefox", "Firefox browser")
        
        # Install Chrome if available
        run_command("wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -", "Chrome signing key")
        run_command('echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list', "Chrome repository")
        run_command("sudo apt-get update", "Updating package list")
        run_command("sudo apt-get install -y google-chrome-stable", "Chrome browser")
        
    elif system == "darwin":  # macOS
        # Use Homebrew
        run_command("brew install firefox", "Firefox browser")
        run_command("brew install --cask google-chrome", "Chrome browser")
        
    elif system == "windows":
        print("On Windows, please install browsers manually:")
        print("1. Firefox: https://www.mozilla.org/firefox/")
        print("2. Chrome: https://www.google.com/chrome/")
        print("3. Edge is pre-installed")

def setup_directories():
    """Create necessary directories"""
    directories = ["logs", "config"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def main():
    """Main installation process"""
    print("=== Ultimate Stealth Bot System - Dependency Installer ===")
    print()
    
    print("Step 1: Installing Python packages...")
    install_python_packages()
    print()
    
    print("Step 2: Installing browsers...")
    install_browsers()
    print()
    
    print("Step 3: Setting up directories...")
    setup_directories()
    print()
    
    print("=== Installation Complete ===")
    print()
    print("You can now run the stealth bots:")
    print("1. Ultimate Stealth Bot (HTTP): python ultimate_stealth_bot.py --categories x_links")
    print("2. Multi-Browser Bot (Selenium): python multi_browser_stealth_bot.py --categories x_links")
    print("3. Quick Launcher: python run_stealth_bot.py --mode x_links")

if __name__ == "__main__":
    main()