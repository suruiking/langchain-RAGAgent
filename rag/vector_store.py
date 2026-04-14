# 轻量级向量数据库（存向量）
from langchain_chroma import Chroma
# LangChain标准文档格式
from langchain_core.documents import Document
# 向量库配置（路径、分块大小等）
from utils.config_handler import chroma_conf
# 向量嵌入模型（之前的工厂类生成）
from model.factory import embed_model
 # 文本分割器
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 绝对路径工具
from utils.path_tool import get_abs_path
# 文件工具
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
 # 日志工具
from utils.logger_handler import logger
import os

#向量库类
class VectorStoreService:
    #初始化向量库和切割器
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_conf["persist_directory"],
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )

#生成检索器
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

#文档入库全流程
#完整流程：扫描→去重→加载→分割→入库→记录→日志
    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算文件的MD5做去重
        :return: None
        """
        #检查文件是否已经处理过（去重检查）
        def check_md5_hex(md5_for_check: str):
            # 如果MD5记录文件不存在，创建空文件
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                # 创建文件
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False            # md5 没处理过
             # 读取MD5记录文件，逐行对比
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True     # md5 处理过

                return False            # md5 没处理过

        #保存已处理文件的 MD5
        def save_md5_hex(md5_for_check: str):
             # 追加写入MD5，下次上传直接跳过
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")
        
        #根据文件类型加载文档
        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path) # 加载TXT

            if read_path.endswith("pdf"):
                return pdf_loader(read_path)# 加载PDF

            return []
        #====================正式入库====================================

        # 1. 找出所有 PDF、TXT 文件
        #声明一个变量叫 allowed_files_path，规定它必须是「存储字符串的列表」
        #listdir_with_allowed_type列出指定文件夹下，指定类型的所有文件
        allowed_files_path: list[str] = listdir_with_allowed_type(
            #去哪个文件夹找文件
            get_abs_path(chroma_conf["data_path"]),
            #只筛选哪些文件
            tuple(chroma_conf["allow_knowledge_file_type"]),
        )
       
       # 2. 遍历每一个文件
        for path in allowed_files_path:
            # 获取文件的MD5
            md5_hex = get_file_md5_hex(path)

            # 3. MD5已存在 → 跳过（去重）
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue

            try:
                # 4. 加载文件 → Document对象
                documents: list[Document] = get_file_documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue
                 
                # 5. 文本分割：长文档切小片段
                split_document: list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容，跳过")
                    continue

                # 6. 存入向量库
                self.vector_store.add_documents(split_document)

                # 7. 保存MD5，标记为已处理
                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库]{path} 内容加载成功")

            # 异常处理：文件损坏、读取失败
            except Exception as e:
                # exc_info为True会记录详细的报错堆栈，如果为False仅记录报错信息本身
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}", exc_info=True)
                continue




