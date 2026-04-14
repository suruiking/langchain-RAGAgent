# 抽象基类工具（核心：定义统一接口）
from abc import ABC, abstractmethod
 # 类型注解：表示返回值可以是指定类型 或 None
from typing import Optional
 # 加载.env环境变量（存API密钥）
from dotenv import load_dotenv, find_dotenv
#langchain嵌入模型基类
from langchain_core.embeddings import Embeddings
 # 通义聊天模型基类
from langchain_community.chat_models.tongyi import BaseChatModel
 # 通义向量嵌入模型
from langchain_community.embeddings import DashScopeEmbeddings
# 通义聊天大模型
from langchain_community.chat_models.tongyi import ChatTongyi
# 从配置文件读取模型名称
from utils.config_handler import rag_conf

 # 自动查找并加载项目根目录的.env文件
load_dotenv(find_dotenv())


#抽象类，不能直接实例化，只能被继承；
class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass

#聊天模型工厂
class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_conf["chat_model_name"])

#嵌入模型工厂
class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])

# 最终创建可用的模型实例
#.generator()是执行
chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()
