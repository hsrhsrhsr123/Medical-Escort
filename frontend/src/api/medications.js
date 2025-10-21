import request from './request'

export const medicationAPI = {
  // 用药指导
  getMedicationGuidance(data) {
    return request.post('/medications/guidance', data)
  },
  
  // 用药提醒
  getMedicationReminders(userId) {
    return request.get(`/medications/reminders/${userId}`)
  },
  
  // 创建用药提醒
  createReminder(data) {
    return request.post('/medications/reminders', data)
  },
  
  // 药物相互作用检查
  checkInteractions(data) {
    return request.post('/medications/interactions', data)
  },
  
  // 用药记录
  getMedicationRecords(userId) {
    return request.get(`/medications/records/${userId}`)
  }
}


