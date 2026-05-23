import { createContext, useState, useEffect } from "react"
import axiosInstance from "./axiosInstance"

// 1) Create a Context — any child component can read/write auth state via useContext()
const AuthContext = createContext()

// 2) Provider component — wraps the whole app in App.jsx
const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false)
    const [loading, setLoading] = useState(true)

    // On app load, ask the backend if our HTTP-only cookie is still valid
    useEffect(() => {
        const checkAuth = async () => {
            try {
                await axiosInstance.get("/dashboard-protected/")
                setIsLoggedIn(true)
            } catch (error) {
                setIsLoggedIn(false)
            } finally {
                setLoading(false)
            }
        }
        checkAuth()
    }, [])

    if (loading) {
        return <div className="text-light text-center p-5">Loading...</div>
    }

    return (
        <AuthContext.Provider value={{ isLoggedIn, setIsLoggedIn }}>
            {children}
        </AuthContext.Provider>
    )
}

export default AuthProvider
export { AuthContext }
