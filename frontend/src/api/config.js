// API base URL — taken from .env via Vite's import.meta.env (VITE_ prefix is required)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

console.log("API_BASE_URL ->", API_BASE_URL)

export default API_BASE_URL
