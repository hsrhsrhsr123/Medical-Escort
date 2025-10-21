"""
数据库连接和会话管理
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pymongo import MongoClient
from config import settings
from models import Base
from typing import Generator


# SQLAlchemy 配置
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# MongoDB 配置
mongodb_client = None
if settings.mongodb_url:
    mongodb_client = MongoClient(settings.mongodb_url)
    mongodb = mongodb_client[settings.mongodb_db_name]


def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_mongodb():
    """获取MongoDB连接"""
    return mongodb if mongodb_client else None





