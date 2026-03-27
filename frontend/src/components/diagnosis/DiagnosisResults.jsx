import ConfidenceBar from './ConfidenceBar'
import { severityBadge } from '../../utils/formatters'

export default function DiagnosisResults({ results }) {
  if (!results || results.diseases.length === 0) {
    return (
      <div className="text-center py-10 text-slate-500">
        No matching diseases found for the selected symptoms.
      </div>
    )
  }

  const maxScore = results.diseases[0]?.score || 1

  return (
    <div className="space-y-3">
      <p className="text-sm text-slate-400">
        Found <span className="text-white font-medium">{results.total}</span> possible conditions
      </p>
      {results.diseases.map((d, i) => (
        <div
          key={d.disease_id}
          className="bg-slate-800 border border-slate-700 rounded-xl p-4 hover:border-slate-600 transition-colors"
        >
          <div className="flex items-start justify-between gap-3 mb-2">
            <div className="flex items-center gap-2">
              <span className="text-slate-500 text-sm font-mono w-5">#{i + 1}</span>
              <h3 className="font-semibold text-white">{d.name}</h3>
              {d.icd_code && (
                <span className="text-xs text-slate-500 font-mono">{d.icd_code}</span>
              )}
            </div>
            <div className="flex items-center gap-2 shrink-0">
              {d.severity && (
                <span className={`text-xs px-2 py-0.5 rounded border ${severityBadge(d.severity)}`}>
                  {d.severity}
                </span>
              )}
              {d.category && (
                <span className="text-xs px-2 py-0.5 rounded border border-slate-600 text-slate-400">
                  {d.category}
                </span>
              )}
            </div>
          </div>
          <div className="flex items-center gap-3 mb-2">
            <ConfidenceBar score={d.score} maxScore={maxScore} />
            <span className="text-xs text-sky-400 whitespace-nowrap font-mono">
              {d.score.toFixed(2)}
            </span>
          </div>
          <p className="text-sm text-slate-400 leading-relaxed">
            {d.description || 'No description available.'}
          </p>
          <p className="text-xs text-slate-600 mt-1">
            Matched {d.match_count} symptom{d.match_count !== 1 ? 's' : ''}
          </p>
        </div>
      ))}
    </div>
  )
}
