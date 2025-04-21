import os
from typing import Optional
from langchain_redis import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

# Redis 連接設定
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

def get_chat_history(session_id: str) -> BaseChatMessageHistory:
    """
    獲取或創建一個新的聊天歷史記錄
    
    Args:
        session_id: 會話ID，用於區分不同的對話
        
    Returns:
        RedisChatMessageHistory 實例
    """
    return RedisChatMessageHistory(
        session_id=session_id,
        redis_url=REDIS_URL,
        key_prefix="cpbl_chat:",  # 自定義前綴
        ttl=3600,  # 設置 TTL 為 1 小時
    )

def clear_chat_history(session_id: str) -> None:
    """
    清除指定會話的聊天歷史
    
    Args:
        session_id: 要清除的會話ID
    """
    history = get_chat_history(session_id)
    history.clear() 