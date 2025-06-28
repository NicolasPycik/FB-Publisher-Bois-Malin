import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import toast from 'react-hot-toast'
import { 
  ArrowPathIcon, 
  MagnifyingGlassIcon,
  ChartBarIcon,
  EyeIcon
} from '@heroicons/react/24/outline'
import PageCard from '../components/ui/PageCard'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { fetchPages, syncPages } from '../services/api'

const Pages = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const queryClient = useQueryClient()

  const { data: pages, isLoading, error } = useQuery('pages', fetchPages)

  const syncMutation = useMutation(syncPages, {
    onSuccess: (data) => {
      if (data.success) {
        toast.success(data.message)
        queryClient.invalidateQueries('pages')
      } else {
        toast.error(data.error || 'Erreur lors de la synchronisation')
      }
    },
    onError: (error) => {
      toast.error('Erreur lors de la synchronisation')
      console.error('Sync error:', error)
    },
  })

  const filteredPages = pages?.filter(page => {
    const matchesSearch = page.name.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = filterStatus === 'all' || page.status === filterStatus
    return matchesSearch && matchesStatus
  }) || []

  const handleSync = () => {
    syncMutation.mutate()
  }

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
        <p className="text-red-600">Erreur lors du chargement des pages</p>
        <button onClick={handleSync} className="btn btn-primary mt-4">
          Réessayer
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Pages Facebook</h1>
          <p className="text-gray-600">
            {pages?.length || 0} page(s) synchronisée(s)
          </p>
        </div>
        <button
          onClick={handleSync}
          disabled={syncMutation.isLoading}
          className="btn btn-primary mt-4 sm:mt-0"
        >
          {syncMutation.isLoading ? (
            <>
              <LoadingSpinner size="sm" className="mr-2" />
              Synchronisation...
            </>
          ) : (
            <>
              <ArrowPathIcon className="h-5 w-5 mr-2" />
              Synchroniser
            </>
          )}
        </button>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
          {/* Search */}
          <div className="relative flex-1 max-w-md">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Rechercher une page..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input pl-10"
            />
          </div>

          {/* Status Filter */}
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="input w-auto"
          >
            <option value="all">Tous les statuts</option>
            <option value="Connectée">Connectée</option>
            <option value="Déconnectée">Déconnectée</option>
          </select>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="text-2xl font-bold text-primary-600">
            {pages?.length || 0}
          </div>
          <div className="text-sm text-gray-500">Pages totales</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-green-600">
            {pages?.filter(p => p.status === 'Connectée').length || 0}
          </div>
          <div className="text-sm text-gray-500">Pages connectées</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-blue-600">
            {pages?.reduce((sum, p) => sum + (p.fan_count || 0), 0).toLocaleString() || 0}
          </div>
          <div className="text-sm text-gray-500">Abonnés totaux</div>
        </div>
      </div>

      {/* Pages Grid */}
      {filteredPages.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPages.map((page) => (
            <div key={page.id} className="relative">
              <PageCard page={page} showStats />
              
              {/* Action buttons */}
              <div className="absolute top-4 right-4 flex space-x-2">
                <button
                  className="p-2 bg-white rounded-lg shadow-sm border border-gray-200 hover:bg-gray-50"
                  title="Voir les statistiques"
                >
                  <ChartBarIcon className="h-4 w-4 text-gray-600" />
                </button>
                <button
                  className="p-2 bg-white rounded-lg shadow-sm border border-gray-200 hover:bg-gray-50"
                  title="Voir la page"
                >
                  <EyeIcon className="h-4 w-4 text-gray-600" />
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <div className="text-gray-500">
            {searchTerm || filterStatus !== 'all' 
              ? 'Aucune page ne correspond aux critères de recherche'
              : 'Aucune page trouvée. Cliquez sur "Synchroniser" pour récupérer vos pages Facebook.'
            }
          </div>
        </div>
      )}
    </div>
  )
}

export default Pages