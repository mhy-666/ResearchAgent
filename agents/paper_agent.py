import json
from typing import List, Dict, Any
from langchain_mcp_adapters.client import MultiServerMCPClient
from utils.types import PaperInfo

class PaperRetrievalAgent:
    """论文检索智能体"""
    
    def __init__(self):
        self.name = "Paper Retrieval Agent"
        self.mcp_client = None
    
    async def initialize_mcp(self):
        """初始化 MCP 客户端"""
        if not self.mcp_client:
            self.mcp_client = MultiServerMCPClient({
                "arxiv": {
                    "command": "python",
                    "args": ["mcp_servers/arxiv_server.py"],
                    "transport": "stdio",
                }
            })
    
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """处理论文检索请求"""
        try:
            await self.initialize_mcp()
            tools = await self.mcp_client.get_tools()
            
            # 使用字典语法访问状态
            domain = state.get("domain", "")
            days = state.get("days", 7)
            
            # 搜索最近的论文
            search_tool = None
            for tool in tools:
                if tool.name == "search_recent_papers":
                    search_tool = tool
                    break
            
            if search_tool:
                papers_json = await search_tool.ainvoke({
                    "domain": domain,
                    "max_results": 10,
                    "days": days
                })
                
                # 解析论文数据
                papers_data = json.loads(papers_json)
                papers = [PaperInfo(**paper) for paper in papers_data]
                
                # 返回状态更新
                return {
                    "papers": papers,
                    "messages": [{
                        "agent": self.name,
                        "action": "retrieved_papers",
                        "count": len(papers),
                        "domain": domain
                    }]
                }
            
            return {"papers": [], "messages": []}
            
        except Exception as e:
            return {
                "papers": [],
                "messages": [{
                    "agent": self.name,
                    "error": f"Failed to retrieve papers: {str(e)}"
                }]
            }
