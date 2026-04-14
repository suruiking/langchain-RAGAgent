
"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复

接收用户的问题 → 去向量库检索相关资料 → 把问题 + 资料一起发给大模型 → 让模型基于资料生成专业回答（不胡说八道）。

"""
# 文档格式
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
# 向量库服务
from rag.vector_store import VectorStoreService
# 加载RAG专用提示词
from utils.prompt_loader import load_rag_prompts
# 提示词模板
from langchain_core.prompts import PromptTemplate
# 通义千问聊天模型
from model.factory import chat_model


#封装好的RAG 问答服务
class RagSummarizeService(object):
    def __init__(self):
        # 1. 连接向量库
        self.vector_store = VectorStoreService()
        # 2. 获取检索器
        self.retriever = self.vector_store.get_retriever()
         # 3. 加载 RAG 提示词
        self.prompt_text = load_rag_prompts()
         # 4. 创建提示词模板
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
         # 5. 加载聊天大模型
        self.model = chat_model
         # 6. 组装流水线
        self.chain = self._init_chain()
   
    #初始化流水线
    def _init_chain(self):
         # 提示词模板 → 打印提示词（调试）→ 发给模型 → 转成纯文本
        chain = self.chain = self.prompt_template | self.model | StrOutputParser()
        return chain

    # 检索
    def retriever_docs(self, query: str) -> list[Document]:
         
        return self.retriever.invoke(query)

    #最终问答入口
    def rag_summarize(self, query: str) -> str:

        # 1. 根据用户问题，检索相关文档
        context_docs = self.retriever_docs(query)
        
         # 2. 把所有检索到的资料，拼接成一段文本
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】: 参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"

        # 3. 把【用户问题】和【参考资料】填入模板 → 丢给模型 → 返回答案
        #就是先根据用户问题检索文档。然后把文档和问题都发给大模型
        #流水线
        return self.chain.invoke(
            {
                "input": query,
                "context": context,
            }
        )

