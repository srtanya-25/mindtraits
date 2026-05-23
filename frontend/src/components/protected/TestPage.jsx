import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axiosInstance from '../../axiosInstance'

// The 20-question Big Five personality test.
// Each question is scored 1-5 (Likert scale).
// We track response time per question for behavioral analytics.
const TestPage = () => {
    const [questions, setQuestions] = useState([])
    const [answers, setAnswers]     = useState({})         // { questionId: { score, response_time_ms } }
    const [loading, setLoading]     = useState(true)
    const [submitting, setSubmitting] = useState(false)
    const [error, setError]         = useState(null)
    const [startTime, setStartTime] = useState(Date.now()) // when current question was shown

    const navigate = useNavigate()

    // Fetch all 20 questions once when the page loads
    useEffect(() => {
        const fetchQuestions = async () => {
            try {
                const response = await axiosInstance.get('/questions/')
                // Backend uses our custom paginator → results live under .results
                const data = response.data.results || response.data
                setQuestions(data)
            } catch (err) {
                setError("Failed to load questions")
                console.log(err)
            } finally {
                setLoading(false)
                setStartTime(Date.now())
            }
        }
        fetchQuestions()
    }, [])

    // When the user clicks a score (1-5) on a question
    const handleAnswer = (questionId, score) => {
        const now = Date.now()
        const responseTime = now - startTime
        setAnswers({
            ...answers,
            [questionId]: { score, response_time_ms: responseTime },
        })
        setStartTime(now)   // reset timer for next question
    }

    // Submit all answers → run ML analysis → go to dashboard
    const handleSubmit = async () => {
        if (Object.keys(answers).length < questions.length) {
            alert(`Please answer all ${questions.length} questions before submitting.`)
            return
        }

        setSubmitting(true)
        try {
            // Step 1: bulk-submit answers
            const responses = Object.entries(answers).map(([questionId, data]) => ({
                question: parseInt(questionId),
                score: data.score,
                response_time_ms: data.response_time_ms,
            }))
            await axiosInstance.post('/responses/submit/', { responses })

            // Step 2: trigger the ML analysis pipeline
            await axiosInstance.post('/analyze/')

            // Step 3: redirect to dashboard which fetches the new result
            navigate('/dashboard')
        } catch (err) {
            console.log("Submit error:", err)
            alert("Something went wrong. Please try again.")
        } finally {
            setSubmitting(false)
        }
    }

    if (loading) {
        return <div className="text-light text-center p-5">Loading questions...</div>
    }

    if (error) {
        return <div className="text-light text-center p-5">{error}</div>
    }

    const answered = Object.keys(answers).length
    const progress = Math.round((answered / questions.length) * 100)

    return (
        <div className="container py-4">
            <div className="row justify-content-center">
                <div className="col-md-10">
                    <div className="text-center mb-4">
                        <h3 className="text-light">Personality Assessment</h3>
                        <p className="text-light small">
                            Rate how much you agree with each statement.
                            1 = Strongly Disagree, 5 = Strongly Agree
                        </p>
                        <div className="trait-bar" style={{ maxWidth: '500px', margin: '0 auto' }}>
                            <div className="trait-bar-fill" style={{ width: `${progress}%` }}></div>
                        </div>
                        <small className="text-light">
                            {answered} / {questions.length} answered
                        </small>
                    </div>

                    {/*  Question list  */}
                    {questions.map((q, idx) => (
                        <div key={q.id} className="question-card">
                            <p className="text-light mb-3">
                                <strong>Q{idx + 1}.</strong> {q.text}
                            </p>
                            <div className="text-center">
                                {[1, 2, 3, 4, 5].map((score) => (
                                    <button
                                        key={score}
                                        type="button"
                                        className={`btn btn-outline-light likert-btn ${
                                            answers[q.id]?.score === score ? 'active' : ''
                                        }`}
                                        onClick={() => handleAnswer(q.id, score)}
                                    >
                                        {score}
                                    </button>
                                ))}
                            </div>
                        </div>
                    ))}

                    {/*  Submit  */}
                    <div className="text-center mt-4">
                        <button
                            className="btn btn-info btn-lg"
                            onClick={handleSubmit}
                            disabled={submitting || answered < questions.length}
                        >
                            {submitting ? "Analysing..." : "Submit & See Results"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default TestPage
