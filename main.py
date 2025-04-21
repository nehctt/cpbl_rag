from app.scrapers.cpbl_scraper import scrape_cpbl_website
from app.rag.document_processor import process_documents
from app.rag.chain import CPBLRAGChain
from app.rag.memory import clear_chat_history

def main():
    # 1. 爬取網站數據
    print("Scraping CPBL website...")
    docs = scrape_cpbl_website()
    
    # 2. 處理文檔並創建向量存儲
    print("Processing documents...")
    vector_store = process_documents(docs)
    
    # 3. 創建 RAG 鏈
    print("Creating RAG chain...")
    rag_chain = CPBLRAGChain(vector_store)
    
    # 4. 測試問答（使用聊天歷史）
    print("\nTesting the RAG system with chat history...")
    session_id = "test_session"
    
    # 清除之前的聊天歷史（如果有的話）
    clear_chat_history(session_id)
    
    # 測試連續對話
    test_questions = [
        "請問CPBL排名第一是哪一隊？",
        "這個球隊的戰績如何？",
        "打擊排行榜上第一名（打擊王）是誰？所屬球隊是？",
        "這位打擊王所屬的球隊最近有什麼球員異動？"
    ]
    
    for question in test_questions:
        print("\n" + "="*50)
        print(f"問題: {question}")
        result = rag_chain.get_answer(question, session_id)
        print(f"回答: {result}")

if __name__ == "__main__":
    main() 