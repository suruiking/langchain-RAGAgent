from typing import Callable
from utils.prompt_loader import load_system_prompts, load_report_prompts
from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger


"""
给AI 智能体（Agent） 加的 **「智能管家 / 监控器 / 场景开关」**，
负责：监控工具调用、打印调试日志、自动切换提示词场景。

1.监控 AI 的所有工具调用（日志 + 标记报告场景）
2.AI 调用大模型前打印日志（调试用）
3.根据场景自动切换系统提示词（普通对话 / 生成报告）

"""

#三个 @ 就是系统的自动开关：

#监控 AI 所有工具调用，标记报告场景
#工具调用装饰器
@wrap_tool_call
def monitor_tool(
        # 请求的数据封装
        request: ToolCallRequest,
        # 执行的函数本身
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:   
           # 打印日志：AI 要用哪个工具、传了什么参数
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}调用成功")

        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context["report"] = True

        return result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败，原因：{str(e)}")
        raise e


#AI 调用模型前，打印调试日志
#模型调用前装饰器
@before_model
def log_before_model(
        state: AgentState,          # 整个Agent智能体中的状态记录
        runtime: Runtime,           # 记录了整个执行过程中的上下文信息
):         
 # 打印：AI 马上要问大模型了，带了多少条聊天记录
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息。")

    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")

    return None

#自动切换提示词（普通对话 / 报告生成）
#动态提示词装饰器
@dynamic_prompt                 # 每一次在生成提示词之前，调用此函数
def report_prompt_switch(request: ModelRequest):     
     # 看一下：刚才有没有标记【报告场景】？
    is_report = request.runtime.context.get("report", False)
    if is_report:               
         # 是报告场景 → 加载【报告专用提示词】
        return load_report_prompts()
    else:  
        # 普通聊天 → 加载【系统对话提示词】
        return load_system_prompts()
