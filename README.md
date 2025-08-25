# 📈 AI News Research Tool for Equity Analysts

This application leverages artificial intelligence to automate news research for equity analysts. It fetches the latest news articles for a specified company, scrapes the content, and uses the Groq Llama 3 model via LangChain to provide a concise, structured analysis, including sentiment, key summaries, potential risks, and opportunities.

<img width="1474" height="912" alt="Screenshot 2025-08-25 at 3 03 11 PM" src="https://github.com/user-attachments/assets/6ab409a6-7959-42be-8a77-fca693535d94" />
<img width="1474" height="912" alt="Screenshot 2025-08-25 at 3 03 19 PM" src="https://github.com/user-attachments/assets/a0c1f885-233c-4332-8760-1ba9f5eb51d9" />
<img width="1474" height="912" alt="Screenshot 2025-08-25 at 3 03 00 PM" src="https://github.com/user-attachments/assets/dcb1519d-d8b1-4f89-aae1-3332511284bc" />


## ✨ Features

- **Real-Time News Fetching**: Gathers the most recent news articles using the NewsAPI.
- **Web Scraping**: Extracts the full text from article URLs, removing clutter.
- **AI-Powered Analysis**: Utilizes the high-speed Groq Llama 3 model for sophisticated analysis.
- **Structured Output**: Presents insights in a clean, easy-to-read format.
- **Secure API Key Management**: Uses a `.env` file to keep secret API keys safe.
- **Web Interface**: Built with Streamlit for an intuitive user experience.

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Language**: Python 3
- **LLM Integration**: LangChain & `langchain-groq`
- **AI Model**: Llama 3 (8B) via Groq API
- **News Source**: NewsAPI
- **Web Scraping**: `newspaper3k`
- **Environment Management**: `python-dotenv`

---

## ⚙️ Setup and Installation

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

git clone [https://github.com/Shwwetcode/ai-news-research-tool.git](https://github.com/Shwwetcode/ai-news-research-tool.git)
cd ai-news-research-tool

###📂 Project Structure
ai-news-research-tool/
│
├── .env                
├── .gitignore          
├── app.py              
├── README.md           
└── venv/               
