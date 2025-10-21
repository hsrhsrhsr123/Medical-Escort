import request from './request'

export const guidanceAPI = {
  // 症状分析
  analyzeSymptom(data) {
    return request.post('/guidance/symptom-analysis', data)
  },
  
  // 就诊流程指导
  getProcessGuidance(data) {
    return request.post('/guidance/process', data)
  },
  
  // 科室推荐
  getDepartmentRecommendation(data) {
    return request.post('/guidance/department-recommend', data)
  },
  
  // 就医准备建议
  getPreparationAdvice(data) {
    return request.post('/guidance/preparation', data)
  }
}


