#!/usr/bin/env python3
"""
Quick Launch Script for Ultimate Stealth Bot System
Provides easy access to different bot execution modes
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_x_links():
    """Run bot with X/Twitter links once"""
    cmd = [
        sys.executable, 
        "ultimate_stealth_bot.py", 
        "--categories", "x_links",
        "--delay-min", "2",
        "--delay-max", "5"
    ]
    subprocess.run(cmd)

def run_firefox_bot():
    """Run Firefox-based Selenium bot"""
    cmd = [
        sys.executable,
        "multi_browser_stealth_bot.py",
        "--categories", "x_links",
        "--browser", "firefox",
        "--headless",
        "--delay-min", "3",
        "--delay-max", "6"
    ]
    subprocess.run(cmd)

def run_continuous_30_5():
    """Run continuous bot: 30 min execution, 5 min sleep"""
    cmd = [
        sys.executable,
        "continuous_stealth_bot.py",
        "--mode", "single",
        "--execution-time", "30",
        "--sleep-time", "5"
    ]
    subprocess.run(cmd)

def run_continuous_15_3():
    """Run continuous bot: 15 min execution, 3 min sleep"""
    cmd = [
        sys.executable,
        "continuous_stealth_bot.py",
        "--mode", "single", 
        "--execution-time", "15",
        "--sleep-time", "3"
    ]
    subprocess.run(cmd)

def run_multi_strategy():
    """Run multiple bot strategies in parallel"""
    cmd = [
        sys.executable,
        "continuous_stealth_bot.py",
        "--mode", "multi"
    ]
    subprocess.run(cmd)

def show_status():
    """Show current bot status and recent logs"""
    print("=== STEALTH BOT SYSTEM STATUS ===")
    
    # Check if logs exist
    logs_dir = Path("logs")
    if logs_dir.exists():
        print(f"Logs directory: {logs_dir.absolute()}")
        
        # Show recent log files
        log_files = list(logs_dir.glob("*.log"))
        if log_files:
            print(f"Available log files: {len(log_files)}")
            for log_file in sorted(log_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                size = log_file.stat().st_size
                print(f"  - {log_file.name} ({size:,} bytes)")
        
        # Show recent execution reports
        report_files = list(logs_dir.glob("*report*.json"))
        if report_files:
            latest_report = max(report_files, key=lambda x: x.stat().st_mtime)
            print(f"Latest report: {latest_report.name}")
    else:
        print("No logs directory found. Run a bot first.")
    
    print("\nAvailable bot commands:")
    print("  python run_stealth_bot.py --mode single       # Single execution")
    print("  python run_stealth_bot.py --mode firefox      # Firefox Selenium bot")
    print("  python run_stealth_bot.py --mode continuous   # 30min run, 5min sleep")
    print("  python run_stealth_bot.py --mode fast         # 15min run, 3min sleep")
    print("  python run_stealth_bot.py --mode multi        # Multiple strategies")

def main():
    parser = argparse.ArgumentParser(
        description="Ultimate Stealth Bot System Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available modes:
  single      - Run HTTP bot once with X/Twitter links
  firefox     - Run Firefox Selenium bot once
  continuous  - Run continuously (30 min execution, 5 min sleep)
  fast        - Run continuously (15 min execution, 3 min sleep)  
  multi       - Run multiple bot strategies in parallel
  status      - Show system status and recent activity

Examples:
  python run_stealth_bot.py --mode single
  python run_stealth_bot.py --mode continuous
  python run_stealth_bot.py --mode status
        """
    )
    
    parser.add_argument('--mode', 
                       choices=['single', 'firefox', 'continuous', 'fast', 'multi', 'status'], 
                       default='single', 
                       help='Execution mode')
    parser.add_argument('--list', action='store_true', 
                       help='List available link categories')
    
    args = parser.parse_args()
    
    if args.list:
        cmd = [sys.executable, "ultimate_stealth_bot.py", "--list-categories"]
        subprocess.run(cmd)
        return
    
    if args.mode == 'single':
        print("Running HTTP stealth bot once...")
        run_x_links()
    elif args.mode == 'firefox':
        print("Running Firefox Selenium bot once...")
        run_firefox_bot()
    elif args.mode == 'continuous':
        print("Starting continuous execution (30 min run, 5 min sleep)...")
        run_continuous_30_5()
    elif args.mode == 'fast':
        print("Starting fast continuous execution (15 min run, 3 min sleep)...")
        run_continuous_15_3()
    elif args.mode == 'multi':
        print("Starting multi-strategy parallel execution...")
        run_multi_strategy()
    elif args.mode == 'status':
        show_status()

if __name__ == "__main__":
    main()