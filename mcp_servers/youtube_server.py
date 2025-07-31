import json
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP
from youtube_search import YoutubeSearch

mcp = FastMCP("YouTube Research Server")

@mcp.tool()
def search_research_videos(domain: str, max_results: int = 10) -> str:
    """搜索指定领域的研究视频"""
    try:
        # 构建搜索查询，添加学术相关关键词
        academic_keywords = ["research", "paper", "study", "academic", "conference", "lecture"]
        search_queries = [f"{domain} {keyword}" for keyword in academic_keywords[:3]]
        
        all_videos = []
        
        for query in search_queries:
            try:
                # 使用 youtube_search 库搜索视频
                results = YoutubeSearch(query, max_results=max_results//len(search_queries)).to_dict()
                
                for video in results:
                    video_info = {
                        "title": video.get("title", ""),
                        "url": f"https://www.youtube.com{video.get('url_suffix', '')}",
                        "description": video.get("long_desc", video.get("description", ""))[:300],
                        "published": video.get("publish_time", ""),
                        "channel": video.get("channel", ""),
                        "duration": video.get("duration", ""),
                        "views": video.get("views", "")
                    }
                    all_videos.append(video_info)
                    
            except Exception as e:
                print(f"Error with query '{query}': {str(e)}")
                continue
        
        # 去重和排序
        unique_videos = []
        seen_urls = set()
        
        for video in all_videos:
            if video["url"] not in seen_urls:
                seen_urls.add(video["url"])
                unique_videos.append(video)
        
        # 限制结果数量
        unique_videos = unique_videos[:max_results]
        
        return json.dumps(unique_videos, ensure_ascii=False, indent=2)
    
    except Exception as e:
        return f"Error searching videos: {str(e)}"

@mcp.tool()
def filter_academic_videos(videos_json: str, keywords: str = "") -> str:
    """过滤学术相关的视频"""
    try:
        videos = json.loads(videos_json)
        academic_keywords = ["research", "paper", "study", "academic", "conference", "lecture", "university", "phd", "science"]
        
        if keywords:
            academic_keywords.extend(keywords.split(","))
        
        filtered_videos = []
        for video in videos:
            title_lower = video.get("title", "").lower()
            desc_lower = video.get("description", "").lower()
            
            # 检查标题和描述中是否包含学术关键词
            is_academic = any(keyword in title_lower or keyword in desc_lower for keyword in academic_keywords)
            
            if is_academic:
                filtered_videos.append(video)
        
        return json.dumps(filtered_videos, ensure_ascii=False, indent=2)
    
    except Exception as e:
        return f"Error filtering videos: {str(e)}"

if __name__ == "__main__":
    print("Starting YouTube MCP Server...")
    mcp.run(transport="stdio")
