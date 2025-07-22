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
    
    # 执行完整的工作流
    def execute_full_workflow(self, user_goal: str, user_context: str = "") -> Dict[str, Any]:
        """执行完整的工作流"""
        
        # 1. 需求分析
        req_task = self.create_requirement_analysis_task(user_goal, user_context)
        
        # 2. 任务规划
        planning_task = self.create_task_planning_task(req_task.output) # 问：为什么这里会用reg_task.output? 不直接用reg_task？
        
        # 3. 市场调研
        research_task = self.create_market_research_task(
            # 问： 这里是如何运作的？get 是如何拿到文档里的project_scope和targeet_market的？

            planning_task.output.get("project_scope", ""),
            planning_task.output.get("target_market", "")
        )
        
        # 4. PRD撰写
        prd_task = self.create_prd_writing_task(
            req_task.output,  # 问：为什么这里会用reg_task.output? 不直接用reg_task？
            research_task.output  # 问：为什么这里会用reg_task.output? 不直接用reg_task？
        )
        
        # 5. 工具选型
        tool_task = self.create_tool_selection_task(
            planning_task.output.get("project_scope", ""),
            prd_task.output  # 问：为什么这里会用reg_task.output? 不直接用reg_task？
        ) 
        
        # 6. 结果评估
        evaluation_task = self.create_result_evaluation_task(
            {
                "requirements": req_task.output,  # 问：为什么这里会用reg_task.output? 不直接用reg_task？
                "task_plan": planning_task.output,
                "market_research": research_task.output,
                "prd": prd_task.output,
                "tool_selection": tool_task.output
            },
            user_goal
        )
        
        # 创建Crew并执行
        crew = Crew(
            agents=[req_task.agent, planning_task.agent, research_task.agent, 
                   prd_task.agent, tool_task.agent, evaluation_task.agent],
            tasks=[req_task, planning_task, research_task, prd_task, tool_task, evaluation_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # 保存到数据库
        self._save_to_database(user_goal, result)
        
        return {
            "workflow_result": result,
            "individual_outputs": {
                "requirements": req_task.output,
                "task_plan": planning_task.output,
                "market_research": research_task.output,
                "prd": prd_task.output,
                "tool_selection": tool_task.output,
                "evaluation": evaluation_task.output
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
            agent_type="crew",
            content=workflow_result,
            content_type="workflow_result"
        )
        self.db_session.add(output)
        self.db_session.commit()
        
        return project.id 