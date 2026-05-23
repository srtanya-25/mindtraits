import { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from "axios"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSpinner } from '@fortawesome/free-solid-svg-icons'
import { AuthContext } from '../AuthProvider'
import API_BASE_URL from '../api/config'

const Login = () => {
    // Local state for form fields and UI state
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [loading, setLoading] = useState(false)
    const [errors, setErrors]   = useState({})
    const [success, setSuccess] = useState(false)

    // Context API — share login state across the whole app
    const { setIsLoggedIn } = useContext(AuthContext)

    // useNavigate hook — redirect after successful login
    const navigate = useNavigate()

    const handleLogin = async (e) => {
        e.preventDefault()      // stop browser from reloading the page
        setLoading(true)

        const userData = { username, password }
        console.log("Login info:", userData)

        try {
            // axios POST to Django backend
            // withCredentials:true tells the browser to accept HTTP-only cookies
            // (access_token + refresh_token are set by Django)
            await axios.post(`${API_BASE_URL}/api/v1/login/`, userData, {
                withCredentials: true,
            })
            console.log("Login successful")
            setIsLoggedIn(true)
            setSuccess(true)
            setErrors({})
            navigate('/dashboard')      // redirect to Dashboard page
        } catch (error) {
            setErrors(error.response?.data || { detail: "Login failed" })
            console.log("Login error:", error.response?.data)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="container">
            <div className="row justify-content-center">
                <div className="col-md-6 bg-light-dark p-5 rounded">
                    <h3 className="text-light text-center mb-4">Login to your Account</h3>
                    <form onSubmit={handleLogin}>
                        <div className="mb-3">
                            <input
                                type="text"
                                className="form-control"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </div>

                        <div className="mb-3">
                            <input
                                type="password"
                                className="form-control"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>

                        <div className="mb-3">
                            {errors.error  && <div className="text-danger">{errors.error}</div>}
                            {errors.detail && <div className="text-danger">{errors.detail}</div>}
                        </div>

                        {success && (
                            <div className="alert alert-success text-center">
                                Login Successful
                            </div>
                        )}

                        {/* Conditional rendering — show spinner while loading */}
                        {loading ? (
                            <button
                                type="submit"
                                className="btn btn-info d-block mx-auto"
                                disabled
                            >
                                <FontAwesomeIcon icon={faSpinner} spin /> Please Wait...
                            </button>
                        ) : (
                            <button
                                type="submit"
                                className="btn btn-info d-block mx-auto"
                            >
                                Login
                            </button>
                        )}
                    </form>
                </div>
            </div>
        </div>
    )
}

export default Login
