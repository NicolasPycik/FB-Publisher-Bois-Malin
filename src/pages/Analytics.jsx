import React, { useState } from 'react'
import { useQuery } from 'react-query'
import { 
  EyeIcon, 
  HeartIcon, 
  ShareIcon,
  TrendingUpIcon,
  CalendarIcon
} from '@heroicons/react/24/outline'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import StatCard from '../components/ui/StatCard'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { fetchAnalytics } from '../services/api'

const Analytics = () => {
  const [dateRange, setDateRange] = useState('7d')
  
  const { data: analytics, isLoading } = useQuery(
    ['analytics', dateRange],
    () => fetchAnalytics(dateRange)
  )

  // Sample data for charts
  const reachData = [
    { name: 'Lun', reach: 1200, engagement: 65 },
    { name: 'Mar', reach: 1900, engagement: 89 },
    { name: 'Mer', reach: 3000, engagement: 180 },
    { name: 'Jeu', reach: 5000, engagement: 281 },
    { name: 'Ven', reach: 2300, engagement: 156 },
    { name: 'Sam', reach: 2200, engagement: 155 },
    { name: 'Dim', reach: 1800, engagement: 140 },
  ]

  const topPosts = [
    {
      id: '1',
      message: 'Découvrez notre nouvelle gamme de terrasses en bois composite ! 🌿',
      reach: 5420,
      engagement: 342,
      shares: 28,
      page: 'Bois Malin Paris'
    },
    {
      id: '2',
      message: 'Promotion spéciale sur les lames de terrasse en pin traité 🏡',
      reach: 4890,
      engagement: 298,
      shares: 45,
      page: 'Bois Malin Lyon'
    },
    {
      id: '3',
      message: 'Conseils d\'entretien pour vos terrasses en bois 🔧',
      reach: 3240,
      engagement: 234,
      shares: 18,
      page: 'Bois Malin Marseille'
    }
  ]

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Statistiques</h1>
          <p className="text-gray-600">Analyse des performances de vos pages Facebook</p>
        </div>
        
        <div className="flex items-center space-x-4 mt-4 sm:mt-0">
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="input w-auto"
          >
            <option value="7d">7 derniers jours</option>
            <option value="30d">30 derniers jours</option>
            <option value="90d">90 derniers jours</option>
          </select>
          
          <button className="btn btn-secondary">
            <CalendarIcon className="h-5 w-5 mr-2" />
            Exporter
          </button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Portée totale"
          value="45.2K"
          change="+8.3% vs période précédente"
          changeType="increase"
          icon={EyeIcon}
        />
        <StatCard
          title="Engagement total"
          value="3.2K"
          change="+12.5% vs période précédente"
          changeType="increase"
          icon={HeartIcon}
        />
        <StatCard
          title="Partages"
          value="892"
          change="+5.2% vs période précédente"
          changeType="increase"
          icon={ShareIcon}
        />
        <StatCard
          title="Taux d'engagement"
          value="7.1%"
          change="+0.8% vs période précédente"
          changeType="increase"
          icon={TrendingUpIcon}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Reach Chart */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Évolution de la portée
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={reachData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="reach" 
                stroke="#3b82f6" 
                strokeWidth={2}
                dot={{ fill: '#3b82f6' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Engagement Chart */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Engagement par jour
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={reachData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="engagement" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Top Posts */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Publications les plus performantes
        </h3>
        <div className="space-y-4">
          {topPosts.map((post, index) => (
            <div key={post.id} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-primary-600">
                    #{index + 1}
                  </span>
                </div>
              </div>
              
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 mb-1">
                  {post.message}
                </p>
                <p className="text-xs text-gray-500 mb-2">{post.page}</p>
                
                <div className="flex items-center space-x-4 text-sm text-gray-600">
                  <div className="flex items-center">
                    <EyeIcon className="h-4 w-4 mr-1" />
                    {post.reach.toLocaleString()}
                  </div>
                  <div className="flex items-center">
                    <HeartIcon className="h-4 w-4 mr-1" />
                    {post.engagement}
                  </div>
                  <div className="flex items-center">
                    <ShareIcon className="h-4 w-4 mr-1" />
                    {post.shares}
                  </div>
                </div>
              </div>
              
              <div className="flex-shrink-0">
                <button className="btn btn-secondary btn-sm">
                  Booster
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Analytics