# Chat with URLs - Setup Guide

This guide will help you set up and run the Streamlit app that scrapes web content using `crawl4ai`, processes it with `ollama`, and allows interactive Q&A.

## Repository
GitHub Repository: [Chat with URLs](https://github.com/omkumar40/chat-with-url)

## Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Git (optional but recommended)

## Step 1: Clone the Repository
Clone the repository and navigate into the project folder:
```sh
git clone https://github.com/omkumar40/chat-with-url.git
cd chat-with-url
```

## Step 2: Install Dependencies
Install the required Python packages from `requirements.txt`:
```sh
pip install -r requirements.txt
```

## Step 3: Set Up Playwright
Playwright is required for `crawl4ai`. Install and set it up with:
```sh
playwright install
```
This installs the necessary browser drivers for web scraping.

## Step 4: Install and Run Ollama
Ollama is required for processing chat requests using the `llama3.2` model.

### Install Ollama
Download and install Ollama from the official website:
- **Windows/macOS/Linux:** [https://ollama.ai/download](https://ollama.ai/download)

### Run Ollama
Once installed, start the Ollama service:
```sh
ollama run llama3.2
```
This downloads and runs the `llama3.2` model if not already installed.

## Step 5: Run the Streamlit App
Start the Streamlit application with:
```sh
streamlit run app.py
```
This will launch the web UI, allowing you to enter URLs, process content, and ask questions based on the scraped data.

## How Crawl4AI is Used for Scraping
This project uses `crawl4ai` to scrape and extract content from web pages asynchronously. The scraping process works as follows:
1. The user enters a list of URLs.
2. `crawl4ai` asynchronously fetches the webpage content using Playwright.
3. The extracted content is summarized to a 4000-character limit to keep responses concise.
4. This processed content is stored in `st.session_state` for further analysis using Ollama.

The function responsible for scraping in `app.py` is:
```python
async def scrape_urls(urls):
    """Scrape content from multiple URLs asynchronously using Crawl4AI"""
    contexts = []
    async with AsyncWebCrawler() as crawler:
        tasks = [crawler.arun(url=url) for url in urls]
        results = await asyncio.gather(*tasks)
        for url, result in zip(urls, results):
            if result:
                contexts.append({
                    "url": url,
                    "content": textwrap.shorten(result.markdown, width=4000, placeholder="...")
                })
    return contexts
```
This ensures efficient and fast content retrieval from multiple web pages.

## Troubleshooting
- If `ollama` is not found, ensure it is correctly installed and added to your system's PATH.
- If Playwright scraping fails, try reinstalling Playwright browsers:
  ```sh
  playwright install
  ```
- If you encounter `ModuleNotFoundError`, ensure dependencies are installed with:
  ```sh
  pip install -r requirements.txt
  ```

## Additional Notes
- The `ollama` model runs locally, ensuring privacy and efficiency.
- `crawl4ai` uses Playwright to extract content from web pages effectively.
- Streamlit provides a simple UI for interactive Q&A based on the scraped content.

Now, you're all set! 🚀 Open the Streamlit app and start chatting with URLs.

