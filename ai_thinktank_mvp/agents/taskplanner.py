from .base import BaseAgent
import datetime
import json
from llm_module import create_llm_function, chat_completion
from typing import Literal, Any

class TaskPlannerAgent(BaseAgent):
    def __init__(self, llm=None):
        llm = llm or create_llm_function()
        super().__init__(
            role="TaskPlanner",
            goal="将用户需求拆解为任务树",
            backstory="你是一个善于结构化思考的AI，负责将项目目标拆解为阶段、任务和子任务。",
            llm=llm
        )
        self._llm_function = llm

    def _build_prompt(self, user_goal: str, output_format: str) -> str:
        return f"""
你是一位结构化思维极强的AI项目顾问，专门将复杂目标拆解为清晰的任务树。你的工作流程如下：

1. 接收用户的总体目标（如：开发一个AI写作助手）。
2. 拆解为若干 **阶段**（例如：需求分析、技术选型、开发、测试、上线等）。
3. 每个阶段包含 **一个或多个子任务**，说明具体做什么、为什么做。
4. 如果用户未指定技术方向，由你判断是否需要进行模型选择、数据准备、UI设计等步骤。
5. 输出结构必须清晰、条理清楚，可读性强，避免泛泛而谈。

用户目标如下：
---
{user_goal}
---

请将上述目标拆解为一个完整的任务树，必须严格按照下面格式输出：

- 如果输出格式是 dict 或 json，请严格输出有效的 JSON 结构，不要带多余说明。
- 如果输出格式是 markdown，请输出符合 Markdown 格式的文本。

当前期望输出格式为：{output_format}
"""

    def plan_tasks(self, user_goal: str, output_format: Literal["dict", "json", "markdown"] = "dict"):
        if output_format not in ["dict", "json", "markdown"]:
            output_format = "dict"

        if self._llm_function is not None:
            prompt = self._build_prompt(user_goal, output_format)
            # 直接调用LLM函数
            if callable(self._llm_function):
                result = self._llm_function(prompt)
            else:
                return {"error": "LLM is not callable"}
            
            if output_format in ["dict", "json"]:
                try:
                    # 确保result是字符串
                    if not isinstance(result, str):
                        result = str(result)
                    
                    # 尝试直接解析JSON
                    return json.loads(result)
                except json.JSONDecodeError:
                    # 如果JSON解析失败，尝试提取JSON部分
                    try:
                        # 查找可能的JSON内容
                        import re
                        result_str = str(result)
                        json_match = re.search(r'\{.*\}', result_str, re.DOTALL)
                        if json_match:
                            json_str = json_match.group()
                            return json.loads(json_str)
                        else:
                            # 如果找不到JSON，返回原始内容作为错误信息
                            return {"error": f"LLM response is not valid JSON. Raw response: {result_str[:200]}..."}
                    except:
                        return {"error": f"LLM response is not valid JSON. Raw response: {str(result)[:200]}..."}
            else:
                return result
        else:
            return {"error": "LLM function is not available"}