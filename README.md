# 📈 AI News Research Tool for Equity Analysts

This application leverages artificial intelligence to automate news research for equity analysts. It fetches the latest news articles for a specified company, builds a knowledge base, and uses a RAG pipeline with the Groq Llama 3 model to answer specific questions about the news.

---

## 🚀 Live Demo

Here is a live demonstration of the application's workflow, from entering a company name to asking a question and receiving an AI-generated answer.



https://github.com/user-attachments/assets/883fdcb7-7189-49d4-aed5-8cd724f1b7ab



---

## ✨ Features

- **Interactive Q&A**: Ask specific questions about the news using a Retrieval-Augmented Generation (RAG) pipeline.
- **Real-Time Knowledge Base**: Gathers the most recent news articles from NewsAPI to build its context.
- **Web Scraping**: Extracts the full text from article URLs, removing clutter.
- **High-Speed AI**: Utilizes the Groq Llama 3 model for fast and sophisticated analysis.
- **Web Interface**: Built with Streamlit for an intuitive user experience.
- **Performance Optimized**: Caching is implemented to speed up repeated searches.

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Language**: Python 3
- **LLM Orchestration**: LangChain & `langchain-groq`
- **AI Model**: Llama 3 (8B) via Groq API
- **Vector Store**: ChromaDB (in-memory)
- **Embeddings**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **News Source**: NewsAPI
- **Web Scraping**: `newspaper3k`

---

## ⚙️ Setup and Installation

Follow these steps to set up the project on your local machine.

#### 1. Clone the Repository
```bash
git clone [https://github.comcom/Shwwetcode/ai-news-research-tool.git](https://github.comcom/Shwwetcode/ai-news-research-tool.git)
cd ai-news-research-tool
