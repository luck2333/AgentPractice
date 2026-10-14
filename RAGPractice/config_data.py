#配置文件，记录诸如md5.txt文件的路径等信息

# chroma
md5_path = "./md5.txt"
collection_name = "test"
persist_directory = "./chroma_db"

#splitter

chunk_size = 1000 # 分割后的文本段最大长度
chunk_overlap = 100  # 连续文本段之间的字符重叠数量
# separators = ["\n\n", "\n", "。", "？", "！", "?", "!", ",", "，"]  # 自然段落划分的符号
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
max_splitter_char_number = 1000  #文本分割的阈值，超过该阈值才进行分割
