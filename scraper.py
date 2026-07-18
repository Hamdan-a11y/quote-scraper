"""
Quote Scraper - Portfolio Project for Upwork.

This script scrapes quotes, authors, and tags from https://quotes.toscrape.com
across all pages, respects scraping practices with request delays, handles errors
gracefully, and exports the data to a CSV file.
"""

import time
import logging
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set up logging for warnings and errors
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BASE_URL = "https://quotes.toscrape.com"


def get_next_page_url(soup: BeautifulSoup, base_url: str) -> Optional[str]:
    """
    Extracts the absolute URL of the next page from the parsed HTML.

    Args:
        soup: The parsed BeautifulSoup object of the current page.
        base_url: The base URL used to resolve relative paths.

    Returns:
        The absolute URL of the next page, or None if there is no next page.
    """
    try:
        next_button = soup.select_one("li.next a")
        if next_button and "href" in next_button.attrs:
            relative_url = next_button["href"]
            return urljoin(base_url, relative_url)
    except Exception as e:
        logger.warning("Error searching for next page button: %s", e)
    return None


def scrape_page(url: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Scrapes quote text, author, and tags from a single page.

    Args:
        url: The URL of the page to scrape.

    Returns:
        A tuple containing:
        - A list of dictionaries, each containing 'text', 'author', and 'tags' keys.
        - The absolute URL of the next page, or None if no next page is found.
    """
    quotes: List[Dict[str, Any]] = []
    
    headers = {
        "User-Agent": "QuoteScraperBot/1.0 (+https://github.com/yourusername/quote-scraper)"
    }
    
    try:
        # Wrap network call in a try-except block
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error("Failed to fetch page %s: %s", url, e)
        return quotes, None

    try:
        # Parse using the fast 'lxml' backend
        soup = BeautifulSoup(response.content, "lxml")
    except Exception as e:
        logger.error("Failed to parse HTML for page %s: %s", url, e)
        return quotes, None

    # Find all quote wrappers
    quote_elements = soup.select("div.quote")
    
    for idx, quote_el in enumerate(quote_elements, start=1):
        try:
            # Extract quote text
            text_el = quote_el.select_one("span.text")
            text = text_el.get_text(strip=True) if text_el else None
            
            # Extract author
            author_el = quote_el.select_one("small.author")
            author = author_el.get_text(strip=True) if author_el else None
            
            # Extract tags as a list of strings
            tag_els = quote_el.select("a.tag")
            tags = [tag.get_text(strip=True) for tag in tag_els]
            
            # Handle cases where expected data is missing
            if not text or not author:
                logger.warning(
                    "Missing expected element(s) in quote %d on page %s. "
                    "Text present: %s, Author present: %s",
                    idx, url, bool(text), bool(author)
                )
                continue
                
            quotes.append({
                "text": text,
                "author": author,
                "tags": tags
            })
            
        except Exception as e:
            logger.warning("Error parsing quote %d on page %s: %s", idx, url, e)
            continue
            
    # Extract the next page URL
    next_page_url = get_next_page_url(soup, BASE_URL)
    
    return quotes, next_page_url


def save_to_csv(quotes: List[Dict[str, Any]], filename: str) -> None:
    """
    Converts quote list to a pandas DataFrame and exports it to a CSV file.

    Args:
        quotes: A list of dictionaries representing quotes.
        filename: The path/name of the CSV file to write.
    """
    if not quotes:
        logger.warning("No quotes found to save.")
        return
        
    try:
        # Process tags list to comma-separated string for clean CSV representation
        processed_quotes = []
        for quote in quotes:
            processed_quote = quote.copy()
            # Convert tags list into a comma-separated string
            processed_quote["tags"] = ", ".join(quote["tags"])
            processed_quotes.append(processed_quote)
            
        df = pd.DataFrame(processed_quotes)
        
        # Reorder columns to be logical and clean
        df = df[["text", "author", "tags"]]
        
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        logger.info("Successfully exported %d quotes to %s", len(df), filename)
    except Exception as e:
        logger.error("Failed to save quotes to CSV file %s: %s", filename, e)


def main() -> None:
    """
    Main orchestrator for the scraping workflow.
    """
    print("Starting Quote Scraper...")
    all_quotes: List[Dict[str, Any]] = []
    current_url: Optional[str] = BASE_URL
    page_number = 1
    
    while current_url:
        quotes, next_url = scrape_page(current_url)
        print(f"Scraping page {page_number}... found {len(quotes)} quotes")
        
        all_quotes.extend(quotes)
        
        current_url = next_url
        if current_url:
            page_number += 1
            # Respectful scraping practice: add a 1-second delay between requests
            time.sleep(1.0)
            
    print(f"Scraping completed. Scraped {len(all_quotes)} quotes in total.")
    save_to_csv(all_quotes, "quotes.csv")


if __name__ == "__main__":
    main()
