main_prompt.txt（主提示词） 这是 Agent 的核心人设和行为规则，包含：

角色定义：扫地机器人专业客服
ReAct 思考流程约束
7个工具的详细使用说明和调用规则
报告生成的固定执行流程（这是关键约束）
输出格式规则

rag_summarize.txt（RAG 提示词） 专门给 RAG 检索用，用 {input} 和 {context} 两个占位符，这就是你学的 PromptTemplate 的实际应用。约束模型只能基于检索到的资料回答，不能编造。

报告提示词（路径有问题读不到，但从 middleware 里知道） 当用户触发报告场景时，report_prompt_switch 中间件会把 main_prompt 换成这个，专门用于生成使用报告。

普通对话用 main_prompt，报告场景自动切换到 report_prompt