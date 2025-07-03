"""
GitHub Trending Scraper

A web scraper that tracks the top trending GitHub repositories daily.
Built for the Anansi Web Crawler Challenge by Hack Club.

Author: SkydioFlyer
License: MIT
"""

import os
import json
import logging
from datetime import datetime, timezone
from urllib import robotparser
import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup

# Configuration
USER_AGENT = 'Mozilla/5.0 (compatible; AnansiScraper/1.0; +https://anansi.hackclub.com/)'
TRENDING_URL = 'https://github.com/trending'
ROBOTS_URL = 'https://github.com/robots.txt'
TIMEOUT = 10
MAX_RETRIES = 3

# Setup logging
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def can_fetch(url, user_agent=USER_AGENT):
    """
    Check if scraping is allowed by robots.txt.
    
    Args:
        url (str): The URL to check
        user_agent (str): User agent string
        
    Returns:
        bool: True if scraping is allowed, False otherwise
    """
    try:
        rp = robotparser.RobotFileParser()
        rp.set_url(ROBOTS_URL)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        logging.warning(f"Could not check robots.txt: {e}")
        return True  # Default to allowing if robots.txt can't be read


def fetch_trending():
    """
    Fetch the GitHub trending page HTML.
    
    Returns:
        str: HTML content of the trending page
        
    Raises:
        requests.RequestException: If the request fails
    """
    headers = {'User-Agent': USER_AGENT}
    session = requests.Session()
    retries = Retry(
        total=MAX_RETRIES,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    logging.info(f"Fetching trending page from {TRENDING_URL}")
    response = session.get(TRENDING_URL, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    
    logging.info("Successfully fetched trending page")
    return response.text


def parse_trending(html):
    """
    Parse the GitHub trending page HTML to extract repository information.
    
    Args:
        html (str): HTML content of the trending page
        
    Returns:
        list: List of dictionaries containing repository information
    """
    soup = BeautifulSoup(html, 'html.parser')
    repo_list = []
    
    repositories = soup.select('article.Box-row')
    logging.info(f"Found {len(repositories)} repositories on trending page")
    
    for repo in repositories:
        try:
            # Extract repository name
            name_element = repo.h2.a
            name = name_element.get('href', '').strip('/') if name_element else ''
            
            # Extract description
            desc_element = repo.p
            desc = desc_element.text.strip() if desc_element else ''
            
            # Extract programming language
            lang_element = repo.find('span', itemprop='programmingLanguage')
            lang = lang_element.text.strip() if lang_element else ''
            
            # Extract star count
            stars_element = repo.find('a', href=lambda x: x and x.endswith('/stargazers'))
            stars = stars_element.text.strip().replace(',', '') if stars_element else '0'
            
            if name:  # Only add if we have a valid repository name
                repo_list.append({
                    'name': name,
                    'description': desc,
                    'language': lang,
                    'stars': stars
                })
                
        except Exception as e:
            logging.warning(f"Error parsing repository: {e}")
            continue
    
    logging.info(f"Successfully parsed {len(repo_list)} repositories")
    return repo_list


def save_data(data):
    """
    Save repository data to a JSON file organized by date.
    
    Args:
        data (list): List of repository dictionaries
        
    Returns:
        bool: True if data was saved, False if file already exists
    """
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    dir_path = os.path.join('data', today)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, 'trending.json')
    
    if os.path.exists(file_path):
        logging.info(f"File {file_path} already exists. Skipping save.")
        print(f"File {file_path} already exists. Skipping save.")
        return False
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logging.info(f'Successfully saved {len(data)} repositories to {file_path}')
        print(f'Successfully saved {len(data)} repositories to {file_path}')
        return True
        
    except Exception as e:
        logging.error(f"Error saving data to {file_path}: {e}")
        print(f"Error saving data: {e}")
        return False


def main():
    """
    Main function to orchestrate the scraping process.
    """
    logging.info("Starting GitHub trending scraper")
    print("Starting GitHub trending scraper...")
    
    try:
        # Check robots.txt compliance
        if not can_fetch(TRENDING_URL):
            logging.warning('Scraping not allowed by robots.txt')
            print('❌ Scraping not allowed by robots.txt')
            return
        
        logging.info("Robots.txt check passed")
        print("✅ Robots.txt check passed")
        
        # Fetch and parse trending page
        html = fetch_trending()
        trending_repos = parse_trending(html)
        
        if not trending_repos:
            logging.warning("No repositories found on trending page")
            print("⚠️  No repositories found on trending page")
            return
        
        # Save data
        saved = save_data(trending_repos)
        
        if saved:
            print(f'✅ Successfully scraped {len(trending_repos)} repositories.')
            logging.info(f"Scraping completed successfully. Found {len(trending_repos)} repositories.")
        else:
            print("ℹ️  Data already exists for today.")
            
    except requests.RequestException as e:
        error_msg = f'Network error: {e}'
        logging.error(error_msg)
        print(f'❌ {error_msg}')
        
    except Exception as e:
        error_msg = f'Unexpected error: {e}'
        logging.error(error_msg)
        print(f'❌ {error_msg}')
    
    finally:
        logging.info("Scraper finished")
        print("Scraper finished.")


if __name__ == '__main__':
    main()
