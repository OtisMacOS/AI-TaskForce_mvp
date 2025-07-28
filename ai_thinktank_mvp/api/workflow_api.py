from typing import Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ai_thinktank_mvp.api.config import OPENAI_API_BASE, OPENAI_API_KEY
from ai_thinktank_mvp.agents.agent_factory import AgentFactory
from ai_thinktank_mvp.models.database import SessionLocal
from ai_thinktank_mvp.workflows.crewai_workflow import AIThinkTankWorkflow

def get_db():
    db = SessionLocal()  
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/workflow", tags=["工作流"])

class ChatWorkflowRequest(BaseModel):
    message: str = Field(..., description="用户聊天消息")

class WorkflowResponse(BaseModel):
    project_id: Optional[int] = None
    workflow_result: str
    individual_outputs: Dict[str, Any]

@router.post("/chat", response_model=WorkflowResponse)
async def execute_chat_workflow(
    request: ChatWorkflowRequest,
    db: Session = Depends(get_db)
):
    """通过聊天消息执行AI参谋团工作流"""
    try:
        from ai_thinktank_mvp.utils.message_parser import MessageParser
        
        # 解析用户消息
        parser = MessageParser()
        parsed = parser.parse_message(request.message)
        
        # 初始化Agent工厂
        agent_factory = AgentFactory() 
        
        # 创建工作流管理器
        workflow = AIThinkTankWorkflow(agent_factory, db)
        
        # 智能判断是否应该执行完整工作流
        if workflow.should_execute_workflow(request.message):
            # 执行完整工作流
            result = workflow.execute_full_workflow(
                user_goal=parsed["user_goal"],
                user_context=parsed["user_context"]
            )
        else:
            # 执行简单对话
            result = workflow.execute_simple_chat(request.message)
        
        # 确保result不为None
        if result is None:
            raise HTTPException(status_code=500, detail="工作流执行返回空结果")
        
        return WorkflowResponse(
            project_id=result.get("project_id", 0),
            workflow_result=result.get("workflow_result", "工作流执行完成"),
            individual_outputs=result.get("individual_outputs", {})
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"聊天工作流执行失败: {str(e)}")

@router.get("/status/{project_id}")
async def get_workflow_status(project_id: int, db: Session = Depends(get_db)):
    """获取工作流执行状态"""
    from ai_thinktank_mvp.models.project import Project
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    return {
        "project_id": project.id,
        "name": project.name,
        "status": project.status, 
        "created_at": project.created_at
    }