import sys
if sys.platform.startswith("win"):
    from crawl4ai.utils import configure_windows_event_loop
    configure_windows_event_loop()


import streamlit as st
import asyncio
from crawl4ai import AsyncWebCrawler
from ollama import chat, ChatResponse
import textwrap

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

async def generate_answer(question, context):
    """Generate answer using Ollama's chat model with context"""
    response: ChatResponse = chat(
        model='llama3.2',
        messages=[
            {"role": "system", "content": "You are a helpful AI that answers questions based on provided link's context."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
    )
    return response.message.content

# Streamlit UI
st.title("Chat with URLs")
st.write("Enter URLs and ask questions based on their content")

if "url_disabled" not in st.session_state:
    st.session_state["url_disabled"] = False

# Initialize session state
if "contexts" not in st.session_state:
    st.session_state["contexts"] = []

# If there are contexts (URLs have been processed), disable the text area
url_input_disabled = bool(st.session_state["contexts"]) or st.session_state["url_disabled"]

# URL input
urls = st.text_area("Enter URLs (one per line)",disabled=url_input_disabled).split('\n')

if st.button("Reset URL"):
    st.session_state["contexts"] = []
    st.session_state["url_disabled"] = False
    st.success("Previous URLs cleared. You can now edit the URL box again.")
    st.rerun()




def process_urls():
    if urls:
        with st.spinner("Scraping content..."):
            try:
                st.session_state["contexts"] = asyncio.run(scrape_urls(urls))
            except Exception as e:
                st.error(f"Error during scraping: {e}")
                # Optionally clear session state if necessary
                st.session_state["contexts"] = []
        st.success(f"Processed {len(st.session_state['contexts'])} URLs")
    else:
        st.warning("Please enter at least one URL")



# Process URLs button (only enabled if the text area is not disabled)
if not url_input_disabled and st.button("Process URLs"):

    process_urls()
    # Optionally, you can also set a flag to disable further URL editing
    st.session_state["url_disabled"] = True

# Question input
question = st.text_input("Ask a question about the content")

def process_question():
    if question and st.session_state["contexts"]:
        with st.spinner("Generating answer..."):
            combined_context = "\n\n".join(
                [f"URL: {c['url']}\nContent: {c['content']}" for c in st.session_state["contexts"]]
            )
            answer = asyncio.run(generate_answer(question, combined_context))
            st.subheader("Answer")
            st.write(answer)
        st.subheader("Scraped Context References")
        for c in st.session_state["contexts"]:
            st.write(f"- {c['url']}")

if st.button("Get Answer"):
    process_question()
