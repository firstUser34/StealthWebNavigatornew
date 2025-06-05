#!/usr/bin/env python3
"""
Advanced Link Manager for Ultimate Stealth Bot
Provides dynamic link management, categorization, and scheduling
"""

import json
import random
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import logging

@dataclass
class LinkInfo:
    """Information about a link to visit"""
    url: str
    category: str
    priority: str
    last_visited: Optional[str] = None
    visit_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    avg_load_time: float = 0.0
    status: str = "active"  # active, disabled, failed
    notes: str = ""
    added_date: Optional[str] = None

class AdvancedLinkManager:
    """Advanced link management system"""
    
    def __init__(self, links_file: str = "links/managed_links.json"):
        self.links_file = Path(links_file)
        self.logger = logging.getLogger("link_manager")
        self.links: Dict[str, LinkInfo] = {}
        self.categories: Dict[str, Dict] = {}
        self.load_links()
    
    def load_links(self):
        """Load links from JSON file"""
        try:
            if self.links_file.exists():
                with open(self.links_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert dict data to LinkInfo objects
                for url, link_data in data.get('links', {}).items():
                    self.links[url] = LinkInfo(**link_data)
                
                self.categories = data.get('categories', {})
                self.logger.info(f"Loaded {len(self.links)} links from {self.links_file}")
            else:
                self.logger.info("No existing links file found, starting fresh")
                self._initialize_from_target_links()
        except Exception as e:
            self.logger.error(f"Failed to load links: {e}")
            self._initialize_from_target_links()
    
    def _initialize_from_target_links(self):
        """Initialize from target_links.py if available"""
        try:
            from target_links import LINK_CATEGORIES
            
            for category_name, config in LINK_CATEGORIES.items():
                self.categories[category_name] = {
                    "priority": config.get("priority", "medium"),
                    "visit_frequency": config.get("visit_frequency", "normal"),
                    "delay_range": config.get("delay_range", {"min": 2, "max": 5}),
                    "human_simulation": config.get("human_simulation", True)
                }
                
                for url in config.get("urls", []):
                    if url.strip():  # Skip empty URLs
                        self.add_link(
                            url=url,
                            category=category_name,
                            priority=config.get("priority", "medium")
                        )
            
            self.save_links()
            self.logger.info(f"Initialized {len(self.links)} links from target_links.py")
        except ImportError:
            self.logger.warning("Could not import target_links.py")
    
    def add_link(self, url: str, category: str, priority: str = "medium", notes: str = "") -> bool:
        """Add a new link to the manager"""
        if url in self.links:
            self.logger.warning(f"Link already exists: {url}")
            return False
        
        link_info = LinkInfo(
            url=url,
            category=category,
            priority=priority,
            notes=notes,
            added_date=datetime.now().isoformat()
        )
        
        self.links[url] = link_info
        self.logger.info(f"Added link: {url} (Category: {category}, Priority: {priority})")
        return True
    
    def remove_link(self, url: str) -> bool:
        """Remove a link from the manager"""
        if url in self.links:
            del self.links[url]
            self.logger.info(f"Removed link: {url}")
            return True
        return False
    
    def update_link_stats(self, url: str, success: bool, load_time: float = 0.0):
        """Update link statistics after a visit"""
        if url not in self.links:
            return
        
        link = self.links[url]
        link.visit_count += 1
        link.last_visited = datetime.now().isoformat()
        
        if success:
            link.success_count += 1
            if load_time > 0:
                # Update average load time
                total_successful = link.success_count
                if total_successful == 1:
                    link.avg_load_time = load_time
                else:
                    link.avg_load_time = ((link.avg_load_time * (total_successful - 1)) + load_time) / total_successful
        else:
            link.failure_count += 1
            
            # Mark as failed if too many failures
            failure_rate = link.failure_count / link.visit_count
            if link.visit_count >= 3 and failure_rate >= 0.8:
                link.status = "failed"
                self.logger.warning(f"Marked link as failed due to high failure rate: {url}")
    
    def get_links_by_category(self, category: str, status: str = "active") -> List[LinkInfo]:
        """Get links from a specific category"""
        return [link for link in self.links.values() 
                if link.category == category and link.status == status]
    
    def get_links_by_priority(self, priority: str, status: str = "active") -> List[LinkInfo]:
        """Get links by priority level"""
        return [link for link in self.links.values() 
                if link.priority == priority and link.status == status]
    
    def get_due_links(self, category: str = None) -> List[LinkInfo]:
        """Get links that are due for visiting based on frequency"""
        due_links = []
        now = datetime.now()
        
        for link in self.links.values():
            if link.status != "active":
                continue
            
            if category and link.category != category:
                continue
            
            # Determine if link is due based on category frequency and last visit
            cat_config = self.categories.get(link.category, {})
            frequency = cat_config.get("visit_frequency", "normal")
            
            # Calculate next visit time based on frequency
            if not link.last_visited:
                due_links.append(link)
                continue
            
            last_visit = datetime.fromisoformat(link.last_visited)
            
            if frequency == "frequent":
                next_visit = last_visit + timedelta(hours=1)
            elif frequency == "normal":
                next_visit = last_visit + timedelta(hours=6)
            elif frequency == "rare":
                next_visit = last_visit + timedelta(hours=24)
            else:
                next_visit = last_visit + timedelta(hours=6)
            
            if now >= next_visit:
                due_links.append(link)
        
        return due_links
    
    def get_random_links(self, count: int, category: str = None, priority: str = None) -> List[LinkInfo]:
        """Get random links for visiting"""
        filtered_links = []
        
        for link in self.links.values():
            if link.status != "active":
                continue
            if category and link.category != category:
                continue
            if priority and link.priority != priority:
                continue
            filtered_links.append(link)
        
        # Shuffle and return requested count
        random.shuffle(filtered_links)
        return filtered_links[:count]
    
    def get_priority_sorted_links(self, category: str = None) -> List[LinkInfo]:
        """Get links sorted by priority (high -> medium -> low)"""
        priority_order = {"high": 3, "medium": 2, "low": 1}
        
        filtered_links = [link for link in self.links.values() 
                         if link.status == "active" and (not category or link.category == category)]
        
        return sorted(filtered_links, 
                     key=lambda x: (priority_order.get(x.priority, 0), random.random()), 
                     reverse=True)
    
    def get_smart_visit_list(self, category: str = None, max_links: int = 50) -> List[LinkInfo]:
        """Get a smart list of links to visit based on various factors"""
        # Start with due links
        visit_list = self.get_due_links(category)
        
        # Add high priority links that haven't been visited recently
        if len(visit_list) < max_links:
            high_priority = self.get_links_by_priority("high")
            for link in high_priority:
                if link not in visit_list and len(visit_list) < max_links:
                    if not link.last_visited or self._is_stale(link):
                        visit_list.append(link)
        
        # Fill with random links if needed
        if len(visit_list) < max_links:
            remaining_slots = max_links - len(visit_list)
            random_links = self.get_random_links(remaining_slots * 2, category)
            for link in random_links:
                if link not in visit_list and len(visit_list) < max_links:
                    visit_list.append(link)
        
        # Shuffle the final list for randomness
        random.shuffle(visit_list)
        return visit_list[:max_links]
    
    def _is_stale(self, link: LinkInfo, hours: int = 12) -> bool:
        """Check if a link hasn't been visited recently"""
        if not link.last_visited:
            return True
        
        last_visit = datetime.fromisoformat(link.last_visited)
        return datetime.now() - last_visit > timedelta(hours=hours)
    
    def save_links(self):
        """Save links to JSON file"""
        try:
            # Ensure directory exists
            self.links_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert LinkInfo objects to dict
            data = {
                "links": {url: asdict(link) for url, link in self.links.items()},
                "categories": self.categories,
                "metadata": {
                    "last_updated": datetime.now().isoformat(),
                    "total_links": len(self.links),
                    "active_links": len([l for l in self.links.values() if l.status == "active"])
                }
            }
            
            with open(self.links_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved {len(self.links)} links to {self.links_file}")
        except Exception as e:
            self.logger.error(f"Failed to save links: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about managed links"""
        stats = {
            "total_links": len(self.links),
            "active_links": 0,
            "failed_links": 0,
            "disabled_links": 0,
            "categories": {},
            "priority_breakdown": {"high": 0, "medium": 0, "low": 0},
            "visit_stats": {
                "total_visits": 0,
                "total_successes": 0,
                "total_failures": 0,
                "avg_success_rate": 0.0
            }
        }
        
        total_visits = 0
        total_successes = 0
        
        for link in self.links.values():
            # Status counts
            if link.status == "active":
                stats["active_links"] += 1
            elif link.status == "failed":
                stats["failed_links"] += 1
            elif link.status == "disabled":
                stats["disabled_links"] += 1
            
            # Category counts
            if link.category not in stats["categories"]:
                stats["categories"][link.category] = {"count": 0, "visits": 0, "successes": 0}
            stats["categories"][link.category]["count"] += 1
            stats["categories"][link.category]["visits"] += link.visit_count
            stats["categories"][link.category]["successes"] += link.success_count
            
            # Priority counts
            stats["priority_breakdown"][link.priority] += 1
            
            # Visit stats
            total_visits += link.visit_count
            total_successes += link.success_count
        
        stats["visit_stats"]["total_visits"] = total_visits
        stats["visit_stats"]["total_successes"] = total_successes
        stats["visit_stats"]["total_failures"] = total_visits - total_successes
        
        if total_visits > 0:
            stats["visit_stats"]["avg_success_rate"] = round((total_successes / total_visits) * 100, 2)
        
        return stats
    
    def cleanup_failed_links(self, min_failures: int = 5) -> int:
        """Remove links that have failed too many times"""
        removed_count = 0
        urls_to_remove = []
        
        for url, link in self.links.items():
            if link.failure_count >= min_failures and link.visit_count >= min_failures:
                failure_rate = link.failure_count / link.visit_count
                if failure_rate >= 0.8:  # 80% failure rate
                    urls_to_remove.append(url)
        
        for url in urls_to_remove:
            self.remove_link(url)
            removed_count += 1
        
        if removed_count > 0:
            self.save_links()
            self.logger.info(f"Cleaned up {removed_count} failed links")
        
        return removed_count

def main():
    """Example usage of the link manager"""
    manager = AdvancedLinkManager()
    
    print("Link Manager Statistics:")
    stats = manager.get_statistics()
    print(f"Total Links: {stats['total_links']}")
    print(f"Active Links: {stats['active_links']}")
    print(f"Categories: {list(stats['categories'].keys())}")
    
    print("\nCategory Breakdown:")
    for category, data in stats['categories'].items():
        print(f"  {category}: {data['count']} links, {data['visits']} visits, {data['successes']} successes")
    
    print(f"\nOverall Success Rate: {stats['visit_stats']['avg_success_rate']}%")

if __name__ == "__main__":
    main()