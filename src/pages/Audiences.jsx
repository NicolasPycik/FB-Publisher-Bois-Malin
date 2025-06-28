import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import toast from 'react-hot-toast'
import { 
  PlusIcon, 
  UsersIcon, 
  PencilIcon,
  TrashIcon,
  DocumentDuplicateIcon
} from '@heroicons/react/24/outline'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { fetchAudiences, createAudience, deleteAudience } from '../services/api'

const Audiences = () => {
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newAudience, setNewAudience] = useState({
    name: '',
    description: '',
    type: 'custom',
    targeting: {
      location: 'FR',
      age_min: 25,
      age_max: 55,
      gender: 'all',
      interests: []
    }
  })
  
  const queryClient = useQueryClient()
  
  const { data: audiences, isLoading } = useQuery('audiences', fetchAudiences)

  const createMutation = useMutation(createAudience, {
    onSuccess: () => {
      toast.success('Audience créée avec succès')
      queryClient.invalidateQueries('audiences')
      setShowCreateModal(false)
      setNewAudience({
        name: '',
        description: '',
        type: 'custom',
        targeting: {
          location: 'FR',
          age_min: 25,
          age_max: 55,
          gender: 'all',
          interests: []
        }
      })
    },
    onError: () => {
      toast.error('Erreur lors de la création de l\'audience')
    }
  })

  const deleteMutation = useMutation(deleteAudience, {
    onSuccess: () => {
      toast.success('Audience supprimée avec succès')
      queryClient.invalidateQueries('audiences')
    },
    onError: () => {
      toast.error('Erreur lors de la suppression')
    }
  })

  const sampleAudiences = [
    {
      id: 'audience_1',
      name: 'Propriétaires 25-55 ans',
      description: 'Propriétaires de maison intéressés par l\'aménagement extérieur',
      type: 'custom',
      size: 45000,
      created_date: '2025-06-20T10:00:00Z'
    },
    {
      id: 'audience_2',
      name: 'Bricoleurs passionnés',
      description: 'Personnes très actives dans le bricolage et la rénovation',
      type: 'custom',
      size: 32000,
      created_date: '2025-06-21T15:20:00Z'
    },
    {
      id: 'audience_3',
      name: 'Audience similaire clients',
      description: 'Audience similaire basée sur les meilleurs clients',
      type: 'lookalike',
      size: 28000,
      created_date: '2025-06-22T11:45:00Z'
    }
  ]

  const audienceData = audiences || sampleAudiences

  const handleCreateAudience = (e) => {
    e.preventDefault()
    if (!newAudience.name || !newAudience.description) {
      toast.error('Veuillez remplir tous les champs obligatoires')
      return
    }
    createMutation.mutate(newAudience)
  }

  const handleDeleteAudience = (audienceId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette audience ?')) {
      deleteMutation.mutate(audienceId)
    }
  }

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
          <h1 className="text-2xl font-bold text-gray-900">Audiences</h1>
          <p className="text-gray-600">Gérez vos audiences personnalisées pour le ciblage publicitaire</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="btn btn-primary mt-4 sm:mt-0"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          Nouvelle audience
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="text-2xl font-bold text-primary-600">
            {audienceData.length}
          </div>
          <div className="text-sm text-gray-500">Audiences créées</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-green-600">
            {audienceData.reduce((sum, a) => sum + a.size, 0).toLocaleString()}
          </div>
          <div className="text-sm text-gray-500">Portée totale</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-blue-600">
            {audienceData.filter(a => a.type === 'custom').length}
          </div>
          <div className="text-sm text-gray-500">Audiences personnalisées</div>
        </div>
      </div>

      {/* Audiences List */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {audienceData.map((audience) => (
          <div key={audience.id} className="card">
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                    <UsersIcon className="w-5 h-5 text-primary-600" />
                  </div>
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-lg font-medium text-gray-900">
                    {audience.name}
                  </h3>
                  <p className="text-sm text-gray-500 mt-1">
                    {audience.description}
                  </p>
                  
                  <div className="mt-3 flex items-center space-x-4 text-sm">
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                      audience.type === 'custom'
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-purple-100 text-purple-800'
                    }`}>
                      {audience.type === 'custom' ? 'Personnalisée' : 'Similaire'}
                    </span>
                    <span className="text-gray-600">
                      {audience.size.toLocaleString()} personnes
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <button
                  className="p-2 text-gray-400 hover:text-gray-600"
                  title="Modifier"
                >
                  <PencilIcon className="h-4 w-4" />
                </button>
                <button
                  className="p-2 text-gray-400 hover:text-blue-600"
                  title="Dupliquer"
                >
                  <DocumentDuplicateIcon className="h-4 w-4" />
                </button>
                <button
                  onClick={() => handleDeleteAudience(audience.id)}
                  className="p-2 text-gray-400 hover:text-red-600"
                  title="Supprimer"
                >
                  <TrashIcon className="h-4 w-4" />
                </button>
              </div>
            </div>
            
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">
                  Créée le {new Date(audience.created_date).toLocaleDateString('fr-FR')}
                </span>
                <button className="btn btn-secondary btn-sm">
                  Utiliser dans une campagne
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {audienceData.length === 0 && (
        <div className="text-center py-12">
          <UsersIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">Aucune audience</h3>
          <p className="mt-1 text-sm text-gray-500">
            Commencez par créer votre première audience personnalisée.
          </p>
          <div className="mt-6">
            <button
              onClick={() => setShowCreateModal(true)}
              className="btn btn-primary"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              Créer une audience
            </button>
          </div>
        </div>
      )}

      {/* Create Audience Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-full max-w-md shadow-lg rounded-md bg-white">
            <form onSubmit={handleCreateAudience}>
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Nouvelle audience
              </h3>
              
              <div className="space-y-4">
                <div>
                  <label className="label">Nom de l'audience *</label>
                  <input
                    type="text"
                    value={newAudience.name}
                    onChange={(e) => setNewAudience({...newAudience, name: e.target.value})}
                    className="input"
                    placeholder="Ex: Propriétaires 25-55 ans"
                    required
                  />
                </div>
                
                <div>
                  <label className="label">Description *</label>
                  <textarea
                    value={newAudience.description}
                    onChange={(e) => setNewAudience({...newAudience, description: e.target.value})}
                    className="input"
                    rows={3}
                    placeholder="Décrivez votre audience cible..."
                    required
                  />
                </div>
                
                <div>
                  <label className="label">Type d'audience</label>
                  <select
                    value={newAudience.type}
                    onChange={(e) => setNewAudience({...newAudience, type: e.target.value})}
                    className="input"
                  >
                    <option value="custom">Personnalisée</option>
                    <option value="lookalike">Similaire</option>
                  </select>
                </div>
                
                {newAudience.type === 'custom' && (
                  <>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="label">Âge minimum</label>
                        <input
                          type="number"
                          value={newAudience.targeting.age_min}
                          onChange={(e) => setNewAudience({
                            ...newAudience,
                            targeting: {...newAudience.targeting, age_min: parseInt(e.target.value)}
                          })}
                          className="input"
                          min="18"
                          max="65"
                        />
                      </div>
                      <div>
                        <label className="label">Âge maximum</label>
                        <input
                          type="number"
                          value={newAudience.targeting.age_max}
                          onChange={(e) => setNewAudience({
                            ...newAudience,
                            targeting: {...newAudience.targeting, age_max: parseInt(e.target.value)}
                          })}
                          className="input"
                          min="18"
                          max="65"
                        />
                      </div>
                    </div>
                    
                    <div>
                      <label className="label">Localisation</label>
                      <select
                        value={newAudience.targeting.location}
                        onChange={(e) => setNewAudience({
                          ...newAudience,
                          targeting: {...newAudience.targeting, location: e.target.value}
                        })}
                        className="input"
                      >
                        <option value="FR">France</option>
                        <option value="BE">Belgique</option>
                        <option value="CH">Suisse</option>
                        <option value="CA">Canada</option>
                      </select>
                    </div>
                  </>
                )}
              </div>
              
              <div className="flex justify-end space-x-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="btn btn-secondary"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  disabled={createMutation.isLoading}
                  className="btn btn-primary"
                >
                  {createMutation.isLoading ? (
                    <>
                      <LoadingSpinner size="sm" className="mr-2" />
                      Création...
                    </>
                  ) : (
                    'Créer l\'audience'
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Audiences