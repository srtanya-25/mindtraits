import { BrowserRouter, Routes, Route } from "react-router-dom"
import AuthProvider from "./AuthProvider"
import PrivateRoute from "./PrivateRoute"
import PublicRoute from "./PublicRoute"

import Header from "./components/Header"
import Footer from "./components/Footer"
import MainContent from "./components/MainContent"
import Login from "./components/Login"
import Register from "./components/Register"
import Dashboard from "./components/protected/Dashboard"
import TestPage from "./components/protected/TestPage"

// Single global stylesheet — imported once at the root
import "./assets/css/styles.css"

function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Header />
                <Routes>
                    {/* Public landing page */}
                    <Route path="/" element={<MainContent />} />

                    {/* Public-only routes — bounce to /dashboard if already logged in */}
                    <Route path="/login"    element={<PublicRoute><Login /></PublicRoute>} />
                    <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />

                    {/* Protected routes — require login */}
                    <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
                    <Route path="/test"      element={<PrivateRoute><TestPage  /></PrivateRoute>} />
                </Routes>
                <Footer />
            </BrowserRouter>
        </AuthProvider>
    )
}

export default App
