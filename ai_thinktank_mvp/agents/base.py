from crewai import Agent
import os

class BaseAgent(Agent):
    """基础Agent，所有自定义Agent继承自此类。"""
    
    def __init__(self, role: str, goal: str, backstory: str, llm=None, **kwargs):
        # 获取LLM配置
        model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        super().__init__(
            role=role,
            goal=goal,
            backstory=backstory,
            llm=model_name,
            **kwargs
        ) 