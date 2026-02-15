# 🚀 Summrly AI — Smart Text & PDF Summarizer

Summrly AI is a GenAI-powered web application that converts long-form content into concise summaries in seconds. It is built using LangChain (LCEL), Groq LLMs, and Streamlit, with a focus on performance, scalability, and real-world constraints like token limits.

---

## ✨ Features

* 📄 PDF Summarization — Upload PDF and get instant summary
* 📝 Text Summarization — Paste text and summarize quickly
* ⚡ Fast & Optimized — Uses Map-Reduce summarization
* 🧠 LLM Powered — Uses llama-3.3-70b-versatile (Groq)
* 🔄 Stateless UX — Clears memory at every step
* 🧹 Reset Button — Start fresh anytime
* 🎯 Adjustable Summary Length
* 📊 LangSmith Tracing Enabled

---

## 🧠 Architecture

Summrly AI uses Map → Reduce summarization:

1. Split large text into chunks
2. Summarize each chunk (Map)
3. Combine summaries into final output (Reduce)

Benefits:

* Avoids token overflow
* Faster performance
* Scalable for large documents

---

## 🛠️ Tech Stack

* Frontend: Streamlit
* LLM Provider: Groq
* Model: llama-3.3-70b-versatile
* Framework: LangChain (LCEL)
* Tracing: LangSmith
* PDF Loader: PyPDFLoader

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/summrly-ai.git
cd summrly-ai
```

Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Setup

Create `.streamlit/secrets.toml`

```toml
GROQ_API_KEY = "your_groq_api_key"
LANGCHAIN_API_KEY = "your_langsmith_key"
LANGCHAIN_PROJECT = "Summrly"
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 👨‍💻 Author

Paranjay Soni

GitHub: [https://github.com/paranjaysoni](https://github.com/paranjaysoni)

---

## ⭐ Support

If you like this project, give it a star ⭐
