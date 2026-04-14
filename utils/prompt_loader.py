#1. 导入提示词配置：从prompts.yml读取提示词文件路径
from utils.config_handler import prompts_conf
# 2. 导入路径工具：把相对路径转绝对路径，防止文件找不到
from utils.path_tool import get_abs_path
# 3. 导入日志工具：记录错误信息，方便排查bug
from utils.logger_handler import logger

"""
统一加载本地的大模型提示词文件，把提示词内容读取出来供模型使用，
同时做了完善的异常排查 + 日志记录，保证项目运行稳定。

"""

# 给大模型设定基础角色 / 规则
def load_system_prompts():
     # 第一步：从配置中读取提示词路径，捕获「配置项缺失」错误
    try:
          # 从prompts.yml拿路径 → 转绝对路径
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
         # 配置里没有main_prompt_path，打印错误日志，抛出异常终止程序
        logger.error(f"[load_system_prompts]在yaml配置项中没有main_prompt_path配置项")
        raise e

  # 第二步：读取提示词文件内容，捕获「文件读取失败」错误
    try:
         # 打开文件，UTF-8编码（防中文乱码），读取全部文本
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
         # 文件不存在/损坏/权限不足，打印日志，抛出异常
        logger.error(f"[load_system_prompts]解析系统提示词出错，{str(e)}")
        raise e

#专门给RAG 检索用的提示词
def load_rag_prompts():
     # 第一步：从配置中读取提示词路径，捕获「配置项缺失」错误
    try:
         # 从prompts.yml拿路径 → 转绝对路径
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
          # 配置里没有main_prompt_path，打印错误日志，抛出异常终止程序
        logger.error(f"[load_rag_prompts]在yaml配置项中没有rag_summarize_prompt_path配置项")
        raise e

    try:
          # 打开文件，UTF-8编码（防中文乱码），读取全部文本
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        # 文件不存在/损坏/权限不足，打印日志，抛出异常
        logger.error(f"[load_rag_prompts]解析RAG总结提示词出错，{str(e)}")
        raise e

#专门给生成报告用的提示词
def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompts]在yaml配置项中没有report_prompt_path配置项")
        raise e

    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompts]解析报告生成提示词出错，{str(e)}")
        raise e


