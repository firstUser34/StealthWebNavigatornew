#!/usr/bin/env python3
"""
Continuous Stealth Bot - Runs indefinitely with scheduled intervals
30 minutes execution, 5 minutes sleep, repeat forever
"""

import os
import sys
import time
import signal
import threading
from datetime import datetime, timedelta
import subprocess
import json
import logging
from pathlib import Path

class ContinuousStealthBot:
    """Manages continuous execution of stealth bots"""
    
    def __init__(self):
        self.running = True
        self.current_process = None
        self.execution_count = 0
        self.total_successes = 0
        self.total_failures = 0
        
        # Configuration
        self.execution_duration = 30 * 60  # 30 minutes
        self.sleep_duration = 5 * 60       # 5 minutes
        self.bot_command = "python ultimate_stealth_bot.py --categories x_links --delay-min 3 --delay-max 8"
        
        # Setup logging
        self.logger = self._setup_logger()
        
        # Handle shutdown signals
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logger(self):
        """Setup comprehensive logging"""
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        logger = logging.getLogger("continuous_bot")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            '%(asctime)s | CONTINUOUS | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler for continuous bot
        file_handler = logging.FileHandler(logs_dir / "continuous_bot.log")
        file_handler.setFormatter(console_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}. Initiating graceful shutdown...")
        self.running = False
        
        if self.current_process:
            self.logger.info("Terminating current bot process...")
            self.current_process.terminate()
            try:
                self.current_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.logger.warning("Force killing bot process...")
                self.current_process.kill()
    
    def _run_single_bot_execution(self):
        """Run a single bot execution with timeout"""
        self.execution_count += 1
        start_time = datetime.now()
        
        self.logger.info(f"=== EXECUTION #{self.execution_count} STARTED ===")
        self.logger.info(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"Command: {self.bot_command}")
        
        try:
            # Start the bot process
            self.current_process = subprocess.Popen(
                self.bot_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for completion or timeout
            try:
                stdout, stderr = self.current_process.communicate(timeout=self.execution_duration)
                return_code = self.current_process.returncode
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                if return_code == 0:
                    self.total_successes += 1
                    self.logger.info(f"✓ EXECUTION #{self.execution_count} COMPLETED SUCCESSFULLY")
                    self.logger.info(f"Execution time: {execution_time:.1f} seconds")
                    
                    # Extract success info from stdout if available
                    if "Success Rate: 100.0%" in stdout:
                        self.logger.info("All URLs visited successfully in this execution")
                    
                else:
                    self.total_failures += 1
                    self.logger.error(f"✗ EXECUTION #{self.execution_count} FAILED (exit code: {return_code})")
                    if stderr:
                        self.logger.error(f"Error output: {stderr[:500]}")
                
            except subprocess.TimeoutExpired:
                self.logger.info(f"⏰ EXECUTION #{self.execution_count} REACHED 30-MINUTE LIMIT")
                self.current_process.terminate()
                try:
                    self.current_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.current_process.kill()
                
                self.total_successes += 1  # Consider timeout as successful completion
                
        except Exception as e:
            self.total_failures += 1
            self.logger.error(f"✗ EXECUTION #{self.execution_count} ERROR: {e}")
        
        finally:
            self.current_process = None
            end_time = datetime.now()
            self.logger.info(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.logger.info(f"=== EXECUTION #{self.execution_count} FINISHED ===")
    
    def _sleep_with_countdown(self):
        """Sleep for 5 minutes with periodic updates"""
        self.logger.info(f"💤 SLEEPING FOR {self.sleep_duration // 60} MINUTES...")
        
        start_sleep = datetime.now()
        end_sleep = start_sleep + timedelta(seconds=self.sleep_duration)
        
        # Log every minute during sleep
        while self.running and datetime.now() < end_sleep:
            remaining = (end_sleep - datetime.now()).total_seconds()
            if remaining > 0:
                if int(remaining) % 60 == 0:  # Log every minute
                    mins_left = int(remaining // 60)
                    if mins_left > 0:
                        self.logger.info(f"Sleep countdown: {mins_left} minutes remaining...")
                
                time.sleep(1)
            else:
                break
        
        if self.running:
            self.logger.info("✨ SLEEP COMPLETED - RESUMING OPERATIONS")
    
    def _log_statistics(self):
        """Log current execution statistics"""
        total_executions = self.execution_count
        success_rate = (self.total_successes / total_executions * 100) if total_executions > 0 else 0
        
        self.logger.info(f"📊 STATISTICS: {total_executions} executions, {self.total_successes} successful, {self.total_failures} failed")
        self.logger.info(f"📈 SUCCESS RATE: {success_rate:.1f}%")
    
    def run_forever(self):
        """Main continuous execution loop"""
        self.logger.info("🚀 CONTINUOUS STEALTH BOT SYSTEM STARTED")
        self.logger.info(f"⏱️  Execution duration: {self.execution_duration // 60} minutes")
        self.logger.info(f"😴 Sleep duration: {self.sleep_duration // 60} minutes")
        self.logger.info(f"🎯 Target: X/Twitter links with random intervals")
        self.logger.info("🔄 Will run indefinitely until stopped (Ctrl+C)")
        self.logger.info("=" * 60)
        
        while self.running:
            try:
                # Run bot execution
                self._run_single_bot_execution()
                
                # Log statistics
                self._log_statistics()
                
                # Only sleep if we're continuing
                if self.running:
                    self._sleep_with_countdown()
                
            except KeyboardInterrupt:
                self.logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in main loop: {e}")
                if self.running:
                    self.logger.info("Continuing after error...")
                    time.sleep(60)  # Wait 1 minute before retrying
        
        self.logger.info("🛑 CONTINUOUS STEALTH BOT SYSTEM STOPPED")
        self.logger.info(f"📊 FINAL STATISTICS:")
        self.logger.info(f"   Total executions: {self.execution_count}")
        self.logger.info(f"   Successful: {self.total_successes}")
        self.logger.info(f"   Failed: {self.total_failures}")
        if self.execution_count > 0:
            final_success_rate = (self.total_successes / self.execution_count * 100)
            self.logger.info(f"   Overall success rate: {final_success_rate:.1f}%")


class MultiStrategyBot:
    """Runs multiple bot strategies in parallel"""
    
    def __init__(self):
        self.bots = [
            {
                "name": "HTTP Bot",
                "command": "python ultimate_stealth_bot.py --categories x_links --delay-min 2 --delay-max 5",
                "interval": 45 * 60  # 45 minutes
            },
            {
                "name": "Firefox Bot", 
                "command": "python multi_browser_stealth_bot.py --categories x_links --browser firefox --delay-min 3 --delay-max 7",
                "interval": 60 * 60  # 1 hour
            }
        ]
        
        self.running = True
        self.threads = []
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging for multi-strategy bot"""
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        logger = logging.getLogger("multi_strategy")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s | MULTI-STRATEGY | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        file_handler = logging.FileHandler(logs_dir / "multi_strategy.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def _run_strategy(self, bot_config):
        """Run a single bot strategy"""
        while self.running:
            try:
                self.logger.info(f"🚀 Starting {bot_config['name']}")
                
                process = subprocess.run(
                    bot_config['command'],
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30 * 60  # 30 minute timeout
                )
                
                if process.returncode == 0:
                    self.logger.info(f"✓ {bot_config['name']} completed successfully")
                else:
                    self.logger.error(f"✗ {bot_config['name']} failed")
                
                # Sleep for the specified interval
                if self.running:
                    sleep_minutes = bot_config['interval'] // 60
                    self.logger.info(f"😴 {bot_config['name']} sleeping for {sleep_minutes} minutes")
                    time.sleep(bot_config['interval'])
                
            except subprocess.TimeoutExpired:
                self.logger.info(f"⏰ {bot_config['name']} timed out after 30 minutes")
            except Exception as e:
                self.logger.error(f"Error in {bot_config['name']}: {e}")
                time.sleep(300)  # Sleep 5 minutes on error
    
    def run_parallel(self):
        """Run all strategies in parallel"""
        self.logger.info("🚀 MULTI-STRATEGY BOT SYSTEM STARTED")
        self.logger.info(f"Running {len(self.bots)} bot strategies in parallel")
        
        try:
            # Start threads for each bot strategy
            for bot_config in self.bots:
                thread = threading.Thread(target=self._run_strategy, args=(bot_config,))
                thread.daemon = True
                thread.start()
                self.threads.append(thread)
                self.logger.info(f"Started thread for {bot_config['name']}")
            
            # Keep main thread alive
            while self.running:
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            self.logger.info("Shutdown signal received")
            self.running = False


def main():
    """Main entry point with mode selection"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Continuous Stealth Bot System")
    parser.add_argument('--mode', choices=['single', 'multi'], default='single',
                       help='Execution mode: single strategy or multi-strategy')
    parser.add_argument('--execution-time', type=int, default=30,
                       help='Execution duration in minutes (default: 30)')
    parser.add_argument('--sleep-time', type=int, default=5,
                       help='Sleep duration in minutes (default: 5)')
    
    args = parser.parse_args()
    
    if args.mode == 'single':
        bot = ContinuousStealthBot()
        bot.execution_duration = args.execution_time * 60
        bot.sleep_duration = args.sleep_time * 60
        bot.run_forever()
    else:
        bot = MultiStrategyBot()
        bot.run_parallel()


if __name__ == "__main__":
    main()