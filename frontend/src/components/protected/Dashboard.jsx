import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axiosInstance from '../../axiosInstance'

// The Dashboard fetches the current user's latest personality result.
// Protected by PrivateRoute → only accessible when logged in.
const Dashboard = () => {
    const [result, setResult]   = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError]     = useState(null)

    // useEffect hook — runs after the component mounts.
    // Empty dependency array [] means it runs only ONCE on first render.
    useEffect(() => {
        const fetchResult = async () => {
            try {
                // GET /api/v1/result/ → returns the user's latest result
                // axiosInstance automatically sends the auth cookie
                const response = await axiosInstance.get('/result/')
                setResult(response.data)
            } catch (err) {
                if (err.response?.status === 404) {
                    setError("no_result")
                } else {
                    setError("fetch_failed")
                    console.log("Dashboard error:", err)
                }
            } finally {
                setLoading(false)
            }
        }
        fetchResult()
    }, [])

    if (loading) {
        return <div className="text-light text-center p-5">Loading your results...</div>
    }

    // No result yet → show CTA to take the test
    if (error === "no_result") {
        return (
            <div className="container py-5">
                <div className="row justify-content-center">
                    <div className="col-md-8 bg-light-dark p-5 rounded text-center">
                        <h3 className="text-light">No results yet</h3>
                        <p className="text-light">
                            You haven't completed the personality assessment yet.
                            Take the 20-question test to see your Big Five profile,
                            ML-predicted personality type, thinking style, and career
                            recommendations.
                        </p>
                        <Link to="/test">
                            <button className="btn btn-info btn-lg mt-3">
                                Take the Test
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
        )
    }

    if (error === "fetch_failed") {
        return (
            <div className="container py-5 text-light text-center">
                Error loading results. Please refresh.
            </div>
        )
    }

    // Helper: render a single trait bar (Bootstrap progress styled)
    const TraitBar = ({ label, value, max = 20 }) => {
        const percent = Math.round((value / max) * 100)
        return (
            <div className="mb-3">
                <div className="d-flex justify-content-between text-light mb-1">
                    <span>{label}</span>
                    <span>{value.toFixed(1)} / {max}</span>
                </div>
                <div className="trait-bar">
                    <div className="trait-bar-fill" style={{ width: `${percent}%` }}></div>
                </div>
            </div>
        )
    }

    return (
        <div className="container py-4">
            <div className="row">
                {/* Left column: trait scores  */}
                <div className="col-md-6 mb-4">
                    <div className="bg-light-dark p-4 rounded h-100">
                        <h4 className="text-info mb-4">Big Five Trait Scores</h4>
                        <TraitBar label="Openness"          value={result.openness} />
                        <TraitBar label="Conscientiousness" value={result.conscientiousness} />
                        <TraitBar label="Extraversion"      value={result.extraversion} />
                        <TraitBar label="Agreeableness"     value={result.agreeableness} />
                        <TraitBar label="Neuroticism"       value={result.neuroticism} />
                    </div>
                </div>

                {/*  Right column: prediction + thinking style  */}
                <div className="col-md-6 mb-4">
                    <div className="bg-light-dark p-4 rounded h-100">
                        <h4 className="text-info mb-3">Your Profile</h4>
                        <p className="text-light mb-2">
                            <strong>Predicted Type:</strong> {result.predicted_type}
                        </p>
                        <p className="text-light mb-2">
                            <strong>Thinking Style:</strong> {result.thinking_style}
                        </p>
                        <p className="text-light mb-3">
                            <strong>Test taken:</strong>{" "}
                            {new Date(result.created_at).toLocaleDateString()}
                        </p>

                        <h5 className="text-info mt-4 mb-2">Career Recommendations</h5>
                        <div>
                            {result.career_recommendations?.map((career, i) => (
                                <span key={i} className="career-chip">{career}</span>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/*  SHAP explanation  */}
            {result.shap_explanation && Object.keys(result.shap_explanation).length > 0 && (
                <div className="row">
                    <div className="col-md-12">
                        <div className="bg-light-dark p-4 rounded">
                            <h4 className="text-info mb-3">Why This Result?</h4>
                            <p className="text-light small">
                                How much each trait contributed to your prediction:
                            </p>
                            {Object.entries(result.shap_explanation).map(([trait, percent]) => (
                                <TraitBar
                                    key={trait}
                                    label={trait}
                                    value={percent}
                                    max={100}
                                />
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Retake button */}
            <div className="text-center mt-3">
                <Link to="/test">
                    <button className="btn btn-outline-info">Retake Test</button>
                </Link>
            </div>
        </div>
    )
}

export default Dashboard
