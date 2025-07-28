from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .config import OPENAI_API_BASE, OPENAI_API_KEY
from agents.agent_factory import AgentFactory
from models.database import Base, engine

app = FastAPI(title="AI Think Tank MVP API")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
Base.metadata.create_all(bind=engine)

# 初始化Agent工厂
agent_factory = AgentFactory()

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy", "message": "AI Think Tank MVP API is running"}

# 包含工作流API路由
from . import workflow_api
app.include_router(workflow_api.router)

# 预留：项目/任务相关API路由
# from . import project_api, task_api
# app.include_router(project_api.router)
# app.include_router(task_api.router) 