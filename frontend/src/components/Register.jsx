import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from "axios"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSpinner } from '@fortawesome/free-solid-svg-icons'
import API_BASE_URL from '../api/config'

const Register = () => {
    const [username, setUsername] = useState('')
    const [email, setEmail]       = useState('')
    const [password, setPassword] = useState('')
    const [errors, setErrors]     = useState({})
    const [success, setSuccess]   = useState(false)
    const [loading, setLoading]   = useState(false)

    const navigate = useNavigate()

    const handleRegistration = async (e) => {
        e.preventDefault()
        setLoading(true)

        const userData = { username, email, password }

        try {
            // axios POST to Django register endpoint
            const response = await axios.post(`${API_BASE_URL}/api/v1/register/`, userData)
            console.log("Response Data:", response.data)
            console.log("Registration successful")
            setErrors({})
            setSuccess(true)
            // Redirect to login after a brief delay so user sees success message
            setTimeout(() => navigate('/login'), 1500)
        } catch (error) {
            setSuccess(false)
            setErrors(error.response?.data || {})
            console.log("Registration error:", error.response?.data)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="container">
            <div className="row justify-content-center">
                <div className="col-md-6 bg-light-dark p-5 rounded">
                    <h3 className="text-light text-center mb-4">Create an Account</h3>
                    <form onSubmit={handleRegistration}>
                        <div className="mb-3">
                            <input
                                type="text"
                                className="form-control"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                            {/* <small> renders smaller text — used for validation hints */}
                            <small>{errors.username && <div className="text-danger">{errors.username}</div>}</small>
                        </div>

                        <div className="mb-3">
                            <input
                                type="email"
                                className="form-control"
                                placeholder="Email address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                            <small>{errors.email && <div className="text-danger">{errors.email}</div>}</small>
                        </div>

                        <div className="mb-3">
                            <input
                                type="password"
                                className="form-control"
                                placeholder="Set password (min 8 characters)"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                            <small>{errors.password && <div className="text-danger">{errors.password}</div>}</small>
                        </div>

                        {success && (
                            <div className="alert alert-success">
                                Registration Successful — redirecting to login...
                            </div>
                        )}

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
                                Register
                            </button>
                        )}
                    </form>
                </div>
            </div>
        </div>
    )
}

export default Register
