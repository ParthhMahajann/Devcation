import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': import.meta.env.VITE_API_KEY || 'dev-insecure-key-change-me',
  },
})

client.interceptors.response.use(
  (res) => res,
  (err) => {
    let detail
    if (!err.response) {
      detail = 'Cannot reach the server. Check your connection or try again later.'
    } else {
      detail = err.response.data?.detail || err.message
    }
    const error = new Error(detail)
    error.status = err.response?.status
    return Promise.reject(error)
  }
)

export default client
