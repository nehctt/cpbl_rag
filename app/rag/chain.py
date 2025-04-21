from langchain import hub
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.rag.llm import openrouter_model
from app.rag.memory import get_chat_history

class CPBLRAGChain:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 1}
        )
        # 更新 prompt template 以包含聊天歷史
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "你是一個專業的中華職棒助手，請根據提供的上下文回答問題。如果上下文中沒有相關資訊，請誠實地說你不知道。"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])

    def get_answer(self, question: str, session_id: str) -> str:
        """
        使用 RAG 鏈回答問題，並保存聊天歷史
        
        Args:
            question: 用戶的問題
            session_id: 會話ID
            
        Returns:
            str: AI 的回答
        """
        # 獲取聊天歷史
        chat_history = get_chat_history(session_id)
        
        # 檢索相關文檔
        retrieved_docs = self.retriever.invoke(question)
        docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
        
        # 準備上下文
        context = f"相關資訊：\n{docs_content}\n\n請根據以上資訊回答問題。"
        
        # 使用 RAG 生成答案
        prompt = self.prompt_template.invoke({
            "question": f"{context}\n\n{question}",
            "chat_history": chat_history.messages
        })
        
        # 獲取回答
        answer = openrouter_model.invoke(prompt)
        
        # 保存對話歷史
        chat_history.add_user_message(question)
        chat_history.add_ai_message(answer.content)
        
        return answer.content

if __name__ == "__main__":
    from app.scrapers.cpbl_scraper import scrape_cpbl_website
    from app.rag.document_processor import process_documents
    
    # 測試 RAG 鏈
    docs = scrape_cpbl_website()
    vector_store = process_documents(docs)
    rag_chain = CPBLRAGChain(vector_store)
    
    # 測試問題（使用固定的 session_id）
    session_id = "test_session"
    questions = [
        "請問CPBL排名第一是哪一隊？",
        "他們目前的戰績如何？",
        "他們的打擊表現如何？"
    ]
    
    for question in questions:
        print("\n" + "="*50)
        print(f"問題: {question}")
        result = rag_chain.get_answer(question, session_id)
        print(f"回答: {result}") 