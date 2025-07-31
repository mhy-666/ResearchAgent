# ResearchAgent / 研究智能体

[English](#english) | [中文](#中文)

---

## English

### Overview

ResearchAgent is a multi-agent research system that automatically discovers, analyzes, and synthesizes the latest academic research and educational content. It combines paper retrieval from ArXiv with video content from YouTube to create comprehensive research summaries.

### System Architecture

The system uses LangGraph multi-agent architecture with the following components:

- **PaperRetrievalAgent**: Retrieves latest papers through MCP ArXiv server
- **ResearchVideoAgent**: Searches related videos through MCP YouTube server  
- **ContentIntegrationAgent**: Uses GPT-4 to integrate content and generate blog posts

### Technology Stack

- **LangChain**: Agent framework and toolchain
- **LangGraph**: Multi-agent workflow orchestration
- **MCP**: Model Context Protocol for unified external service interfaces
- **FastMCP**: Rapid MCP server development framework
- **OpenAI GPT-4**: Content generation and integration

### Installation & Setup

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Configure Environment Variables**:
   Create a `.env` file and add your OpenAI API Key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Run the System**:
   ```bash
   uv run python main.py
   ```

### Usage

1. **Input Research Domain**: Enter your research area (e.g., machine learning, natural language processing)
2. **Set Time Range**: Specify the time range (default: 7 days)
3. **Automatic Processing**: The system will:
   - 🔍 Search for latest academic papers
   - 🎥 Find related research videos
   - 📝 Generate comprehensive blog articles
   - 💾 Save results to local files

### Core Features

- **Parallel Processing**: Paper and video retrieval run simultaneously for efficiency
- **MCP Integration**: Uses standardized protocols to connect ArXiv and YouTube services
- **Intelligent Integration**: GPT-4-driven content generation and structured output
- **Modular Design**: Easily extensible and maintainable architecture
- **Real-time Data**: Retrieves research from the latest few days

---

## 中文

### 概述

ResearchAgent 是一个多智能体研究系统，能够自动发现、分析和综合最新的学术研究和教育内容。它结合了来自 ArXiv 的论文检索和来自 YouTube 的视频内容，创建全面的研究摘要。

### 系统架构

系统采用 LangGraph 多智能体架构，包含以下组件：

- **PaperRetrievalAgent**：通过 MCP ArXiv 服务器获取最新论文
- **ResearchVideoAgent**：通过 MCP YouTube 服务器搜索相关视频
- **ContentIntegrationAgent**：使用 GPT-4 整合内容生成博客

### 技术栈

- **LangChain**：智能体框架和工具链
- **LangGraph**：多智能体工作流编排
- **MCP**：模型上下文协议，统一外部服务接口
- **FastMCP**：MCP 服务器快速开发框架
- **OpenAI GPT-4**：内容生成和整合

### 安装与配置

1. **安装依赖**：
   ```bash
   uv sync
   ```

2. **配置环境变量**：
   创建 `.env` 文件并添加你的 OpenAI API Key：
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

3. **运行系统**：
   ```bash
   uv run python main.py
   ```

### 使用方法

1. **输入研究领域**：输入你的研究领域（如：机器学习、自然语言处理）
2. **设置时间范围**：指定时间范围（默认：7天）
3. **自动处理**：系统将：
   - 🔍 搜索最新的学术论文
   - 🎥 找到相关的研究视频
   - 📝 生成完整的博客文章
   - 💾 保存结果到本地文件

### 核心特性

- **并行处理**：论文和视频检索同时进行，提高效率
- **MCP 集成**：使用标准化协议连接 ArXiv 和 YouTube 服务
- **智能整合**：GPT-4 驱动的内容生成和结构化输出
- **模块化设计**：易于扩展和维护的架构
- **实时数据**：获取最新几天内的研究成果

---

## License / 许可证

MIT License / MIT 许可证