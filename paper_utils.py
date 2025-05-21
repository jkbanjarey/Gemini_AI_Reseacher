# paper_utils.py
import arxiv
import os
import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def search_and_download(query, num_papers=4):
    search = arxiv.Search(query=query, max_results=num_papers)
    pdf_paths = []

    for i, result in enumerate(search.results()):
        pdf_url = result.pdf_url
        filename = f"paper_{i}.pdf"
        response = requests.get(pdf_url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        pdf_paths.append(filename)

    return pdf_paths

def extract_chunks_from_pdfs(pdf_paths):
    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    for path in pdf_paths:
        loader = PyPDFLoader(path)
        documents = loader.load()

        paper_title = extract_title_from_text(documents)
        for doc in documents:
            doc.metadata["title"] = paper_title
            doc.metadata["source"] = path

        chunks = splitter.split_documents(documents)
        for chunk in chunks:
            chunk.metadata["title"] = paper_title
            chunk.metadata["source"] = path

        all_chunks.extend(chunks)

    return all_chunks


def extract_title_from_text(documents):
    for doc in documents:
        text = doc.page_content
        lines = text.strip().split("\n")
        for line in lines:
            clean = line.strip()
            if clean and len(clean.split()) <= 15:
                return clean
    return "Untitled Paper"
