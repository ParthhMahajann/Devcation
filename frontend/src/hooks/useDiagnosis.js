import { useState, useCallback } from 'react'
import { diagnose } from '../api/symptoms'

export function useDiagnosis() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const runDiagnosis = useCallback(async (symptoms) => {
    setLoading(true)
    setError(null)
    try {
      const data = await diagnose(symptoms)
      setResults(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [])

  return { results, loading, error, runDiagnosis }
}
