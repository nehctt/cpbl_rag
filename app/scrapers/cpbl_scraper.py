import bs4
from langchain_community.document_loaders import WebBaseLoader
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_cpbl_website():
    """
    爬取中華職棒官網的資訊
    """
    bs4_strainer = bs4.SoupStrainer(class_=["RecordTableWrap", "TopFiveList"])
    loader = WebBaseLoader(
        web_paths=(
            "https://www.cpbl.com.tw/standings/season",  # 球隊戰績
            "https://www.cpbl.com.tw/player/trans",  # 球員異動
            "https://www.cpbl.com.tw/stats/toplist",  # 球員排行榜
        ),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()
    
    print(f"Total characters: {len(docs[0].page_content)}")
    return docs

if __name__ == "__main__":
    docs = scrape_cpbl_website()
    print(f"Scraped {len(docs)} documents from CPBL website") 