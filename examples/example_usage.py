"""
医疗陪诊Agent系统使用示例
演示完整的就医流程
"""
import requests
import json
from datetime import datetime, timedelta

# API基础URL
BASE_URL = "http://localhost:8000"


def print_section(title):
    """打印章节标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def create_user_example():
    """示例1: 创建用户"""
    print_section("示例1: 创建用户档案")
    
    user_data = {
        "name": "王奶奶",
        "phone": "13800138888",
        "age": 75,
        "gender": "女",
        "address": "北京市海淀区中关村大街1号",
        "emergency_contact_name": "王小华",
        "emergency_contact_phone": "13900139999",
        "medical_history": "曾患心肌梗塞，已康复",
        "chronic_diseases": "高血压、糖尿病、冠心病",
        "allergies": "青霉素过敏、磺胺类药物过敏"
    }
    
    response = requests.post(f"{BASE_URL}/api/users/", json=user_data)
    
    if response.status_code == 200:
        user = response.json()
        print(f"✓ 用户创建成功")
        print(f"  用户ID: {user['id']}")
        print(f"  姓名: {user['name']}")
        print(f"  手机: {user['phone']}")
        return user['id']
    else:
        print(f"✗ 创建失败: {response.text}")
        return None


def analyze_symptoms_example(user_id):
    """示例2: 症状分析"""
    print_section("示例2: AI症状分析")
    
    symptoms = "最近一周总是感觉胸闷，有时候喘不上气，走路走快了就心慌，昨晚还出了一身冷汗"
    
    print(f"症状描述: {symptoms}\n")
    
    response = requests.post(
        f"{BASE_URL}/api/appointments/analyze-symptoms",
        json={
            "user_id": user_id,
            "symptoms": symptoms
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✓ AI分析结果:")
        print(f"  推荐科室: {result['recommended_department']}")
        print(f"  紧急程度: {result['urgency']}")
        print(f"\n  就医建议:")
        print(f"  {result['advice']}")
        return result['recommended_department']
    else:
        print(f"✗ 分析失败: {response.text}")
        return None


def search_hospitals_example(department):
    """示例3: 搜索医院"""
    print_section("示例3: 搜索附近医院")
    
    response = requests.get(
        f"{BASE_URL}/api/appointments/hospitals",
        params={
            "location": "海淀区",
            "department": department
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        hospitals = result['hospitals']
        print(f"✓ 找到 {len(hospitals)} 家医院\n")
        
        for i, hospital in enumerate(hospitals, 1):
            print(f"{i}. {hospital['name']}")
            print(f"   等级: {hospital['level']}")
            print(f"   距离: {hospital['distance']}")
            print(f"   地址: {hospital['address']}")
            print()
        
        return hospitals[0] if hospitals else None
    else:
        print(f"✗ 搜索失败: {response.text}")
        return None


def make_appointment_example(user_id, hospital, department):
    """示例4: 创建预约"""
    print_section("示例4: 预约挂号")
    
    # 预约明天上午9点
    tomorrow = datetime.now() + timedelta(days=1)
    appointment_time = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
    
    response = requests.post(
        f"{BASE_URL}/api/appointments/",
        json={
            "user_id": user_id,
            "hospital_id": hospital['id'],
            "hospital_name": hospital['name'],
            "department": department,
            "doctor_name": "张主任",
            "appointment_date": appointment_time.isoformat(),
            "symptoms": "胸闷、气短、心慌"
        }
    )
    
    if response.status_code == 200:
        appointment = response.json()
        print("✓ 预约成功!")
        print(f"  预约单号: {appointment.get('appointment_number', 'N/A')}")
        print(f"  医院: {appointment['hospital_name']}")
        print(f"  科室: {appointment['department']}")
        print(f"  医生: {appointment.get('doctor_name', '待定')}")
        print(f"  时间: {appointment_time.strftime('%Y年%m月%d日 %H:%M')}")
        return appointment['id']
    else:
        print(f"✗ 预约失败: {response.text}")
        return None


def get_guidance_example(appointment_id):
    """示例5: 获取就医指导"""
    print_section("示例5: 获取就医指导")
    
    response = requests.get(
        f"{BASE_URL}/api/guidance/appointment/{appointment_id}/full"
    )
    
    if response.status_code == 200:
        guidance = response.json()
        
        print("✓ 就医须知:")
        for reminder in guidance['important_reminders']:
            print(f"  • {reminder}")
        
        print("\n✓ 就医流程:")
        for step_key, step_info in guidance['process'].items():
            print(f"\n  【{step_info['name']}】")
            for i, instruction in enumerate(step_info['steps'], 1):
                print(f"    {i}. {instruction}")
    else:
        print(f"✗ 获取指导失败: {response.text}")


def get_step_guidance_example(user_id, appointment_id):
    """示例6: 获取特定步骤指导"""
    print_section("示例6: 挂号取号指导")
    
    response = requests.post(
        f"{BASE_URL}/api/guidance/step",
        json={
            "user_id": user_id,
            "appointment_id": appointment_id,
            "current_step": "registration"
        }
    )
    
    if response.status_code == 200:
        guidance = response.json()
        
        if guidance.get('success'):
            print(f"✓ {guidance['step_name']} 详细步骤:")
            for i, step in enumerate(guidance['steps'], 1):
                print(f"  {i}. {step}")
            
            print("\n温馨提示:")
            for tip in guidance['tips']:
                print(f"  💡 {tip}")
    else:
        print(f"✗ 获取指导失败: {response.text}")


def medication_example(user_id):
    """示例7: 用药指导"""
    print_section("示例7: 用药管理")
    
    # 模拟处方
    medications = [
        {
            "name": "阿司匹林肠溶片",
            "dosage": "100mg",
            "frequency": "每日1次",
            "timing": "晚饭后",
            "duration": "长期"
        },
        {
            "name": "硝酸甘油片",
            "dosage": "0.5mg",
            "frequency": "必要时",
            "timing": "胸痛时舌下含服",
            "duration": "长期备用"
        }
    ]
    
    # 创建用药时间表
    response = requests.post(
        f"{BASE_URL}/api/medications/schedule",
        json={"medications": medications}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✓ 用药时间安排:")
        print(result['summary'])
        
        schedule = result['schedule']
        if schedule['morning']:
            print("\n  早上:")
            for med in schedule['morning']:
                print(f"    • {med['name']} {med['dosage']}")
        
        if schedule['evening']:
            print("\n  晚上:")
            for med in schedule['evening']:
                print(f"    • {med['name']} {med['dosage']}")
        
        if schedule['as_needed']:
            print("\n  必要时:")
            for med in schedule['as_needed']:
                print(f"    • {med['name']} {med['dosage']} - {med['timing']}")
    
    # 获取用药说明
    print("\n" + "-"*60)
    response = requests.post(
        f"{BASE_URL}/api/medications/instructions",
        json={
            "user_id": user_id,
            "medication_name": "阿司匹林肠溶片"
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\n✓ 用药说明 - 阿司匹林肠溶片:")
        print(result['instructions'])


def pharmacy_guidance_example():
    """示例8: 取药指导"""
    print_section("示例8: 取药流程指导")
    
    response = requests.get(
        f"{BASE_URL}/api/medications/pharmacy-guidance/市人民医院"
    )
    
    if response.status_code == 200:
        guidance = response.json()
        
        print("✓ 取药步骤:")
        for step in guidance['steps']:
            print(f"\n  第{step['step']}步: {step['action']}")
            print(f"  {step['description']}")
        
        print("\n温馨提示:")
        for tip in guidance['tips']:
            print(f"  💡 {tip}")


def main():
    """主程序"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "医疗陪诊Agent系统演示" + " "*15 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        # 1. 创建用户
        user_id = create_user_example()
        if not user_id:
            print("\n创建用户失败，演示终止")
            return
        
        # 2. 症状分析
        department = analyze_symptoms_example(user_id)
        if not department:
            department = "心血管内科"
        
        # 3. 搜索医院
        hospital = search_hospitals_example(department)
        if not hospital:
            print("\n搜索医院失败，演示终止")
            return
        
        # 4. 预约挂号
        appointment_id = make_appointment_example(user_id, hospital, department)
        if not appointment_id:
            print("\n预约失败，演示终止")
            return
        
        # 5. 获取完整指导
        get_guidance_example(appointment_id)
        
        # 6. 获取特定步骤指导
        get_step_guidance_example(user_id, appointment_id)
        
        # 7. 用药指导
        medication_example(user_id)
        
        # 8. 取药指导
        pharmacy_guidance_example()
        
        print_section("演示完成")
        print("✓ 所有功能演示成功!")
        print("\n更多API文档请访问: http://localhost:8000/docs")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 连接失败: 请确保API服务已启动")
        print("启动命令: cd api && python main.py")
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")


if __name__ == "__main__":
    main()




