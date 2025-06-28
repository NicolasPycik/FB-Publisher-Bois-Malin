import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  HomeIcon, 
  PencilIcon, 
  DocumentTextIcon,
  ChartBarIcon,
  MegaphoneIcon,
  UsersIcon,
  CogIcon,
  FacebookIcon
} from '@heroicons/react/24/outline'
import { clsx } from 'clsx'

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Publier', href: '/publish', icon: PencilIcon },
  { name: 'Pages Facebook', href: '/pages', icon: DocumentTextIcon },
  { name: 'Statistiques', href: '/analytics', icon: ChartBarIcon },
  { name: 'Publicités', href: '/campaigns', icon: MegaphoneIcon },
  { name: 'Audiences', href: '/audiences', icon: UsersIcon },
  { name: 'Paramètres', href: '/settings', icon: CogIcon },
]

const Sidebar = () => {
  const location = useLocation()

  return (
    <div className="flex flex-col flex-grow bg-white border-r border-gray-200">
      {/* Logo */}
      <div className="flex items-center flex-shrink-0 px-6 py-4 border-b border-gray-200">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-facebook-500 rounded-lg flex items-center justify-center">
              <FacebookIcon className="w-5 h-5 text-white" />
            </div>
          </div>
          <div className="ml-3">
            <h1 className="text-lg font-semibold text-gray-900">FB Publisher</h1>
            <p className="text-xs text-gray-500">Bois Malin v4.0</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-4 space-y-1">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href
          return (
            <Link
              key={item.name}
              to={item.href}
              className={clsx(
                'sidebar-link',
                isActive ? 'sidebar-link-active' : 'sidebar-link-inactive'
              )}
            >
              <item.icon className="w-5 h-5 mr-3" />
              {item.name}
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="flex-shrink-0 px-4 py-4 border-t border-gray-200">
        <div className="text-xs text-gray-500">
          <p>© 2025 Bois Malin</p>
          <p>Version 4.0.0</p>
        </div>
      </div>
    </div>
  )
}

export default Sidebar