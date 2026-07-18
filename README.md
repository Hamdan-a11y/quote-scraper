# Quote Scraper - Portfolio Project

A robust, respectful, and fully documented Python web scraper designed to extract and compile quotes from paginated web resources. This project is built as a demonstrative portfolio piece showcasing clean code structure, production-grade error handling, and web scraping best practices.

## Project Overview

This project automatically browses the quote repository website [Quotes to Scrape](https://quotes.toscrape.com), navigating through all pages of quotes by programmatically following the "Next" page button. It extracts:
- **Quote Text**: The exact text of the quote.
- **Author Name**: The author's name.
- **Tags**: Relevant keywords categorizing the quote.

The scraper operates respectfully by introducing request delays to prevent server overload and exports all gathered data into a clean, structured CSV file (`quotes.csv`) that can be immediately opened in Excel, Google Sheets, or loaded into data analysis pipelines.

## Tech Stack & Libraries Used

- **Python 3.13+**: The programming language for clean scripting.
- **Requests**: For making reliable HTTP network requests.
- **BeautifulSoup4 & lxml**: For parsing the fetched HTML structure efficiently and extracting target content using CSS selectors.
- **Pandas**: For organizing the scraped data into structured tables (DataFrames) and exporting to CSV.

## Key Skills Demonstrated

- **Robust Web Scraping**: Target element extraction using CSS selectors with fallback safety.
- **Dynamic Pagination Handling**: Following pagination links dynamically until no further pages exist.
- **Respectful Crawling Practices**: Using rate-limiting/delays (`time.sleep`) and professional User-Agent headers to protect source server health.
- **Comprehensive Error Handling**: Wrapping network requests and extraction blocks in structured exceptions to prevent crashes on network hiccups or structural site changes.
- **Data Export & Structuring**: Converting unstructured web text into a clean relational CSV table.
- **Modern Python Standards**: Utilizing PEP8 styling, full type hinting, and clear function documentation (Docstrings).

## Setup & Installation

### Prerequisites
- Python 3.13 or newer installed on your machine.

### Installation Steps

1. **Clone or download** this repository.
2. **Open a terminal** in the project directory.
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```
4. **Activate the virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD)**:
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   - **macOS / Linux**:
     ```bash
     source venv/bin/activate
     ```
5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Scraper

Once the environment is active and dependencies are installed, run the scraper script:
```bash
python scraper.py
```

### Script Execution Logs Example
When running, you should see console logs reporting the scraper's real-time progress:
```text
Starting Quote Scraper...
Scraping page 1... found 10 quotes
Scraping page 2... found 10 quotes
...
Scraping page 10... found 10 quotes
Scraping completed. Scraped 100 quotes in total.
2026-07-18 16:10:59,757 - INFO - Successfully exported 100 quotes to quotes.csv
```

## Sample Output Format

The output is written to `quotes.csv` in the root folder. Here is a preview of the structured data:

| text | author | tags |
|---|---|---|
| “The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.” | Albert Einstein | change, deep-thoughts, thinking, world |
| “It is our choices, Harry, that show what we truly are, far more than our abilities.” | J.K. Rowling | abilities, choices |
| “There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.” | Albert Einstein | inspirational, life, live, miracle, miracles |
| “The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.” | Jane Austen | aliteracy, books, classic, humor |
