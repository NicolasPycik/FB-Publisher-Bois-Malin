import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Dashboard
export const fetchDashboardData = () => api.get('/dashboard/overview')

// Pages
export const fetchPages = () => api.get('/facebook/pages')
export const syncPages = () => api.post('/facebook/pages/sync')

// Publishing
export const publishToPages = (data) => api.post('/facebook/publish/multi', data)

// Analytics
export const fetchAnalytics = (dateRange) => api.get(`/analytics?period=${dateRange}`)
export const fetchPostsPerformance = () => api.get('/facebook/posts/performance')

// Campaigns
export const fetchCampaigns = () => api.get('/facebook/campaigns')
export const createCampaign = (data) => api.post('/facebook/campaigns/create', data)
export const deleteCampaign = (id) => api.delete(`/facebook/campaigns/${id}`)

// Audiences
export const fetchAudiences = () => api.get('/facebook/audiences')
export const createAudience = (data) => api.post('/facebook/audiences', data)
export const updateAudience = (id, data) => api.put(`/facebook/audiences/${id}`, data)
export const deleteAudience = (id) => api.delete(`/facebook/audiences/${id}`)
export const duplicateAudience = (id) => api.post(`/facebook/audiences/${id}/duplicate`)

// Settings
export const fetchSettings = () => api.get('/settings')
export const saveSettings = (data) => api.post('/settings', data)
export const testConnection = () => api.post('/facebook/test-connection')

// Boost
export const boostPost = (postId, data) => api.post(`/facebook/posts/${postId}/boost`, data)

export default api