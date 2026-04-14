#创造智能体
from langchain.agents import create_agent
from model.factory import chat_model
#系统提示词
from utils.prompt_loader import load_system_prompts
# 导入7个AI工具
from agent.tools.agent_tools import (rag_summarize, get_weather, get_user_location, get_user_id,
                                     get_current_month, fetch_external_data, fill_context_for_report)
## 导入3个中间件（监控、日志、动态提示词）                                     
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch


"""
1.把大模型、所有工具、中间件、提示词拼装成一个完整的智能体
2.提供流式输出接口，逐字返回 AI 的回答
3.初始化上下文，支持报告场景自动切换

"""

#AI 智能体本体
class ReactAgent:
    #组装智能体
    def __init__(self):
        self.agent = create_agent(
            # 1. 大脑：通义千问大模型
            model=chat_model,
              # 2. 基础人设：系统提示词
            system_prompt=load_system_prompts(),
             # 3. 工具库：给AI配备的7个工具
            tools=[rag_summarize, get_weather, get_user_location, get_user_id,
                   get_current_month, fetch_external_data, fill_context_for_report],
            # 4. 管家团：3个中间件
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )
        
    #流式输出回答
    def execute_stream(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }

        # 第三个参数context就是上下文runtime中的信息，就是我们做提示词切换的标记
        #self.agent.stream() 是 agent 的流式运行，stream_mode="values"按「数据块」返回回答
        #context={"report": False}，关闭额外的日志 / 报告，只返回纯回答
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                # 把大模型返回的片段，流式吐出去
                yield latest_message.content.strip() + "\n"



