from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../db/thinktank.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 

# --- 数据库迁移脚本（手动示例）---
# 如果你没有用Alembic等自动迁移工具，可以用如下SQL手动迁移：
#
# ALTER TABLE projects ADD COLUMN status VARCHAR(32) DEFAULT 'pending';
#
# 如果用Alembic，建议生成自动迁移脚本。 