import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import LandingNav from './LandingNav/LandingNav.tsx'
import LandingBody from './LandingBody/LandingBody.tsx'
import Login from './Login/Login.tsx'

function LandingPage() {
  return (
    <>
      <LandingNav />
        <LandingBody />
    </>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
        </Routes>
    </BrowserRouter>
  </StrictMode>,
)