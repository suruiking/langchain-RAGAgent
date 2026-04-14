"""
yaml
k: v
"""
 # 核心：Python解析YAML文件的库
 #yaml：把 .yml 配置文件 → 转换成 Python 字典；
import yaml
# 自定义工具：获取文件【绝对路径】
from utils.path_tool import get_abs_path

## 加载 RAG 核心配置（模型名称、API参数等）
def load_rag_config(config_path: str=get_abs_path("config/rag.yml"), encoding: str="utf-8"):
    #打开文件夹
    with open(config_path, "r", encoding=encoding) as f:
        #把yaml解析为python字典，FullLoader：安全解析。
        return yaml.load(f, Loader=yaml.FullLoader)


# 加载向量库 Chroma 配置
def load_chroma_config(config_path: str=get_abs_path("config/chroma.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# 加载提示词 Prompt 配置
def load_prompts_config(config_path: str=get_abs_path("config/prompts.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# 加载智能体 Agent 配置
def load_agent_config(config_path: str=get_abs_path("config/agent.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


#直接调用函数，加载好所有配置，全局可用
rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()


