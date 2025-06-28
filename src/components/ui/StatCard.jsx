import React from 'react'
import { clsx } from 'clsx'

const StatCard = ({ title, value, change, changeType, icon: Icon, className }) => {
  return (
    <div className={clsx('card', className)}>
      <div className="flex items-center">
        <div className="flex-shrink-0">
          {Icon && (
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100">
              <Icon className="h-6 w-6 text-primary-600" />
            </div>
          )}
        </div>
        <div className="ml-4 flex-1">
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">{value}</p>
          {change && (
            <p className={clsx(
              'text-sm',
              changeType === 'increase' ? 'text-green-600' : 'text-red-600'
            )}>
              {changeType === 'increase' ? '↗' : '↘'} {change}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

export default StatCard