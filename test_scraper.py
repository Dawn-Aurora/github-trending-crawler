"""
Unit tests for the GitHub Trending Scraper.

Tests the HTML parsing functionality to ensure correct data extraction.
"""

import unittest
from scraper import parse_trending

# Sample HTML matching GitHub's trending page structure
SAMPLE_HTML = '''
<html><body>
<article class="Box-row">
  <h2><a href="/torvalds/linux">torvalds/linux</a></h2>
  <p>Linux kernel source tree</p>
  <span itemprop="programmingLanguage">C</span>
  <a href="/torvalds/linux/stargazers">160,000</a>
</article>
<article class="Box-row">
  <h2><a href="/microsoft/vscode">microsoft/vscode</a></h2>
  <p>Visual Studio Code</p>
  <span itemprop="programmingLanguage">TypeScript</span>
  <a href="/microsoft/vscode/stargazers">120,000</a>
</article>
<article class="Box-row">
  <h2><a href="/example/no-language">example/no-language</a></h2>
  <p>Repository with no language specified</p>
  <a href="/example/no-language/stargazers">1,234</a>
</article>
</body></html>
'''


class TestParseTrending(unittest.TestCase):
    """Test cases for the parse_trending function."""
    
    def test_parse_trending_basic(self):
        """Test basic parsing functionality."""
        repos = parse_trending(SAMPLE_HTML)
        
        # Should find 3 repositories
        self.assertEqual(len(repos), 3)
        
        # Test first repository
        self.assertEqual(repos[0]['name'], 'torvalds/linux')
        self.assertEqual(repos[0]['description'], 'Linux kernel source tree')
        self.assertEqual(repos[0]['language'], 'C')
        self.assertEqual(repos[0]['stars'], '160000')  # Commas should be removed
        
        # Test second repository
        self.assertEqual(repos[1]['name'], 'microsoft/vscode')
        self.assertEqual(repos[1]['description'], 'Visual Studio Code')
        self.assertEqual(repos[1]['language'], 'TypeScript')
        self.assertEqual(repos[1]['stars'], '120000')
        
        # Test third repository (no language)
        self.assertEqual(repos[2]['name'], 'example/no-language')
        self.assertEqual(repos[2]['description'], 'Repository with no language specified')
        self.assertEqual(repos[2]['language'], '')  # Should be empty string
        self.assertEqual(repos[2]['stars'], '1234')
    
    def test_parse_trending_empty_html(self):
        """Test parsing with empty HTML."""
        repos = parse_trending('<html><body></body></html>')
        self.assertEqual(len(repos), 0)
    
    def test_parse_trending_malformed_html(self):
        """Test parsing with malformed HTML."""
        malformed_html = '''
        <html><body>
        <article class="Box-row">
          <h2><a href="/incomplete/repo">incomplete/repo</a></h2>
          <!-- Missing description and other elements -->
        </article>
        </body></html>
        '''
        repos = parse_trending(malformed_html)
        
        # Should still parse what it can
        self.assertEqual(len(repos), 1)
        self.assertEqual(repos[0]['name'], 'incomplete/repo')
        self.assertEqual(repos[0]['description'], '')
        self.assertEqual(repos[0]['language'], '')
        self.assertEqual(repos[0]['stars'], '0')


if __name__ == '__main__':
    print("Running GitHub Trending Scraper tests...")
    unittest.main(verbosity=2)
