import { Link, useNavigate } from "react-router-dom"
import { useContext } from "react"
import { AuthContext } from "../AuthProvider"
import axiosInstance from "../axiosInstance"

const Header = () => {
    const { isLoggedIn, setIsLoggedIn } = useContext(AuthContext)
    const navigate = useNavigate()

    const handleLogout = async () => {
        try {
            // POST /api/v1/logout/ — Django clears the HTTP-only cookies
            await axiosInstance.post("logout/")
            setIsLoggedIn(false)
            console.log("Logged Out!")
            navigate("/login")
        } catch (error) {
            console.log("Logout error: ", error)
        }
    }

    return (
        <div className="text-light">
            <nav className="navbar container">
                <Link className="navbar-brand text-light" to="/">
                    MindTraits
                </Link>
                <div className="ms-auto">
                    {isLoggedIn ? (
                        <>
                            <Link to="/dashboard">
                                <button className="btn btn-outline-light me-2">Dashboard</button>
                            </Link>
                            <Link to="/test">
                                <button className="btn btn-outline-info me-2">Take Test</button>
                            </Link>
                            <button className="btn btn-danger" onClick={handleLogout}>
                                Logout
                            </button>
                        </>
                    ) : (
                        <>
                            <Link to="/login">
                                <button className="btn btn-outline-light me-2">Login</button>
                            </Link>
                            <Link to="/register">
                                <button className="btn btn-primary">Register</button>
                            </Link>
                        </>
                    )}
                </div>
            </nav>
        </div>
    )
}

export default Header
