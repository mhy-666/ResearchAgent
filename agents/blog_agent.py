from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from utils.types import PaperInfo, VideoInfo

class ContentIntegrationAgent:
    """内容整合智能体"""
    
    def __init__(self, openai_api_key: str):
        self.name = "Content Integration Agent"
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            openai_api_key=openai_api_key
        )
        
        self.blog_prompt = ChatPromptTemplate.from_template("""
你是一位专业的科研博客作者。请根据提供的最新论文和视频资源，为"{domain}"领域撰写一篇引人入胜的博客文章。

最新论文资料：
{papers_content}

相关视频资源：
{videos_content}

请撰写一篇结构完整的博客文章，包含以下部分：

1. **引言**：简介该领域的当前发展态势
2. **最新研究进展**：基于论文内容总结关键发现和创新点
3. **深度解读**：选择1-2篇重要论文进行详细分析
4. **视频推荐**：推荐相关的学习和研究视频
5. **未来展望**：基于当前研究趋势的发展预测
6. **总结**：概括要点和建议

要求：
- 使用专业但易懂的语言
- 确保内容准确性和客观性
- 适当引用论文标题和作者
- 包含视频链接和简要说明
- 文章长度控制在1500-2000字
- 使用Markdown格式

请开始撰写：
        """)
    
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """处理内容整合请求"""
        try:
            # 使用字典语法访问状态
            domain = state.get("domain", "")
            papers_data = state.get("papers", [])
            videos_data = state.get("videos", [])
            
            # 将字典转换为 Pydantic 模型（如果需要）
            papers = []
            for paper_dict in papers_data:
                if isinstance(paper_dict, dict):
                    papers.append(PaperInfo(**paper_dict))
                else:
                    papers.append(paper_dict)
            
            videos = []
            for video_dict in videos_data:
                if isinstance(video_dict, dict):
                    videos.append(VideoInfo(**video_dict))
                else:
                    videos.append(video_dict)
            
            # 准备内容
            papers_content = self._format_papers(papers)
            videos_content = self._format_videos(videos)
            
            # 生成博客内容
            blog_response = await self.llm.ainvoke(
                self.blog_prompt.format(
                    domain=domain,
                    papers_content=papers_content,
                    videos_content=videos_content
                )
            )
            
            # 返回状态更新
            return {
                "blog_content": blog_response.content,
                "messages": [{
                    "agent": self.name,
                    "action": "generated_blog",
                    "domain": domain,
                    "papers_count": len(papers),
                    "videos_count": len(videos)
                }]
            }
            
        except Exception as e:
            return {
                "blog_content": "",
                "messages": [{
                    "agent": self.name,
                    "error": f"Failed to generate blog: {str(e)}"
                }]
            }
    
    def _format_papers(self, papers: List[PaperInfo]) -> str:
        """格式化论文信息"""
        if not papers:
            return "暂无最新论文数据"
        
        formatted_papers = []
        for i, paper in enumerate(papers[:8], 1):
            formatted_paper = f"""
{i}. **{paper.title}**
   - 作者：{', '.join(paper.authors[:3])}{'等' if len(paper.authors) > 3 else ''}
   - 发布时间：{paper.published}
   - 摘要：{paper.summary}
   - ArXiv ID：{paper.arxiv_id}
            """
            formatted_papers.append(formatted_paper)
        
        return '\n'.join(formatted_papers)
    
    def _format_videos(self, videos: List[VideoInfo]) -> str:
        """格式化视频信息"""
        if not videos:
            return "暂无相关视频推荐"
        
        formatted_videos = []
        for i, video in enumerate(videos[:6], 1):
            formatted_video = f"""
{i}. **{video.title}**
   - 链接：{video.url}
   - 频道：{video.channel or '未知'}
   - 描述：{video.description[:150]}...
            """
            formatted_videos.append(formatted_video)
        
        return '\n'.join(formatted_videos)
