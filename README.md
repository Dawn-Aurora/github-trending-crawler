# GitHub Trending Scraper

A Python web scraper that tracks the top trending GitHub repositories daily. Built for the [Anansi Web Crawler Challenge](https://anansi.hackclub.com/) by Hack Club.

## Purpose
This scraper monitors GitHub's trending repositories to identify popular open-source projects and emerging technologies in the developer community.

## Features
-  **Web Scraping**: Crawls https://github.com/trending and parses HTML (no GitHub API used)
-  **Structured Storage**: Organizes data in `data/YYYY-MM-DD/trending.json` format
-  **Ethical Scraping**: Respects robots.txt and uses proper user-agent identification
-  **Error Handling**: Comprehensive logging and retry mechanisms
-  **Clean Data**: Extracts repository name, description, language, and star count
-  **Easy to Use**: Simple setup and execution

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/github-trending-scraper.git
   cd github-trending-scraper
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the scraper:**
   ```bash
   python scraper.py
   ```

The scraper will create a `data/` directory and save today's trending repositories in `data/YYYY-MM-DD/trending.json`.

## 📁 Project Structure
```
github-trending-scraper/
├── data/                    # Scraped data storage
│   └── YYYY-MM-DD/          # Daily data folders
│       └── trending.json    # Daily trending repositories
├── scraper.py               # Main scraper script
├── test_scraper.py          # Unit tests
├── requirements.txt         # Python dependencies
├── example-trending.json    # Sample output format
├── scraper.log              # Application logs (generated)
├── LICENSE                  # MIT License
└── README.md                # This file
```

## Configuration

The scraper includes several configurable options in `scraper.py`:

- **USER_AGENT**: Custom user agent identifying the scraper
- **RETRY_SETTINGS**: Automatic retry on network failures
- **TIMEOUT**: Request timeout (10 seconds)
- **LOG_LEVEL**: Logging configuration

## Sample Output

Each repository entry contains:

```json
[
  {
    "name": "torvalds/linux",
    "description": "Linux kernel source tree",
    "language": "C",
    "stars": "160000"
  },
  {
    "name": "microsoft/vscode",
    "description": "Visual Studio Code",
    "language": "TypeScript",
    "stars": "120000"
  }
]
```

## Automation

Schedule the scraper to run daily:

**Windows (Task Scheduler):**
```cmd
# Run daily at 9 AM
schtasks /create /sc daily /tn "GitHub Trending Scraper" /tr "python C:\path\to\scraper.py" /st 09:00
```

**Linux/Mac (Cron):**
```bash
# Add to crontab (runs daily at 9 AM)
0 9 * * * cd /path/to/github-trending-scraper && python scraper.py
```

## Testing

Run the unit tests to verify functionality:

```bash
python test_scraper.py
```

## Features Details

- **Robots.txt Compliance**: Checks GitHub's robots.txt before scraping
- **Rate Limiting**: Implements respectful delays and retry logic
- **Duplicate Prevention**: Skips scraping if data already exists for the current date
- **Error Logging**: Comprehensive logging to `scraper.log`
- **Unicode Support**: Handles international characters in repository descriptions

## Ethical Considerations

This scraper follows web scraping best practices:
- Respects robots.txt directives
- Uses appropriate user-agent identification
- Implements rate limiting to avoid overwhelming servers
- Only scrapes publicly available data
- Does not use GitHub's API to avoid rate limits

## Use Cases

- **Trend Analysis**: Track popular technologies and programming languages
- **Market Research**: Identify emerging tools and frameworks
- **Data Science**: Analyze GitHub ecosystem trends over time
- **Developer Insights**: Monitor what the developer community is building

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for the [Anansi Web Crawler Challenge](https://anansi.hackclub.com/) by Hack Club
- Thanks to the open-source community for the tools and libraries used
