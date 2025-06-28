import React from 'react'
import { useQuery } from 'react-query'
import { 
  DocumentTextIcon, 
  PencilIcon, 
  EyeIcon, 
  HeartIcon,
  TrendingUpIcon,
  UsersIcon
} from '@heroicons/react/24/outline'
import StatCard from '../components/ui/StatCard'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { fetchDashboardData } from '../services/api'

const Dashboard = () => {
  const { data: dashboardData, isLoading, error } = useQuery(
    'dashboard',
    fetchDashboardData,
    {
      refetchInterval: 30000, // Refresh every 30 seconds
    }
  )

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">Erreur lors du chargement du dashboard</p>
      </div>
    )
  }

  const stats = [
    {
      title: 'Pages connectées',
      value: dashboardData?.pages_count || '66',
      change: '+2 cette semaine',
      changeType: 'increase',
      icon: DocumentTextIcon,
    },
    {
      title: 'Publications',
      value: dashboardData?.posts_today || '247',
      change: '+15 aujourd\'hui',
      changeType: 'increase',
      icon: PencilIcon,
    },
    {
      title: 'Portée totale',
      value: dashboardData?.total_reach || '45.2K',
      change: '+8.3% ce mois',
      changeType: 'increase',
      icon: EyeIcon,
    },
    {
      title: 'Engagement',
      value: dashboardData?.engagement || '12.8%',
      change: '+2.1% ce mois',
      changeType: 'increase',
      icon: HeartIcon,
    },
  ]

  const recentActivities = dashboardData?.recent_activities || [
    {
      activity: 'Publication sur 5 pages',
      type: 'Post',
      status: 'Publié',
      time: 'Il y a 2h'
    },
    {
      activity: 'Campagne "Promo Été" créée',
      type: 'Publicité',
      status: 'En attente',
      time: 'Il y a 4h'
    },
    {
      activity: 'Boost post avec budget 20€',
      type: 'Boost',
      status: 'Actif',
      time: 'Il y a 6h'
    }
  ]

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-xl p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">Bienvenue sur Facebook Publisher</h1>
        <p className="text-primary-100">
          Gérez vos {stats[0].value} pages Facebook depuis une interface unique
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => (
          <StatCard
            key={index}
            title={stat.title}
            value={stat.value}
            change={stat.change}
            changeType={stat.changeType}
            icon={stat.icon}
            className="animate-fade-in"
            style={{ animationDelay: `${index * 100}ms` }}
          />
        ))}
      </div>

      {/* Recent Activities */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Activités récentes
          </h3>
          <div className="space-y-4">
            {recentActivities.map((activity, index) => (
              <div key={index} className="flex items-center space-x-3">
                <div className="flex-shrink-0">
                  <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                    <TrendingUpIcon className="h-4 w-4 text-primary-600" />
                  </div>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900">
                    {activity.activity}
                  </p>
                  <p className="text-sm text-gray-500">
                    {activity.type} • {activity.time}
                  </p>
                </div>
                <div className="flex-shrink-0">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    activity.status === 'Publié' || activity.status === 'Actif'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {activity.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Actions rapides
          </h3>
          <div className="space-y-3">
            <button className="btn btn-primary w-full justify-start">
              <PencilIcon className="h-5 w-5 mr-2" />
              Nouvelle publication
            </button>
            <button className="btn btn-secondary w-full justify-start">
              <UsersIcon className="h-5 w-5 mr-2" />
              Créer une audience
            </button>
            <button className="btn btn-secondary w-full justify-start">
              <TrendingUpIcon className="h-5 w-5 mr-2" />
              Voir les statistiques
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard