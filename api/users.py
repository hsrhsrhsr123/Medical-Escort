"""
用户管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import User
from loguru import logger

router = APIRouter()


class UserCreate(BaseModel):
    """用户创建模型"""
    name: str
    phone: str
    id_card: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    chronic_diseases: Optional[str] = None


class UserUpdate(BaseModel):
    """用户更新模型"""
    name: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    chronic_diseases: Optional[str] = None


class UserResponse(BaseModel):
    """用户响应模型"""
    id: int
    name: str
    phone: str
    age: Optional[int]
    gender: Optional[str]
    
    class Config:
        from_attributes = True


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """创建新用户"""
    # 检查手机号是否已存在
    existing_user = db.query(User).filter(User.phone == user.phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="该手机号已注册")
    
    # 创建用户
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"创建用户: {user.name} ({user.phone})")
    
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """获取用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.get("/phone/{phone}")
async def get_user_by_phone(phone: str, db: Session = Depends(get_db)):
    """通过手机号获取用户"""
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {
        "id": user.id,
        "name": user.name,
        "phone": user.phone,
        "age": user.age,
        "gender": user.gender,
        "medical_history": user.medical_history,
        "allergies": user.allergies,
        "chronic_diseases": user.chronic_diseases,
        "emergency_contact": {
            "name": user.emergency_contact_name,
            "phone": user.emergency_contact_phone
        }
    }


@router.put("/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """更新用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新字段
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"更新用户信息: {user.name} (ID: {user_id})")
    
    return {"success": True, "message": "用户信息已更新"}


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """删除用户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db.delete(user)
    db.commit()
    
    logger.info(f"删除用户: {user.name} (ID: {user_id})")
    
    return {"success": True, "message": "用户已删除"}


@router.get("/{user_id}/health-profile")
async def get_health_profile(user_id: int, db: Session = Depends(get_db)):
    """获取用户健康档案"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {
        "user_id": user.id,
        "name": user.name,
        "age": user.age,
        "gender": user.gender,
        "medical_history": user.medical_history,
        "allergies": user.allergies,
        "chronic_diseases": user.chronic_diseases,
        "recent_appointments": len(user.appointments),
        "recent_records": len(user.medical_records)
    }




