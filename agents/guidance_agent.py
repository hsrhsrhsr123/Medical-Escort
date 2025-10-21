"""
就医流程引导Agent
为老人提供就医全流程的语音/文字指导
"""
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger


class GuidanceAgent:
    """就医流程引导代理"""
    
    def __init__(self):
        # 定义就医流程步骤
        self.process_steps = {
            "registration": {
                "name": "挂号取号",
                "steps": [
                    "到达医院后，找到挂号大厅",
                    "在自助机上扫描预约二维码，或到人工窗口报预约号",
                    "取得挂号单和候诊号码",
                    "保管好挂号单，看病时需要"
                ]
            },
            "waiting": {
                "name": "候诊等待",
                "steps": [
                    "根据挂号单上的科室信息，找到对应的诊区",
                    "在候诊区坐下等待",
                    "留意大屏幕或广播叫号",
                    "听到您的号码时，到相应的诊室"
                ]
            },
            "consultation": {
                "name": "医生诊疗",
                "steps": [
                    "进入诊室后向医生问好",
                    "清楚描述您的不舒服症状",
                    "如实回答医生的问题",
                    "如果听不清楚，请让医生说慢一点",
                    "医生开处方或检查单后，请确认是否听明白"
                ]
            },
            "examination": {
                "name": "检查检验",
                "steps": [
                    "拿着检查单到缴费窗口或自助机缴费",
                    "缴费后到相应的检查科室",
                    "向工作人员出示缴费凭证",
                    "按照医护人员指示配合检查",
                    "检查完成后询问多久能取结果"
                ]
            },
            "payment": {
                "name": "缴费",
                "steps": [
                    "拿着医生开的处方到收费窗口",
                    "可以使用医保卡、现金或手机支付",
                    "保存好缴费凭证"
                ]
            },
            "pharmacy": {
                "name": "取药",
                "steps": [
                    "缴费后到药房窗口",
                    "把缴费凭证给药房工作人员",
                    "等待叫号取药",
                    "取药时请核对药品名称和数量",
                    "询问药师如何服用药物"
                ]
            },
            "follow_up": {
                "name": "复诊安排",
                "steps": [
                    "如果医生要求复诊，记住复诊时间",
                    "可以在离开前预约下次挂号",
                    "保存好所有的检查报告和病历"
                ]
            }
        }
    
    def get_full_guidance(
        self,
        appointment_info: Dict
    ) -> Dict:
        """
        获取完整的就医流程指导
        
        Args:
            appointment_info: 预约信息
        
        Returns:
            完整流程指导
        """
        hospital_name = appointment_info.get("hospital_name", "医院")
        department = appointment_info.get("department", "相关科室")
        appointment_time = appointment_info.get("appointment_time", "预约时间")
        
        guidance = {
            "title": "就医流程完整指导",
            "appointment_info": appointment_info,
            "timeline": self._generate_timeline(appointment_time),
            "process": self.process_steps,
            "important_reminders": [
                "请提前30分钟到达医院",
                "携带身份证、医保卡",
                "带上以前的病历和检查报告",
                "如果不舒服可随时告诉医护人员",
                "遇到困难可以找医院的志愿者或导医台"
            ],
            "emergency_contacts": self._get_emergency_info(hospital_name)
        }
        
        logger.info(f"生成完整就医指导: {hospital_name}/{department}")
        
        return guidance
    
    def get_current_step_guidance(
        self,
        current_step: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        获取当前步骤的详细指导
        
        Args:
            current_step: 当前步骤（registration/waiting/consultation等）
            context: 上下文信息
        
        Returns:
            当前步骤的详细指导
        """
        if current_step not in self.process_steps:
            return {
                "success": False,
                "error": "未知步骤"
            }
        
        step_info = self.process_steps[current_step]
        
        guidance = {
            "success": True,
            "step_name": step_info["name"],
            "steps": step_info["steps"],
            "tips": self._get_step_tips(current_step),
            "next_step": self._get_next_step(current_step),
            "voice_guidance": self._generate_voice_guidance(current_step, step_info)
        }
        
        # 根据上下文添加个性化信息
        if context:
            guidance["personalized_info"] = self._personalize_guidance(current_step, context)
        
        return guidance
    
    def get_location_guidance(
        self,
        hospital_id: str,
        target_location: str
    ) -> Dict:
        """
        获取医院内部位置指引
        
        Args:
            hospital_id: 医院ID
            target_location: 目标位置（如：药房、检验科等）
        
        Returns:
            位置指引信息
        """
        # 这里应该从医院地图数据库获取实际路线
        # 目前返回模拟数据
        location_guides = {
            "药房": {
                "description": "药房在一楼大厅左侧",
                "route": [
                    "从门诊大厅进入",
                    "向左转",
                    "看到绿色的「药房」标志",
                    "在窗口等待叫号"
                ],
                "landmarks": ["ATM机旁边", "便利店对面"]
            },
            "检验科": {
                "description": "检验科在二楼",
                "route": [
                    "乘坐电梯到二楼",
                    "出电梯后向右走",
                    "看到「检验科」标识",
                    "在抽血窗口排队"
                ],
                "landmarks": ["儿科诊区旁边"]
            },
            "收费处": {
                "description": "收费处在一楼大厅",
                "route": [
                    "在门诊大厅中央",
                    "有多个窗口",
                    "也可使用自助缴费机"
                ],
                "landmarks": ["挂号处对面"]
            }
        }
        
        return location_guides.get(target_location, {
            "description": f"请向医院导医台询问{target_location}的位置",
            "route": ["找到导医台", "向工作人员询问"],
            "landmarks": []
        })
    
    def generate_voice_guidance(
        self,
        step: str,
        language: str = "zh-CN"
    ) -> str:
        """
        生成适合语音播报的指导文本
        
        Args:
            step: 步骤名称
            language: 语言
        
        Returns:
            语音指导文本
        """
        if step not in self.process_steps:
            return "请按照医院指示进行操作"
        
        step_info = self.process_steps[step]
        
        voice_text = f"现在需要进行{step_info['name']}。"
        voice_text += "请按照以下步骤操作：\n"
        
        for i, instruction in enumerate(step_info["steps"], 1):
            voice_text += f"第{i}步，{instruction}。\n"
        
        return voice_text
    
    def _generate_timeline(self, appointment_time: str) -> List[Dict]:
        """生成就医时间线"""
        return [
            {
                "time": "就诊前30分钟",
                "action": "从家出发",
                "note": "预留足够的路上时间"
            },
            {
                "time": "到达医院",
                "action": "挂号取号",
                "note": "找到自助机或人工窗口"
            },
            {
                "time": "等待叫号",
                "action": "在候诊区等待",
                "note": "注意听叫号"
            },
            {
                "time": "轮到就诊",
                "action": "进入诊室看病",
                "note": "向医生说明病情"
            },
            {
                "time": "诊疗后",
                "action": "缴费和取药",
                "note": "按医嘱服药"
            }
        ]
    
    def _get_step_tips(self, step: str) -> List[str]:
        """获取步骤提示"""
        tips = {
            "registration": [
                "如果不会用自助机，可以去人工窗口",
                "告诉工作人员您的预约号或姓名",
                "不要着急，慢慢来"
            ],
            "waiting": [
                "坐在候诊椅上休息",
                "如果等待时间长，可以喝点水",
                "不要走远，以免错过叫号"
            ],
            "consultation": [
                "不要紧张，医生很和蔼",
                "把症状说清楚",
                "有问题就问医生"
            ],
            "pharmacy": [
                "仔细听药师讲解服药方法",
                "记住每天吃几次，每次吃几片",
                "有不明白的一定要问"
            ]
        }
        return tips.get(step, [])
    
    def _get_next_step(self, current_step: str) -> Optional[str]:
        """获取下一步骤"""
        step_order = [
            "registration", "waiting", "consultation", 
            "examination", "payment", "pharmacy", "follow_up"
        ]
        
        try:
            current_index = step_order.index(current_step)
            if current_index < len(step_order) - 1:
                next_step = step_order[current_index + 1]
                return self.process_steps[next_step]["name"]
        except ValueError:
            pass
        
        return None
    
    def _generate_voice_guidance(self, step: str, step_info: Dict) -> str:
        """生成语音指导文本"""
        text = f"{step_info['name']}指导：\n"
        for i, instruction in enumerate(step_info["steps"], 1):
            text += f"{i}. {instruction}\n"
        return text.strip()
    
    def _personalize_guidance(self, step: str, context: Dict) -> Dict:
        """个性化指导信息"""
        personalized = {}
        
        # 根据患者年龄调整指导
        if context.get("age") and context["age"] > 70:
            personalized["age_note"] = "如需帮助，可以请志愿者陪同"
        
        # 根据就诊科室提供特定建议
        if step == "examination" and context.get("department"):
            dept = context["department"]
            if "心血管" in dept:
                personalized["dept_note"] = "心电图检查时请保持平静，不要紧张"
            elif "消化" in dept:
                personalized["dept_note"] = "胃镜检查前需要空腹6小时"
        
        return personalized
    
    def _get_emergency_info(self, hospital_name: str) -> Dict:
        """获取紧急联系信息"""
        return {
            "hospital_hotline": "12345678",  # 医院总机
            "emergency": "120",
            "family_contact": "已设置的紧急联系人",
            "service_desk": "医院一楼服务台"
        }





