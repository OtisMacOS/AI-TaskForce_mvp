from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(32), default="pending")
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    parent_id = Column(Integer, ForeignKey('tasks.id'), nullable=True)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    status = Column(String(32), default="pending")
    agent = Column(String(64))
    output_id = Column(Integer, ForeignKey('agent_outputs.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    project = relationship("Project", back_populates="tasks")
    parent = relationship("Task", remote_side=[id], backref="subtasks")
    output = relationship("AgentOutput", back_populates="task", uselist=False)

class AgentOutput(Base):
    __tablename__ = 'agent_outputs'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    type = Column(String(32))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    task = relationship("Task", back_populates="output", uselist=False) 