import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP
from langchain_community.utilities import ArxivAPIWrapper
import arxiv

mcp = FastMCP("ArXiv Research Server")

@mcp.tool()
def search_recent_papers(domain: str, max_results: int = 10, days: int = 7) -> str:
    """搜索指定领域最近几天的论文"""
    try:
        # 创建 ArXiv 客户端
        client = arxiv.Client()
        
        # 构建搜索查询
        search_query = f"all:{domain}"
        
        # 计算日期范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 创建搜索对象
        search = arxiv.Search(
            query=search_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        for result in client.results(search):
            # 检查论文是否在指定日期范围内
            if result.published.replace(tzinfo=None) >= start_date:
                paper_info = {
                    "title": result.title,
                    "authors": [author.name for author in result.authors],
                    "summary": result.summary[:500] + "..." if len(result.summary) > 500 else result.summary,
                    "published": result.published.strftime("%Y-%m-%d"),
                    "arxiv_id": result.entry_id.split('/')[-1],
                    "url": result.entry_id
                }
                papers.append(paper_info)
        
        return json.dumps(papers, ensure_ascii=False, indent=2)
    
    except Exception as e:
        return f"Error searching papers: {str(e)}"

@mcp.tool()
def get_paper_details(arxiv_id: str) -> str:
    """获取特定论文的详细信息"""
    try:
        # 使用 ArXiv API 获取论文详情
        wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
        result = wrapper.run(arxiv_id)
        return result
    except Exception as e:
        return f"Error getting paper details: {str(e)}"

if __name__ == "__main__":
    print("Starting ArXiv MCP Server...")
    mcp.run(transport="stdio")
