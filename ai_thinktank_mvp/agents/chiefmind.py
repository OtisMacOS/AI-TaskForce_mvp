from .base import BaseAgent
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from llm_module import create_llm_function
from typing import Dict, Any, Literal

class ChiefMindAgent(BaseAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="ChiefMind",
            goal="作为AI参谋团的头脑，负责需求分析、结果整合和项目评估",
            backstory="你是一个经验丰富的AI项目顾问，擅长通过对话理解用户需求，协调多个AI专家协作，并提供综合建议。"
        )
        # 保留LLM函数用于直接调用
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
        from llm_module import create_llm_function
        self._llm_function = create_llm_function()

    def _build_requirement_analysis_prompt(self, user_goal: str, user_context: str = "") -> str:
        """构建需求分析prompt"""
        return f"""
你是一位资深的AI项目顾问，专门负责深入理解用户需求并进行分析。

用户目标：{user_goal}
用户背景：{user_context}

请执行以下分析步骤：
1. 深入分析用户的核心需求和痛点
2. 识别项目的关键要素（目标用户、核心功能、技术方向、商业模式等）
3. 评估项目的可行性和风险点
4. 提出需要进一步明确的关键问题
5. 制定初步的项目范围和边界

请输出结构化的需求分析报告，包含以下字段：
- refined_requirements: 细化后的需求描述
- user_persona: 目标用户画像
- project_scope: 项目范围定义
- key_features: 核心功能列表
- technical_considerations: 技术考虑点
- risk_assessment: 风险评估
- success_metrics: 成功指标

输出格式：严格的JSON格式
"""

    def _build_evaluation_prompt(self, project_goals: str, all_outputs: Dict[str, str]) -> str:
        """构建项目评估prompt"""
        return f"""
你是一位资深的项目评估专家，需要对整个项目的完成情况进行综合评估。

项目目标：{project_goals}
各任务产出：{json.dumps(all_outputs, ensure_ascii=False, indent=2)}

请进行以下评估：
1. 各任务完成质量评估（需求分析、任务规划、市场调研、PRD撰写、工具选型）
2. 项目整体进展分析
3. 潜在风险和问题识别
4. 下一步行动建议
5. 项目成功概率评估
6. 资源投入和成本效益分析

请输出结构化的评估报告，包含：
- quality_assessment: 质量评估
- progress_analysis: 进展分析
- risk_analysis: 风险分析
- next_steps: 下一步建议
- success_probability: 成功概率
- recommendations: 具体建议

输出格式：Markdown格式的评估报告
"""

    def analyze_requirements(self, user_goal: str, user_context: str = "") -> Dict[str, Any]:
        """需求分析方法"""
        if self._llm_function is not None:
            prompt = self._build_requirement_analysis_prompt(user_goal, user_context)
            result = self._llm_function(prompt)
            
            try:
                if isinstance(result, str):
                    return json.loads(result)
                else:
                    return {"error": f"LLM response is not valid JSON: {str(result)[:200]}..."}
            except json.JSONDecodeError:
                return {"error": f"LLM response is not valid JSON: {str(result)[:200]}..."}
        else:
            return {"error": "LLM function is not available"}

    def evaluate_project(self, project_goals: str, all_outputs: Dict[str, str]) -> str:
        """项目评估方法"""
        if self._llm_function is not None:
            prompt = self._build_evaluation_prompt(project_goals, all_outputs)
            return self._llm_function(prompt)
        else:
            return "LLM function is not available" 