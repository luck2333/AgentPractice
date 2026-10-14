import os
from datetime import datetime

from langchain_chroma import Chroma

import config_data as config
import hashlib
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def check_md5(md5_str:str):  #md5值查重,检查传入文件的md5值是否已经被处理过
    if not os.path.exists(config.md5_path):
        # md5.txt文件都不存在，说明此时知识库为空，即该md5值不存在
        return False  #返回False，表示该md5值不存在
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()     # 处理字符串两端的空格和回车
            if line == md5_str:
                return True         # 已处理过
        return False


def save_md5(md5_str:str):  #保存md5值
    with open(config.md5_path,'a',encoding='utf-8') as f:  # ‘a’表示将写入指针指向文件末尾，如果以'w'格式打开则会将文件清空，然后把指针指向最开头
        f.write(md5_str + '\n')  # 写入md5值，并换行
    return True


def get_string_md5(input_str: str, encoding='utf-8'):  #获取字符串的md5值
    str_bytes = input_str.encode(encoding=encoding)  # 将字符串转为bytes字节数组，用于hashlib库进行md5的计算
    md5_obj = hashlib.md5()  # 创建md5对象
    md5_obj.update(str_bytes)  # 更新内容（传入即将要转换的字节数组）
    md5_hex = md5_obj.hexdigest()  # 得到md5的十六进制字符串
    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory,exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory,
        )  # 向量存储的实例 chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,# 分割后的文本段最大长度
            chunk_overlap=config.chunk_overlap,  #相邻文本段之间的字符重叠数量
            separators=config.separators, # 自然段落的分割符
            length_function=len  # 使用python自带的len函数计算文本长度
            ) # 文本分割器的对象
    def upload_by_str(self, data:str, filename):
        """将传入的字符串，进行向量化，存入向量数据库中"""
        # 先得到字符串的md5值
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "（跳过），内容库已存在该文件的md5值"
        if len(data) > config.max_splitter_char_number:
            """大于文本分割阈值，需要进行分割"""
            knowledge_chunks:list[str] = self.spliter.split_text(data)  #使用spliter内置的分割函数对字符串进行分割
        else:
            """小于文本分割阈值，不进行分割,直接把整个data作为一个知识块塞到列表里"""
            knowledge_chunks = [data]

        metadata = {
            "source" : filename,
            "create_time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator" : "luck233"
        }# 元信息，用于存储文件来源、创建时间、操作人等信息

        self.chroma.add_texts(  # 运行完该函数后，对应文档就存入知识库里了
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks] #对同文档中的每个知识块都创建一个metadata，用列表metadatas保存
        )

        save_md5(md5_hex)  # 保存md5值到文件中

        return f"（成功），已成功将文件{filename}的md5值{md5_hex}存入知识库"

if __name__ == "__main__":
    service = KnowledgeBaseService()
    r = service.upload_by_str("周杰轮222", "testfile")
    print(r)