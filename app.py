# app.py

import streamlit as st
import os
from dotenv import load_dotenv
import requests
# UPDATED: Import Config from newspaper
from newspaper import Article, ArticleException, Config

# --- RAG-specific imports ---
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
# --- End RAG-specific imports ---

from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# --- Functions ---

@st.cache_data
def fetch_news_articles(api_key, company_name, num_articles=20): # INCREASED to 20
    """Fetches news articles for a given company using NewsAPI."""
    st.write(f"Cache miss: Calling NewsAPI for {company_name}...")
    url = (f"https://newsapi.org/v2/everything?"
           f"q={company_name}&"
           f"sortBy=publishedAt&"
           f"language=en&"
           f"pageSize={num_articles}&"
           f"apiKey={api_key}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return articles
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
        return []

@st.cache_data
def get_article_content(url):
    """Scrapes and returns the main text content of an article from a URL."""
    try:
        # --- NEW: Add a user-agent to mimic a real browser ---
        config = Config()
        config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        
        article = Article(url, config=config)
        # --- END NEW ---
        
        article.download()
        article.parse()
        return article.text
    except ArticleException:
        return None

# RAG Processing Function (no changes needed here)
@st.cache_resource
def create_rag_pipeline(articles_text):
    """Creates a RAG pipeline from scraped article text."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(articles_text)
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_texts(texts=chunks, embedding=embedding_model)
    llm = ChatGroq(model_name="llama3-8b-8192", groq_api_key=os.getenv("GROQ_API_KEY"))
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    return qa_chain

# --- Streamlit Page Configuration (no changes) ---
st.set_page_config(page_title="AI News Q&A Tool", page_icon="🧠", layout="wide")
st.title("🧠 AI News Q&A Tool")
st.write("Ask specific questions about a company based on its latest news.")

# --- API Key Status Sidebar (no changes) ---
with st.sidebar:
    st.header("API Key Status")
    groq_api_key = os.getenv("GROQ_API_KEY")
    news_api_key = os.getenv("NEWS_API_KEY")
    if groq_api_key: st.success("Groq API key loaded.")
    else: st.error("Groq API key not found.")
    if news_api_key: st.success("NewsAPI key loaded.")
    else: st.error("NewsAPI key not found.")

# --- Main App Logic (no changes) ---
company_name = st.text_input("Enter a company name (e.g., 'Apple', 'NVIDIA')", "NVIDIA")
if company_name:
    with st.spinner(f"Building knowledge base for {company_name}..."):
        articles_list = fetch_news_articles(news_api_key, company_name)
        if not articles_list:
            st.info("No articles found. Please try another company.")
        else:
            combined_text = ""
            for article_info in articles_list:
                content = get_article_content(article_info['url'])
                if content:
                    combined_text += content + "\n\n---\n\n"
            
            if len(combined_text) < 500:
                st.error("Could not retrieve enough content to build a reliable knowledge base. This is often due to anti-scraping measures on news sites.")
            else:
                qa_chain = create_rag_pipeline(combined_text)
                st.success(f"Knowledge base for {company_name} is ready. You can now ask questions.")
                st.subheader("Ask a Question")
                user_question = st.text_input("e.g., What were the latest financial results?")
                if user_question:
                    with st.spinner("Finding answers..."):
                        try:
                            result = qa_chain.invoke({"query": user_question})
                            st.markdown("### Answer")
                            st.write(result["result"])
                        except Exception as e:
                            st.error(f"An error occurred: {e}")