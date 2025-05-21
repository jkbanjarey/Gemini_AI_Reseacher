# 📚 Gemini-Powered Academic Research Assistant

An interactive Streamlit web app that uses **Google's Gemini model** to help researchers find, analyze, and summarize recent academic papers from arXiv based on any query.

### 🔍 Key Features

* **Natural Language Query Interface**
  Ask any research question, and get a synthesized, citation-backed response.

* **Live Paper Search & Download**
  Fetches the latest relevant papers from **arXiv** based on your query.

* **Chunk-Based Semantic Processing**
  Splits paper content into manageable sections for better LLM performance.

* **AI-Powered Answer Generation**
  Uses **LangChain** with Gemini to generate context-rich answers and paper summaries.

* **Downloadable PDFs**
  Easily download the original research papers used in the response.

---

### 🛠️ Technologies Used

* [Streamlit](https://streamlit.io/)
* [LangChain](https://www.langchain.com/)
* [Google Gemini (via langchain-google-genai)](https://python.langchain.com/docs/integrations/llms/google_genai/)
* [arXiv API](https://arxiv.org/help/api/index)
* FAISS Vector Store
* PDF Processing via `PyPDF2` and LangChain’s `PyPDFLoader`

---

### 🚀 Getting Started

#### 1. **Clone the repository**

```bash
git clone https://github.com/yourusername/Gemini_AI_Researcher.git
cd Gemini_AI_Researcher
```

#### 2. **Install dependencies**

```bash
pip install -r requirements.txt
```

#### 3. **Set up environment variables**

Create a `.env` file in the root directory with the following:

```
GOOGLE_API_KEY=your_google_generative_ai_api_key
```

#### 4. **Run the app**

```bash
streamlit run app.py
```

---

### 🧠 Example Use Case

> **Query**: *What are recent advancements in quantum machine learning?*

> **Output**: A concise answer with summaries of 3–4 top papers from arXiv, pros/cons, and download links for each paper.

---

### 📁 Project Structure

```bash
.
├── app.py                  # Streamlit front-end
├── paper_utils.py          # arXiv paper fetching + text chunking
├── research_agent.py       # LangChain QA pipeline + summarizer
├── requirements.txt        # Dependencies
└── README.md               # You are here
```
