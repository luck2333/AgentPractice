"""

基于steamlit完成WEB网页文件上传的功能

streamlit 可以用简单的几行代码实现一个效果不错的web网页，简单易用。

使用方法：在命令行中app_files_uploader.py的根目录下执行 streamlit run app_files_uploader.py指令

"""
import time

import streamlit as st

from knowledge_base import KnowledgeBaseService

#添加网页标题
st.title("知识库更新服务")

# 添加一个文件上传组件框
uploader_file = st.file_uploader(
    "请选择要上传的文件",   # 组件框的提示语
    type=["csv", "txt"],
    accept_multiple_files=False   # 是否允许上传多个文件
)

#创建KnowledgeBaseService对象，存入session_state中，防止streamlit重新加载时，service对象多次重建
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


if uploader_file is not None:
    file_name = uploader_file.name
    file_size = uploader_file.size / 1024
    file_type = uploader_file.type
    # file_content = uploader_file.read().decode("utf-8")# read() 像用手指一行行读，手指会停在读到的位置，下次接着从那儿读；getvalue() 像拍一张整页的照片，不管手指在哪，拍出来永远是完整一页。
    text = uploader_file.getvalue().decode("utf-8")

    st.subheader(f"文件名：{file_name}")  # 以副标题格式显示文件名
    st.write(f"文件大小: {file_size:.2f}KB")  # 以普通文本格式显示文件大小
    st.write(f"文件类型: {file_type}") # 以普通文本格式显示文件类型
    st.write(f"文件内容: {text}") # 以普通文本格式显示文件内容

    # """使用KnowledgeBaseService对象，调用upload_by_str方法，传入文件内容和文件名"""
    with st.spinner("正在上传知识库中。。。"):
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, file_name)

        st.write(result)

