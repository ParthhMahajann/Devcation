import { useState } from 'react'
import LoadingSpinner from '../components/common/LoadingSpinner'
import { getPatient, addPatient } from '../api/patients'
import { severityBadge } from '../utils/formatters'

export default function PatientPage() {
  const [tab, setTab] = useState('lookup')
  const [patientId, setPatientId] = useState('')
  const [patient, setPatient] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [form, setForm] = useState({ name: '', age: '', conditions: '', medications: '' })
  const [saved, setSaved] = useState(false)

  const handleLookup = async (e) => {
    e.preventDefault()
    if (!patientId.trim()) return
    setLoading(true)
    setError(null)
    setPatient(null)
    try {
      const data = await getPatient(patientId.trim())
      setPatient(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = async (e) => {
    e.preventDefault()
    const age = parseInt(form.age)
    if (isNaN(age) || age < 0 || age > 150) {
      setError('Age must be a number between 0 and 150')
      return
    }
    setLoading(true)
    setError(null)
    setSaved(false)
    try {
      await addPatient({
        name: form.name,
        age: parseInt(form.age),
        conditions: form.conditions.split(',').map(s => s.trim()).filter(Boolean),
        medications: form.medications.split(',').map(s => s.trim()).filter(Boolean),
      })
      setSaved(true)
      setForm({ name: '', age: '', conditions: '', medications: '' })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Patient Records</h1>
        <p className="text-slate-400">
          Look up existing patients or register a new patient in the knowledge graph.
        </p>
      </div>

      <div className="flex gap-2 mb-6">
        {['lookup', 'add'].map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              tab === t
                ? 'bg-sky-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-white border border-slate-700'
            }`}
          >
            {t === 'lookup' ? 'Look Up Patient' : 'Add Patient'}
          </button>
        ))}
      </div>

      {tab === 'lookup' && (
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6">
          <form onSubmit={handleLookup} className="flex gap-3 mb-6">
            <input
              type="text"
              value={patientId}
              onChange={e => setPatientId(e.target.value)}
              placeholder="Enter Patient ID (e.g. P001)"
              className="flex-1 bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
            />
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 text-white font-medium rounded-lg transition-colors"
            >
              {loading ? '...' : 'Search'}
            </button>
          </form>

          {error && (
            <div className="p-3 bg-red-900/20 border border-red-700 rounded-lg text-red-300 text-sm mb-4">
              {error}
            </div>
          )}

          {patient && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-bold text-white">{patient.name}</h2>
                  <p className="text-slate-400 text-sm">ID: {patient.patient_id} · Age: {patient.age}</p>
                </div>
              </div>

              {patient.conditions?.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium text-slate-400 mb-2">Conditions</h3>
                  <div className="flex flex-wrap gap-2">
                    {patient.conditions.map(c => (
                      <span key={c} className={`text-xs px-2 py-1 rounded border ${severityBadge(c.severity)}`}>
                        {c.name || c}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {patient.medications?.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium text-slate-400 mb-2">Medications</h3>
                  <div className="flex flex-wrap gap-2">
                    {patient.medications.map(m => (
                      <span key={m} className="text-xs px-2 py-1 rounded border border-sky-700 bg-sky-900/20 text-sky-300">
                        {m.name || m}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {patient.drug_interactions?.length > 0 && (
                <div className="p-3 bg-red-900/20 border border-red-700 rounded-lg">
                  <h3 className="text-sm font-semibold text-red-300 mb-1">
                    ⚠️ {patient.drug_interactions.length} drug interaction{patient.drug_interactions.length !== 1 ? 's' : ''} detected
                  </h3>
                  {patient.drug_interactions.map((i) => (
                    <p key={`${i.from_drug}-${i.to_drug}`} className="text-xs text-red-400">
                      {i.from_drug} ↔ {i.to_drug}: {i.interaction_type}
                    </p>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {tab === 'add' && (
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6">
          <form onSubmit={handleAdd} className="space-y-4">
            {[
              { key: 'name', label: 'Patient Name', placeholder: 'John Doe' },
              { key: 'age', label: 'Age', placeholder: '45', type: 'number' },
              { key: 'conditions', label: 'Conditions (comma-separated)', placeholder: 'Diabetes, Hypertension' },
              { key: 'medications', label: 'Medications (comma-separated)', placeholder: 'Metformin, Lisinopril' },
            ].map(({ key, label, placeholder, type = 'text' }) => (
              <div key={key}>
                <label className="block text-sm font-medium text-slate-300 mb-1">{label}</label>
                <input
                  type={type}
                  value={form[key]}
                  onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))}
                  placeholder={placeholder}
                  className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                />
              </div>
            ))}

            {error && (
              <div className="p-3 bg-red-900/20 border border-red-700 rounded-lg text-red-300 text-sm">
                {error}
              </div>
            )}
            {saved && (
              <div className="p-3 bg-green-900/20 border border-green-700 rounded-lg text-green-300 text-sm">
                Patient added to the knowledge graph successfully.
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !form.name || !form.age}
              className="w-full py-3 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 disabled:text-slate-500 text-white font-semibold rounded-lg transition-colors"
            >
              {loading ? 'Saving...' : 'Add Patient'}
            </button>
          </form>
        </div>
      )}
    </div>
  )
}
