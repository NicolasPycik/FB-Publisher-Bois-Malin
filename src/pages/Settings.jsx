import React, { useState } from 'react'
import { useQuery, useMutation } from 'react-query'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { 
  CogIcon, 
  KeyIcon, 
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { fetchSettings, saveSettings, testConnection } from '../services/api'

const Settings = () => {
  const [activeTab, setActiveTab] = useState('facebook')
  const [connectionStatus, setConnectionStatus] = useState(null)
  
  const { register, handleSubmit, setValue, formState: { errors } } = useForm()
  
  const { data: settings, isLoading } = useQuery('settings', fetchSettings, {
    onSuccess: (data) => {
      setValue('app_id', data.app_id || '')
      setValue('email_notifications', data.email_notifications || false)
      setValue('auto_reports', data.auto_reports || false)
      setValue('timezone', data.timezone || 'Europe/Paris')
    }
  })

  const saveMutation = useMutation(saveSettings, {
    onSuccess: () => {
      toast.success('Paramètres sauvegardés avec succès')
    },
    onError: () => {
      toast.error('Erreur lors de la sauvegarde')
    }
  })

  const testMutation = useMutation(testConnection, {
    onSuccess: (data) => {
      if (data.success) {
        setConnectionStatus({
          type: 'success',
          message: data.message,
          pages_count: data.pages_count
        })
        toast.success('Connexion réussie !')
      } else {
        setConnectionStatus({
          type: 'error',
          message: data.error
        })
        toast.error('Erreur de connexion')
      }
    },
    onError: () => {
      setConnectionStatus({
        type: 'error',
        message: 'Erreur de connexion au serveur'
      })
      toast.error('Erreur de connexion')
    }
  })

  const onSubmit = (data) => {
    saveMutation.mutate(data)
  }

  const handleTestConnection = () => {
    setConnectionStatus(null)
    testMutation.mutate()
  }

  const tabs = [
    { id: 'facebook', name: 'Facebook API', icon: KeyIcon },
    { id: 'preferences', name: 'Préférences', icon: CogIcon },
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
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Paramètres</h1>
        <p className="text-gray-600">Configuration de l'application et des comptes Facebook</p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <tab.icon className="h-5 w-5 mr-2" />
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Facebook API Tab */}
        {activeTab === 'facebook' && (
          <div className="space-y-6">
            <div className="card">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Configuration Facebook API
              </h3>
              
              <div className="space-y-4">
                <div>
                  <label className="label">App ID Facebook *</label>
                  <input
                    {...register('app_id', { required: 'App ID requis' })}
                    type="text"
                    className="input"
                    placeholder="Votre Facebook App ID"
                  />
                  {errors.app_id && (
                    <p className="mt-1 text-sm text-red-600">{errors.app_id.message}</p>
                  )}
                </div>
                
                <div>
                  <label className="label">App Secret Facebook *</label>
                  <input
                    {...register('app_secret', { required: 'App Secret requis' })}
                    type="password"
                    className="input"
                    placeholder="Votre Facebook App Secret"
                  />
                  {errors.app_secret && (
                    <p className="mt-1 text-sm text-red-600">{errors.app_secret.message}</p>
                  )}
                </div>
                
                <div>
                  <label className="label">Access Token *</label>
                  <textarea
                    {...register('access_token', { required: 'Access Token requis' })}
                    rows={3}
                    className="input"
                    placeholder="Votre token d'accès Facebook"
                  />
                  {errors.access_token && (
                    <p className="mt-1 text-sm text-red-600">{errors.access_token.message}</p>
                  )}
                  <p className="mt-1 text-sm text-gray-500">
                    Générez votre token sur{' '}
                    <a
                      href="https://developers.facebook.com/tools/explorer/"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary-600 hover:text-primary-500"
                    >
                      Facebook Graph API Explorer
                    </a>
                  </p>
                </div>
              </div>
            </div>

            {/* Connection Status */}
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-gray-900">
                  Statut de la Connexion
                </h3>
                <button
                  type="button"
                  onClick={handleTestConnection}
                  disabled={testMutation.isLoading}
                  className="btn btn-secondary"
                >
                  {testMutation.isLoading ? (
                    <>
                      <LoadingSpinner size="sm" className="mr-2" />
                      Test...
                    </>
                  ) : (
                    <>
                      <ArrowPathIcon className="h-5 w-5 mr-2" />
                      Tester la connexion
                    </>
                  )}
                </button>
              </div>
              
              {connectionStatus && (
                <div className={`flex items-center p-4 rounded-lg ${
                  connectionStatus.type === 'success'
                    ? 'bg-green-50 text-green-800'
                    : 'bg-red-50 text-red-800'
                }`}>
                  {connectionStatus.type === 'success' ? (
                    <CheckCircleIcon className="h-5 w-5 mr-2" />
                  ) : (
                    <ExclamationTriangleIcon className="h-5 w-5 mr-2" />
                  )}
                  <div>
                    <p className="font-medium">
                      {connectionStatus.type === 'success' ? 'Connexion réussie' : 'Erreur de connexion'}
                    </p>
                    <p className="text-sm">{connectionStatus.message}</p>
                    {connectionStatus.pages_count && (
                      <p className="text-sm">
                        {connectionStatus.pages_count} page(s) synchronisée(s)
                      </p>
                    )}
                  </div>
                </div>
              )}
              
              {!connectionStatus && (
                <div className="text-center py-8 text-gray-500">
                  <KeyIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                  <p>Cliquez sur "Tester la connexion" pour vérifier vos paramètres</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Preferences Tab */}
        {activeTab === 'preferences' && (
          <div className="space-y-6">
            <div className="card">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Notifications
              </h3>
              
              <div className="space-y-4">
                <div className="flex items-center">
                  <input
                    {...register('email_notifications')}
                    type="checkbox"
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label className="ml-3 text-sm text-gray-700">
                    Recevoir les notifications par email
                  </label>
                </div>
                
                <div className="flex items-center">
                  <input
                    {...register('auto_reports')}
                    type="checkbox"
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label className="ml-3 text-sm text-gray-700">
                    Rapports automatiques hebdomadaires
                  </label>
                </div>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Localisation
              </h3>
              
              <div>
                <label className="label">Fuseau horaire</label>
                <select {...register('timezone')} className="input">
                  <option value="Europe/Paris">Europe/Paris (GMT+1)</option>
                  <option value="Europe/London">Europe/London (GMT+0)</option>
                  <option value="America/New_York">America/New_York (GMT-5)</option>
                  <option value="America/Los_Angeles">America/Los_Angeles (GMT-8)</option>
                </select>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Informations Système
              </h3>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Version:</span>
                  <span className="ml-2 font-medium">Facebook Publisher SaaS v4.0</span>
                </div>
                <div>
                  <span className="text-gray-500">API Facebook:</span>
                  <span className="ml-2 font-medium">Graph API v18.0</span>
                </div>
                <div>
                  <span className="text-gray-500">Dernière mise à jour:</span>
                  <span className="ml-2 font-medium">25 juin 2025</span>
                </div>
                <div>
                  <span className="text-gray-500">Statut:</span>
                  <span className="ml-2 font-medium text-green-600">Opérationnel</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={saveMutation.isLoading}
            className="btn btn-primary"
          >
            {saveMutation.isLoading ? (
              <>
                <LoadingSpinner size="sm" className="mr-2" />
                Sauvegarde...
              </>
            ) : (
              'Sauvegarder les paramètres'
            )}
          </button>
        </div>
      </form>
    </div>
  )
}

export default Settings