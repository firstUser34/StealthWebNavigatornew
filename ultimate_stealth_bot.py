#!/usr/bin/env python3
"""
Ultimate Stealth Bot - Advanced URL Visitor with Dynamic Link Management
Features: Multiple user agents, random intervals, comprehensive logging, X/Twitter link support
"""

import os
import sys
import time
import json
import random
import requests
import argparse
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import urljoin, urlparse
from pathlib import Path
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from fake_useragent import UserAgent
from dotenv import load_dotenv
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import link configurations
sys.path.append(str(Path(__file__).parent))
try:
    from links.target_links import LINK_CATEGORIES, GLOBAL_SETTINGS, get_all_links, get_links_by_category, get_category_config
except ImportError:
    print("Warning: Could not import target_links. Using default configuration.")
    LINK_CATEGORIES = {}
    GLOBAL_SETTINGS = {}

class UltimateStealthBot:
    """Ultimate stealth bot with advanced features and comprehensive logging"""
    
    def __init__(self, config_file: str = "config/settings.json"):
        """Initialize the ultimate stealth bot"""
        self.config = self._load_config(config_file)
        self.session_pool = {}  # Multiple sessions for different categories
        self.logger = self._setup_advanced_logger()
        self.user_agent_generators = self._setup_user_agent_pool()
        self.visit_stats = {
            "total_visits": 0,
            "successful_visits": 0,
            "failed_visits": 0,
            "category_stats": {},
            "start_time": datetime.now(),
            "end_time": None
        }
        self.active_sessions = []
        self.failed_urls = []
        self.visited_urls = []
        
        # Initialize stealth components
        self._setup_stealth_infrastructure()
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load comprehensive configuration"""
        default_config = {
            "execution_mode": "continuous",  # single, continuous, scheduled
            "categories_to_visit": ["x_links", "api_links"],  # which categories to visit
            "randomization": {
                "shuffle_urls": True,
                "random_delays": True,
                "rotate_user_agents": True,
                "vary_request_patterns": True
            },
            "stealth_features": {
                "multiple_sessions": True,
                "session_rotation": True,
                "header_randomization": True,
                "timing_randomization": True,
                "proxy_rotation": False,
                "cookie_management": True
            },
            "performance": {
                "concurrent_requests": 3,
                "max_workers": 5,
                "request_timeout": 30,
                "retry_attempts": 3
            },
            "logging": {
                "detailed_logs": True,
                "json_logs": True,
                "performance_logs": True,
                "error_tracking": True
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
        
        # Override with environment variables
        env_categories = os.getenv('BOT_CATEGORIES')
        if env_categories:
            default_config['categories_to_visit'] = [cat.strip() for cat in env_categories.split(',')]
            
        return default_config
    
    def _setup_advanced_logger(self) -> logging.Logger:
        """Setup advanced logging system with multiple handlers"""
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        logger = logging.getLogger("ultimate_stealth_bot")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        
        # Console handler with colored output
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # Main log file handler
        main_handler = RotatingFileHandler(
            logs_dir / "ultimate_stealth_bot.log",
            maxBytes=20*1024*1024,  # 20MB
            backupCount=10
        )
        main_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        main_handler.setFormatter(main_formatter)
        logger.addHandler(main_handler)
        
        # Performance log handler
        perf_handler = TimedRotatingFileHandler(
            logs_dir / "performance.log",
            when='midnight',
            interval=1,
            backupCount=30
        )
        perf_formatter = logging.Formatter(
            '%(asctime)s | PERFORMANCE | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        perf_handler.setFormatter(perf_formatter)
        perf_handler.setLevel(logging.INFO)
        
        # Create performance logger
        perf_logger = logging.getLogger("performance")
        perf_logger.addHandler(perf_handler)
        perf_logger.setLevel(logging.INFO)
        
        # Error tracking handler
        error_handler = RotatingFileHandler(
            logs_dir / "errors.log",
            maxBytes=10*1024*1024,
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(main_formatter)
        logger.addHandler(error_handler)
        
        # GitHub Actions compatibility
        if os.getenv('GITHUB_ACTIONS'):
            logger.info("GitHub Actions environment detected - Enhanced logging enabled")
        
        return logger
    
    def _setup_user_agent_pool(self) -> Dict[str, UserAgent]:
        """Setup multiple user agent generators for different categories"""
        generators = {}
        
        try:
            # Different user agent strategies for different link types
            generators['mobile'] = UserAgent(platforms=['mobile'])
            generators['desktop'] = UserAgent(platforms=['pc'])
            generators['random'] = UserAgent()
        except Exception as e:
            self.logger.warning(f"Failed to create user agent generators: {e}")
            generators['fallback'] = None
            
        return generators
    
    def _get_random_user_agent(self, category: str = "random") -> str:
        """Get random user agent based on category"""
        fallback_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0"
        ]
        
        # Try to get from appropriate generator
        if category in self.user_agent_generators:
            try:
                ua_gen = self.user_agent_generators[category]
                if ua_gen:
                    return ua_gen.random
            except Exception:
                pass
        
        # Fallback to random selection
        return random.choice(fallback_agents)
    
    def _setup_stealth_infrastructure(self):
        """Setup stealth infrastructure for different categories"""
        for category in self.config['categories_to_visit']:
            session = requests.Session()
            
            # Configure session with stealth features
            self._configure_stealth_session(session, category)
            
            self.session_pool[category] = session
            self.visit_stats["category_stats"][category] = {
                "visited": 0,
                "successful": 0,
                "failed": 0,
                "last_visit": None
            }
        
        self.logger.info(f"Stealth infrastructure setup for {len(self.session_pool)} categories")
    
    def _configure_stealth_session(self, session: requests.Session, category: str):
        """Configure session with advanced stealth features"""
        # Get category-specific configuration
        cat_config = get_category_config(category) if category in LINK_CATEGORIES else {}
        
        # Set user agent
        user_agent = self._get_random_user_agent(category)
        
        # Advanced headers that mimic real browser behavior
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': random.choice([
                'en-US,en;q=0.9',
                'en-GB,en;q=0.9',
                'en-US,en;q=0.8,es;q=0.7',
                'en-US,en;q=0.9,fr;q=0.8,de;q=0.7'
            ]),
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Charset': 'utf-8, iso-8859-1;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'same-site']),
            'Sec-Fetch-User': '?1',
            'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store']),
            'Pragma': 'no-cache',
            'DNT': '1',
        }
        
        # Add random additional headers
        if random.random() < 0.3:  # 30% chance
            headers['X-Requested-With'] = 'XMLHttpRequest'
        
        if random.random() < 0.2:  # 20% chance
            headers['Origin'] = 'https://www.google.com'
            
        if random.random() < 0.4:  # 40% chance
            headers['Referer'] = random.choice([
                'https://www.google.com/',
                'https://www.bing.com/',
                'https://duckduckgo.com/',
                'https://twitter.com/',
                'https://x.com/'
            ])
        
        session.headers.update(headers)
        
        # Configure session settings
        session.verify = GLOBAL_SETTINGS.get('verify_ssl', True)
        session.max_redirects = 10
        
        self.logger.debug(f"Configured stealth session for {category} with User-Agent: {user_agent[:50]}...")
    
    def _smart_delay(self, category: str, base_delay: Tuple[int, int] = None):
        """Implement smart delays based on category and human-like patterns"""
        if not base_delay:
            cat_config = get_category_config(category)
            if cat_config and 'delay_range' in cat_config:
                delay_range = cat_config['delay_range']
                base_delay = (delay_range['min'], delay_range['max'])
            else:
                base_delay = (2, 5)  # Default
        
        # Base delay
        base = random.uniform(base_delay[0], base_delay[1])
        
        # Add human-like micro variations
        micro_variations = []
        for _ in range(random.randint(1, 4)):
            micro_variations.append(random.uniform(0.01, 0.2))
        
        # Add occasional longer pauses (simulating reading/thinking)
        if random.random() < 0.15:  # 15% chance of longer pause
            thinking_pause = random.uniform(2, 8)
            micro_variations.append(thinking_pause)
        
        total_delay = base + sum(micro_variations)
        
        self.logger.debug(f"Smart delay for {category}: {total_delay:.2f}s")
        time.sleep(total_delay)
    
    def _visit_url_advanced(self, url: str, category: str, session: requests.Session) -> Dict[str, Any]:
        """Advanced URL visiting with comprehensive logging and error handling"""
        visit_start = time.time()
        visit_id = f"{category}_{self.visit_stats['total_visits']:04d}"
        
        self.logger.info(f"[{visit_id}] VISITING: {url}")
        
        try:
            # Rotate user agent for this request
            if self.config['randomization']['rotate_user_agents']:
                new_ua = self._get_random_user_agent(category)
                session.headers['User-Agent'] = new_ua
            
            # Add random headers variation
            if random.random() < 0.3:
                session.headers['Cache-Control'] = random.choice(['no-cache', 'max-age=0'])
            
            # Make the request
            response = session.get(
                url,
                timeout=self.config['performance']['request_timeout'],
                allow_redirects=True
            )
            
            load_time = round(time.time() - visit_start, 3)
            
            # Extract comprehensive page information
            page_info = self._extract_page_info(response, url, load_time)
            page_info.update({
                "visit_id": visit_id,
                "category": category,
                "user_agent": session.headers.get('User-Agent', '')[:50],
                "status": "SUCCESS"
            })
            
            # Enhanced logging with detailed information
            self.logger.info(f"✓ SUCCESS [{visit_id}] - URL: {response.url}")
            self.logger.info(f"  ├─ Original: {url}")
            self.logger.info(f"  ├─ Final: {response.url}")
            self.logger.info(f"  ├─ Status: {response.status_code}")
            self.logger.info(f"  ├─ Title: {page_info.get('title', 'N/A')[:80]}...")
            self.logger.info(f"  ├─ Size: {page_info.get('content_length', 0):,} bytes")
            self.logger.info(f"  ├─ Type: {page_info.get('content_type', 'unknown')}")
            self.logger.info(f"  ├─ Load Time: {load_time}s")
            self.logger.info(f"  └─ Category: {category}")
            
            # Log performance metrics
            perf_logger = logging.getLogger("performance")
            perf_logger.info(f"URL_VISIT|{category}|{load_time}|{response.status_code}|{len(response.content)}|SUCCESS")
            
            # Update statistics
            self.visit_stats["successful_visits"] += 1
            self.visit_stats["category_stats"][category]["successful"] += 1
            self.visit_stats["category_stats"][category]["last_visit"] = datetime.now().isoformat()
            
            # Log to structured format
            self._log_visit_structured(page_info)
            
            return page_info
            
        except requests.exceptions.Timeout as e:
            error_info = self._handle_visit_error(url, category, "TIMEOUT", str(e), visit_start, visit_id)
            self.logger.error(f"✗ TIMEOUT [{visit_id}] - {url}")
            
        except requests.exceptions.ConnectionError as e:
            error_info = self._handle_visit_error(url, category, "CONNECTION_ERROR", str(e), visit_start, visit_id)
            self.logger.error(f"✗ CONNECTION_ERROR [{visit_id}] - {url}")
            
        except requests.exceptions.RequestException as e:
            error_info = self._handle_visit_error(url, category, "REQUEST_ERROR", str(e), visit_start, visit_id)
            self.logger.error(f"✗ REQUEST_ERROR [{visit_id}] - {url}")
            
        except Exception as e:
            error_info = self._handle_visit_error(url, category, "UNEXPECTED_ERROR", str(e), visit_start, visit_id)
            self.logger.error(f"✗ UNEXPECTED_ERROR [{visit_id}] - {url}: {e}")
        
        return {"status": "FAILED", "url": url, "category": category}
    
    def _extract_page_info(self, response: requests.Response, original_url: str, load_time: float) -> Dict[str, Any]:
        """Extract comprehensive information from the response"""
        info = {
            "timestamp": datetime.now().isoformat(),
            "original_url": original_url,
            "final_url": response.url,
            "status_code": response.status_code,
            "content_length": len(response.content),
            "content_type": response.headers.get('Content-Type', 'unknown'),
            "load_time": load_time,
            "headers": dict(response.headers),
            "title": "N/A"
        }
        
        # Extract title if HTML content
        if 'text/html' in info["content_type"]:
            try:
                import re
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
                if title_match:
                    info["title"] = title_match.group(1).strip()
            except Exception:
                pass
        
        # Extract additional metadata
        try:
            # Server information
            info["server"] = response.headers.get('Server', 'unknown')
            
            # Response time from headers
            info["response_time"] = response.elapsed.total_seconds()
            
            # Cookies received
            info["cookies_received"] = len(response.cookies)
            
            # Redirects
            info["redirect_count"] = len(response.history)
            
        except Exception as e:
            self.logger.debug(f"Failed to extract additional metadata: {e}")
        
        return info
    
    def _handle_visit_error(self, url: str, category: str, error_type: str, error_msg: str, start_time: float, visit_id: str) -> Dict[str, Any]:
        """Handle and log visit errors"""
        duration = round(time.time() - start_time, 3)
        
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "visit_id": visit_id,
            "url": url,
            "category": category,
            "error_type": error_type,
            "error_message": error_msg,
            "duration": duration,
            "status": "FAILED"
        }
        
        # Update statistics
        self.visit_stats["failed_visits"] += 1
        self.visit_stats["category_stats"][category]["failed"] += 1
        self.failed_urls.append(url)
        
        # Log performance metrics
        perf_logger = logging.getLogger("performance")
        perf_logger.info(f"URL_VISIT|{category}|{duration}|0|0|{error_type}")
        
        # Log to structured format
        self._log_visit_structured(error_info)
        
        return error_info
    
    def _log_visit_structured(self, visit_info: Dict[str, Any]):
        """Log visit information in structured JSON format"""
        try:
            logs_dir = Path("logs")
            
            # Main visits log
            visits_log = logs_dir / "visits.jsonl"
            with open(visits_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(visit_info, ensure_ascii=False) + '\n')
            
            # Category-specific log
            category = visit_info.get('category', 'unknown')
            category_log = logs_dir / f"visits_{category}.jsonl"
            with open(category_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(visit_info, ensure_ascii=False) + '\n')
                
        except Exception as e:
            self.logger.warning(f"Failed to write structured log: {e}")
    
    def _visit_category_urls(self, category: str) -> List[Dict[str, Any]]:
        """Visit all URLs in a specific category"""
        if category not in self.session_pool:
            self.logger.warning(f"No session configured for category: {category}")
            return []
        
        urls = get_links_by_category(category)
        if not urls:
            self.logger.info(f"No URLs found for category: {category}")
            return []
        
        # Shuffle URLs if randomization is enabled
        if self.config['randomization']['shuffle_urls']:
            random.shuffle(urls)
        
        session = self.session_pool[category]
        results = []
        
        self.logger.info(f"Starting to visit {len(urls)} URLs in category: {category}")
        
        for i, url in enumerate(urls, 1):
            self.visit_stats["total_visits"] += 1
            self.visit_stats["category_stats"][category]["visited"] += 1
            
            self.logger.info(f"Progress: {i}/{len(urls)} URLs in {category}")
            
            # Visit URL
            result = self._visit_url_advanced(url, category, session)
            results.append(result)
            
            # Smart delay between requests
            if i < len(urls):  # Don't delay after the last URL
                self._smart_delay(category)
        
        return results
    
    def _generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive execution report"""
        self.visit_stats["end_time"] = datetime.now()
        execution_time = (self.visit_stats["end_time"] - self.visit_stats["start_time"]).total_seconds()
        
        total_visits = self.visit_stats["total_visits"]
        success_rate = (self.visit_stats["successful_visits"] / total_visits * 100) if total_visits > 0 else 0
        
        report = {
            "execution_summary": {
                "start_time": self.visit_stats["start_time"].isoformat(),
                "end_time": self.visit_stats["end_time"].isoformat(),
                "execution_time_seconds": round(execution_time, 2),
                "total_visits": total_visits,
                "successful_visits": self.visit_stats["successful_visits"],
                "failed_visits": self.visit_stats["failed_visits"],
                "success_rate_percentage": round(success_rate, 2),
                "average_time_per_visit": round(execution_time / total_visits, 2) if total_visits > 0 else 0
            },
            "category_breakdown": self.visit_stats["category_stats"],
            "configuration": {
                "categories_visited": self.config['categories_to_visit'],
                "stealth_features_enabled": self.config['stealth_features'],
                "randomization_settings": self.config['randomization'],
                "performance_settings": self.config['performance']
            },
            "failed_urls": self.failed_urls,
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform,
                "github_actions": bool(os.getenv('GITHUB_ACTIONS'))
            }
        }
        
        # Save report
        try:
            logs_dir = Path("logs")
            report_file = logs_dir / f"execution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Also save as latest report
            latest_report = logs_dir / "latest_report.json"
            with open(latest_report, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Comprehensive report saved: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save report: {e}")
        
        return report
    
    def run_single_execution(self) -> Dict[str, Any]:
        """Run a single execution visiting all configured categories"""
        self.logger.info("=== Ultimate Stealth Bot - Single Execution Started ===")
        self.logger.info(f"Categories to visit: {self.config['categories_to_visit']}")
        self.logger.info(f"Stealth features: {list(self.config['stealth_features'].keys())}")
        
        try:
            all_results = []
            
            # Visit each category
            for category in self.config['categories_to_visit']:
                self.logger.info(f"\n--- Starting category: {category} ---")
                
                category_results = self._visit_category_urls(category)
                all_results.extend(category_results)
                
                self.logger.info(f"--- Completed category: {category} ---")
                
                # Delay between categories
                if category != self.config['categories_to_visit'][-1]:
                    inter_category_delay = random.uniform(5, 15)
                    self.logger.info(f"Inter-category delay: {inter_category_delay:.1f}s")
                    time.sleep(inter_category_delay)
            
            # Generate comprehensive report
            report = self._generate_comprehensive_report()
            
            # Log summary
            self.logger.info("\n=== EXECUTION SUMMARY ===")
            summary = report["execution_summary"]
            self.logger.info(f"Total Visits: {summary['total_visits']}")
            self.logger.info(f"Successful: {summary['successful_visits']}")
            self.logger.info(f"Failed: {summary['failed_visits']}")
            self.logger.info(f"Success Rate: {summary['success_rate_percentage']}%")
            self.logger.info(f"Execution Time: {summary['execution_time_seconds']}s")
            self.logger.info(f"Average Time/Visit: {summary['average_time_per_visit']}s")
            
            # Category breakdown
            self.logger.info("\n=== CATEGORY BREAKDOWN ===")
            for category, stats in report["category_breakdown"].items():
                self.logger.info(f"{category}: {stats['successful']}/{stats['visited']} successful")
            
            return report
            
        except Exception as e:
            self.logger.error(f"Fatal error during execution: {e}", exc_info=True)
            return {"error": str(e), "execution_summary": {"total_visits": 0}}
        
        finally:
            self.logger.info("=== Ultimate Stealth Bot Execution Completed ===")


def main():
    """Main entry point with enhanced command line interface"""
    parser = argparse.ArgumentParser(
        description="Ultimate Stealth Bot - Advanced URL Visitor with Dynamic Link Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ultimate_stealth_bot.py --categories x_links,api_links
  python ultimate_stealth_bot.py --categories x_links --delay-min 3 --delay-max 8
  python ultimate_stealth_bot.py --all-categories --concurrent 5
        """
    )
    
    parser.add_argument('--categories', type=str, help='Comma-separated categories to visit')
    parser.add_argument('--all-categories', action='store_true', help='Visit all available categories')
    parser.add_argument('--list-categories', action='store_true', help='List available categories and exit')
    parser.add_argument('--config', type=str, default='config/settings.json', help='Config file path')
    parser.add_argument('--delay-min', type=int, help='Minimum delay between requests')
    parser.add_argument('--delay-max', type=int, help='Maximum delay between requests')
    parser.add_argument('--concurrent', type=int, help='Number of concurrent requests')
    parser.add_argument('--log-level', type=str, default='INFO', help='Logging level')
    parser.add_argument('--no-shuffle', action='store_true', help='Disable URL shuffling')
    parser.add_argument('--no-user-agent-rotation', action='store_true', help='Disable user agent rotation')
    
    # Compatibility arguments
    parser.add_argument('--urls', type=str, help='Comma-separated URLs (compatibility mode)')
    parser.add_argument('--headless', action='store_true', help='Compatibility flag (ignored)')
    
    args = parser.parse_args()
    
    # List categories if requested
    if args.list_categories:
        print("Available link categories:")
        if LINK_CATEGORIES:
            for category, config in LINK_CATEGORIES.items():
                print(f"  {category}: {len(config['urls'])} URLs (Priority: {config['priority']})")
        else:
            print("  No categories configured. Check links/target_links.py")
        sys.exit(0)
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Create bot instance
        bot = UltimateStealthBot(args.config)
        
        # Configure categories to visit
        if args.all_categories:
            if LINK_CATEGORIES:
                bot.config['categories_to_visit'] = list(LINK_CATEGORIES.keys())
            else:
                print("No categories available. Using compatibility mode.")
                bot.config['categories_to_visit'] = ['compatibility']
        elif args.categories:
            bot.config['categories_to_visit'] = [cat.strip() for cat in args.categories.split(',')]
        elif args.urls:
            # Compatibility mode - create temporary category
            bot.config['categories_to_visit'] = ['compatibility']
            # Override with provided URLs
            
        # Apply command line overrides
        if args.delay_min is not None or args.delay_max is not None:
            # Apply to all categories
            for category in bot.config['categories_to_visit']:
                if category in LINK_CATEGORIES:
                    if args.delay_min is not None:
                        LINK_CATEGORIES[category]['delay_range']['min'] = args.delay_min
                    if args.delay_max is not None:
                        LINK_CATEGORIES[category]['delay_range']['max'] = args.delay_max
        
        if args.concurrent is not None:
            bot.config['performance']['concurrent_requests'] = args.concurrent
            
        if args.no_shuffle:
            bot.config['randomization']['shuffle_urls'] = False
            
        if args.no_user_agent_rotation:
            bot.config['randomization']['rotate_user_agents'] = False
        
        # Validate configuration
        if not bot.config['categories_to_visit']:
            print("No categories specified. Use --categories, --all-categories, or --urls")
            sys.exit(1)
        
        # Run bot
        report = bot.run_single_execution()
        
        # Exit with appropriate code
        summary = report.get("execution_summary", {})
        total_visits = summary.get("total_visits", 0)
        successful_visits = summary.get("successful_visits", 0)
        
        if total_visits > 0 and successful_visits == total_visits:
            print("All URLs visited successfully!")
            sys.exit(0)
        elif successful_visits > 0:
            print(f"Partial success: {successful_visits}/{total_visits} URLs visited successfully")
            sys.exit(0)
        else:
            print("All URL visits failed. Check logs for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nBot execution interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()