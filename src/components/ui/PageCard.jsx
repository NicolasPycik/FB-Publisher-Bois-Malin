import React from 'react'
import { clsx } from 'clsx'
import { CheckIcon } from '@heroicons/react/24/solid'

const PageCard = ({ page, selected, onSelect, showStats = false }) => {
  return (
    <div
      className={clsx(
        'relative cursor-pointer rounded-lg border-2 p-4 transition-all duration-200 hover:shadow-md',
        selected
          ? 'border-primary-500 bg-primary-50'
          : 'border-gray-200 bg-white hover:border-gray-300'
      )}
      onClick={() => onSelect?.(page.id)}
    >
      {selected && (
        <div className="absolute -top-2 -right-2 h-6 w-6 rounded-full bg-primary-500 flex items-center justify-center">
          <CheckIcon className="h-4 w-4 text-white" />
        </div>
      )}
      
      <div className="flex items-start space-x-3">
        {page.picture && (
          <img
            src={page.picture}
            alt={page.name}
            className="h-12 w-12 rounded-lg object-cover"
          />
        )}
        
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-medium text-gray-900 truncate">
            {page.name}
          </h3>
          <p className="text-sm text-gray-500">{page.category}</p>
          
          {showStats && (
            <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
              <div>
                <span className="text-gray-500">Abonnés:</span>
                <span className="ml-1 font-medium">{page.fan_count?.toLocaleString() || 'N/A'}</span>
              </div>
              <div>
                <span className="text-gray-500">Posts:</span>
                <span className="ml-1 font-medium">{page.posts_count || 0}</span>
              </div>
            </div>
          )}
        </div>
      </div>
      
      <div className="mt-3 flex items-center justify-between">
        <span className={clsx(
          'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
          page.status === 'Connectée'
            ? 'bg-green-100 text-green-800'
            : 'bg-red-100 text-red-800'
        )}>
          {page.status}
        </span>
        
        {page.last_post && (
          <span className="text-xs text-gray-500">{page.last_post}</span>
        )}
      </div>
    </div>
  )
}

export default PageCard