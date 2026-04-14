cd "f:\1017\agent项目\扫地机器人项目\04扫地"

@"
# 智扫通机器人智能客服

基于 LangChain + ReAct 架构的扫地机器人智能客服系统，支持 RAG 知识检索、工具调用和使用报告生成。

## 功能特性

- ReAct 智能体：思考 → 工具调用 → 观察 → 回答的完整循环
- RAG 知识库：基于 ChromaDB 的向量检索，回答产品相关问题
- 工具系统：7 个专业工具，覆盖故障排查、使用记录查询等场景
- 报告生成：自动切换提示词，生成结构化使用报告
- 流式输出：逐字打字效果，提升交互体验
- Streamlit 前端：开箱即用的聊天界面

## 项目结构

\`\`\`
04扫地/
├── app.py              # 主入口（Streamlit）
├── agent/
│   ├── react_agent.py  # ReAct 智能体核心
│   └── tools/          # 工具定义与中间件
├── rag/                # RAG 检索服务 + 向量库
├── config/             # 配置文件（agent/rag/prompts）
├── prompts/            # 提示词模板
├── data/               # 外部数据（用户使用记录）
└── utils/              # 日志工具
\`\`\`

## 快速开始

1. 安装依赖

\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. 配置环境变量

复制 \`.env.example\` 为 \`.env\`，填入你的 API Key：

\`\`\`
OPENAI_API_KEY=your_api_key_here
\`\`\`

3. 启动应用

\`\`\`bash
streamlit run app.py
\`\`\`

浏览器访问 http://localhost:8501

## 技术栈

- LangChain
- ChromaDB
- Streamlit
- Python 3.11+
"@ | Out-File -FilePath README.md -Encoding utf8
