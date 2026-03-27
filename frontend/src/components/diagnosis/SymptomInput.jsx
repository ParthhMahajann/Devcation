import { useState, useEffect } from 'react'
import Select from 'react-select'
import { listSymptoms } from '../../api/symptoms'

const selectStyles = {
  control: (base) => ({
    ...base,
    background: '#1e293b',
    borderColor: '#334155',
    '&:hover': { borderColor: '#0ea5e9' },
    boxShadow: 'none',
    minHeight: '44px',
  }),
  menu: (base) => ({ ...base, background: '#1e293b', border: '1px solid #334155' }),
  option: (base, { isFocused }) => ({
    ...base,
    background: isFocused ? '#0f172a' : '#1e293b',
    color: '#e2e8f0',
  }),
  multiValue: (base) => ({ ...base, background: '#0ea5e920' }),
  multiValueLabel: (base) => ({ ...base, color: '#7dd3fc' }),
  multiValueRemove: (base) => ({ ...base, color: '#7dd3fc', '&:hover': { background: '#ef4444', color: 'white' } }),
  placeholder: (base) => ({ ...base, color: '#64748b' }),
  input: (base) => ({ ...base, color: '#e2e8f0' }),
  singleValue: (base) => ({ ...base, color: '#e2e8f0' }),
}

export default function SymptomInput({ onSubmit, loading }) {
  const [options, setOptions] = useState([])
  const [selected, setSelected] = useState([])

  useEffect(() => {
    listSymptoms()
      .then(data =>
        setOptions((data.symptoms || []).map(s => ({ value: s.name, label: s.name, ...s })))
      )
      .catch(() => {
        // fallback options
        setOptions([
          { value: 'Fever', label: 'Fever' },
          { value: 'Cough', label: 'Cough' },
          { value: 'Headache', label: 'Headache' },
          { value: 'Fatigue', label: 'Fatigue' },
          { value: 'Nausea', label: 'Nausea' },
          { value: 'Chest Pain', label: 'Chest Pain' },
          { value: 'Shortness of Breath', label: 'Shortness of Breath' },
          { value: 'Sore Throat', label: 'Sore Throat' },
        ])
      })
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (selected.length > 0) {
      onSubmit(selected.map(s => s.value))
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-slate-300 mb-2">
          Select your symptoms
        </label>
        <Select
          isMulti
          options={options}
          value={selected}
          onChange={setSelected}
          styles={selectStyles}
          placeholder="Search and select symptoms..."
          className="text-sm"
        />
      </div>
      <button
        type="submit"
        disabled={loading || selected.length === 0}
        className="w-full py-3 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 disabled:text-slate-500 text-white font-semibold rounded-lg transition-colors"
      >
        {loading ? 'Analyzing...' : `Analyze ${selected.length} symptom${selected.length !== 1 ? 's' : ''}`}
      </button>
    </form>
  )
}
