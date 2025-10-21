"""
数据模型定义
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """用户（老人）信息表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    id_card = Column(String(18), unique=True)
    age = Column(Integer)
    gender = Column(String(10))
    address = Column(String(200))
    emergency_contact_name = Column(String(50))  # 紧急联系人（子女）
    emergency_contact_phone = Column(String(20))
    
    # 健康档案
    medical_history = Column(Text)  # 病史
    allergies = Column(Text)  # 过敏史
    chronic_diseases = Column(Text)  # 慢性病
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关联关系
    appointments = relationship("Appointment", back_populates="user")
    medical_records = relationship("MedicalRecord", back_populates="user")


class Appointment(Base):
    """预约挂号表"""
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 预约信息
    hospital_name = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)  # 科室
    doctor_name = Column(String(50))
    appointment_date = Column(DateTime, nullable=False)
    appointment_number = Column(String(50))  # 挂号单号
    
    # 症状和诊断
    symptoms = Column(Text)  # 症状描述
    ai_analysis = Column(Text)  # AI分析结果
    
    # 状态
    status = Column(String(20), default="pending")  # pending, confirmed, completed, cancelled
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关联关系
    user = relationship("User", back_populates="appointments")
    medical_record = relationship("MedicalRecord", back_populates="appointment", uselist=False)


class MedicalRecord(Base):
    """就医记录表"""
    __tablename__ = "medical_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    
    # 就医信息
    visit_date = Column(DateTime, nullable=False)
    hospital_name = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    doctor_name = Column(String(50))
    
    # 诊断信息
    diagnosis = Column(Text)  # 诊断结果
    treatment_plan = Column(Text)  # 治疗方案
    
    # 处方信息
    prescriptions = Column(JSON)  # 药品清单
    
    # 检查检验
    examinations = Column(JSON)  # 检查项目
    test_results = Column(JSON)  # 化验结果
    
    # 费用
    total_cost = Column(String(20))
    
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联关系
    user = relationship("User", back_populates="medical_records")
    appointment = relationship("Appointment", back_populates="medical_record")


class GuidanceLog(Base):
    """引导记录表"""
    __tablename__ = "guidance_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    
    # 引导信息
    guidance_type = Column(String(50), nullable=False)  # registration, payment, pharmacy, examination
    guidance_content = Column(Text, nullable=False)
    step_number = Column(Integer)
    
    # 状态
    is_completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.now)





