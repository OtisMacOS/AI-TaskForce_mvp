from .base import BaseAgent
from llm_module import create_llm_function
from typing import Dict, Any

class ResearcherAgent(BaseAgent):
    def __init__(self, llm=None):
        llm = llm or create_llm_function()
        super().__init__(
            role="Researcher",
            goal="为项目提供详实的市场调研和洞察分析",
            backstory="你是一个AI市场调研专家，能够快速收集、分析并总结行业信息和趋势。",
            llm=llm
        )
        self._llm_function = llm

    def _build_market_research_prompt(self, project_scope: str, target_market: str = "") -> str:
        """构建市场调研prompt"""
        return f"""
你是一位资深的AI市场调研专家，专门负责深入的市场分析和洞察提取。

项目范围：{project_scope}
目标市场：{target_market}

请执行以下调研分析：
1. 市场现状分析
   - 市场规模和增长趋势
   - 市场驱动因素和挑战
   - 用户需求和痛点分析

2. 竞品分析（至少3个主要竞品）
   - 竞品功能对比
   - 竞品优劣势分析
   - 竞品商业模式分析
   - 市场定位分析

3. 用户需求调研
   - 目标用户画像
   - 用户行为分析
   - 用户痛点识别
   - 用户需求优先级

4. 技术趋势分析
   - 相关技术发展现状
   - 技术趋势预测
   - 技术选型建议

5. 商业模式分析
   - 盈利模式分析
   - 成本结构分析
   - 竞争优势分析

请输出结构化的市场调研报告，包含：
- market_overview: 市场概览
- competitor_analysis: 竞品分析
- user_insights: 用户洞察
- technology_trends: 技术趋势
- business_model: 商业模式分析
- recommendations: 建议和机会

输出格式：Markdown格式的市场调研报告
"""

    def conduct_market_research(self, project_scope: str, target_market: str = "") -> str:
        """市场调研方法"""
        if self._llm_function is not None:
            prompt = self._build_market_research_prompt(project_scope, target_market)
            return self._llm_function(prompt)
        else:
            return "LLM function is not available" 