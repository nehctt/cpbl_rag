from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from transformers import logging
logging.set_verbosity_error()

def process_documents(docs):
    """
    處理文件：分割文本並創建向量存儲
    """
    # 分割文本
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=256,  # chunk size (characters)
        chunk_overlap=32,  # chunk overlap (characters)
        add_start_index=True,  # track index in original document
    )
    all_splits = text_splitter.split_documents(docs)
    print(f"Split documents into {len(all_splits)} sub-documents.")

    # 創建向量存儲
    embedding = HuggingFaceEmbeddings(
        model_name="Alibaba-NLP/gte-multilingual-base",
        model_kwargs={"trust_remote_code": True}
    )
    vector_store = FAISS.from_documents(documents=all_splits, embedding=embedding)
    
    return vector_store

if __name__ == "__main__":
    from app.scrapers.cpbl_scraper import scrape_cpbl_website
    docs = scrape_cpbl_website()
    vector_store = process_documents(docs)
    print("Vector store created successfully") 