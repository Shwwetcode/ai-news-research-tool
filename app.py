# app.py

import streamlit as st
import os
from dotenv import load_dotenv
import requests

# NEW IMPORTS for this step
from newspaper import Article, ArticleException
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables from .env file
load_dotenv()

# --- Functions ---

def fetch_news_articles(api_key, company_name, num_articles=5):
    """Fetches news articles for a given company using NewsAPI."""
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

# NEW: Function to scrape the full text content of an article
def get_article_content(url):
    """Scrapes and returns the main text content of an article from a URL."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except ArticleException:
        # st.warning(f"Could not parse article at {url}. Skipping.")
        return None

# NEW: Function to analyze articles using Groq and LangChain
def analyze_articles_with_groq(api_key, articles_text, company_name):
    """Analyzes the combined text of articles using LangChain and Groq."""
    
    # Define the prompt template for the analyst
    prompt_template = """
    You are an expert equity research analyst. Your task is to analyze the following news articles about {company_name}.
    Based ONLY on the provided text, please provide a clear and concise analysis.

    Here is the combined text from the articles:
    ---
    {articles_text}
    ---

    Please format your response as follows, using Markdown:

    ### 1. Overall Sentiment
    **Sentiment:** (Positive, Negative, or Neutral)
    **Justification:** (A brief, one-sentence explanation for your sentiment choice).

    ### 2. Key Summary Points
    - Provide 3-5 bullet points summarizing the most critical information, events, or financial data mentioned.

    ### 3. Potential Risks
    - List 2-3 potential risks or challenges for the company highlighted in the articles.

    ### 4. Potential Opportunities
    - List 2-3 potential opportunities or positive catalysts mentioned.
    """
    
    # Set up the LLM with Groq
    # Llama3 8B is a great choice for speed and quality for this task
    llm = ChatGroq(model_name="llama3-8b-8192", groq_api_key=api_key)
    
    # Create the prompt from the template
    prompt = PromptTemplate(template=prompt_template, input_variables=["company_name", "articles_text"])
    
    # Create the LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain with the provided text and company name
    try:
        response = chain.run(company_name=company_name, articles_text=articles_text)
        return response
    except Exception as e:
        st.error(f"An error occurred during AI analysis: {e}")
        return None

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="AI News Research Tool",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI News Research Tool for Equity Analysts")
st.write("Enter a company name to fetch, scrape, and analyze recent news using Groq's Llama3.")

# --- API Key Status Sidebar ---
with st.sidebar:
    st.header("API Key Status")
    groq_api_key = os.getenv("GROQ_API_KEY")
    news_api_key = os.getenv("NEWS_API_KEY")
    if groq_api_key: st.success("Groq API key loaded.")
    else: st.error("Groq API key not found.")
    
    if news_api_key: st.success("NewsAPI key loaded.")
    else: st.error("NewsAPI key not found.")


# --- Main App Logic ---
company_name = st.text_input("Enter a company name (e.g., 'Apple', 'NVIDIA')", "NVIDIA")

if st.button("Analyze News"):
    # Validate inputs
    if not company_name:
        st.warning("Please enter a company name.")
    elif not groq_api_key or not news_api_key:
        st.error("API key(s) are missing. Please check the sidebar status.")
    else:
        # STAGE 1: Fetch news articles
        with st.spinner(f"Fetching news for {company_name}..."):
            articles_list = fetch_news_articles(news_api_key, company_name)
        
        if not articles_list:
            st.info("No articles found for the given company.")
        else:
            # STAGE 2: Scrape and combine article content
            with st.spinner("Parsing articles... this may take a moment."):
                combined_text = ""
                st.subheader("📰 Fetched Articles")
                for article_info in articles_list:
                    st.write(f"  - [{article_info['title']}]({article_info['url']})")
                    content = get_article_content(article_info['url'])
                    if content:
                        combined_text += content + "\n\n---\n\n"
            
            # STAGE 3: Analyze with Groq LLM
            if len(combined_text) < 250: # Check if we have enough content
                st.error("Could not retrieve enough content from the articles to perform an analysis.")
            else:
                with st.spinner("AI is analyzing... Groq is making this lightning fast! ⚡️"):
                    analysis_result = analyze_articles_with_groq(groq_api_key, combined_text, company_name)
                
                st.subheader("🤖 AI-Powered Analysis")
                if analysis_result:
                    st.markdown(analysis_result)