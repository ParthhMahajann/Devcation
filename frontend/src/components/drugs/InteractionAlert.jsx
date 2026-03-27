import { severityBadge } from '../../utils/formatters'

export default function InteractionAlert({ interactions }) {
  if (!interactions || interactions.length === 0) {
    return (
      <div className="flex items-center gap-3 p-4 bg-green-900/20 border border-green-700 rounded-xl">
        <span className="text-2xl">✅</span>
        <div>
          <p className="font-semibold text-green-300">No known interactions</p>
          <p className="text-sm text-green-400/70">The selected drugs appear safe to combine.</p>
        </div>
      </div>
    )
  }

  const dangerous = interactions.filter(i => i.severity === 'dangerous')

  return (
    <div className="space-y-3">
      {dangerous.length > 0 && (
        <div className="flex items-center gap-3 p-4 bg-red-900/20 border border-red-700 rounded-xl mb-4">
          <span className="text-2xl">🚨</span>
          <div>
            <p className="font-semibold text-red-300">{dangerous.length} dangerous interaction{dangerous.length !== 1 ? 's' : ''} detected</p>
            <p className="text-sm text-red-400/70">Consult a healthcare professional before combining these medications.</p>
          </div>
        </div>
      )}
      {interactions.map((i, idx) => (
        <div key={idx} className="bg-slate-800 border border-slate-700 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <p className="font-medium text-white">
              <span className="text-sky-400">{i.from_drug}</span>
              <span className="text-slate-500 mx-2">↔</span>
              <span className="text-sky-400">{i.to_drug}</span>
            </p>
            <span className={`text-xs px-2 py-0.5 rounded border ${severityBadge(i.severity)}`}>
              {i.severity || 'unknown'}
            </span>
          </div>
          {i.interaction_type && (
            <p className="text-sm text-slate-400 mt-1">{i.interaction_type}</p>
          )}
        </div>
      ))}
    </div>
  )
}
