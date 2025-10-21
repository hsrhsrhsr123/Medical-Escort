import request from './request'

export const userAPI = {
  // 获取用户列表
  getUsers(params) {
    return request.get('/users/', { params })
  },
  
  // 创建用户
  createUser(data) {
    return request.post('/users/', data)
  },
  
  // 获取用户详情
  getUser(userId) {
    return request.get(`/users/${userId}`)
  },
  
  // 更新用户
  updateUser(userId, data) {
    return request.put(`/users/${userId}`, data)
  },
  
  // 删除用户
  deleteUser(userId) {
    return request.delete(`/users/${userId}`)
  }
}


