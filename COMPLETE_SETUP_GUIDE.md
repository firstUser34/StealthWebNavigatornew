# 🤖 Complete Stealth Bot System - Setup Guide

This project provides three advanced stealth bot systems for visiting your X/Twitter links with different user agents and random intervals.

## 🎯 Available Bot Systems

### 1. Ultimate Stealth Bot (HTTP-Based) ⭐ RECOMMENDED
- **Status**: ✅ Working perfectly (100% success rate)
- **Technology**: Pure HTTP requests (no browser needed)
- **File**: `ultimate_stealth_bot.py`
- **Advantages**: Fastest, most reliable, works everywhere

### 2. Multi-Browser Stealth Bot (Selenium)
- **Status**: ✅ Working with Firefox
- **Technology**: Selenium WebDriver (Firefox/Edge/Chrome)
- **File**: `multi_browser_stealth_bot.py`  
- **Advantages**: Full browser automation, JavaScript execution

### 3. Legacy Chrome Bot
- **Status**: ❌ Removed (Chrome driver issues in cloud)
- **Reason**: ChromeDriver compatibility problems

## 🚀 Quick Start (Recommended)

### Option 1: Ultimate Stealth Bot (HTTP)
```bash
# Install dependencies
pip install requests fake-useragent python-dotenv

# Visit your X/Twitter links
python ultimate_stealth_bot.py --categories x_links

# Continuous execution
python run_stealth_bot.py --mode continuous
```

### Option 2: Multi-Browser Bot (Selenium)
```bash
# Install additional Selenium dependency
pip install selenium

# Visit with Firefox
python multi_browser_stealth_bot.py --categories x_links --browser firefox
```

## 📊 Your X/Twitter Links Configuration

Your links are configured in `links/target_links.py`:

```python
X_LINKS = [
    "https://x.com/Hitansh54/status/1930194500724334705",
    "https://x.com/ArjunMehra985/status/1930199659798032610",
    "https://x.com/sahil_gopanii/status/1930207213521412417",
    "https://x.com/AlCoinverse/status/1929125757801890030",
    "https://x.com/Raj45307/status/1930202834756071790",
    "https://x.com/Snax4ogs/status/1930201674355814471",
    "https://x.com/sahil2dev/status/1930204847598428283",
    "https://x.com/Rahul113383/status/1930205881255239751",
    "https://x.com/AlCoinverse/status/1929512117993910469",
    "https://x.com/CoinWipe42313/status/1930197012625969263",
    "https://x.com/ArjunMehra985/status/1930284895202377904"
]
```

## 📈 Performance Results

**Latest Ultimate Stealth Bot execution:**
- Total Visits: 11 X/Twitter links
- Success Rate: 100%
- Execution Time: 63.91 seconds
- Average Time per Visit: 5.81 seconds
- Different user agents for each visit
- Random delays between requests

## 🔧 Advanced Usage

### Environment Variables
```bash
export BOT_CATEGORIES="x_links"
export BOT_DELAY_MIN=2
export BOT_DELAY_MAX=8
```

### Command Line Options
```bash
# Ultimate Stealth Bot
python ultimate_stealth_bot.py --categories x_links,custom_links --delay-min 3 --delay-max 7

# Multi-Browser Bot
python multi_browser_stealth_bot.py --categories x_links --browser firefox --headless

# Quick Launcher
python run_stealth_bot.py --mode x_links
python run_stealth_bot.py --mode continuous
```

### Adding More Links
Edit `links/target_links.py`:
```python
# Add to X_LINKS
X_LINKS.append("https://x.com/new_account/status/123456789")

# Or create custom category
CUSTOM_LINKS = [
    "https://your-website.com/page1",
    "https://your-website.com/page2"
]
```

## 📋 Stealth Features

### User Agent Rotation
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Android Chrome)
- Different operating systems
- Realistic browser headers

### Anti-Detection
- No browser fingerprinting
- Human-like timing patterns
- Random delays with micro-variations
- Realistic HTTP request patterns

### Smart Request Patterns
- 2-5 second delays between X/Twitter links
- Random header variations
- Session management
- Automatic retry logic

## 📊 Logging & Monitoring

### Log Files
- `logs/ultimate_stealth_bot.log` - Main execution logs
- `logs/visits.jsonl` - Structured visit data
- `logs/performance.log` - Performance metrics
- `logs/execution_report_*.json` - Comprehensive reports

### Real-Time Logs Example
```
05:53:00 | INFO | [x_links_0001] VISITING: https://x.com/Hitansh54/status/1930194500724334705
05:53:00 | INFO | ✓ SUCCESS [x_links_0001] - URL: https://x.com/Hitansh54/status/1930194500724334705
05:53:00 | INFO |   ├─ Original: https://x.com/Hitansh54/status/1930194500724334705
05:53:00 | INFO |   ├─ Final: https://x.com/Hitansh54/status/1930194500724334705
05:53:00 | INFO |   ├─ Status: 200
05:53:00 | INFO |   ├─ Load Time: 0.156s
05:53:00 | INFO |   └─ Category: x_links
```

## 🌐 GitHub Actions Integration

### Automated Workflow
```yaml
name: Ultimate Stealth Bot
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  run-bot:
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
```

## 🛠️ Troubleshooting

### Issue: No URLs visited
```bash
# Check configuration
python ultimate_stealth_bot.py --list-categories
```

### Issue: Import errors
```bash
# Install dependencies
pip install requests fake-useragent python-dotenv selenium
```

### Issue: Permission errors
```bash
# Create logs directory
mkdir -p logs
chmod 755 logs
```

## 📁 Project Structure

```
stealth-bot-system/
├── ultimate_stealth_bot.py         # HTTP-based bot (recommended)
├── multi_browser_stealth_bot.py    # Selenium-based bot
├── run_stealth_bot.py              # Quick launcher
├── project-requirements.txt        # Dependencies
├── links/
│   ├── target_links.py             # Your X/Twitter links
│   └── link_manager.py             # Advanced link management
├── logs/                           # Generated logs
│   ├── ultimate_stealth_bot.log
│   ├── visits.jsonl
│   └── execution_reports/
├── .github/workflows/              # GitHub Actions
│   └── bot-automation.yml
└── README.md                       # Documentation
```

## ✅ Recommended Usage

1. **For maximum reliability**: Use `ultimate_stealth_bot.py`
2. **For browser automation**: Use `multi_browser_stealth_bot.py`
3. **For continuous operation**: Use `run_stealth_bot.py --mode continuous`
4. **For cloud deployment**: Use GitHub Actions with Ultimate Stealth Bot

## 🔒 Security Features

- No data collection
- Local log storage only
- Configurable request patterns
- Anti-detection mechanisms
- Realistic browser simulation

Your stealth bot system is ready to visit all X/Twitter links with different user agents and random intervals while maintaining comprehensive logging of each URL visited.