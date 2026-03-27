import SymptomInput from '../components/diagnosis/SymptomInput'
import DiagnosisResults from '../components/diagnosis/DiagnosisResults'
import LoadingSpinner from '../components/common/LoadingSpinner'
import { useDiagnosis } from '../hooks/useDiagnosis'

export default function DiagnosePage() {
  const { results, loading, error, runDiagnosis } = useDiagnosis()

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Symptom Checker</h1>
        <p className="text-slate-400">
          Select your symptoms to receive AI-powered differential diagnoses using
          TigerGraph's weighted multi-hop traversal.
        </p>
      </div>

      <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 mb-8">
        <SymptomInput onSubmit={runDiagnosis} loading={loading} />
      </div>

      {loading && <LoadingSpinner message="Running diagnosis query on TigerGraph..." />}

      {error && (
        <div className="p-4 bg-red-900/20 border border-red-700 rounded-xl text-red-300 text-sm mb-6">
          Error: {error}
        </div>
      )}

      {results && !loading && <DiagnosisResults results={results} />}

      {!results && !loading && (
        <div className="text-center py-16 text-slate-600">
          <div className="text-6xl mb-4">🔬</div>
          <p className="text-lg">Select symptoms above to begin diagnosis</p>
          <p className="text-sm mt-2 text-slate-700">
            Powered by TigerGraph multi-hop graph traversal
          </p>
        </div>
      )}
    </div>
  )
}
