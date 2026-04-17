# # Python官方内置的日志库（标准模块，不用安装）
import logging
##获取项目绝对路径（你之前的工具）
from utils.path_tool import get_abs_path
import os
#获取当前时间，用于按天生成日志文件
from datetime import datetime

"""
项目的标准化日志管理工具，核心功能：
日志同时打印到控制台 + 保存到本地文件；
自动创建 logs 文件夹，按天生成日志文件；
统一日志格式（包含时间、文件名、行号、错误信息）；
全局共用一个日志器，避免重复打印。
DEBUG（调试）< INFO（普通信息）< WARNING（警告）< ERROR（错误）< CRITICAL（严重错误）
"""



# 日志保存的根目录
LOG_ROOT = get_abs_path("logs")

# 确保日志的目录存在,如果不存在就自动创建，存在就不报错（exist_ok=True）
os.makedirs(LOG_ROOT, exist_ok=True)

# 日志的格式配置  2026-04-05 10:00:00,123 - agent - INFO - file_tool.py:20 - 信息日志
#levelname日志级别（INFO/ERROR/DEBUG）
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

#（创建日志器）
def get_logger(
        name: str = "agent", # 日志器名称
        console_level: int = logging.INFO,  # 控制台只打印 INFO及以上 级别
        file_level: int = logging.DEBUG,    # 文件保存 DEBUG及以上 所有级别
        log_file = None,                    # 日志文件路径，默认自动生成
) -> logging.Logger:
    # 1. 创建日志器对象
    logger = logging.getLogger(name)
    # 2. 设置日志器最低级别：DEBUG（所有级别都处理）
    logger.setLevel(logging.DEBUG)

     # 3. 关键：避免重复添加处理器（防止日志打印多次）
    if logger.handlers:
        return logger

    # ===================== 控制台处理器：专门管屏幕打印=====================
    console_handler = logging.StreamHandler()# 控制台处理器
    console_handler.setLevel(console_level)# 控制台级别：INFO
    console_handler.setFormatter(DEFAULT_LOG_FORMAT) # 设置格式

    logger.addHandler(console_handler)# 把控制台处理器添加到日志器


    # ===================== 文件处理器：专门管文件保存=====================
    if not log_file:        # 日志文件的存放路径
         # 自动生成日志文件名：logs/agent_20260405.log（按天命名）
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    #创建一个工具，把日志写进指定的文件
    #logging.FileHandler 这个工具自带文件写入功能
    file_handler = logging.FileHandler(log_file, encoding='utf-8') # 文件处理器
    file_handler.setLevel(file_level)# 文件级别：DEBUG
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)# 设置格式

    logger.addHandler(file_handler)# 把文件处理器添加到日志器

    return logger


# 快捷获取日志器
logger = get_logger()

