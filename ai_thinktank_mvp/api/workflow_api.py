from typing import Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from api.config import OPENAI_API_BASE, OPENAI_API_KEY
from agents.agent_factory import AgentFactory
from models.database import SessionLocal
from workflows.crewai_workflow import AIThinkTankWorkflow

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
    project_id: int
    workflow_result: str
    individual_outputs: Dict[str, Any]

@router.post("/chat", response_model=WorkflowResponse)
async def execute_chat_workflow(
    request: ChatWorkflowRequest,
    db: Session = Depends(get_db)
):
    """通过聊天消息执行AI参谋团工作流"""
    try:
        from utils.message_parser import MessageParser
        
        # 解析用户消息
        parser = MessageParser()
        parsed = parser.parse_message(request.message)
        
        # 初始化Agent工厂
        agent_factory = AgentFactory() 
        
        # 创建工作流管理器
        workflow = AIThinkTankWorkflow(agent_factory, db)
        
        # 执行工作流
        result = workflow.execute_full_workflow(
            user_goal=parsed["user_goal"],
            user_context=parsed["user_context"]
        )
        
        return WorkflowResponse(
            project_id=result.get("project_id", 0),
            workflow_result=result["workflow_result"],
            individual_outputs=result["individual_outputs"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"聊天工作流执行失败: {str(e)}")

@router.get("/status/{project_id}")
async def get_workflow_status(project_id: int, db: Session = Depends(get_db)):
    """获取工作流执行状态"""
    from models.project import Project
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    return {
        "project_id": project.id,
        "name": project.name,
        "status": project.status, 
        "created_at": project.created_at
    }