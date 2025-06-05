#!/usr/bin/env python3
"""
Multi-Browser Stealth Bot - Works with Firefox, Edge, Chrome, or any available browser
Advanced Selenium automation with automatic browser detection and stealth features
"""

import os
import sys
import time
import json
import random
import argparse
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import WebDriverException, TimeoutException
from fake_useragent import UserAgent
from dotenv import load_dotenv

# Import link configurations
sys.path.append(str(Path(__file__).parent))
try:
    from links.target_links import LINK_CATEGORIES, get_links_by_category
except ImportError:
    print("Warning: Could not import target_links. Using default configuration.")
    LINK_CATEGORIES = {}

class MultiBrowserStealthBot:
    """Multi-browser stealth bot with automatic browser detection"""
    
    def __init__(self, config_file: str = "config/settings.json"):
        """Initialize the multi-browser stealth bot"""
        self.config = self._load_config(config_file)
        self.driver: Optional[webdriver.Remote] = None
        self.browser_type = None
        self.logger = self._setup_logger()
        self.user_agent_generator = UserAgent()
        
        # Statistics
        self.visit_count = 0
        self.success_count = 0
        self.failed_urls = []
        self.visited_urls = []
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration"""
        default_config = {
            "categories_to_visit": ["x_links"],
            "browser_preferences": ["firefox", "edge", "chrome"],  # Priority order
            "stealth_features": {
                "user_agent_rotation": True,
                "random_delays": True,
                "human_simulation": True,
                "header_spoofing": True
            },
            "execution": {
                "headless": True,
                "timeout": 30,
                "implicit_wait": 10,
                "delay_range": {"min": 2, "max": 5}
            }
        }
        
        # Load from file if exists
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                default_config.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
        
        return default_config
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging system"""
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        logger = logging.getLogger("multi_browser_stealth_bot")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler
        file_handler = RotatingFileHandler(
            logs_dir / "multi_browser_bot.log",
            maxBytes=10*1024*1024,
            backupCount=5
        )
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def _get_random_user_agent(self) -> str:
        """Get random user agent"""
        try:
            return self.user_agent_generator.random
        except Exception:
            # Fallback user agents
            fallback_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
            ]
            return random.choice(fallback_agents)
    
    def _create_firefox_driver(self) -> webdriver.Firefox:
        """Create Firefox driver with stealth options"""
        options = FirefoxOptions()
        
        if self.config['execution']['headless']:
            options.add_argument('--headless')
        
        # Stealth options for Firefox
        stealth_args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-gpu',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',
            '--disable-javascript',  # Can be selective
            '--disable-default-apps',
            '--disable-sync',
            '--disable-translate',
        ]
        
        for arg in stealth_args:
            options.add_argument(arg)
        
        # Set user agent
        if self.config['stealth_features']['user_agent_rotation']:
            user_agent = self._get_random_user_agent()
            options.set_preference("general.useragent.override", user_agent)
            self.logger.info(f"Firefox User-Agent: {user_agent[:50]}...")
        
        # Additional Firefox preferences for stealth
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        options.set_preference("privacy.trackingprotection.enabled", True)
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("media.navigator.enabled", False)
        
        try:
            driver = webdriver.Firefox(options=options)
            self.browser_type = "Firefox"
            self.logger.info("Successfully created Firefox driver")
            return driver
        except Exception as e:
            self.logger.warning(f"Failed to create Firefox driver: {e}")
            raise
    
    def _create_edge_driver(self) -> webdriver.Edge:
        """Create Edge driver with stealth options"""
        options = EdgeOptions()
        
        if self.config['execution']['headless']:
            options.add_argument('--headless=new')
        
        # Stealth options for Edge
        stealth_args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-gpu',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',
            '--disable-default-apps',
            '--disable-sync',
            '--disable-translate',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
        ]
        
        for arg in stealth_args:
            options.add_argument(arg)
        
        # Set user agent
        if self.config['stealth_features']['user_agent_rotation']:
            user_agent = self._get_random_user_agent()
            options.add_argument(f'--user-agent={user_agent}')
            self.logger.info(f"Edge User-Agent: {user_agent[:50]}...")
        
        # Additional Edge preferences
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            driver = webdriver.Edge(options=options)
            self.browser_type = "Edge"
            self.logger.info("Successfully created Edge driver")
            return driver
        except Exception as e:
            self.logger.warning(f"Failed to create Edge driver: {e}")
            raise
    
    def _create_chrome_driver(self) -> webdriver.Chrome:
        """Create Chrome driver with stealth options"""
        options = ChromeOptions()
        
        if self.config['execution']['headless']:
            options.add_argument('--headless=new')
        
        # Stealth options for Chrome
        stealth_args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-gpu',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',
            '--disable-default-apps',
            '--disable-sync',
            '--disable-translate',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
        ]
        
        for arg in stealth_args:
            options.add_argument(arg)
        
        # Set user agent
        if self.config['stealth_features']['user_agent_rotation']:
            user_agent = self._get_random_user_agent()
            options.add_argument(f'--user-agent={user_agent}')
            self.logger.info(f"Chrome User-Agent: {user_agent[:50]}...")
        
        # Additional Chrome preferences
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            driver = webdriver.Chrome(options=options)
            self.browser_type = "Chrome"
            self.logger.info("Successfully created Chrome driver")
            return driver
        except Exception as e:
            self.logger.warning(f"Failed to create Chrome driver: {e}")
            raise
    
    def _create_driver(self) -> webdriver.Remote:
        """Create driver with automatic browser detection"""
        self.logger.info("Attempting to create browser driver...")
        
        # Try browsers in preference order
        browser_creators = {
            "firefox": self._create_firefox_driver,
            "edge": self._create_edge_driver,
            "chrome": self._create_chrome_driver
        }
        
        for browser in self.config['browser_preferences']:
            if browser in browser_creators:
                try:
                    self.logger.info(f"Trying {browser.title()} browser...")
                    driver = browser_creators[browser]()
                    
                    # Set timeouts
                    driver.set_page_load_timeout(self.config['execution']['timeout'])
                    driver.implicitly_wait(self.config['execution']['implicit_wait'])
                    
                    # Execute stealth scripts
                    self._execute_stealth_scripts(driver)
                    
                    return driver
                    
                except Exception as e:
                    self.logger.warning(f"{browser.title()} failed: {e}")
                    continue
        
        # If all browsers fail, raise error
        raise Exception("No compatible browser found. Install Firefox, Edge, or Chrome.")
    
    def _execute_stealth_scripts(self, driver: webdriver.Remote):
        """Execute JavaScript to enhance stealth"""
        stealth_scripts = [
            # Remove webdriver property
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
            
            # Mock plugins
            """
            Object.defineProperty(navigator, 'plugins', {
                get: () => [{
                    0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                    description: "Portable Document Format",
                    filename: "internal-pdf-viewer",
                    length: 1,
                    name: "Chrome PDF Plugin"
                }]
            });
            """,
            
            # Mock languages
            "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
            
            # Hide automation indicators
            "delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;",
            "delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;",
            "delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;",
        ]
        
        for script in stealth_scripts:
            try:
                driver.execute_script(script)
            except Exception as e:
                self.logger.debug(f"Failed to execute stealth script: {e}")
    
    def _human_like_delay(self):
        """Create human-like delay"""
        if self.config['stealth_features']['random_delays']:
            delay_range = self.config['execution']['delay_range']
            base_delay = random.uniform(delay_range['min'], delay_range['max'])
            
            # Add micro-delays for realism
            micro_delays = [random.uniform(0.01, 0.2) for _ in range(random.randint(1, 3))]
            total_delay = base_delay + sum(micro_delays)
            
            self.logger.debug(f"Human-like delay: {total_delay:.2f}s")
            time.sleep(total_delay)
    
    def _human_like_interaction(self, driver: webdriver.Remote):
        """Perform human-like interactions"""
        if not self.config['stealth_features']['human_simulation']:
            return
        
        try:
            # Random scrolling
            if random.random() < 0.7:  # 70% chance
                scroll_actions = [
                    "window.scrollTo(0, Math.floor(Math.random() * 500));",
                    "window.scrollBy(0, Math.floor(Math.random() * 300) + 100);",
                    "window.scrollTo(0, document.body.scrollHeight / 2);",
                ]
                script = random.choice(scroll_actions)
                driver.execute_script(script)
                time.sleep(random.uniform(0.5, 2.0))
            
            # Simulate reading time
            if random.random() < 0.8:  # 80% chance
                read_time = random.uniform(1.0, 4.0)
                self.logger.debug(f"Simulating reading for {read_time:.1f}s")
                time.sleep(read_time)
            
        except Exception as e:
            self.logger.debug(f"Human-like interaction failed: {e}")
    
    def _visit_url(self, url: str, category: str) -> bool:
        """Visit a single URL with comprehensive logging"""
        self.visit_count += 1
        start_time = time.time()
        visit_id = f"{category}_{self.visit_count:04d}"
        
        self.logger.info(f"[{visit_id}] VISITING: {url}")
        
        try:
            # Navigate to URL
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Get page information
            current_url = self.driver.current_url
            title = self.driver.title
            page_source_length = len(self.driver.page_source)
            load_time = round(time.time() - start_time, 3)
            
            # Log detailed visit information
            visit_info = {
                "timestamp": datetime.now().isoformat(),
                "visit_id": visit_id,
                "browser": self.browser_type,
                "request_url": url,
                "final_url": current_url,
                "title": title,
                "page_size": page_source_length,
                "load_time": load_time,
                "category": category,
                "status": "SUCCESS"
            }
            
            # Enhanced logging
            self.logger.info(f"✓ SUCCESS [{visit_id}] - URL: {current_url}")
            self.logger.info(f"  ├─ Browser: {self.browser_type}")
            self.logger.info(f"  ├─ Original: {url}")
            self.logger.info(f"  ├─ Final: {current_url}")
            self.logger.info(f"  ├─ Title: {title[:80]}{'...' if len(title) > 80 else ''}")
            self.logger.info(f"  ├─ Load Time: {load_time}s")
            self.logger.info(f"  ├─ Page Size: {page_source_length:,} bytes")
            self.logger.info(f"  └─ Category: {category}")
            
            # Log to structured format
            self._log_visit_json(visit_info)
            
            # Human-like interactions
            self._human_like_interaction(self.driver)
            
            # Delay before next request
            self._human_like_delay()
            
            self.success_count += 1
            self.visited_urls.append(visit_info)
            return True
            
        except TimeoutException:
            error_msg = f"Timeout loading {url}"
            self.logger.error(f"✗ TIMEOUT [{visit_id}] - {url}")
            self._log_visit_error(url, category, "timeout", error_msg, start_time, visit_id)
            
        except WebDriverException as e:
            error_msg = f"WebDriver error: {str(e)}"
            self.logger.error(f"✗ WEBDRIVER_ERROR [{visit_id}] - {url}")
            self._log_visit_error(url, category, "webdriver_error", error_msg, start_time, visit_id)
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(f"✗ UNEXPECTED_ERROR [{visit_id}] - {url}: {e}")
            self._log_visit_error(url, category, "unexpected_error", error_msg, start_time, visit_id)
        
        self.failed_urls.append(url)
        return False
    
    def _log_visit_json(self, visit_info: Dict[str, Any]):
        """Log visit information in JSON format"""
        try:
            logs_dir = Path("logs")
            
            # Main visits log
            visits_log = logs_dir / "browser_visits.jsonl"
            with open(visits_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(visit_info, ensure_ascii=False) + '\n')
            
        except Exception as e:
            self.logger.warning(f"Failed to write JSON log: {e}")
    
    def _log_visit_error(self, url: str, category: str, error_type: str, error_msg: str, start_time: float, visit_id: str):
        """Log failed visit attempts"""
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "visit_id": visit_id,
            "browser": self.browser_type,
            "url": url,
            "category": category,
            "error_type": error_type,
            "error_message": error_msg,
            "duration": round(time.time() - start_time, 3),
            "status": "FAILED"
        }
        
        self._log_visit_json(error_info)
    
    def _visit_category_urls(self, category: str) -> List[Dict[str, Any]]:
        """Visit all URLs in a specific category"""
        if category not in LINK_CATEGORIES:
            self.logger.warning(f"Category not found: {category}")
            return []
        
        urls = LINK_CATEGORIES[category].get('urls', [])
        if not urls:
            self.logger.info(f"No URLs found for category: {category}")
            return []
        
        # Shuffle URLs for randomness
        random.shuffle(urls)
        
        results = []
        self.logger.info(f"Starting to visit {len(urls)} URLs in category: {category}")
        
        for i, url in enumerate(urls, 1):
            self.logger.info(f"Progress: {i}/{len(urls)} URLs in {category}")
            
            result = self._visit_url(url, category)
            results.append({"url": url, "success": result})
        
        return results
    
    def _generate_summary_report(self) -> Dict[str, Any]:
        """Generate execution summary"""
        total_visits = self.visit_count
        success_rate = (self.success_count / total_visits * 100) if total_visits > 0 else 0
        
        report = {
            "execution_summary": {
                "timestamp": datetime.now().isoformat(),
                "browser_used": self.browser_type,
                "total_visits": total_visits,
                "successful_visits": self.success_count,
                "failed_visits": len(self.failed_urls),
                "success_rate_percentage": round(success_rate, 2)
            },
            "categories_visited": self.config['categories_to_visit'],
            "failed_urls": self.failed_urls,
            "stealth_features": self.config['stealth_features']
        }
        
        # Save report
        try:
            logs_dir = Path("logs")
            report_file = logs_dir / f"browser_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Report saved: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save report: {e}")
        
        return report
    
    def run(self) -> Dict[str, Any]:
        """Main execution method"""
        self.logger.info("=== Multi-Browser Stealth Bot Started ===")
        
        try:
            # Create driver
            self.driver = self._create_driver()
            self.logger.info(f"Using {self.browser_type} browser for automation")
            
            # Visit categories
            for category in self.config['categories_to_visit']:
                self.logger.info(f"\n--- Starting category: {category} ---")
                self._visit_category_urls(category)
                self.logger.info(f"--- Completed category: {category} ---")
            
            # Generate summary
            report = self._generate_summary_report()
            
            # Log summary
            self.logger.info("\n=== EXECUTION SUMMARY ===")
            summary = report["execution_summary"]
            self.logger.info(f"Browser Used: {summary['browser_used']}")
            self.logger.info(f"Total Visits: {summary['total_visits']}")
            self.logger.info(f"Successful: {summary['successful_visits']}")
            self.logger.info(f"Failed: {summary['failed_visits']}")
            self.logger.info(f"Success Rate: {summary['success_rate_percentage']}%")
            
            return report
            
        except Exception as e:
            self.logger.error(f"Fatal error: {e}", exc_info=True)
            return {"error": str(e)}
        
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                    self.logger.info("Browser driver closed successfully")
                except Exception as e:
                    self.logger.warning(f"Error closing driver: {e}")
            
            self.logger.info("=== Multi-Browser Stealth Bot Completed ===")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Multi-Browser Stealth Bot")
    parser.add_argument('--categories', type=str, default='x_links', help='Categories to visit')
    parser.add_argument('--browser', type=str, choices=['firefox', 'edge', 'chrome'], help='Preferred browser')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--delay-min', type=int, help='Minimum delay between requests')
    parser.add_argument('--delay-max', type=int, help='Maximum delay between requests')
    
    args = parser.parse_args()
    
    try:
        load_dotenv()
        
        bot = MultiBrowserStealthBot()
        
        # Override config with arguments
        if args.categories:
            bot.config['categories_to_visit'] = [cat.strip() for cat in args.categories.split(',')]
        
        if args.browser:
            bot.config['browser_preferences'] = [args.browser]
        
        if args.headless:
            bot.config['execution']['headless'] = True
        
        if args.delay_min is not None:
            bot.config['execution']['delay_range']['min'] = args.delay_min
        
        if args.delay_max is not None:
            bot.config['execution']['delay_range']['max'] = args.delay_max
        
        # Run bot
        report = bot.run()
        
        # Exit with appropriate code
        if "error" in report:
            sys.exit(1)
        
        summary = report.get("execution_summary", {})
        if summary.get("success_rate_percentage", 0) == 100:
            print("All URLs visited successfully!")
            sys.exit(0)
        else:
            print("Some URLs failed. Check logs for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nBot execution interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()