from openai import OpenAI

#1.获取client对象，即OpenAI类对象
client = OpenAI(
    base_url="https://llm-eh2erc31w68kmwrz.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
#2.调用参数
response = client.chat.completions.create(
    model="qwen3.7-max",
    messages=[
        {"role":"system", "content":"你是一个专业的agent工程师，并且不说废话"},
        {"role":"assistant", "content":"好的，我是专业agent工程师，你要问什么？"},
        {"role":"user", "content":"告诉我一名agent实习生需要具备什么前备知识？"}
    ]
)
#3. 处理结果
print(response.choices[0].message.content)