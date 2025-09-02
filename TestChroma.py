from langchain.vectorstores import Chroma
# 注意：此处的嵌入模型必须与创建数据库时使用的一致（如阿里云嵌入服务、all-MiniLM等）
from langchain_community.embeddings import DashScopeEmbeddings  # 以阿里云为例，替换为你实际使用的嵌入类

# 模型设置相关
API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"
API_KEY = "sk-dd5ce984d600440980a3e6c2f97f0bc3"
EMBEDDING_MODEL = "text-embedding-v4"


# 1. 初始化与创建时相同的嵌入模型（参数必须一致）
embeddings = DashScopeEmbeddings(
        model=EMBEDDING_MODEL,
        dashscope_api_key=API_KEY,
        # other params...
    )

# 2. 加载本地持久化的Chroma数据库
vector_db = Chroma(
    persist_directory="./travel_chroma_db",  # 本地存储目录（与创建时一致）
    embedding_function=embeddings  # 与创建时相同的嵌入模型
)

def test_chroma_retrieval(query):
    
    print(f"\n=== 检索查询：{query} ===")
    # 检索相关性最高的3条结果
    results = vector_db.similarity_search(query, k=3)
    for i, doc in enumerate(results, 1):
        print(f"结果{i}：{doc.page_content}")
        # 打印文档元数据（如城市、类型等，创建时存入的额外信息）
        print(f"元数据：{doc.metadata}\n")

if __name__ == "__main__":
    # 测试几个典型查询（根据你的旅游数据内容调整）
    test_queries = [
        "成都大熊猫基地门票",
        "锦里古街开放时间",
        "成都不吃辣的美食"
    ]

    # 执行测试
    for query in test_queries:
        test_chroma_retrieval(query)