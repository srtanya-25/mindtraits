import { useContext } from "react"
import { Navigate } from "react-router-dom"
import { AuthContext } from "./AuthProvider"

// Wrap any route that requires login.
// If the user is logged in -> render the page. Otherwise -> /login
const PrivateRoute = ({ children }) => {
    const { isLoggedIn } = useContext(AuthContext)
    return isLoggedIn ? children : <Navigate to="/login" />
}

export default PrivateRoute
