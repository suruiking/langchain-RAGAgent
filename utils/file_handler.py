#操作系统文件/文件夹操作（核心：找文件、读文件、判断路径）
import os
# 计算文件MD5（生成文件唯一指纹）
import hashlib
#日志工具（打印错误/提示信息）
from utils.logger_handler import logger
# LangChain标准文档格式（RAG专用）
from langchain_core.documents import Document
# PDF/TXT加载器
from langchain_community.document_loaders import PyPDFLoader, TextLoader


 #计算文件的 MD5 唯一标识，用于文件去重
def get_file_md5_hex(filepath: str):     

 # 1. 判断文件是否存在
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件{filepath}不存在")
        return

 # 2. 判断路径是不是文件（排除文件夹）
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径{filepath}不是文件")
        return

    # 3. 创建MD5计算对象
    md5_obj = hashlib.md5()

    # 4. 分片大小：4KB（避免大文件占满内存）
    chunk_size = 4096       
    try:
         # 5. 二进制模式读取文件（所有文件都必须用rb，包括PDF/图片/文本）
        with open(filepath, "rb") as f:     
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)

            """
            chunk = f.read(chunk_size)
            while chunk:
                
                md5_obj.update(chunk)
                chunk = f.read(chunk_size)
            """
            # 6. 转换成十六进制字符串（最终的MD5标识）
            md5_hex = md5_obj.hexdigest()
            return md5_hex
     # 异常捕获：文件损坏、权限不足等
    except Exception as e:
        logger.error(f"计算文件{filepath}md5失败，{str(e)}")
        return None

#遍历一个文件夹，只保留你允许的文件类型
#筛选出所有 PDF/TXT 文件；
def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):  
    files = []

 # 1. 判断路径是不是文件夹
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return allowed_types

 # 2. 遍历文件夹里的所有文件
    for f in os.listdir(path):
         # 3. 判断文件后缀是否在允许的列表里（如 .pdf, .txt）
        if f.endswith(allowed_types):
             # 拼接完整文件路径（如：data/1.pdf）
            files.append(os.path.join(path, f))

# 4. 返回符合要求的文件路径（元组格式）
    return tuple(files)

#加载 PDF 文件，把文件转成 Document，转成文档才能分割
def pdf_loader(filepath: str, passwd=None) -> list[Document]:
    return PyPDFLoader(filepath, passwd).load()

#加载 TXT 文件，把文件转成 Document
def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()
