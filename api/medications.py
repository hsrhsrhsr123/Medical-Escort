"""
用药指导API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from models import User, MedicalRecord
from agents import MedicationGuide
from loguru import logger

router = APIRouter()

# 初始化Agent
medication_guide = MedicationGuide()


class PrescriptionParseRequest(BaseModel):
    """处方解析请求"""
    prescription_text: str
    prescription_image: Optional[str] = None


class MedicationInstructionRequest(BaseModel):
    """用药说明请求"""
    user_id: int
    medication_name: str


class Medication(BaseModel):
    """药品模型"""
    name: str
    dosage: str
    frequency: str
    timing: str
    duration: str
    notes: Optional[str] = None


class MedicationScheduleRequest(BaseModel):
    """用药时间表请求"""
    medications: List[Medication]


class ReminderRequest(BaseModel):
    """提醒请求"""
    user_id: int
    medications: List[Medication]
    start_date: Optional[str] = None


@router.post("/parse-prescription")
async def parse_prescription(request: PrescriptionParseRequest):
    """解析处方"""
    result = medication_guide.parse_prescription(
        request.prescription_text,
        request.prescription_image
    )
    
    logger.info("处方解析完成")
    
    return result


@router.post("/instructions")
async def get_medication_instructions(
    request: MedicationInstructionRequest,
    db: Session = Depends(get_db)
):
    """获取用药说明"""
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    patient_info = {
        "allergies": user.allergies,
        "chronic_diseases": user.chronic_diseases
    }
    
    result = medication_guide.get_medication_instructions(
        request.medication_name,
        patient_info
    )
    
    logger.info(f"提供用药说明: 用户{user.name} - {request.medication_name}")
    
    return result


@router.post("/schedule")
async def create_medication_schedule(request: MedicationScheduleRequest):
    """创建用药时间表"""
    medications = [med.dict() for med in request.medications]
    result = medication_guide.create_medication_schedule(medications)
    
    logger.info(f"创建用药时间表: {len(medications)}种药品")
    
    return result


@router.post("/reminders")
async def generate_reminders(request: ReminderRequest):
    """生成用药提醒"""
    medications = [med.dict() for med in request.medications]
    reminders = medication_guide.generate_reminders(
        medications,
        request.start_date
    )
    
    logger.info(f"生成用药提醒: 用户{request.user_id}, {len(reminders)}条提醒")
    
    return {
        "success": True,
        "count": len(reminders),
        "reminders": reminders
    }


@router.get("/pharmacy-guidance/{hospital_name}")
async def get_pharmacy_guidance(hospital_name: str):
    """获取取药指导"""
    guidance = medication_guide.get_pharmacy_guidance(hospital_name)
    
    return {
        "success": True,
        **guidance
    }


@router.post("/check-interactions")
async def check_drug_interactions(medications: List[str]):
    """检查药物相互作用"""
    result = medication_guide.check_drug_interactions(medications)
    
    return result


@router.get("/user/{user_id}/medications")
async def get_user_medications(user_id: int, db: Session = Depends(get_db)):
    """获取用户的用药记录"""
    records = db.query(MedicalRecord)\
        .filter(MedicalRecord.user_id == user_id)\
        .filter(MedicalRecord.prescriptions.isnot(None))\
        .order_by(MedicalRecord.visit_date.desc())\
        .limit(10)\
        .all()
    
    return {
        "success": True,
        "count": len(records),
        "records": [
            {
                "id": record.id,
                "visit_date": record.visit_date.isoformat(),
                "hospital_name": record.hospital_name,
                "department": record.department,
                "prescriptions": record.prescriptions
            }
            for record in records
        ]
    }





