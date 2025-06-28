import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Publish from './pages/Publish'
import Pages from './pages/Pages'
import Analytics from './pages/Analytics'
import Campaigns from './pages/Campaigns'
import Audiences from './pages/Audiences'
import Settings from './pages/Settings'
import { useAuthStore } from './stores/authStore'

function App() {
  const { isAuthenticated } = useAuthStore()

  return (
    <div className="min-h-screen bg-gray-50">
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/publish" element={<Publish />} />
          <Route path="/pages" element={<Pages />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/campaigns" element={<Campaigns />} />
          <Route path="/audiences" element={<Audiences />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </div>
  )
}

export default App