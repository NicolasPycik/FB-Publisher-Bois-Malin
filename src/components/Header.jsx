import React from 'react'
import { Bars3Icon, BellIcon } from '@heroicons/react/24/outline'
import { useLocation } from 'react-router-dom'

const pageNames = {
  '/': 'Dashboard',
  '/publish': 'Publication',
  '/pages': 'Pages Facebook',
  '/analytics': 'Statistiques',
  '/campaigns': 'Publicités',
  '/audiences': 'Audiences',
  '/settings': 'Paramètres',
}

const Header = ({ onMenuClick }) => {
  const location = useLocation()
  const pageName = pageNames[location.pathname] || 'Facebook Publisher'

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="flex items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center">
          <button
            type="button"
            className="lg:hidden -ml-0.5 -mt-0.5 h-12 w-12 inline-flex items-center justify-center rounded-md text-gray-500 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
            onClick={onMenuClick}
          >
            <span className="sr-only">Ouvrir le menu</span>
            <Bars3Icon className="h-6 w-6" />
          </button>
          
          <div className="lg:ml-0 ml-4">
            <h1 className="text-2xl font-semibold text-gray-900">{pageName}</h1>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {/* Notifications */}
          <button
            type="button"
            className="relative p-2 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded-lg"
          >
            <span className="sr-only">Voir les notifications</span>
            <BellIcon className="h-6 w-6" />
            <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400 ring-2 ring-white" />
          </button>

          {/* Connection status */}
          <div className="flex items-center space-x-2">
            <div className="h-2 w-2 bg-green-400 rounded-full"></div>
            <span className="text-sm text-gray-500">Connecté</span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header