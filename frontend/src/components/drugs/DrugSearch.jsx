import { useState, useEffect } from 'react'
import Select from 'react-select'
import { listDrugs } from '../../api/drugs'

const selectStyles = {
  control: (base) => ({
    ...base, background: '#1e293b', borderColor: '#334155',
    '&:hover': { borderColor: '#0ea5e9' }, boxShadow: 'none', minHeight: '44px',
  }),
  menu: (base) => ({ ...base, background: '#1e293b', border: '1px solid #334155' }),
  option: (base, { isFocused }) => ({ ...base, background: isFocused ? '#0f172a' : '#1e293b', color: '#e2e8f0' }),
  multiValue: (base) => ({ ...base, background: '#0ea5e920' }),
  multiValueLabel: (base) => ({ ...base, color: '#7dd3fc' }),
  multiValueRemove: (base) => ({ ...base, color: '#7dd3fc', '&:hover': { background: '#ef4444', color: 'white' } }),
  placeholder: (base) => ({ ...base, color: '#64748b' }),
  input: (base) => ({ ...base, color: '#e2e8f0' }),
}

export default function DrugSearch({ onSubmit, loading }) {
  const [options, setOptions] = useState([])
  const [selected, setSelected] = useState([])

  useEffect(() => {
    listDrugs()
      .then(data => setOptions((data.drugs || []).map(d => ({ value: d.name, label: d.name, ...d }))))
      .catch(() => {
        setOptions([
          { value: 'Aspirin', label: 'Aspirin' },
          { value: 'Ibuprofen', label: 'Ibuprofen' },
          { value: 'Warfarin', label: 'Warfarin' },
          { value: 'Metformin', label: 'Metformin' },
          { value: 'Lisinopril', label: 'Lisinopril' },
        ])
      })
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (selected.length >= 2) onSubmit(selected.map(s => s.value))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <label className="block text-sm font-medium text-slate-300 mb-2">
        Select medications to check (minimum 2)
      </label>
      <Select
        isMulti options={options} value={selected} onChange={setSelected}
        styles={selectStyles} placeholder="Search drugs..."
      />
      <button
        type="submit"
        disabled={loading || selected.length < 2}
        className="w-full py-3 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 disabled:text-slate-500 text-white font-semibold rounded-lg transition-colors"
      >
        {loading ? 'Checking...' : `Check ${selected.length} drug${selected.length !== 1 ? 's' : ''} for interactions`}
      </button>
    </form>
  )
}
