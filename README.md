# CPBL RAG 聊天機器人

這是一個基於 RAG (Retrieval-Augmented Generation) 技術的中華職棒聊天機器人，能夠回答關於中華職棒的問題。系統會從中華職棒官網爬取最新資訊，並使用 LangChain 框架實現智能問答功能。

## 功能特點

- 自動爬取中華職棒官網最新資訊
- 使用 RAG 技術進行智能問答
- 支援多輪對話，具有上下文理解能力
- 使用 Redis 儲存對話歷史
- 支援多個會話（通過 session_id 區分）

## 系統需求

- Python 3.12
- Redis 服務器
- Docker（可選，用於運行 Redis）

## 安裝步驟

1. 克隆專案：
```bash
git clone [your-repository-url]
cd cpbl_rag
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 設置環境變數：
創建 `.env` 文件並添加以下內容：
```
OPENROUTER_API_KEY=your_api_key_here
REDIS_URL=redis://localhost:6379  # 可選，如果使用默認設定則不需要
```

4. 啟動 Redis：
使用 Docker：
```bash
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

## 專案結構

```
cpbl_rag/
├── app/
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── llm.py              # LLM 相關程式碼
│   │   ├── memory.py           # 聊天歷史管理
│   │   ├── document_processor.py # 文件處理
│   │   └── chain.py            # RAG 鏈
│   └── scrapers/
│       ├── __init__.py
│       └── cpbl_scraper.py     # 爬蟲模組
├── data/
│   ├── raw/                    # 原始爬蟲數據
│   └── vectors/                # 向量數據庫
├── main.py                     # 主程式
└── requirements.txt            # 依賴管理
```

## 使用方法

1. 運行主程式：
```bash
python main.py
```

2. 系統會自動：
   - 爬取中華職棒官網最新資訊
   - 處理文檔並創建向量存儲
   - 初始化 RAG 鏈
   - 開始測試對話

## 技術細節

- 使用 LangChain 框架實現 RAG 功能
- 使用 OpenRouter API 作為 LLM 提供者
- 使用 Redis 儲存對話歷史
- 使用 FAISS 作為向量數據庫
- 使用 BeautifulSoup4 進行網頁爬蟲

## 注意事項

- 需要有效的 OpenRouter API 密鑰
- 需要運行中的 Redis 服務器
- 爬蟲功能需要遵守網站的使用條款
- 對話歷史會在 1 小時後自動過期（可配置）

## 未來計劃

- [ ] 添加 Flask 網頁界面
- [ ] 實現定期自動更新數據
- [ ] 添加更多數據源
- [ ] 優化回答品質
- [ ] 添加用戶反饋機制

## 授權

[Your License] 