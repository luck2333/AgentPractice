from langchain_ollama import OllamaLLM
model = OllamaLLM(model="qwen3.5:9B")

res = model.stream("你是否支持多模态功能？能否读取表格截图里的信息？")

for item in res:
    print(item, end="", flush=True)