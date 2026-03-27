import { formatNumber } from '../../utils/formatters'

export default function StatsCard({ label, value, icon, color = 'sky' }) {
  const colorMap = {
    sky:    'border-sky-700 bg-sky-900/20 text-sky-400',
    red:    'border-red-700 bg-red-900/20 text-red-400',
    amber:  'border-amber-700 bg-amber-900/20 text-amber-400',
    purple: 'border-purple-700 bg-purple-900/20 text-purple-400',
    green:  'border-green-700 bg-green-900/20 text-green-400',
    pink:   'border-pink-700 bg-pink-900/20 text-pink-400',
  }
  return (
    <div className={`rounded-xl border p-5 ${colorMap[color]}`}>
      <div className="flex items-center gap-3 mb-2">
        <span className="text-2xl">{icon}</span>
        <span className="text-sm text-slate-400 uppercase tracking-wider">{label}</span>
      </div>
      <p className="text-3xl font-bold text-white">{formatNumber(value)}</p>
    </div>
  )
}
