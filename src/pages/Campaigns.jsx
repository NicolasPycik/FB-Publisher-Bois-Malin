import React, { useState } from 'react'
import { useQuery } from 'react-query'
import { 
  PlusIcon, 
  PlayIcon, 
  PauseIcon,
  TrashIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { fetchCampaigns } from '../services/api'

const Campaigns = () => {
  const [showCreateModal, setShowCreateModal] = useState(false)
  
  const { data: campaigns, isLoading } = useQuery('campaigns', fetchCampaigns)

  const sampleCampaigns = [
    {
      id: 'campaign_1',
      name: 'Promotion Terrasses Été 2025',
      objective: 'REACH',
      status: 'ACTIVE',
      budget: 500,
      spent: 245.50,
      reach: 12500,
      impressions: 18750,
      clicks: 234,
      created_time: '2025-06-15T10:00:00+0000',
    },
    {
      id: 'campaign_2',
      name: 'Lancement Clôtures Composite',
      objective: 'TRAFFIC',
      status: 'PAUSED',
      budget: 300,
      spent: 89.25,
      reach: 8900,
      impressions: 13400,
      clicks: 156,
      created_time: '2025-06-20T14:30:00+0000',
    }
  ]

  const campaignData = campaigns || sampleCampaigns

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
          <h1 className="text-2xl font-bold text-gray-900">Publicités</h1>
          <p className="text-gray-600">Gérez vos campagnes publicitaires Facebook</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="btn btn-primary mt-4 sm:mt-0"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          Nouvelle campagne
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-6">
        <div className="card text-center">
          <div className="text-2xl font-bold text-primary-600">
            {campaignData.length}
          </div>
          <div className="text-sm text-gray-500">Campagnes actives</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-green-600">
            {campaignData.reduce((sum, c) => sum + c.spent, 0).toFixed(2)}€
          </div>
          <div className="text-sm text-gray-500">Dépensé ce mois</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-blue-600">
            {campaignData.reduce((sum, c) => sum + c.reach, 0).toLocaleString()}
          </div>
          <div className="text-sm text-gray-500">Portée totale</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-purple-600">
            {campaignData.reduce((sum, c) => sum + c.clicks, 0)}
          </div>
          <div className="text-sm text-gray-500">Clics totaux</div>
        </div>
      </div>

      {/* Campaigns List */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Campagnes en cours
        </h3>
        
        {campaignData.length > 0 ? (
          <div className="space-y-4">
            {campaignData.map((campaign) => (
              <div key={campaign.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <h4 className="text-lg font-medium text-gray-900">
                        {campaign.name}
                      </h4>
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        campaign.status === 'ACTIVE'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {campaign.status === 'ACTIVE' ? 'Actif' : 'En pause'}
                      </span>
                    </div>
                    
                    <div className="mt-2 grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500">Objectif:</span>
                        <span className="ml-1 font-medium">{campaign.objective}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Budget:</span>
                        <span className="ml-1 font-medium">{campaign.budget}€</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Dépensé:</span>
                        <span className="ml-1 font-medium">{campaign.spent}€</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Portée:</span>
                        <span className="ml-1 font-medium">{campaign.reach.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <button
                      className="p-2 text-gray-400 hover:text-gray-600"
                      title="Voir les statistiques"
                    >
                      <ChartBarIcon className="h-5 w-5" />
                    </button>
                    <button
                      className="p-2 text-gray-400 hover:text-green-600"
                      title={campaign.status === 'ACTIVE' ? 'Mettre en pause' : 'Activer'}
                    >
                      {campaign.status === 'ACTIVE' ? (
                        <PauseIcon className="h-5 w-5" />
                      ) : (
                        <PlayIcon className="h-5 w-5" />
                      )}
                    </button>
                    <button
                      className="p-2 text-gray-400 hover:text-red-600"
                      title="Supprimer"
                    >
                      <TrashIcon className="h-5 w-5" />
                    </button>
                  </div>
                </div>
                
                {/* Progress bar */}
                <div className="mt-4">
                  <div className="flex justify-between text-sm text-gray-600 mb-1">
                    <span>Progression du budget</span>
                    <span>{((campaign.spent / campaign.budget) * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full"
                      style={{ width: `${Math.min((campaign.spent / campaign.budget) * 100, 100)}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-500">Aucune campagne trouvée</p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="btn btn-primary mt-4"
            >
              Créer votre première campagne
            </button>
          </div>
        )}
      </div>

      {/* Create Campaign Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Nouvelle campagne
              </h3>
              <p className="text-sm text-gray-500 mb-4">
                Fonctionnalité en cours de développement. Utilisez l'assistant de création pour créer vos campagnes.
              </p>
              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="btn btn-secondary"
                >
                  Fermer
                </button>
                <button className="btn btn-primary">
                  Assistant de création
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Campaigns