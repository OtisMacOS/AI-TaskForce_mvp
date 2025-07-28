from crewai import Agent, Task, Crew, Process
from typing import Dict, List, Any
from agents.agent_factory import AgentFactory
from models.project import Project, Task as ProjectTask, AgentOutput
from sqlalchemy.orm import Session
import json

class AIThinkTankWorkflow:
    """AI参谋团工作流管理器"""
    
    def __init__(self, agent_factory: AgentFactory, db_session: Session):
        self.agent_factory = agent_factory
        self.db_session = db_session
        
    # 创建需求分析任务
    def create_requirement_analysis_task(self, user_goal: str, user_context: str = "") -> Task:
        chiefmind = self.agent_factory.get_agent("chiefmind")
        
        return Task(
            description=f"""
            请使用你的专业能力，分析以下项目需求：
            
            用户目标：{user_goal}  
            用户背景：{user_context}
            
            输出格式：JSON格式，包含以下字段：
            - refined_requirements: 细化后的需求描述
            - user_persona: 目标用户画像
            - project_scope: 项目范围定义
            - key_features: 核心功能列表
            - technical_considerations: 技术考虑点
            """,
            agent=chiefmind,
            expected_output="需求分析报告（JSON格式）"
        )
    
    # 创建任务计划任务
    def create_task_planning_task(self, requirements: str) -> Task:
        
        taskplanner = self.agent_factory.get_agent("taskplanner")
        
        return Task(
            description=f"""
            请使用你的专业能力，将以下需求分析结果拆解为任务树：
            
            {requirements}
            
            输出格式：JSON格式的任务树结构
            """,
            agent=taskplanner,
            expected_output="项目任务树（JSON格式）"
        )
    
    # 创建市场分析任务
    def create_market_research_task(self, project_scope: str, target_market: str = "") -> Task:
        """创建市场调研任务"""
        researcher = self.agent_factory.get_agent("researcher")
        
        return Task(
            description=f"""
            请使用你的专业能力，对以下项目进行市场调研：
            
            项目范围：{project_scope}
            目标市场：{target_market}
            
            输出格式：Markdown格式的市场调研报告
            """,
            agent=researcher,
            expected_output="市场调研报告（Markdown格式）"
        )
    
    # 创建撰写PRD任务
    def create_prd_writing_task(self, requirements: str, market_report: str) -> Task:
        """创建PRD撰写任务"""
        prdwriter = self.agent_factory.get_agent("prdwriter")
        
        return Task(
            description=f"""
            请使用你的专业能力，基于以下信息撰写PRD文档：
            
            需求分析：{requirements}
            市场调研：{market_report}
            
            输出格式：Markdown格式的PRD文档
            """,
            agent=prdwriter,
            expected_output="产品需求文档（PRD）"
        )
    
    # 创建工具选择任务
    def create_tool_selection_task(self, project_scope: str, feature_specs: str) -> Task:
        """创建工具选型任务"""
        toolfinder = self.agent_factory.get_agent("toolfinder")
        
        return Task(
            description=f"""
            请使用你的专业能力，为以下项目推荐技术栈和工具：
            
            项目范围：{project_scope}
            功能规格：{feature_specs}
            
            输出格式：Markdown格式的工具选型报告
            """,
            agent=toolfinder,
            expected_output="工具选型报告"
        )
    
    # 创建结果评估任务
    def create_result_evaluation_task(self, all_outputs: Dict[str, str], project_goals: str) -> Task:
        """创建结果评估任务"""
        chiefmind = self.agent_factory.get_agent("chiefmind")
        
        return Task(
            description=f"""
            请使用你的专业能力，评估以下项目的完成情况：
            
            项目目标：{project_goals}
            各任务产出：{json.dumps(all_outputs, ensure_ascii=False, indent=2)}
            
            输出格式：Markdown格式的评估报告
            """,
            agent=chiefmind,
            expected_output="项目评估报告"
        )
    
    # 智能判断是否应该执行完整工作流
    def should_execute_workflow(self, user_message: str) -> bool:
        """判断用户消息是否包含项目需求"""
        # 扩展的关键词检测
        project_keywords = [
            "开发", "设计", "创建", "构建", "制作", "建立", "实现",
            "项目", "应用", "系统", "平台", "网站", "软件", "程序",
            "功能", "需求", "想要", "需要", "希望", "计划",
            "游戏", "app", "应用", "工具", "服务", "产品"
        ]
        
        # 检查是否包含项目相关关键词
        has_project_keywords = any(keyword in user_message for keyword in project_keywords)
        
        # 检查消息长度（降低要求，只要超过5个字符即可）
        is_long_enough = len(user_message.strip()) > 5
        
        # 调试信息
        print(f"DEBUG: 消息='{user_message}', 长度={len(user_message.strip())}, 包含关键词={has_project_keywords}, 足够长={is_long_enough}")
        
        return has_project_keywords and is_long_enough
    
    # 执行简单对话
    def execute_simple_chat(self, user_message: str) -> Dict[str, Any]:
        """执行简单对话，不启动完整工作流"""
        chiefmind = self.agent_factory.get_agent("chiefmind")
        
        # 构建简单的回复
        if "你好" in user_message or "hello" in user_message.lower():
            response = """你好！我是AI参谋团的首席指挥官。我可以帮助您：

🎯 **项目咨询**：分析项目需求和技术可行性
📋 **任务规划**：制定详细的任务分解计划
🔍 **市场调研**：进行竞品分析和市场研究
📝 **PRD撰写**：编写专业的产品需求文档
🛠️ **技术选型**：推荐合适的技术栈和工具

请告诉我您想要开发什么项目，我会为您提供专业的分析和建议！"""
        else:
            response = """我理解您的消息，但为了更好地帮助您，请告诉我：

1. 您想要开发什么类型的项目？
2. 项目的主要功能是什么？
3. 目标用户群体是谁？

例如：\"我想开发一个在线教育平台\" 或 \"帮我设计一个电商网站\"

这样我就能为您提供专业的项目分析和建议了！"""
        
        return {
            "project_id": None,
            "workflow_result": response,
            "individual_outputs": {
                "chiefmind": "简单对话模式",
                "taskplanner": "等待项目需求", 
                "researcher": "等待项目需求",
                "prdwriter": "等待项目需求",
                "toolfinder": "等待项目需求"
            }
        }
    
    # 执行完整的工作流
    def execute_full_workflow(self, user_goal: str, user_context: str = "") -> Dict[str, Any]:
        """执行完整的工作流"""
        
        # 1. 需求分析
        req_task = self.create_requirement_analysis_task(user_goal, user_context)
        
        # 2. 任务规划 - 使用占位符，实际执行时会被替换
        planning_task = self.create_task_planning_task("待执行")
        
        # 3. 市场调研 - 使用占位符
        research_task = self.create_market_research_task("待执行", "待执行")
        
        # 4. PRD撰写 - 使用占位符
        prd_task = self.create_prd_writing_task("待执行", "待执行")
        
        # 5. 工具选型 - 使用占位符
        tool_task = self.create_tool_selection_task("待执行", "待执行")
        
        # 6. 结果评估 - 使用占位符
        evaluation_task = self.create_result_evaluation_task({
            "requirements": "待执行",
            "task_plan": "待执行", 
            "market_research": "待执行",
            "prd": "待执行",
            "tool_selection": "待执行"
        }, user_goal)
        
        # 创建Crew并执行
        crew = Crew(
            agents=[req_task.agent, planning_task.agent, research_task.agent, 
                   prd_task.agent, tool_task.agent, evaluation_task.agent],
            tasks=[req_task, planning_task, research_task, prd_task, tool_task, evaluation_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # 将CrewOutput转换为字符串
        if hasattr(result, 'raw'):
            result_str = result.raw
        else:
            result_str = str(result)
        
        # 保存到数据库
        project_id = self._save_to_database(user_goal, result_str)
        
        return {
            "project_id": project_id,
            "workflow_result": result_str,
            "individual_outputs": {
                "chiefmind": "需求分析完成",
                "taskplanner": "任务规划完成", 
                "researcher": "市场调研完成",
                "prdwriter": "PRD撰写完成",
                "toolfinder": "工具选型完成"
            }
        }
    
    # 保存到数据库
    def _save_to_database(self, user_goal: str, workflow_result: str):
        """保存工作流结果到数据库"""
        # 创建项目记录
        project = Project(
            name=f"AI参谋团项目 - {user_goal[:50]}...",
            description=user_goal,
            status="completed"
        )
        self.db_session.add(project)
        self.db_session.commit()
        
        # 保存最终结果
        output = AgentOutput(
            type="crew",
            content=workflow_result
        )
        self.db_session.add(output)
        self.db_session.commit()
        
        return project.id 