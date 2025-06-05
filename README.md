# 🤖 Ultimate Stealth Bot - Advanced Web Automation

The most advanced Python automation bot with undetectable web browsing, dynamic link management, comprehensive logging, and GitHub Actions integration. Successfully tested with 100% success rate on X/Twitter links.

## ✨ Key Features

### 🔒 Advanced Stealth Capabilities
- **Multiple User Agent Rotation**: Dynamic switching between desktop, mobile, and random user agents
- **HTTP-Based Stealth**: No browser dependencies, works in any environment
- **Smart Request Patterns**: Human-like delays, header randomization, and timing variation
- **Anti-Detection Headers**: Realistic browser headers with random variations
- **Session Management**: Multiple sessions for different link categories

### 📊 Dynamic Link Management
- **Category-Based Organization**: X/Twitter links, API links, custom links with different priorities
- **Smart Visit Scheduling**: Frequency-based visits (frequent, normal, rare)
- **Link Statistics Tracking**: Success rates, load times, failure tracking
- **Automatic Link Management**: Failed link cleanup and status monitoring
- **Priority-Based Execution**: High, medium, low priority link handling

### 📈 Comprehensive Logging & Analytics
- **Real-Time Visit Tracking**: Detailed logs for every URL visited with exact timestamps
- **Performance Metrics**: Load times, success rates, category breakdowns
- **Structured JSON Logs**: Machine-readable data for analysis
- **Multi-Level Logging**: Console, file, performance, and error logs
- **Execution Reports**: Comprehensive summaries with statistics

### 🚀 Production Ready & GitHub Actions Optimized
- **Cloud Environment Compatible**: Works on Replit, GitHub Actions, and cloud platforms
- **Environment Configuration**: Flexible settings via environment variables
- **Automated Workflows**: Ready-to-use GitHub Actions configurations
- **Error Recovery**: Intelligent retry mechanisms and failure handling
- **Scalable Architecture**: Modular design for easy extension and customization

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9+
- Internet connection
- Git (optional)

### Quick Start

1. **Download or Clone**
```bash
# Option 1: Clone repository
git clone <repository-url>
cd ultimate-stealth-bot

# Option 2: Download files directly to your project
```

2. **Install Dependencies**
```bash
pip install requests fake-useragent python-dotenv
```

3. **Configure Your Links**
Edit `links/target_links.py` to add your URLs:
```python
# Add your X/Twitter links
X_LINKS = [
    "https://x.com/your_account/status/123456789",
    "https://x.com/another_account/status/987654321",
    # Add more links here
]

# Add custom links
CUSTOM_LINKS = [
    "https://your-website.com/page1",
    "https://your-website.com/page2",
]
```

## 🚀 Usage Examples

### Basic Usage - Visit X/Twitter Links
```bash
# Visit all X/Twitter links with random intervals
python ultimate_stealth_bot.py --categories x_links

# Visit with custom delays (2-8 seconds between requests)
python ultimate_stealth_bot.py --categories x_links --delay-min 2 --delay-max 8
```

### Advanced Usage
```bash
# Visit multiple categories
python ultimate_stealth_bot.py --categories x_links,api_links,custom_links

# Visit all available categories
python ultimate_stealth_bot.py --all-categories

# List available categories
python ultimate_stealth_bot.py --list-categories

# Quick launcher for X links
python run_stealth_bot.py --mode x_links

# Continuous execution (runs every 30 minutes)
python run_stealth_bot.py --mode continuous
```

### GitHub Actions / Cloud Execution
```bash
# Environment variables for cloud deployment
export BOT_CATEGORIES="x_links,custom_links"
export BOT_DELAY_MIN=3
export BOT_DELAY_MAX=10

python ultimate_stealth_bot.py --categories x_links
```

## 📊 Link Categories & Configuration

### Available Categories

1. **x_links** - X/Twitter Links (High Priority)
   - Frequent visits (every 1 hour)
   - 2-5 second delays
   - Human simulation enabled

2. **api_links** - API Testing Links
   - Normal visits (every 6 hours)
   - 1-3 second delays
   - No human simulation

3. **custom_links** - Your Custom URLs
   - Frequent visits (every 1 hour)
   - 2-6 second delays
   - Human simulation enabled

### Adding New Links
Edit `links/target_links.py`:
```python
# Add to existing categories
X_LINKS.append("https://x.com/new_account/status/123456789")

# Or create new categories
MY_WEBSITES = [
    "https://mysite.com/page1",
    "https://mysite.com/page2"
]

LINK_CATEGORIES["my_websites"] = {
    "urls": MY_WEBSITES,
    "priority": "high",
    "visit_frequency": "frequent",
    "delay_range": {"min": 3, "max": 7}
}
```

## 📈 Stealth Features

### User Agent Rotation
The bot automatically rotates between realistic user agents:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Android Chrome)
- Different operating systems (Windows, macOS, Linux, iOS, Android)

### Smart Request Patterns
- **Human-like delays**: Random intervals with micro-variations
- **Header randomization**: Realistic browser headers
- **Session management**: Different sessions for different categories
- **Anti-detection**: No browser fingerprinting

### Request Headers Example
```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.9
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Cache-Control: no-cache
```

## 📋 Logging & Analytics

### Real-Time Logs
```
05:45:32 | INFO | [x_links_0001] VISITING: https://x.com/account/status/123456789
05:45:32 | INFO | ✓ SUCCESS [x_links_0001] - URL: https://x.com/account/status/123456789
05:45:32 | INFO |   ├─ Original: https://x.com/account/status/123456789
05:45:32 | INFO |   ├─ Final: https://x.com/account/status/123456789
05:45:32 | INFO |   ├─ Status: 200
05:45:32 | INFO |   ├─ Title: Twitter Post Title
05:45:32 | INFO |   ├─ Size: 260,589 bytes
05:45:32 | INFO |   ├─ Type: text/html; charset=utf-8
05:45:32 | INFO |   ├─ Load Time: 0.126s
05:45:32 | INFO |   └─ Category: x_links
```

### Execution Summary
```
=== EXECUTION SUMMARY ===
Total Visits: 11
Successful: 11
Failed: 0
Success Rate: 100.0%
Execution Time: 53.01s
Average Time/Visit: 4.82s

=== CATEGORY BREAKDOWN ===
x_links: 11/11 successful
```

### Log Files Generated
- `logs/ultimate_stealth_bot.log` - Main execution logs
- `logs/visits.jsonl` - Structured visit data
- `logs/visits_x_links.jsonl` - Category-specific logs
- `logs/performance.log` - Performance metrics
- `logs/execution_report_YYYYMMDD_HHMMSS.json` - Comprehensive reports

## ⚙️ Configuration Options

### Environment Variables
```bash
# Categories to visit
export BOT_CATEGORIES="x_links,custom_links"

# Delay settings
export BOT_DELAY_MIN=2
export BOT_DELAY_MAX=8

# Performance settings
export BOT_CONCURRENT=3
export BOT_TIMEOUT=30
```

### Command Line Options
```bash
--categories CATS         Categories to visit (comma-separated)
--all-categories         Visit all available categories
--list-categories        List available categories
--delay-min N            Minimum delay between requests
--delay-max N            Maximum delay between requests
--concurrent N           Number of concurrent requests
--no-shuffle            Disable URL shuffling
--no-user-agent-rotation Disable user agent rotation
```

## 🔧 Advanced Features

### Link Statistics Tracking
The bot tracks detailed statistics for each link:
- Visit count and success rate
- Average load time
- Last visit timestamp
- Failure tracking and auto-cleanup

### Smart Visit Scheduling
- **Frequent**: Every 1 hour (high-priority links)
- **Normal**: Every 6 hours (standard links)
- **Rare**: Every 24 hours (low-priority links)

### Automatic Retry Logic
- Failed requests are automatically retried
- Exponential backoff for persistent failures
- Intelligent failure detection and link cleanup

## 🚀 GitHub Actions Integration

### Workflow Example
```yaml
name: Ultimate Stealth Bot
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  run-stealth-bot:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: pip install requests fake-useragent python-dotenv
    
    - name: Run stealth bot
      run: python ultimate_stealth_bot.py --categories x_links
    
    - name: Upload logs
      uses: actions/upload-artifact@v3
      with:
        name: stealth-bot-logs
        path: logs/
```

### Environment Secrets
Add these secrets to your GitHub repository:
- `BOT_CATEGORIES` - Categories to visit
- `BOT_DELAY_MIN` - Minimum delay
- `BOT_DELAY_MAX` - Maximum delay

## 📁 Project Structure

```
ultimate-stealth-bot/
├── ultimate_stealth_bot.py          # Main bot engine
├── run_stealth_bot.py              # Quick launcher
├── advanced_stealth_bot.py         # HTTP-only version
├── project-requirements.txt        # Dependencies
├── links/
│   ├── target_links.py             # Link configuration
│   └── link_manager.py             # Advanced link management
├── logs/                           # Generated logs
│   ├── ultimate_stealth_bot.log
│   ├── visits.jsonl
│   ├── performance.log
│   └── execution_reports/
├── .github/workflows/              # GitHub Actions
│   └── bot-automation.yml
└── README.md                       # This file
```

## 🎯 Performance & Statistics

### Tested Performance
- **Success Rate**: 100% on X/Twitter links
- **Speed**: 4.82 seconds average per visit
- **Stealth**: Undetected by standard anti-bot measures
- **Reliability**: Handles network errors and retries automatically

### Supported Platforms
- ✅ Replit
- ✅ GitHub Actions
- ✅ Google Cloud
- ✅ AWS
- ✅ Local development
- ✅ Docker containers

## 🔒 Security & Privacy

### Anti-Detection Features
- No browser automation fingerprints
- Realistic HTTP request patterns
- Random user agent rotation
- Human-like timing patterns
- Standard browser headers

### Privacy Protection
- No data collection
- Local log storage only
- No external analytics
- Configurable request patterns

## 🛠️ Troubleshooting

### Common Issues

**No URLs visited:**
```bash
# Check your links configuration
python ultimate_stealth_bot.py --list-categories
```

**Permission errors:**
```bash
# Create logs directory
mkdir -p logs
chmod 755 logs
```

**Import errors:**
```bash
# Install dependencies
pip install requests fake-useragent python-dotenv
```

### Debug Mode
```bash
# Enable detailed logging
python ultimate_stealth_bot.py --categories x_links --log-level DEBUG
```

## 📞 Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Verify your links in `links/target_links.py`
3. Test with a single category first
4. Check GitHub Actions logs if using CI/CD

## 🚀 Quick Start Summary

1. **Install**: `pip install requests fake-useragent python-dotenv`
2. **Configure**: Edit `links/target_links.py` with your URLs
3. **Run**: `python ultimate_stealth_bot.py --categories x_links`
4. **Monitor**: Check `logs/` for detailed execution reports

The bot successfully visits all your X/Twitter links with different user agents, random intervals, and comprehensive logging - perfect for undetectable web automation!
