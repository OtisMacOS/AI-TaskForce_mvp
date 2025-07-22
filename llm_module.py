import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY', 'sk-xxx')
base_url = os.getenv('OPENAI_API_BASE', 'https://xiaoai.plus/v1')
model_name = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

def get_llm_client():
    """返回OpenAI客户端实例"""
    return OpenAI(base_url=base_url, api_key=api_key)

def chat_completion(messages, model=model_name, **kwargs):
    """
    统一的对话生成接口，返回OpenAI回复内容。
    :param messages: 消息列表
    :param model: 使用的模型
    :param kwargs: 其他参数
    :return: 回复内容
    """
    try:
        client = get_llm_client()
        completion = client.chat.completions.create(
            model=model or model_name,
            messages=messages,
            **kwargs
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise e

def create_llm_function():
    """
    创建一个可调用的LLM函数，用于agent中直接调用
    """
    def llm_function(prompt_text):
        messages = [{"role": "user", "content": prompt_text}]
        return chat_completion(messages)
    
    return llm_function

 
