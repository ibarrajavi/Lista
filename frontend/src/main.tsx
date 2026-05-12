import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import LandingNav from './LandingNav/LandingNav.tsx'
import LandingBody from './LandingBody/LandingBody.tsx'


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <LandingNav/>
    <LandingBody />
  </StrictMode>,
)
