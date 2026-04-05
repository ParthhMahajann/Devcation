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
  const [form, setForm] = useState({
    patient_id: '', name: '', age: '', gender: '', blood_type: '',
    conditions: '', medications: '',
  })
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
        patient_id: form.patient_id.trim(),
        name: form.name.trim(),
        age,
        gender: form.gender,
        blood_type: form.blood_type.trim(),
      })
      setSaved(true)
      setForm({ patient_id: '', name: '', age: '', gender: '', blood_type: '', conditions: '', medications: '' })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const setField = (key) => (e) => setForm(f => ({ ...f, [key]: e.target.value }))

  const inputClass = "w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500"

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Patient Records</h1>
        <p className="text-slate-400">
          Look up existing patients or register a new patient in the knowledge graph.
        </p>
      </div>

      <div className="flex gap-2 mb-6" role="tablist" aria-label="Patient record tabs">
        {['lookup', 'add'].map(t => (
          <button
            key={t}
            role="tab"
            aria-selected={tab === t}
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
            <label htmlFor="patient-lookup-id" className="sr-only">Patient ID</label>
            <input
              id="patient-lookup-id"
              type="text"
              value={patientId}
              onChange={e => setPatientId(e.target.value)}
              placeholder="Enter Patient ID (e.g. P001)"
              className={inputClass + ' flex-1'}
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
            <div role="alert" className="p-3 bg-red-900/20 border border-red-700 rounded-lg text-red-300 text-sm mb-4">
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
                      <span key={typeof c === 'object' ? c.name : c} className={`text-xs px-2 py-1 rounded border ${severityBadge(c.severity)}`}>
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
                      <span key={typeof m === 'object' ? m.name : m} className="text-xs px-2 py-1 rounded border border-sky-700 bg-sky-900/20 text-sky-300">
                        {m.name || m}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {patient.drug_interactions?.length > 0 && (
                <div className="p-3 bg-red-900/20 border border-red-700 rounded-lg">
                  <h3 className="text-sm font-semibold text-red-300 mb-1">
                    {patient.drug_interactions.length} drug interaction{patient.drug_interactions.length !== 1 ? 's' : ''} detected
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

            <div>
              <label htmlFor="pid" className="block text-sm font-medium text-slate-300 mb-1">
                Patient ID <span className="text-slate-500 font-normal">(letters, numbers, - or _)</span>
              </label>
              <input id="pid" type="text" value={form.patient_id} onChange={setField('patient_id')}
                placeholder="P001" pattern="^[A-Za-z0-9_-]+$"
                title="Letters, numbers, hyphens and underscores only"
                className={inputClass} />
            </div>

            <div>
              <label htmlFor="pname" className="block text-sm font-medium text-slate-300 mb-1">Full Name</label>
              <input id="pname" type="text" value={form.name} onChange={setField('name')}
                placeholder="John Doe" className={inputClass} />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="page" className="block text-sm font-medium text-slate-300 mb-1">Age</label>
                <input id="page" type="number" value={form.age} onChange={setField('age')}
                  placeholder="45" min="0" max="150" className={inputClass} />
              </div>
              <div>
                <label htmlFor="pblood" className="block text-sm font-medium text-slate-300 mb-1">Blood Type</label>
                <input id="pblood" type="text" value={form.blood_type} onChange={setField('blood_type')}
                  placeholder="O+" className={inputClass} />
              </div>
            </div>

            <div>
              <label htmlFor="pgender" className="block text-sm font-medium text-slate-300 mb-1">Gender</label>
              <select id="pgender" value={form.gender} onChange={setField('gender')}
                className={inputClass + ' cursor-pointer'}>
                <option value="" disabled>Select gender…</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            {error && (
              <div role="alert" className="p-3 bg-red-900/20 border border-red-700 rounded-lg text-red-300 text-sm">
                {error}
              </div>
            )}
            {saved && (
              <div role="status" className="p-3 bg-green-900/20 border border-green-700 rounded-lg text-green-300 text-sm">
                Patient added to the knowledge graph successfully.
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !form.patient_id || !form.name || !form.age || !form.gender || !form.blood_type}
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
