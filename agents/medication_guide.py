"""
用药指导Agent
提供取药指导和用药提醒
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from openai import OpenAI
from config import settings
from loguru import logger


class MedicationGuide:
    """用药指导助手"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    def parse_prescription(
        self,
        prescription_text: str,
        prescription_image: Optional[str] = None
    ) -> Dict:
        """
        解析处方信息
        
        Args:
            prescription_text: 处方文本
            prescription_image: 处方图片（可选）
        
        Returns:
            解析后的处方信息
        """
        try:
            # 使用AI解析处方
            prompt = f"""
请解析以下处方信息，提取药品名称、用法用量：

{prescription_text}

请以JSON格式返回，包含以下字段：
- medications: 药品列表，每个药品包含：
  - name: 药品名称
  - dosage: 剂量
  - frequency: 服用频率（如：每日3次）
  - timing: 服用时间（如：饭后）
  - duration: 疗程（如：7天）
  - notes: 注意事项
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的药师助手，帮助解析和解释处方信息。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )
            
            # 解析响应（实际应该解析JSON）
            result = {
                "success": True,
                "raw_text": prescription_text,
                "ai_response": response.choices[0].message.content,
                "parsed_at": datetime.now().isoformat()
            }
            
            logger.info("处方解析完成")
            return result
            
        except Exception as e:
            logger.error(f"处方解析失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_medication_instructions(
        self,
        medication_name: str,
        patient_info: Optional[Dict] = None
    ) -> Dict:
        """
        获取药品使用说明
        
        Args:
            medication_name: 药品名称
            patient_info: 患者信息
        
        Returns:
            用药说明
        """
        try:
            prompt = f"请用简单易懂的语言，为老年人讲解{medication_name}的用法用量和注意事项。"
            
            if patient_info:
                if patient_info.get("allergies"):
                    prompt += f"\n患者过敏史：{patient_info['allergies']}"
                if patient_info.get("chronic_diseases"):
                    prompt += f"\n患者病史：{patient_info['chronic_diseases']}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个耐心的药师，用简单的话讲解用药知识，避免使用专业术语。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
            
            instructions = response.choices[0].message.content
            
            result = {
                "success": True,
                "medication_name": medication_name,
                "instructions": instructions,
                "voice_guide": self._generate_voice_instructions(medication_name, instructions)
            }
            
            logger.info(f"生成用药说明: {medication_name}")
            return result
            
        except Exception as e:
            logger.error(f"获取用药说明失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_medication_schedule(
        self,
        medications: List[Dict]
    ) -> Dict:
        """
        创建用药时间表
        
        Args:
            medications: 药品列表
        
        Returns:
            用药时间表
        """
        schedule = {
            "morning": [],      # 早上
            "noon": [],         # 中午
            "evening": [],      # 晚上
            "bedtime": [],      # 睡前
            "as_needed": []     # 必要时
        }
        
        for med in medications:
            name = med.get("name", "")
            frequency = med.get("frequency", "").lower()
            timing = med.get("timing", "").lower()
            
            # 根据服用频率和时间分配到时间表
            if "每日3次" in frequency or "tid" in frequency:
                schedule["morning"].append(med)
                schedule["noon"].append(med)
                schedule["evening"].append(med)
            elif "每日2次" in frequency or "bid" in frequency:
                schedule["morning"].append(med)
                schedule["evening"].append(med)
            elif "每日1次" in frequency or "qd" in frequency:
                if "晚" in timing or "睡前" in timing:
                    schedule["bedtime"].append(med)
                else:
                    schedule["morning"].append(med)
            elif "必要时" in frequency or "prn" in frequency:
                schedule["as_needed"].append(med)
        
        logger.info(f"创建用药时间表: {len(medications)}种药品")
        
        return {
            "success": True,
            "schedule": schedule,
            "summary": self._generate_schedule_summary(schedule)
        }
    
    def generate_reminders(
        self,
        medications: List[Dict],
        start_date: Optional[str] = None
    ) -> List[Dict]:
        """
        生成用药提醒
        
        Args:
            medications: 药品列表
            start_date: 开始日期
        
        Returns:
            提醒列表
        """
        reminders = []
        start = datetime.now() if not start_date else datetime.fromisoformat(start_date)
        
        # 定义提醒时间点
        reminder_times = {
            "morning": "08:00",
            "noon": "12:00",
            "evening": "18:00",
            "bedtime": "21:00"
        }
        
        # 为每种药品生成提醒
        for med in medications:
            duration_days = self._parse_duration(med.get("duration", "7天"))
            frequency = med.get("frequency", "").lower()
            
            # 确定需要提醒的时间点
            times = []
            if "每日3次" in frequency:
                times = ["morning", "noon", "evening"]
            elif "每日2次" in frequency:
                times = ["morning", "evening"]
            elif "每日1次" in frequency:
                times = ["morning"]
            
            # 生成具体提醒
            for day in range(duration_days):
                date = start + timedelta(days=day)
                for time_slot in times:
                    reminders.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "time": reminder_times[time_slot],
                        "medication": med.get("name"),
                        "dosage": med.get("dosage"),
                        "timing": med.get("timing"),
                        "message": f"该吃药了：{med.get('name')} {med.get('dosage')}"
                    })
        
        logger.info(f"生成{len(reminders)}条用药提醒")
        
        return reminders
    
    def get_pharmacy_guidance(
        self,
        hospital_name: str
    ) -> Dict:
        """
        获取取药流程指导
        
        Args:
            hospital_name: 医院名称
        
        Returns:
            取药指导
        """
        guidance = {
            "title": "取药指导",
            "steps": [
                {
                    "step": 1,
                    "action": "找到药房位置",
                    "description": "通常在一楼大厅，有明显的「药房」标识"
                },
                {
                    "step": 2,
                    "action": "准备缴费凭证",
                    "description": "把缴费单据拿在手上"
                },
                {
                    "step": 3,
                    "action": "在窗口等待",
                    "description": "把凭证交给药房工作人员，然后坐下等待叫号"
                },
                {
                    "step": 4,
                    "action": "取药并核对",
                    "description": "听到您的名字时到窗口取药，检查药品种类和数量"
                },
                {
                    "step": 5,
                    "action": "咨询用法",
                    "description": "向药师询问每种药怎么吃，什么时间吃"
                }
            ],
            "tips": [
                "药品较多时可以请药师帮忙用袋子分装",
                "记得询问药品的存储方法",
                "不明白的地方一定要问清楚",
                "把药师的叮嘱记在手机或纸上"
            ]
        }
        
        return guidance
    
    def check_drug_interactions(
        self,
        medications: List[str]
    ) -> Dict:
        """
        检查药物相互作用
        
        Args:
            medications: 药品名称列表
        
        Returns:
            相互作用检查结果
        """
        # 这应该对接专业的药物数据库
        # 这里返回简化的结果
        return {
            "success": True,
            "checked_medications": medications,
            "has_interactions": False,
            "warnings": [],
            "advice": "建议按医嘱服药，如有不适请及时就医"
        }
    
    def _parse_duration(self, duration_str: str) -> int:
        """解析疗程天数"""
        import re
        match = re.search(r'(\d+)', duration_str)
        if match:
            return int(match.group(1))
        return 7  # 默认7天
    
    def _generate_voice_instructions(
        self,
        medication_name: str,
        instructions: str
    ) -> str:
        """生成语音指导"""
        # 简化说明，适合语音播报
        voice_text = f"{medication_name}的服用方法：{instructions[:200]}"
        return voice_text
    
    def _generate_schedule_summary(self, schedule: Dict) -> str:
        """生成时间表摘要"""
        summary = "您的用药时间安排：\n"
        
        if schedule["morning"]:
            summary += f"早上：{len(schedule['morning'])}种药\n"
        if schedule["noon"]:
            summary += f"中午：{len(schedule['noon'])}种药\n"
        if schedule["evening"]:
            summary += f"晚上：{len(schedule['evening'])}种药\n"
        if schedule["bedtime"]:
            summary += f"睡前：{len(schedule['bedtime'])}种药\n"
        if schedule["as_needed"]:
            summary += f"必要时：{len(schedule['as_needed'])}种药\n"
        
        return summary.strip()





