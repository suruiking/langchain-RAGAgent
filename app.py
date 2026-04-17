import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# 控制流式打字的延迟效果
import time
# Python前端框架：快速生成网页
import streamlit as st
# 导入你写的AI智能体
from agent.react_agent import ReactAgent

"""
这是用 Streamlit（Python 快速网页框架）写的 AI 智能客服前端页面！
它是你整个项目的最终入口：把后面所有的智能体、工具、向量库、提示词，
封装成一个用户能直接聊天的网页窗口，实现可视化交互、历史对话记录、流式打字效果。

"""

# 标题
st.title("智扫通机器人智能客服")
# 分割线（美观用）
st.divider()

# 1. 只创建一次AI智能体，避免重复初始化
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

# 2. 保存聊天历史消息
if "message" not in st.session_state:
    st.session_state["message"] = []

# 循环遍历历史消息，展示在页面上
for message in st.session_state["message"]:
    # 根据角色（user/assistant）展示不同样式的消息
    #创建一个聊天气泡框，write把文字内容写进刚才创建的气泡框里
    st.chat_message(message["role"]).write(message["content"])

""" 接收用户输入 """
prompt = st.chat_input()

#最大长度
MAX_HISTORY=20
if len(st.session_state["message"])>MAX_HISTORY:
    # 超过则只保留最新的20条消息
    st.session_state["message"]=st.session_state["message"][-MAX_HISTORY:]
    # 如果用户输入了内容
if prompt:
       # 1. 展示用户发送的消息
    st.chat_message("user").write(prompt)
     # 2. 把用户消息保存到历史记录
    st.session_state["message"].append({"role": "user", "content": prompt})

     # 存储AI的响应内容
    response_messages = []
     # 显示加载动画：智能客服思考中...
    with st.spinner("智能客服思考中..."):
        # 返回生成器，包含最终答案
        res_stream = st.session_state["agent"].execute_stream(prompt)
        
         # 捕获流式内容 + 添加打字延迟效果
        def capture(generator, cache_list):

            for chunk in generator:     # 遍历AI返回的每一段文字
                cache_list.append(chunk)# 缓存回答

                for char in chunk: # 逐字输出
                    time.sleep(0.01) # 控制打字速度
                    yield char# 逐字返回给前端

        # 3. 流式展示AI的回答（逐字打字效果）
        #传入回答和response_messages空列表
        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
         # 4. 把AI回答保存到历史记录
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})
        # 5. 刷新页面，展示最新对话
        st.rerun()
