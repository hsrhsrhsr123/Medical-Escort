"""
配置管理模块
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用配置
    app_name: str = "医疗陪诊Agent"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # OpenAI配置
    openai_api_key: str
    openai_model: str = "gpt-4"
    
    # 数据库配置
    database_url: str = "sqlite:///./medical_escort.db"
    mongodb_url: Optional[str] = "mongodb://localhost:27017"
    mongodb_db_name: str = "medical_escort"
    
    # 安全配置
    secret_key: str
    access_token_expire_minutes: int = 60
    
    # 医院API配置
    hospital_api_base_url: Optional[str] = None
    hospital_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()





