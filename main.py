import asyncio
import os
from typing import Dict, Any
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START
from utils.types import ResearchState  # 这现在是 TypedDict
from agents.paper_agent import PaperRetrievalAgent
from agents.video_agent import ResearchVideoAgent
from agents.blog_agent import ContentIntegrationAgent

# 加载环境变量
load_dotenv()

class ResearchMultiAgentSystem:
    """研究多智能体系统"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("请设置 OPENAI_API_KEY 环境变量")
        
        # 初始化智能体
        self.paper_agent = PaperRetrievalAgent()
        self.video_agent = ResearchVideoAgent()
        self.blog_agent = ContentIntegrationAgent(self.openai_api_key)
        
        # 构建工作流
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """构建 LangGraph 工作流"""
        # 使用 ResearchState (TypedDict) 作为状态类型
        workflow = StateGraph(ResearchState)
        
        # 添加节点
        workflow.add_node("paper_retrieval", self.paper_agent.process)
        workflow.add_node("video_retrieval", self.video_agent.process)
        workflow.add_node("content_integration", self.blog_agent.process)
        
        # 添加边：从开始到论文和视频检索（并行）
        workflow.add_edge(START, "paper_retrieval")
        workflow.add_edge(START, "video_retrieval")
        
        # 添加边：论文和视频检索完成后到内容整合
        workflow.add_edge("paper_retrieval", "content_integration")
        workflow.add_edge("video_retrieval", "content_integration")
        
        # 添加边：内容整合完成后结束
        workflow.add_edge("content_integration", END)
        
        return workflow.compile()
    
    async def run_research(self, domain: str, days: int = 7) -> Dict[str, Any]:
        """运行研究流程"""
        print(f"🔍 开始研究领域：{domain}")
        print(f"📅 时间范围：最近 {days} 天")
        
        # 直接使用字典初始化状态，不调用 model_dump()
        initial_state = {
            "domain": domain,
            "days": days,
            "papers": [],
            "videos": [],
            "blog_content": "",
            "messages": []
        }
        
        try:
            # 运行工作流 - 直接传递字典
            final_state = await self.workflow.ainvoke(initial_state)
            
            print(f"✅ 研究完成！")
            print(f"📄 找到论文：{len(final_state.get('papers', []))} 篇")
            print(f"🎥 找到视频：{len(final_state.get('videos', []))} 个")
            print(f"📝 博客字数：{len(final_state.get('blog_content', ''))} 字符")
            
            return final_state
            
        except Exception as e:
            print(f"❌ 研究过程中出现错误：{str(e)}")
            return {"error": str(e)}
    
    def print_results(self, results: Dict[str, Any]):
        """打印结果摘要"""
        if "error" in results:
            print(f"错误：{results['error']}")
            return
        
        print("\n" + "="*80)
        print("📊 研究结果摘要")
        print("="*80)
        
        # 打印论文信息
        papers = results.get("papers", [])
        if papers:
            print(f"\n📄 最新论文 ({len(papers)} 篇)：")
            for i, paper in enumerate(papers[:5], 1):
                # 处理论文对象（可能是字典或 Pydantic 模型）
                if isinstance(paper, dict):
                    title = paper.get("title", "未知标题")
                    authors = paper.get("authors", [])
                    published = paper.get("published", "未知日期")
                else:
                    title = getattr(paper, 'title', "未知标题")
                    authors = getattr(paper, 'authors', [])
                    published = getattr(paper, 'published', "未知日期")
                
                print(f"{i}. {title}")
                if authors:
                    author_list = authors[:2] if isinstance(authors, list) else [authors]
                    print(f"   作者：{', '.join(author_list)}{'等' if len(authors) > 2 else ''}")
                print(f"   发布：{published}")
                print()
        
        # 打印视频信息
        videos = results.get("videos", [])
        if videos:
            print(f"\n🎥 相关视频 ({len(videos)} 个)：")
            for i, video in enumerate(videos[:5], 1):
                # 处理视频对象（可能是字典或 Pydantic 模型）
                if isinstance(video, dict):
                    title = video.get("title", "未知标题")
                    channel = video.get("channel")
                    url = video.get("url", "")
                else:
                    title = getattr(video, 'title', "未知标题")
                    channel = getattr(video, 'channel', None)
                    url = getattr(video, 'url', "")
                
                print(f"{i}. {title}")
                if channel:
                    print(f"   频道：{channel}")
                print(f"   链接：{url}")
                print()
        
        # 打印博客内容预览
        blog_content = results.get("blog_content", "")
        if blog_content:
            print("\n📝 生成的博客内容预览：")
            print("-" * 60)
            print(blog_content[:500] + "..." if len(blog_content) > 500 else blog_content)
            print("-" * 60)
        
        print("\n✨ 研究完成！")

async def main():
    """主函数"""
    try:
        # 创建研究系统
        research_system = ResearchMultiAgentSystem()
        
        # 示例：研究机器学习领域
        domain = input("请输入研究领域（默认：machine learning）：").strip() or "machine learning"
        days = int(input("请输入时间范围（天数，默认：7）：").strip() or "7")
        
        # 运行研究
        results = await research_system.run_research(domain, days)
        
        # 显示结果
        research_system.print_results(results)
        
        # 保存博客到文件
        if "blog_content" in results and results["blog_content"]:
            filename = f"research_blog_{domain.replace(' ', '_')}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(results["blog_content"])
            print(f"\n💾 博客内容已保存到：{filename}")
    
    except KeyboardInterrupt:
        print("\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"❌ 程序运行错误：{str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
