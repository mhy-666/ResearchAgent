from typing import List, Dict, Any, Optional, Annotated
from pydantic import BaseModel
from datetime import datetime
import operator

class PaperInfo(BaseModel):
    """论文信息数据模型"""
    title: str
    authors: List[str]
    summary: str
    published: str
    arxiv_id: str
    url: str

class VideoInfo(BaseModel):
    """视频信息数据模型"""
    title: str
    url: str
    description: str
    published: Optional[str] = None
    channel: Optional[str] = None

# 使用 TypedDict 而不是 BaseModel 来避免下标访问问题
from typing_extensions import TypedDict

class ResearchState(TypedDict):
    """研究状态数据模型"""
    domain: str
    days: int
    papers: Annotated[List[PaperInfo], operator.add]
    videos: Annotated[List[VideoInfo], operator.add]
    blog_content: str
    messages: Annotated[List[Dict[str, Any]], operator.add]
