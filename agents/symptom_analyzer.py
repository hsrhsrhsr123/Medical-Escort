"""
症状分析Agent
基于AI分析患者症状，推荐合适的科室和医生
"""
from typing import Dict, List, Optional
from openai import OpenAI
from config import settings
from loguru import logger


class SymptomAnalyzer:
    """症状分析器"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        
        # 常见科室列表
        self.departments = [
            "内科", "外科", "妇科", "儿科", "骨科", "神经内科", "心血管内科",
            "消化内科", "呼吸内科", "内分泌科", "肾内科", "皮肤科", "眼科",
            "耳鼻喉科", "口腔科", "泌尿外科", "胸外科", "神经外科", "肿瘤科",
            "精神科", "中医科", "康复科", "急诊科"
        ]
    
    def analyze_symptoms(
        self,
        symptoms: str,
        patient_info: Optional[Dict] = None
    ) -> Dict:
        """
        分析症状并推荐科室
        
        Args:
            symptoms: 症状描述
            patient_info: 患者信息（年龄、性别、病史等）
        
        Returns:
            分析结果，包含推荐科室、紧急程度、就医建议等
        """
        try:
            # 构建提示词
            prompt = self._build_prompt(symptoms, patient_info)
            
            # 调用AI进行分析
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的医疗导诊助手，帮助患者分析症状并推荐合适的就医科室。"
                                 "你的回答要简洁明了，适合老年人理解。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            
            # 解析AI响应
            result = self._parse_ai_response(ai_response, symptoms)
            
            logger.info(f"症状分析完成: {symptoms[:50]}... -> {result['recommended_department']}")
            
            return result
            
        except Exception as e:
            logger.error(f"症状分析失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "recommended_department": "内科",  # 默认推荐
                "urgency": "normal",
                "advice": "建议先挂内科，由医生进一步诊断。"
            }
    
    def _build_prompt(self, symptoms: str, patient_info: Optional[Dict] = None) -> str:
        """构建AI提示词"""
        prompt = f"患者症状：{symptoms}\n\n"
        
        if patient_info:
            prompt += "患者信息：\n"
            if patient_info.get("age"):
                prompt += f"- 年龄：{patient_info['age']}岁\n"
            if patient_info.get("gender"):
                prompt += f"- 性别：{patient_info['gender']}\n"
            if patient_info.get("chronic_diseases"):
                prompt += f"- 既往病史：{patient_info['chronic_diseases']}\n"
            if patient_info.get("allergies"):
                prompt += f"- 过敏史：{patient_info['allergies']}\n"
            prompt += "\n"
        
        prompt += f"""请根据症状分析并回答以下问题：

1. 推荐科室：从以下科室中选择最合适的（可以列出1-2个）
   {', '.join(self.departments)}

2. 紧急程度：紧急(urgent)/较急(semi-urgent)/普通(normal)

3. 就医建议：给老人简单明了的建议，包括：
   - 为什么推荐这个科室
   - 去医院前需要注意什么
   - 大概的就诊流程

请用以下格式回答：
【推荐科室】科室名称
【紧急程度】urgent/semi-urgent/normal
【就医建议】具体建议内容"""
        
        return prompt
    
    def _parse_ai_response(self, ai_response: str, symptoms: str) -> Dict:
        """解析AI响应"""
        result = {
            "success": True,
            "original_symptoms": symptoms,
            "recommended_department": "内科",
            "alternative_departments": [],
            "urgency": "normal",
            "advice": "",
            "ai_analysis": ai_response
        }
        
        lines = ai_response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if '【推荐科室】' in line or '推荐科室：' in line:
                dept = line.split('】')[-1].split('：')[-1].strip()
                # 提取主要科室和备选科室
                depts = [d.strip() for d in dept.replace('或', ',').split(',')]
                if depts:
                    result["recommended_department"] = depts[0]
                    if len(depts) > 1:
                        result["alternative_departments"] = depts[1:]
            
            elif '【紧急程度】' in line or '紧急程度：' in line:
                urgency = line.split('】')[-1].split('：')[-1].strip().lower()
                if 'urgent' in urgency or '紧急' in urgency:
                    result["urgency"] = "urgent" if 'semi' not in urgency else "semi-urgent"
                else:
                    result["urgency"] = "normal"
            
            elif '【就医建议】' in line or '就医建议：' in line:
                advice_start = ai_response.find(line)
                result["advice"] = ai_response[advice_start + len(line):].strip()
                break
        
        return result
    
    def get_department_info(self, department: str) -> Dict:
        """获取科室详细信息"""
        # 这里可以扩展为从数据库或API获取科室信息
        department_guides = {
            "内科": {
                "description": "诊治内科常见疾病，如感冒、发烧、咳嗽、腹泻等",
                "common_symptoms": ["发热", "咳嗽", "乏力", "头痛", "腹痛"],
                "preparation": "无需特殊准备，如需抽血检查建议空腹"
            },
            "心血管内科": {
                "description": "诊治心脏和血管相关疾病",
                "common_symptoms": ["胸闷", "胸痛", "心慌", "气短", "高血压"],
                "preparation": "携带近期心电图和血压记录"
            },
            "消化内科": {
                "description": "诊治消化系统疾病",
                "common_symptoms": ["胃痛", "腹泻", "便秘", "恶心", "呕吐"],
                "preparation": "如需胃镜检查，需提前预约并空腹"
            },
            # 可以继续添加更多科室信息
        }
        
        return department_guides.get(department, {
            "description": f"{department}相关疾病诊治",
            "common_symptoms": [],
            "preparation": "按医院要求准备"
        })





