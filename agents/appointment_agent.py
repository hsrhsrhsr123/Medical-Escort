"""
预约挂号Agent
处理医院预约挂号的自动化流程
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import requests
from config import settings
from loguru import logger


class AppointmentAgent:
    """预约挂号代理"""
    
    def __init__(self):
        self.hospital_api_base = settings.hospital_api_base_url
        self.api_key = settings.hospital_api_key
    
    def search_hospitals(
        self,
        location: str,
        department: Optional[str] = None
    ) -> List[Dict]:
        """
        搜索附近的医院
        
        Args:
            location: 地理位置
            department: 科室（可选）
        
        Returns:
            医院列表
        """
        # 这里是模拟数据，实际应对接真实的医院系统API
        hospitals = [
            {
                "id": "h001",
                "name": "市人民医院",
                "address": "城区人民路123号",
                "level": "三甲",
                "distance": "2.5公里",
                "departments": ["内科", "外科", "心血管内科", "消化内科", "骨科"],
                "available_dates": self._get_available_dates(7)
            },
            {
                "id": "h002",
                "name": "市中医院",
                "address": "城区中山路456号",
                "level": "三甲",
                "distance": "3.8公里",
                "departments": ["中医内科", "针灸科", "康复科", "骨伤科"],
                "available_dates": self._get_available_dates(7)
            },
            {
                "id": "h003",
                "name": "区中心医院",
                "address": "新区建设路789号",
                "level": "二甲",
                "distance": "4.2公里",
                "departments": ["内科", "外科", "儿科", "妇科"],
                "available_dates": self._get_available_dates(5)
            }
        ]
        
        # 如果指定了科室，过滤医院
        if department:
            hospitals = [
                h for h in hospitals 
                if department in h["departments"] or any(department in d for d in h["departments"])
            ]
        
        logger.info(f"搜索医院: 地点={location}, 科室={department}, 找到{len(hospitals)}家")
        return hospitals
    
    def get_available_slots(
        self,
        hospital_id: str,
        department: str,
        date: str
    ) -> List[Dict]:
        """
        获取可预约的时间段
        
        Args:
            hospital_id: 医院ID
            department: 科室
            date: 日期（YYYY-MM-DD）
        
        Returns:
            可用时间段列表
        """
        # 模拟号源数据
        slots = []
        
        # 上午时段
        morning_slots = [
            {"time": "08:00-08:30", "available": True, "doctor": "张主任", "title": "主任医师"},
            {"time": "08:30-09:00", "available": True, "doctor": "李医生", "title": "副主任医师"},
            {"time": "09:00-09:30", "available": False, "doctor": "王医生", "title": "主治医师"},
            {"time": "09:30-10:00", "available": True, "doctor": "赵医生", "title": "主治医师"},
            {"time": "10:00-10:30", "available": True, "doctor": "张主任", "title": "主任医师"},
        ]
        
        # 下午时段
        afternoon_slots = [
            {"time": "14:00-14:30", "available": True, "doctor": "孙医生", "title": "副主任医师"},
            {"time": "14:30-15:00", "available": True, "doctor": "周医生", "title": "主治医师"},
            {"time": "15:00-15:30", "available": False, "doctor": "吴医生", "title": "主任医师"},
            {"time": "15:30-16:00", "available": True, "doctor": "郑医生", "title": "主治医师"},
        ]
        
        slots.extend(morning_slots)
        slots.extend(afternoon_slots)
        
        logger.info(f"获取号源: 医院={hospital_id}, 科室={department}, 日期={date}")
        return slots
    
    def make_appointment(
        self,
        user_info: Dict,
        hospital_id: str,
        hospital_name: str,
        department: str,
        doctor: str,
        appointment_time: str
    ) -> Dict:
        """
        创建预约
        
        Args:
            user_info: 用户信息
            hospital_id: 医院ID
            hospital_name: 医院名称
            department: 科室
            doctor: 医生姓名
            appointment_time: 预约时间
        
        Returns:
            预约结果
        """
        try:
            # 在实际应用中，这里会调用医院的预约API
            # 模拟预约成功
            appointment_number = f"GH{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            result = {
                "success": True,
                "appointment_number": appointment_number,
                "hospital_id": hospital_id,
                "hospital_name": hospital_name,
                "department": department,
                "doctor": doctor,
                "appointment_time": appointment_time,
                "patient_name": user_info.get("name"),
                "patient_phone": user_info.get("phone"),
                "qr_code": f"QR_{appointment_number}",  # 就诊二维码
                "instructions": self._generate_appointment_instructions(
                    hospital_name, department, appointment_time
                )
            }
            
            logger.info(f"预约成功: {appointment_number} - {user_info.get('name')} - {hospital_name}/{department}")
            
            return result
            
        except Exception as e:
            logger.error(f"预约失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def cancel_appointment(self, appointment_number: str) -> Dict:
        """
        取消预约
        
        Args:
            appointment_number: 预约单号
        
        Returns:
            取消结果
        """
        try:
            # 实际应用中调用医院API取消预约
            logger.info(f"取消预约: {appointment_number}")
            
            return {
                "success": True,
                "message": "预约已取消",
                "appointment_number": appointment_number
            }
            
        except Exception as e:
            logger.error(f"取消预约失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_appointment_status(self, appointment_number: str) -> Dict:
        """
        查询预约状态
        
        Args:
            appointment_number: 预约单号
        
        Returns:
            预约状态信息
        """
        # 模拟查询结果
        return {
            "appointment_number": appointment_number,
            "status": "confirmed",  # confirmed, pending, completed, cancelled
            "queue_number": 5,  # 排队人数
            "estimated_wait_time": "30分钟"
        }
    
    def _get_available_dates(self, days: int) -> List[str]:
        """生成未来可预约的日期"""
        dates = []
        for i in range(1, days + 1):
            date = datetime.now() + timedelta(days=i)
            dates.append(date.strftime("%Y-%m-%d"))
        return dates
    
    def _generate_appointment_instructions(
        self,
        hospital_name: str,
        department: str,
        appointment_time: str
    ) -> str:
        """生成就诊须知"""
        return f"""
【就诊须知】

您已成功预约{hospital_name} {department}

就诊时间：{appointment_time}

请注意：
1. 请提前30分钟到达医院
2. 携带身份证、医保卡
3. 如需空腹检查，请不要进食
4. 到达后请先在自助机或窗口取号
5. 到相应科室候诊区等待叫号

如需帮助，请联系医院服务台或拨打医院电话。
        """.strip()




