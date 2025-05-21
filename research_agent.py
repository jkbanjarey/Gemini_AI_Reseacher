import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

load_dotenv()

def build_qa_chain(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa

def summarize_paper(llm, content, title):
    prompt = f"""
        You are an expert research assistant. Read the following academic paper titled "{title}" and provide:

        1. 📘 **Title**: {title}
        2. 📝 **Summary**: A brief summary (3–4 sentences)
        3. ✅ **Pros**: 2–3 strengths of the paper
        4. ❌ **Cons**: 2–3 weaknesses or limitations

        Here is the paper content:
        \"\"\"{content}\"\"\"
        
        Respond in markdown format.
    """
    return llm.invoke(prompt).content
