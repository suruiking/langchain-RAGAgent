# 智扫通机器人智能客服

基于 LangChain ReAct 架构的扫地机器人智能客服系统，集成 RAG 知识检索、多工具调用、动态提示词切换和流式输出。

## 技术栈

- LangChain + ReAct Agent
- ChromaDB 向量数据库
- Streamlit 前端界面
- 阿里云 DashScope（通义千问）

## 功能

- **RAG 知识库问答**：基于产品手册、故障排除、选购指南等文档进行向量检索
- **7 个专业工具**：知识检索、天气查询、用户定位、使用记录查询、报告生成等
- **动态提示词切换**：普通问答与报告生成场景自动切换系统提示词
- **中间件系统**：工具调用监控、请求日志、报告上下文注入
- **流式打字效果**：逐字输出 AI 回答，提升交互体验

## 项目结构

    04扫地/
    ├── app.py                  # 主入口（Streamlit）
    ├── requirements.txt        # 依赖列表
    ├── agent/
    │   ├── react_agent.py      # ReAct 智能体核心
    │   └── tools/
    │       ├── agent_tools.py  # 7 个工具定义
    │       └── middleware.py   # 中间件（监控/日志/提示词切换）
    ├── rag/
    │   ├── rag_service.py      # RAG 问答服务
    │   └── vector_store.py     # ChromaDB 向量存储
    ├── model/
    │   └── factory.py          # 大模型初始化
    ├── config/                 # YAML 配置文件
    ├── prompts/                # 提示词模板
    ├── data/                   # 知识库原始文档
    └── utils/                  # 日志、配置、路径工具

## 快速开始

**1. 安装依赖**

    pip install -r requirements.txt

**2. 配置 API Key**

复制 `.env.example` 为 `.env`，填入阿里云 DashScope API Key：

    DASHSCOPE_API_KEY=your_api_key_here

获取地址：https://dashscope.console.aliyun.com/

**3. 启动**

    streamlit run app.py

浏览器访问 http://localhost:8501

## 示例问题

- 扫地机器人吸力不足怎么办？
- 帮我查一下我这个月的使用报告
- 我所在城市今天适合开启扫地机器人吗？
