import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { 
  PaperAirplaneIcon, 
  PhotoIcon, 
  LinkIcon,
  ClockIcon
} from '@heroicons/react/24/outline'
import PageCard from '../components/ui/PageCard'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { fetchPages, publishToPages } from '../services/api'

const Publish = () => {
  const [selectedPages, setSelectedPages] = useState([])
  const [mediaFiles, setMediaFiles] = useState([])
  const queryClient = useQueryClient()

  const { register, handleSubmit, watch, reset, formState: { errors } } = useForm()
  const message = watch('message', '')

  const { data: pages, isLoading: pagesLoading } = useQuery('pages', fetchPages)

  const publishMutation = useMutation(publishToPages, {
    onSuccess: (data) => {
      if (data.success) {
        toast.success(`Publication réussie sur ${data.summary?.successful || 0} page(s)`)
        reset()
        setSelectedPages([])
        setMediaFiles([])
      } else {
        toast.error('Erreur lors de la publication')
      }
    },
    onError: (error) => {
      toast.error('Erreur lors de la publication')
      console.error('Publish error:', error)
    },
  })

  const handlePageSelect = (pageId) => {
    setSelectedPages(prev => 
      prev.includes(pageId)
        ? prev.filter(id => id !== pageId)
        : [...prev, pageId]
    )
  }

  const handleSelectAll = () => {
    if (selectedPages.length === pages?.length) {
      setSelectedPages([])
    } else {
      setSelectedPages(pages?.map(page => page.id) || [])
    }
  }

  const handleMediaUpload = (event) => {
    const files = Array.from(event.target.files)
    setMediaFiles(prev => [...prev, ...files])
  }

  const removeMedia = (index) => {
    setMediaFiles(prev => prev.filter((_, i) => i !== index))
  }

  const onSubmit = (data) => {
    if (selectedPages.length === 0) {
      toast.error('Veuillez sélectionner au moins une page')
      return
    }

    if (!data.message.trim()) {
      toast.error('Veuillez saisir un message')
      return
    }

    const publishData = {
      page_ids: selectedPages,
      message: data.message,
      link: data.link || null,
      media_files: mediaFiles,
    }

    publishMutation.mutate(publishData)
  }

  if (pagesLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Publication Multi-Pages</h1>
          <p className="text-gray-600">Publiez simultanément sur vos pages Facebook</p>
        </div>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={() => window.location.href = '/pages'}
        >
          <ClockIcon className="h-5 w-5 mr-2" />
          Programmer
        </button>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Page Selection */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium text-gray-900">
              Sélection des Pages ({selectedPages.length}/{pages?.length || 0})
            </h3>
            <button
              type="button"
              onClick={handleSelectAll}
              className="btn btn-secondary btn-sm"
            >
              {selectedPages.length === pages?.length ? 'Désélectionner tout' : 'Sélectionner tout'}
            </button>
          </div>

          {pages && pages.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {pages.map((page) => (
                <PageCard
                  key={page.id}
                  page={page}
                  selected={selectedPages.includes(page.id)}
                  onSelect={handlePageSelect}
                  showStats
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500">Aucune page trouvée. Synchronisez vos pages dans les paramètres.</p>
            </div>
          )}
        </div>

        {/* Content */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Contenu de la Publication</h3>
          
          <div className="space-y-4">
            {/* Message */}
            <div>
              <label className="label">
                Message *
              </label>
              <textarea
                {...register('message', { required: 'Le message est obligatoire' })}
                rows={4}
                className="input"
                placeholder="Rédigez votre message..."
              />
              {errors.message && (
                <p className="mt-1 text-sm text-red-600">{errors.message.message}</p>
              )}
              <p className="mt-1 text-sm text-gray-500">
                {message.length} caractères
              </p>
            </div>

            {/* Link */}
            <div>
              <label className="label">
                Lien (optionnel)
              </label>
              <div className="relative">
                <LinkIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  {...register('link')}
                  type="url"
                  className="input pl-10"
                  placeholder="https://example.com"
                />
              </div>
            </div>

            {/* Media Upload */}
            <div>
              <label className="label">
                Médias (optionnel)
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
                <PhotoIcon className="mx-auto h-12 w-12 text-gray-400" />
                <div className="mt-4">
                  <label htmlFor="media-upload" className="cursor-pointer">
                    <span className="mt-2 block text-sm font-medium text-gray-900">
                      Cliquez pour ajouter des images ou vidéos
                    </span>
                    <input
                      id="media-upload"
                      type="file"
                      multiple
                      accept="image/*,video/*"
                      className="sr-only"
                      onChange={handleMediaUpload}
                    />
                  </label>
                  <p className="mt-1 text-xs text-gray-500">
                    PNG, JPG, GIF, MP4 jusqu'à 10MB
                  </p>
                </div>
              </div>

              {/* Media Preview */}
              {mediaFiles.length > 0 && (
                <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-4">
                  {mediaFiles.map((file, index) => (
                    <div key={index} className="relative">
                      <div className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
                        {file.type.startsWith('image/') ? (
                          <img
                            src={URL.createObjectURL(file)}
                            alt="Preview"
                            className="w-full h-full object-cover rounded-lg"
                          />
                        ) : (
                          <PhotoIcon className="h-8 w-8 text-gray-400" />
                        )}
                      </div>
                      <button
                        type="button"
                        onClick={() => removeMedia(index)}
                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs hover:bg-red-600"
                      >
                        ×
                      </button>
                      <p className="mt-1 text-xs text-gray-500 truncate">{file.name}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-500">
            {selectedPages.length > 0 && (
              <span>Publication sur {selectedPages.length} page(s) sélectionnée(s)</span>
            )}
          </div>
          
          <div className="flex space-x-3">
            <button
              type="button"
              onClick={() => {
                reset()
                setSelectedPages([])
                setMediaFiles([])
              }}
              className="btn btn-secondary"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={publishMutation.isLoading || selectedPages.length === 0}
              className="btn btn-primary"
            >
              {publishMutation.isLoading ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Publication...
                </>
              ) : (
                <>
                  <PaperAirplaneIcon className="h-5 w-5 mr-2" />
                  Publier maintenant
                </>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  )
}

export default Publish