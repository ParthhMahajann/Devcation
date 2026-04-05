import { useState } from 'react'
import DrugSearch from '../components/drugs/DrugSearch'
import InteractionAlert from '../components/drugs/InteractionAlert'
import LoadingSpinner from '../components/common/LoadingSpinner'
import { checkInteractions } from '../api/drugs'

export default function DrugInteractionsPage() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (drugs) => {
    setLoading(true)
    setError(null)
    try {
      const data = await checkInteractions(drugs)
      setResults(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Drug Interaction Checker</h1>
        <p className="text-slate-400">
          Select two or more drugs to check for known interactions using
          TigerGraph's N-hop network traversal.
        </p>
      </div>

      <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 mb-8">
        <DrugSearch onSubmit={handleSubmit} loading={loading} />
      </div>

      {loading && <LoadingSpinner message="Querying drug interaction network..." />}

      {error && (
        <div className="p-4 bg-red-900/20 border border-red-700 rounded-xl text-red-300 text-sm mb-6">
          Error: {error}
        </div>
      )}

      {results && !loading && results.interactions.length === 0 && (
        <div className="text-center py-8 text-slate-500">
          No known interactions found between the selected drugs.
        </div>
      )}

      {results && !loading && results.interactions.length > 0 && (
        <InteractionAlert interactions={results.interactions} />
      )}

      {!results && !loading && (
        <div className="text-center py-16 text-slate-600">
          <div className="text-6xl mb-4">💊</div>
          <p className="text-lg">Select at least 2 drugs above to check interactions</p>
          <p className="text-sm mt-2 text-slate-700">Powered by TigerGraph N-hop traversal</p>
        </div>
      )}
    </div>
  )
}
