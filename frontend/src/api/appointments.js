import request from './request'

export const appointmentAPI = {
  // 获取预约列表
  getAppointments(userId) {
    return request.get(`/appointments/user/${userId}`)
  },
  
  // 创建预约
  createAppointment(data) {
    return request.post('/appointments/', data)
  },
  
  // 获取预约详情
  getAppointment(appointmentId) {
    return request.get(`/appointments/${appointmentId}`)
  },
  
  // 更新预约
  updateAppointment(appointmentId, data) {
    return request.put(`/appointments/${appointmentId}`, data)
  },
  
  // 取消预约
  cancelAppointment(appointmentId) {
    return request.put(`/appointments/${appointmentId}/cancel`)
  },
  
  // 智能预约推荐
  getRecommendation(data) {
    return request.post('/appointments/recommend', data)
  }
}


