from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

vector_store = Chroma(
    collection_name="test",             # 指定向量存储的名称
    embedding_function = DashScopeEmbeddings(),  # 指定向量存储的嵌入模型
    persist_directory="./chroma_data"   # 指定向量存储的本地存储路径
)

loader = CSVLoader(
    file_path="../AI大模型RAG与智能体开发/P3_LangChainRAG开发/data/info.csv",
    encoding="utf-8",
    source_column="source",     # 指定本条数据的来源是csv中的哪个key
)

documents = loader.load()  #将csv中的数据加载为document对象的列表

# document对象要使用id标记：id1 id2 id3 id4 ...
# 向量存储的 新增、删除、检索
vector_store.add_documents(
    documents=documents,        # 被添加的文档，类型：list[Document]
    ids = ["id"+str(i) for i in range(1,1+len(documents))]   # 给添加的文档提供id（字符串）  list[str]
)

#删除 使用idx进行删除操作：
vector_store.delete(["id1", "id2"])   # 以id访问需要删除的文档

# 相似度检索 返回类型list[Document]
result = vector_store.similarity_search(
    "瑞达法",
    3,       # 检索的结果要几个
    filter={"source": "黑马程序员"})  # 过滤条件:只在source为黑马程序员的条目中检索
print(result)


data = vector_store.get(
    include=["documents","metadatas"]
)

print(data)