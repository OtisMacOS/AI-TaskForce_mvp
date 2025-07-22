from typing import Dict, Any
from llm_module import create_llm_function
import json

class MessageParser:
    """智能消息解析器，从用户聊天内容中提取结构化信息"""
    
    def __init__(self):
        self.llm = create_llm_function()
    
    def _build_parsing_prompt(self, user_message: str) -> str:
        """构建解析prompt，增加few-shot示例"""
        return f"""
你是一个智能消息解析器，需要从用户的聊天内容中提取项目目标和背景信息。

【输入示例1】
我想做个AI写作助手，我是程序员，预算10万，3个月上线
【输出示例1】
{{
    "user_goal": "开发一个AI写作助手",
    "user_context": "用户是程序员，预算10万，希望3个月上线"
}}

【输入示例2】
我要开发一个智能客服系统，团队有3人，计划半年内完成
【输出示例2】
{{
    "user_goal": "开发一个智能客服系统",
    "user_context": "团队3人，计划半年内完成"
}}

【输入示例3】
我想做一个在线教育平台
【输出示例3】
{{
    "user_goal": "开发一个在线教育平台",
    "user_context": ""
}}

【输入】
{user_message}
【输出】
请严格输出JSON格式：
{{
    "user_goal": "...",
    "user_context": "..."
}}
"""
    
    def parse_message(self, user_message: str) -> Dict[str, str]:
        """解析用户消息"""
        try:
            prompt = self._build_parsing_prompt(user_message)
            result = self.llm(prompt)
            # 尝试解析JSON
            if isinstance(result, str):
                parsed = json.loads(result)
                return {
                    "user_goal": parsed.get("user_goal", user_message),
                    "user_context": parsed.get("user_context", "")
                }
            else:
                return {
                    "user_goal": user_message,
                    "user_context": ""
                }
        except Exception as e:
            return {
                "user_goal": user_message,
                "user_context": ""
            }
    
    def extract_key_info(self, user_message: str) -> Dict[str, Any]:
        """提取关键信息，增加few-shot示例"""
        parsed = self.parse_message(user_message)
        analysis_prompt = f"""
你是一个AI助手，需要基于项目信息提取关键要素。

【输入示例1】
项目目标：开发一个AI写作助手
项目背景：用户是程序员，预算10万，希望3个月上线
【输出示例1】
{{
    "project_type": "AI工具",
    "target_users": "内容创作者、程序员",
    "budget_range": "10万",
    "timeline": "3个月",
    "complexity": "中等",
    "main_features": ["自动写作", "多语言支持", "智能纠错"]
}}

【输入示例2】
项目目标：开发一个在线教育平台
项目背景：团队3人，计划半年内完成
【输出示例2】
{{
    "project_type": "Web应用",
    "target_users": "学生、教师",
    "budget_range": "未说明",
    "timeline": "半年",
    "complexity": "较高",
    "main_features": ["课程管理", "在线直播", "作业批改"]
}}

【输入】
项目目标：{parsed['user_goal']}
项目背景：{parsed['user_context']}
【输出】
请严格输出JSON格式：
{{
    "project_type": "...",
    "target_users": "...",
    "budget_range": "...",
    "timeline": "...",
    "complexity": "...",
    "main_features": ["...", "...", "..."]
}}
"""
        try:
            result = self.llm(analysis_prompt)
            if isinstance(result, str):
                key_info = json.loads(result)
                return {
                    **parsed,
                    **key_info
                }
        except:
            pass
        return parsed 