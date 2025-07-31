import json
from typing import List, Dict, Any
from langchain_mcp_adapters.client import MultiServerMCPClient
from utils.types import VideoInfo

class ResearchVideoAgent:
    """研究视频智能体"""
    
    def __init__(self):
        self.name = "Research Video Agent"
        self.mcp_client = None
    
    async def initialize_mcp(self):
        """初始化 MCP 客户端"""
        if not self.mcp_client:
            self.mcp_client = MultiServerMCPClient({
                "youtube": {
                    "command": "python",
                    "args": ["mcp_servers/youtube_server.py"],
                    "transport": "stdio",
                }
            })
    
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """处理视频检索请求"""
        try:
            await self.initialize_mcp()
            tools = await self.mcp_client.get_tools()
            
            # 使用字典语法访问状态
            domain = state.get("domain", "")
            
            # 搜索研究视频
            search_tool = None
            filter_tool = None
            
            for tool in tools:
                if tool.name == "search_research_videos":
                    search_tool = tool
                elif tool.name == "filter_academic_videos":
                    filter_tool = tool
            
            if search_tool:
                videos_json = await search_tool.ainvoke({
                    "domain": domain,
                    "max_results": 15
                })
                
                # 过滤学术视频
                if filter_tool:
                    filtered_videos_json = await filter_tool.ainvoke({
                        "videos_json": videos_json,
                        "keywords": domain
                    })
                    videos_data = json.loads(filtered_videos_json)
                else:
                    videos_data = json.loads(videos_json)
                
                videos = [VideoInfo(**video) for video in videos_data[:10]]
                
                # 返回状态更新
                return {
                    "videos": videos,
                    "messages": [{
                        "agent": self.name,
                        "action": "retrieved_videos",
                        "count": len(videos),
                        "domain": domain
                    }]
                }
            
            return {"videos": [], "messages": []}
            
        except Exception as e:
            return {
                "videos": [],
                "messages": [{
                    "agent": self.name,
                    "error": f"Failed to retrieve videos: {str(e)}"
                }]
            }
