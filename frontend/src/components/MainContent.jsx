import { Link } from "react-router-dom"
import { useContext } from "react"
import { AuthContext } from "../AuthProvider"

// Landing page shown at "/"
const MainContent = () => {
    const { isLoggedIn } = useContext(AuthContext)

    return (
        <div className="container py-5">
            <div className="row justify-content-center">
                <div className="col-md-8 text-center">
                    <h1 className="text-light mb-3">
                        Discover How You <span className="text-info">Think</span>
                    </h1>
                    <p className="text-light mb-4">
                        MindTraits analyses your{" "}
                        <strong>Big Five personality traits</strong>, thinking style,
                        and behaviour through a short questionnaire with response-time
                        tracking, then suggests careers that fit your profile.
                    </p>

                    <div className="row mt-5 text-start">
                        <div className="col-md-4 mb-3">
                            <div className="bg-light-dark p-3 rounded h-100">
                                <h5 className="text-info">Big Five Analysis</h5>
                                <p className="text-light small mb-0">
                                    Openness, Conscientiousness, Extraversion, Agreeableness,
                                    and Neuroticism, scored from your answers.
                                </p>
                            </div>
                        </div>
                        <div className="col-md-4 mb-3">
                            <div className="bg-light-dark p-3 rounded h-100">
                                <h5 className="text-info">ML Predictions</h5>
                                <p className="text-light small mb-0">
                                    A trained model predicts your type and shows how
                                    each trait contributed to the result.
                                </p>
                            </div>
                        </div>
                        <div className="col-md-4 mb-3">
                            <div className="bg-light-dark p-3 rounded h-100">
                                <h5 className="text-info">Career Insights</h5>
                                <p className="text-light small mb-0">
                                    Role recommendations matched to your thinking style
                                    and behaviour patterns.
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="mt-4">
                        {isLoggedIn ? (
                            <Link to="/test">
                                <button className="btn btn-info btn-lg">
                                    Take the Test
                                </button>
                            </Link>
                        ) : (
                            <>
                                <Link to="/register">
                                    <button className="btn btn-info btn-lg me-2">
                                        Get Started
                                    </button>
                                </Link>
                                <Link to="/login">
                                    <button className="btn btn-outline-light btn-lg">
                                        Login
                                    </button>
                                </Link>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default MainContent
