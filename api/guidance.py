"""
就医指导API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Appointment, GuidanceLog
from agents import GuidanceAgent
from loguru import logger

router = APIRouter()

# 初始化Agent
guidance_agent = GuidanceAgent()


class GuidanceRequest(BaseModel):
    """指导请求"""
    user_id: int
    appointment_id: int
    current_step: str


class LocationRequest(BaseModel):
    """位置指引请求"""
    hospital_id: str
    target_location: str


@router.get("/appointment/{appointment_id}/full")
async def get_full_guidance(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """获取完整的就医流程指导"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    appointment_info = {
        "hospital_name": appointment.hospital_name,
        "department": appointment.department,
        "doctor_name": appointment.doctor_name,
        "appointment_time": appointment.appointment_date.isoformat(),
        "appointment_number": appointment.appointment_number
    }
    
    guidance = guidance_agent.get_full_guidance(appointment_info)
    
    logger.info(f"生成完整就医指导: 预约ID={appointment_id}")
    
    return guidance


@router.post("/step")
async def get_step_guidance(
    request: GuidanceRequest,
    db: Session = Depends(get_db)
):
    """获取当前步骤的指导"""
    appointment = db.query(Appointment).filter(Appointment.id == request.appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    # 获取上下文信息
    context = {
        "department": appointment.department,
        "symptoms": appointment.symptoms
    }
    
    guidance = guidance_agent.get_current_step_guidance(request.current_step, context)
    
    # 记录指导日志
    if guidance.get("success"):
        log = GuidanceLog(
            user_id=request.user_id,
            appointment_id=request.appointment_id,
            guidance_type=request.current_step,
            guidance_content=str(guidance),
            is_completed=False
        )
        db.add(log)
        db.commit()
    
    logger.info(f"提供步骤指导: 用户{request.user_id} - {request.current_step}")
    
    return guidance


@router.post("/location")
async def get_location_guidance(request: LocationRequest):
    """获取医院内位置指引"""
    guidance = guidance_agent.get_location_guidance(
        request.hospital_id,
        request.target_location
    )
    
    return {
        "success": True,
        "target": request.target_location,
        **guidance
    }


@router.get("/voice/{step}")
async def get_voice_guidance(step: str, language: str = "zh-CN"):
    """获取语音指导文本"""
    voice_text = guidance_agent.generate_voice_guidance(step, language)
    
    return {
        "success": True,
        "step": step,
        "language": language,
        "text": voice_text
    }


@router.get("/steps")
async def get_all_steps():
    """获取所有就医流程步骤"""
    return {
        "success": True,
        "steps": guidance_agent.process_steps
    }


@router.put("/log/{log_id}/complete")
async def mark_guidance_complete(log_id: int, db: Session = Depends(get_db)):
    """标记指导步骤已完成"""
    log = db.query(GuidanceLog).filter(GuidanceLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="指导记录不存在")
    
    log.is_completed = True
    db.commit()
    
    return {"success": True, "message": "已标记完成"}


@router.get("/user/{user_id}/history")
async def get_guidance_history(user_id: int, db: Session = Depends(get_db)):
    """获取用户的指导历史"""
    logs = db.query(GuidanceLog)\
        .filter(GuidanceLog.user_id == user_id)\
        .order_by(GuidanceLog.created_at.desc())\
        .limit(50)\
        .all()
    
    return {
        "success": True,
        "count": len(logs),
        "history": [
            {
                "id": log.id,
                "guidance_type": log.guidance_type,
                "is_completed": log.is_completed,
                "created_at": log.created_at.isoformat()
            }
            for log in logs
        ]
    }






