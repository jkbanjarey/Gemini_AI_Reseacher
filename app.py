# app.py
import streamlit as st
import os
from dotenv import load_dotenv

from paper_utils import search_and_download, extract_chunks_from_pdfs
from research_agent import build_qa_chain, summarize_paper

load_dotenv()

st.set_page_config(page_title="GenAI Scholar")
st.title("📚 Gemini-Powered Academic Research Assistant")
st.markdown("Ask a question — get a research-based answer using recent academic papers!")

query = st.text_input("🧠 Enter your research query:")

# Initialize session state
if "pdfs" not in st.session_state:
    st.session_state.pdfs = []

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

if "result" not in st.session_state:
    st.session_state.result = None

if "llm" not in st.session_state:
    st.session_state.llm = None

# Handle the Generate Answer button
if st.button("🔍 Generate Answer") and query:
    with st.spinner("📥 Fetching academic papers..."):
        st.session_state.pdfs = search_and_download(query)

    with st.spinner("🔎 Extracting and processing..."):
        st.session_state.chunks = extract_chunks_from_pdfs(st.session_state.pdfs)

    with st.spinner("🤖 Generating answer using Gemini..."):
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0)
        st.session_state.llm = llm
        st.session_state.qa_chain = build_qa_chain(st.session_state.chunks)
        st.session_state.result = st.session_state.qa_chain.invoke({"query": query})

# Display results if available
if st.session_state.get("result") and st.session_state.result.get("result"):
    st.success("📌 Answer:")
    st.markdown(st.session_state.result["result"])

    if st.session_state.result.get("source_documents"):
        st.markdown("### 📄 Source Papers with Summaries")
        seen_sources = set()

        for i, doc in enumerate(st.session_state.result["source_documents"]):
            source_id = doc.metadata.get("source", "") + doc.metadata.get("title", "")
            if source_id in seen_sources:
                continue
            seen_sources.add(source_id)

            # Fallback title if missing
            title = doc.metadata.get("title") or "Untitled Research Paper"
            pdf_path = doc.metadata.get("source")

            st.markdown(f"**📘 Title: {title}**")
            summary_output = summarize_paper(st.session_state.llm, doc.page_content, title)
            st.markdown(summary_output)

            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label=f"📥 Download {os.path.basename(pdf_path)}",
                        data=f.read(),
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                        key=f"download_button_{i}"
                    )
    else:
        st.warning("⚠️ No source documents found to summarize.")
elif query and not st.session_state.get("result"):
    st.info("ℹ️ Please click 'Generate Answer' to start.")
