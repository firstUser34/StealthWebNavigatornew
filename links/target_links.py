#!/usr/bin/env python3
"""
Target Links Configuration File
Add your URLs here for the stealth bot to visit automatically
"""

# X/Twitter Links - High Priority Targets
X_LINKS = [
    # "https://x.com/Hitansh54/status/1930194500724334705",
    "https://x.com/Hitansh54/status/1931754193489957133",
    "https://x.com/Raj45307/status/1936455544069300299",
    # "https://x.com/AlCoinverse/status/1929125757801890030",
    # "https://x.com/Raj45307/status/1930202834756071790",
    # "https://x.com/Snax4ogs/status/1930201674355814471",
    # "https://x.com/sahil2dev/status/1930204847598428283",
    # "https://x.com/Rahul113383/status/1930205881255239751",
    # "https://x.com/AlCoinverse/status/1929512117993910469",
    # "https://x.com/CoinWipe42313/status/1930197012625969263",
]

# Website Links - Medium Priority
WEBSITE_LINKS = []

# API Testing Links - For verification
API_LINKS = []

# Social Media Links - Low Priority
SOCIAL_LINKS = [
    # Add your social media links here
]

# News and Content Links
NEWS_LINKS = [
    # Add news websites or content links here
]

# E-commerce Links
ECOMMERCE_LINKS = [
    # Add shopping or e-commerce links here
]

# Custom User Links - Add your own links here
CUSTOM_LINKS = [
    # Add any custom URLs you want to visit
]

# Configuration for different link categories
LINK_CATEGORIES = {
    "x_links": {
        "urls": X_LINKS,
        "priority": "high",
        "visit_frequency": "frequent",  # frequent, normal, rare
        "user_agent_rotation": True,
        "delay_range": {
            "min": 2,
            "max": 5
        },
        "human_simulation": True
    },
    "website_links": {
        "urls": WEBSITE_LINKS,
        "priority": "medium",
        "visit_frequency": "normal",
        "user_agent_rotation": True,
        "delay_range": {
            "min": 3,
            "max": 8
        },
        "human_simulation": True
    },
    "api_links": {
        "urls": API_LINKS,
        "priority": "low",
        "visit_frequency": "normal",
        "user_agent_rotation": True,
        "delay_range": {
            "min": 1,
            "max": 3
        },
        "human_simulation": False
    },
    "social_links": {
        "urls": SOCIAL_LINKS,
        "priority": "medium",
        "visit_frequency": "normal",
        "user_agent_rotation": True,
        "delay_range": {
            "min": 4,
            "max": 10
        },
        "human_simulation": True
    },
    "news_links": {
        "urls": NEWS_LINKS,
        "priority": "low",
        "visit_frequency": "rare",
        "user_agent_rotation": True,
        "delay_range": {
            "min": 5,
            "max": 12
        },
        "human_simulation": True
    },
    "ecommerce_links": {
        "urls": ECOMMERCE_LINKS,
        "priority": "medium",
        "visit_frequency": "normal",
        "user_agent_rotation": True,
        "delay_range": {
            "min": 6,
            "max": 15
        },
        "human_simulation": True
    },
    "custom_links": {
        "urls": CUSTOM_LINKS,
        "priority": "high",
        "visit_frequency": "frequent",
        "user_agent_rotation": True,
        "delay_range": {
            "min": 2,
            "max": 6
        },
        "human_simulation": True
    }
}

# Global settings for all categories
GLOBAL_SETTINGS = {
    "max_retries": 3,
    "timeout": 30,
    "verify_ssl": True,
    "follow_redirects": True,
    "save_screenshots": False,
    "log_level": "INFO"
}


def get_all_links():
    """Get all links from all categories"""
    all_links = []
    for category, config in LINK_CATEGORIES.items():
        all_links.extend(config["urls"])
    return all_links


def get_links_by_category(category_name):
    """Get links from a specific category"""
    return LINK_CATEGORIES.get(category_name, {}).get("urls", [])


def get_links_by_priority(priority_level):
    """Get links filtered by priority level"""
    links = []
    for category, config in LINK_CATEGORIES.items():
        if config["priority"] == priority_level:
            links.extend(config["urls"])
    return links


def get_high_priority_links():
    """Get only high priority links"""
    return get_links_by_priority("high")


def get_category_config(category_name):
    """Get configuration for a specific category"""
    return LINK_CATEGORIES.get(category_name, {})


# Example usage:
if __name__ == "__main__":
    print("Available link categories:")
    for category, config in LINK_CATEGORIES.items():
        print(
            f"- {category}: {len(config['urls'])} links (Priority: {config['priority']})"
        )

    print(f"\nTotal links: {len(get_all_links())}")
    print(f"High priority links: {len(get_high_priority_links())}")
