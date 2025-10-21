"""
预约挂号API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from database import get_db
from models import Appointment, User
from agents import SymptomAnalyzer, AppointmentAgent
from loguru import logger

router = APIRouter()

# 初始化Agent
symptom_analyzer = SymptomAnalyzer()
appointment_agent = AppointmentAgent()


class SymptomAnalysisRequest(BaseModel):
    """症状分析请求"""
    user_id: int
    symptoms: str


class AppointmentCreate(BaseModel):
    """预约创建请求"""
    user_id: int
    hospital_id: str
    hospital_name: str
    department: str
    doctor_name: Optional[str] = None
    appointment_date: str
    symptoms: Optional[str] = None


class AppointmentResponse(BaseModel):
    """预约响应"""
    id: int
    user_id: int
    hospital_name: str
    department: str
    appointment_date: datetime
    status: str
    
    class Config:
        from_attributes = True


@router.post("/analyze-symptoms")
async def analyze_symptoms(
    request: SymptomAnalysisRequest,
    db: Session = Depends(get_db)
):
    """分析症状并推荐科室"""
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 获取用户健康信息
    patient_info = {
        "age": user.age,
        "gender": user.gender,
        "chronic_diseases": user.chronic_diseases,
        "allergies": user.allergies
    }
    
    # 调用症状分析Agent
    result = symptom_analyzer.analyze_symptoms(request.symptoms, patient_info)
    
    logger.info(f"症状分析: 用户{user.name} - {request.symptoms[:30]}... -> {result.get('recommended_department')}")
    
    return result


@router.get("/hospitals")
async def search_hospitals(
    location: str,
    department: Optional[str] = None
):
    """搜索医院"""
    hospitals = appointment_agent.search_hospitals(location, department)
    return {
        "success": True,
        "count": len(hospitals),
        "hospitals": hospitals
    }


@router.get("/hospitals/{hospital_id}/slots")
async def get_available_slots(
    hospital_id: str,
    department: str,
    date: str
):
    """获取可预约时间段"""
    slots = appointment_agent.get_available_slots(hospital_id, department, date)
    return {
        "success": True,
        "hospital_id": hospital_id,
        "department": department,
        "date": date,
        "slots": slots
    }


@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    """创建预约"""
    user = db.query(User).filter(User.id == appointment.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 调用预约Agent
    user_info = {
        "name": user.name,
        "phone": user.phone,
        "id_card": user.id_card
    }
    
    result = appointment_agent.make_appointment(
        user_info,
        appointment.hospital_id,
        appointment.hospital_name,
        appointment.department,
        appointment.doctor_name or "门诊医生",
        appointment.appointment_date
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "预约失败"))
    
    # 保存到数据库
    db_appointment = Appointment(
        user_id=appointment.user_id,
        hospital_name=appointment.hospital_name,
        department=appointment.department,
        doctor_name=appointment.doctor_name,
        appointment_date=datetime.fromisoformat(appointment.appointment_date),
        appointment_number=result["appointment_number"],
        symptoms=appointment.symptoms,
        status="confirmed"
    )
    
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    logger.info(f"创建预约: 用户{user.name} - {appointment.hospital_name}/{appointment.department}")
    
    return db_appointment


@router.get("/{appointment_id}")
async def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """获取预约详情"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    return {
        "id": appointment.id,
        "user_id": appointment.user_id,
        "hospital_name": appointment.hospital_name,
        "department": appointment.department,
        "doctor_name": appointment.doctor_name,
        "appointment_date": appointment.appointment_date.isoformat(),
        "appointment_number": appointment.appointment_number,
        "status": appointment.status,
        "symptoms": appointment.symptoms
    }


@router.get("/user/{user_id}/appointments")
async def get_user_appointments(
    user_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取用户的预约列表"""
    query = db.query(Appointment).filter(Appointment.user_id == user_id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    appointments = query.order_by(Appointment.appointment_date.desc()).all()
    
    return {
        "success": True,
        "count": len(appointments),
        "appointments": [
            {
                "id": apt.id,
                "hospital_name": apt.hospital_name,
                "department": apt.department,
                "doctor_name": apt.doctor_name,
                "appointment_date": apt.appointment_date.isoformat(),
                "status": apt.status
            }
            for apt in appointments
        ]
    }


@router.put("/{appointment_id}/cancel")
async def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """取消预约"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    # 调用预约Agent取消预约
    result = appointment_agent.cancel_appointment(appointment.appointment_number)
    
    if result.get("success"):
        appointment.status = "cancelled"
        db.commit()
        
        logger.info(f"取消预约: ID={appointment_id}, 单号={appointment.appointment_number}")
        
        return {"success": True, "message": "预约已取消"}
    else:
        raise HTTPException(status_code=400, detail="取消预约失败")


@router.get("/{appointment_id}/status")
async def get_appointment_status(appointment_id: int, db: Session = Depends(get_db)):
    """查询预约状态"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    # 查询实时状态
    status = appointment_agent.get_appointment_status(appointment.appointment_number)
    
    return {
        "appointment_id": appointment_id,
        "appointment_number": appointment.appointment_number,
        **status
    }





