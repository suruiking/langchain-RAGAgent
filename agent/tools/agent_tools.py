import os
 # 日志
from utils.logger_handler import logger
from langchain_core.tools import tool
# 你的RAG问答服务
from rag.rag_service import RagSummarizeService
# 随机生成模拟数据
import random
# 智能体配置
from utils.config_handler import agent_conf
# 路径工具
from utils.path_tool import get_abs_path

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 初始化RAG服务
rag = RagSummarizeService()

# 模拟的用户ID列表
user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010",]
# 模拟的2025年12个月份
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
             "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", ]

# 全局字典：缓存加载好的外部业务数据
external_data = {}


#RAG 知识库查询
@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)


#查天气
@tool(description="获取指定城市的实时天气，包含天气状况、气温、湿度等信息，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    #Python 最常用的发送网络请求库
    import requests
    import urllib3
    #关闭烦人的安全警告
    urllib3.disable_warnings()
    #天气翻译字典：把接口返回的英文天气 → 翻译成中文
    weather_map = {
        "Sunny": "晴天", "Clear": "晴天", "Partly cloudy": "多云",
        "Cloudy": "阴天", "Overcast": "阴天", "Mist": "薄雾",
        "Fog": "大雾", "Light rain": "小雨", "Moderate rain": "中雨",
        "Heavy rain": "大雨", "Light snow": "小雪", "Moderate snow": "中雪",
        "Heavy snow": "大雪", "Thundery outbreaks possible": "雷阵雨",
        "Blizzard": "暴风雪", "Patchy rain possible": "局部小雨",
    }
    try:
        url = f"https://wttr.in/{city}?format=j1"
        # 发送网络请求：超时5秒，不验证SSL证书
        resp = requests.get(url, timeout=5, verify=False)
        # 如果请求失败（404/500），直接抛出异常
        resp.raise_for_status()
         #  解析接口返回的JSON数据，提取核心信息
        data = resp.json()
        current = data["current_condition"][0]# 获取当前天气
        desc_en = current["weatherDesc"][0]["value"]# 英文天气描述
        desc = weather_map.get(desc_en, desc_en)# 转中文
        temp = current["temp_C"] # 摄氏度气温
        humidity = current["humidity"] # 湿度
        return f"{city}当前天气：{desc}，气温{temp}℃，湿度{humidity}%"
    except Exception as e:
        return f"天气查询失败：{str(e)}"


#获取用户所在城市
@tool(description="获取用户所在城市的名称，以纯字符串形式返回")
def get_user_location() -> str:
    return random.choice(["深圳", "合肥", "杭州"])


#获取用户 ID
@tool(description="获取用户的ID，以纯字符串形式返回")
def get_user_id() -> str:
    return random.choice(user_ids)

#获取当前月份
@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month() -> str:
    return random.choice(month_arr)

#加载外部数据函数
def generate_external_data():
    """
    {
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        ...
    }
    :return:
    """
    #读取外部 CSV 格式的用户数据文件，整理成程序能快速查询的嵌套字典格式。
   
    if not external_data:
        # 2. 找到外部CSV文件的路径
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

         # 3. 打开CSV文件，逐行读取解析
        with open(external_data_path, "r", encoding="utf-8") as f:
            #跳过表头
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")

                user_id: str = arr[0].replace('"', "")#用户ID
                feature: str = arr[1].replace('"', "")#特征
                efficiency: str = arr[2].replace('"', "")#效率
                consumables: str = arr[3].replace('"', "")#耗材
                comparison: str = arr[4].replace('"', "")#对比
                time: str = arr[5].replace('"', "")#时间
                
                  # 4. 整理成嵌套字典格式，存入全局变量 external_data
                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }

#从内存字典里按 user_id + month 查数据
@tool(description="从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回， 如果未检索到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()

    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[fetch_external_data]未能检索到用户：{user_id}在{month}的使用记录数据")
        return ""

#报告场景专用工具
@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"
