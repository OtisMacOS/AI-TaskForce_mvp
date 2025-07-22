from .base import BaseAgent
from llm_module import create_llm_function
from typing import Dict, Any

class PRDWriterAgent(BaseAgent):
    def __init__(self, llm=None):
        llm = llm or create_llm_function()
        super().__init__(
            role="PRDWriter",
            goal="根据任务树和用户需求撰写高质量的PRD文档",
            backstory="你是一个资深产品经理AI，擅长将需求转化为结构化的产品需求文档。",
            llm=llm
        )
        self._llm_function = llm

    def _build_prd_writing_prompt(self, requirements: str, market_report: str) -> str:
        """构建PRD撰写prompt"""
        return f"""
你是一位资深的产品经理，专门负责撰写高质量的产品需求文档（PRD）。

需求分析：{requirements}
市场调研：{market_report}

请撰写一份完整的PRD文档，包含以下内容：

1. 产品概述和目标
   - 产品愿景和使命
   - 核心价值主张
   - 产品目标

2. 用户故事和用例
   - 主要用户角色定义
   - 用户故事（User Stories）
   - 用例场景分析

3. 功能需求规格
   - 核心功能列表
   - 功能优先级排序
   - 功能详细描述
   - 用户界面要求

4. 非功能需求
   - 性能要求
   - 安全要求
   - 可用性要求
   - 可扩展性要求

5. 用户界面设计建议
   - 界面设计原则
   - 主要页面布局
   - 交互设计建议

6. 技术架构建议
   - 系统架构概览
   - 技术选型建议
   - 数据模型设计

7. 项目里程碑和交付计划
   - 开发阶段划分
   - 关键里程碑
   - 交付时间表

请输出结构化的PRD文档，包含：
- product_overview: 产品概述
- user_stories: 用户故事
- functional_requirements: 功能需求
- non_functional_requirements: 非功能需求
- ui_design: 界面设计
- technical_architecture: 技术架构
- project_timeline: 项目时间线

输出格式：Markdown格式的PRD文档
"""

    def write_prd(self, requirements: str, market_report: str) -> str:
        """PRD撰写方法"""
        if self._llm_function is not None:
            prompt = self._build_prd_writing_prompt(requirements, market_report)
            return self._llm_function(prompt)
        else:
            return "LLM function is not available" 