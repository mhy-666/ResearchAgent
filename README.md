# ResearchAgent


## 系统架构

系统采用 LangGraph 多智能体架构，包含：

- **PaperRetrievalAgent**：通过 MCP ArXiv 服务器获取最新论文
- **ResearchVideoAgent**：通过 MCP YouTube 服务器搜索相关视频
- **ContentIntegrationAgent**：使用 GPT-4 整合内容生成博客

## 技术栈

- **LangChain**: 智能体框架和工具链
- **LangGraph**: 多智能体工作流编排
- **MCP**: 模型上下文协议，统一外部服务接口
- **FastMCP**: MCP 服务器快速开发框架
- **OpenAI GPT-4**: 内容生成和整合


使用方法
安装依赖：

bash
uv sync
配置环境变量：
创建 .env 文件并添加你的 OpenAI API Key：

text
OPENAI_API_KEY=your_api_key_here
运行系统：

bash
uv run python main.py
按提示输入：

研究领域（如：machine learning, natural language processing）

时间范围（默认7天）

系统将自动：

🔍 搜索最新的学术论文

🎥 找到相关的研究视频

📝 生成完整的博客文章

💾 保存结果到本地文件

核心特性
并行处理：论文和视频检索同时进行，提高效率

MCP 集成：使用标准化协议连接 ArXiv 和 YouTube 服务

智能整合：GPT-4 驱动的内容生成和结构化输出

模块化设计：易于扩展和维护的架构

实时数据：获取最新几天内的研究成果