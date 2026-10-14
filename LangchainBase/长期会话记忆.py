import os, json
from typing import Sequence

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
'''

class FileChatMessageHistory(BaseChatMessageHistory):
    storage_path: str
    session_id: str

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(
                    os.path.join(self.storage_path, self.session_id),
                    "r",
                    encoding="utf-8",
            ) as f:
                messages_data = json.load(f)
            return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def add_messages(self,) -> None:
        all_messages = list(self.messages)  # Existing messages
        all_messages.extend(messages)  # Add new messages

        serialized = [message_to_dict(message) for message in all_messages]
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f)

    def clear(self) -> None:
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


'''
class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id = session_id        # 会话id
        self.storage_path = storage_path    # 不同会话id的存储文件，所在的文件夹路径
        # 完整的文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)

        #创建该文件夹，如果存在则不操作
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    # 将消息写入文件
    def add_messages(self,messages:Sequence[BaseMessage]):
        all_messages = list(self.messages) #现将类中已有的消息存入all_messages中
        all_messages.extend(messages) #将新消息添加到all_messages中

        new_messages = [message_to_dict(message) for message in all_messages] # 遍历消息，将其转换为字典，存储在列表里
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(new_messages,f) # 将消息列表整体写入文件

    @property   # 将 messages 方法转为只读属性，外部可通过 self.messages 直接访问（无需加括号调用）
    def messages(self) -> list[BaseMessage]:
        """从本地 JSON 文件中读取并还原该会话的全部历史消息"""
        try:
            # 打开该会话对应的持久化文件
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)            # 读取文件内容，解析为 list[dict]
            return messages_from_dict(messages_data)     # 将 list[dict] 还原为 list[BaseMessage] 并返回
        except FileNotFoundError:
            # 首次运行，文件尚不存在，返回空列表
            return []

    def clear(self) -> None:
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f)


model = ChatTongyi(model="qwen3.7-max")
# prompt = PromptTemplate.from_template(
#     "你需要根据会话历史回应用户问题。对话历史：{chat_history}，用户提问：{input}，请回答"
# )
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史回应用户问题。对话历史："),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{input}")
    ]
)

str_parser = StrOutputParser()


def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(), "="*20)
    return full_prompt


base_chain = prompt | print_prompt | model | str_parser


def get_history(session_id):
    return FileChatMessageHistory(session_id, "../history")

# 创建一个新的链，对原有链增强功能：自动附加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain,     # 被增强的原有chain
    get_history,    # 通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="input",             # 表示用户输入在模板中的占位符
    history_messages_key="chat_history"     # 表示用户输入在模板中的占位符
)


if __name__ == '__main__':
    # 固定格式，添加LangChain的配置，为当前程序配置所属的session_id
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }

    # res = conversation_chain.invoke({"input": "小明有2个猫"}, session_config)
    # print("第1次执行：", res)
    #
    # res = conversation_chain.invoke({"input": "小刚有1只狗"}, session_config)
    # print("第2次执行：", res)

    res = conversation_chain.invoke({"input": "总共有几个宠物"}, session_config)
    print("第3次执行：", res)
