import { useState, useCallback } from 'react'
import { exploreGraph } from '../api/graph'
import { toForceGraphData } from '../utils/graphHelpers'

export function useGraphData() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchGraph = useCallback(async (params = {}) => {
    setLoading(true)
    setError(null)
    try {
      const raw = await exploreGraph(params)
      setGraphData(toForceGraphData(raw))
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [])

  return { graphData, loading, error, fetchGraph, load: fetchGraph }
}
