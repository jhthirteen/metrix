import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from './App.jsx'
import Search from './pages/Search'
import PlayerPage from './pages/PlayerPage'
import Testing from './pages/Testing'
import LandingPage from './pages/LandingPage'
import Newsletter from './pages/Newsletter'

// for testing purposes --> comment the working prod page out and uncomment the <Testing /> page

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      {/* <Testing /> */}
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/news" element={<Newsletter />} />
        <Route path="/search" element={<Search />} />
        <Route path="/player/:playerName" element={<PlayerPage />} />
      </Routes>
    </BrowserRouter> 
  </StrictMode>
)