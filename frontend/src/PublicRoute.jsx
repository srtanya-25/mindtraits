import { useContext } from "react"
import { Navigate } from "react-router-dom"
import { AuthContext } from "./AuthProvider"

// Wrap routes that should ONLY be visible when logged OUT (login/register).
// If already logged in -> bounce to /dashboard
const PublicRoute = ({ children }) => {
    const { isLoggedIn } = useContext(AuthContext)
    return isLoggedIn ? <Navigate to="/dashboard" /> : children
}

export default PublicRoute
