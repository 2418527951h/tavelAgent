
def union():
    """
    合并数据
    """
    import pandas as pd
    # 读取所有城市的旅游数据
    df_hotel = pd.read_csv("data/chengdu/hotel.csv")
    df_spots = pd.read_csv("data/chengdu/travel_spots.csv")
    df_restaurant = pd.read_csv("data/chengdu/restaurant.csv")
    # 合并为一个DataFrame
    df_clean = pd.concat([df_hotel, df_spots, df_restaurant], ignore_index=True)
    # 1. 处理NaN空值：将NaN替换为占位文本（如"无内容"）
    df_clean["content"] = df_clean["content"].fillna("无内容")

    # 2. 确保所有值都是字符串类型：强制转换为str
    df_clean["content"] = df_clean["content"].astype(str)

    # 3. （可选）去除纯空白字符串（如果有）
    df_clean = df_clean[df_clean["content"].str.strip() != ""]

    return df_clean


def createDB(df_clean):
    """
    构建向量数据库
    """
    from langchain_community.vectorstores import Chroma
    from langchain.text_splitter import CharacterTextSplitter
    from langchain_community.document_loaders import DataFrameLoader
    # 导入阿里云嵌入模型适配类
    from langchain_community.embeddings import DashScopeEmbeddings

    # 模型设置相关
    API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    API_KEY = "sk-dd5ce984d600440980a3e6c2f97f0bc3"
    EMBEDDING_MODEL = "text-embedding-v4"

    # 1. 加载清洗后的数据（用LangChain的DataFrameLoader读取CSV）
    loader = DataFrameLoader(df_clean, page_content_column="content")  # "content"是检索用的文本
    documents = loader.load()

    # 2. 文本分割
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)  # 每100字分割一段
    split_docs = text_splitter.split_documents(documents)

    # 3. 选择嵌入模型（推荐开源的all-MiniLM-L6-v2，轻量且效果好）
    # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings = DashScopeEmbeddings(
        model=EMBEDDING_MODEL,
        dashscope_api_key=API_KEY,
        # other params...
    )


    # 4. 构建Chroma向量库并保存到本地（后续可直接加载）
    vector_db = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory="./travel_chroma_db"  # 保存路径（本地文件夹）
    )
    vector_db.persist()  # 持久化存储（确保关闭程序后数据不丢失）
    print("Chroma向量库构建完成！")


if __name__ == "__main__":
    df = union()
    createDB(df)
    