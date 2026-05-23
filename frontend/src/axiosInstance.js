import axios from 'axios'
import API_BASE_URL from './api/config'

// All requests go to <backend>/api/v1/*
const baseURL = `${API_BASE_URL}/api/v1`

// Create a configurable axios instance (we can attach interceptors to this)
const axiosInstance = axios.create({
    baseURL: baseURL,
    headers: { 'Content-Type': 'application/json' },
    withCredentials: true,   // tell browser to include HTTP-only cookies on cross-origin requests
})

//  Request Interceptor 
// Runs BEFORE every request leaves the browser.
// We could attach auth headers here, but since we use HTTP-only cookies
// the browser sends them automatically — this is mostly for debugging.
axiosInstance.interceptors.request.use(
    function (config) {
        console.log("Request config ->", config)
        return config
    },
    function (error) {
        return Promise.reject(error)
    }
)

//  Response Interceptor 
// Runs AFTER every response arrives.
// If we get a 401 (access token expired), we try ONCE to refresh
// using the refresh-token cookie, then replay the original request.
// This is what keeps the user logged in seamlessly.
axiosInstance.interceptors.response.use(
    function (response) {
        return response
    },
    async function (error) {
        const originalRequest = error.config

        if (
            error.response?.status === 401 &&
            !originalRequest._retry &&
            !originalRequest.url.includes("refresh/") &&
            !originalRequest.url.includes("dashboard-protected/")
        ) {
            originalRequest._retry = true
            try {
                // Hit /api/v1/refresh/ — Django reads refresh_token cookie,
                // issues a new access_token cookie
                await axiosInstance.post('refresh/')
                // Retry the original request — new cookie is automatically attached
                return axiosInstance(originalRequest)
            } catch {
                // Refresh failed → user is genuinely logged out
                window.location.href = '/login'
            }
        }
        return Promise.reject(error)
    }
)

export default axiosInstance
