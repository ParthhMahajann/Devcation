export function formatScore(score) {
  return (score || 0).toFixed(2)
}

export function severityColor(severity) {
  const map = {
    critical: 'text-red-500',
    severe:   'text-orange-500',
    moderate: 'text-yellow-500',
    mild:     'text-green-500',
  }
  return map[severity?.toLowerCase()] || 'text-slate-400'
}

export function severityBadge(severity) {
  const map = {
    critical: 'bg-red-900/50 text-red-300 border-red-700',
    severe:   'bg-orange-900/50 text-orange-300 border-orange-700',
    moderate: 'bg-yellow-900/50 text-yellow-300 border-yellow-700',
    mild:     'bg-green-900/50 text-green-300 border-green-700',
    dangerous:'bg-red-900/50 text-red-300 border-red-700',
  }
  return map[severity?.toLowerCase()] || 'bg-slate-700 text-slate-300 border-slate-600'
}

export function formatNumber(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'K'
  return n?.toString() || '0'
}
