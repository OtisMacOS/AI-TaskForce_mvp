from .base import BaseAgent
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from llm_module import create_llm_function
from typing import Dict, Any

class ToolFinderAgent(BaseAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="ToolFinder",
            goal="为项目推荐合适的工具和技术方案",
            backstory="你是一个AI技术选型专家，能够根据项目需求分析并推荐最佳工具和技术路径。"
        )
        self._llm_function = create_llm_function()

    def _build_tool_selection_prompt(self, project_scope: str, feature_specs: str) -> str:
        """构建工具选型prompt"""
        return f"""
你是一位资深的技术选型专家，专门负责为项目推荐最佳的技术栈和工具。

项目范围：{project_scope}
功能规格：{feature_specs}

请进行以下技术选型分析：

1. 技术栈推荐
   - 前端技术栈（框架、UI库、状态管理等）
   - 后端技术栈（语言、框架、数据库等）
   - 移动端技术栈（如需要）
   - 云服务和基础设施

2. 开发工具推荐
   - 代码编辑器/IDE
   - 版本控制工具
   - 项目管理工具
   - 测试工具
   - 部署工具

3. 第三方服务推荐
   - 身份认证服务
   - 支付服务
   - 消息推送服务
   - 监控和分析服务
   - 存储服务

4. 成本分析
   - 开发成本估算
   - 运维成本分析
   - 第三方服务费用
   - 总体成本效益分析

5. 实施计划
   - 技术学习曲线
   - 团队技能匹配度
   - 实施时间估算
   - 风险评估

请输出结构化的工具选型报告，包含：
- frontend_stack: 前端技术栈
- backend_stack: 后端技术栈
- development_tools: 开发工具
- third_party_services: 第三方服务
- cost_analysis: 成本分析
- implementation_plan: 实施计划
- recommendations: 最终推荐

输出格式：Markdown格式的工具选型报告
"""

    def select_tools(self, project_scope: str, feature_specs: str) -> str:
        """工具选型方法"""
        if self._llm_function is not None:
            prompt = self._build_tool_selection_prompt(project_scope, feature_specs)
            return self._llm_function(prompt)
        else:
            return "LLM function is not available" 