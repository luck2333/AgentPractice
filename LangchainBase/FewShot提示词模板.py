from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate
from langchain_community.llms.tongyi import Tongyi

example_template = PromptTemplate.from_template("单词: {word}, 反义词: {antonym}")

examples_data = [
    {"word": "大", "antonym": "小"},
    {"word": "上", "antonym": "下"},
]

few_shot_template = FewShotPromptTemplate(
    examples = examples_data,
    example_prompt = example_template,
    prefix = "告知我单词的反义词，我提供如下的示例：",
    suffix = "基于前面的示例告知我，{input_word}的反义词是？",
    input_variables = ['input_word'] # 前/后缀若需要注入数据，应使用“input_word = xxx”
)
prompt_text = few_shot_template.invoke(input={"input_word": "左"}).to_string()

print(prompt_text)
model = Tongyi(model="qwen-max")
print(model.invoke(input=prompt_text))