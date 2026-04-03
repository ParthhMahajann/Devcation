import { useState, useEffect, useRef } from 'react'
import GraphVisualization from '../components/graph/GraphVisualization'
import LoadingSpinner from '../components/common/LoadingSpinner'
import { useGraphData } from '../hooks/useGraphData'
import { NODE_COLORS } from '../utils/graphHelpers'

const NODE_TYPES = ['Disease', 'Symptom', 'Drug', 'SideEffect', 'Gene', 'Patient']

export default function GraphExplorerPage() {
  const containerRef = useRef(null)
  const [dims, setDims] = useState({ w: 800, h: 600 })
  const [activeTypes, setActiveTypes] = useState(new Set(NODE_TYPES))
  const { graphData, loading, error, load } = useGraphData()

  useEffect(() => {
    load({ limit: 200 })
  }, [])

  useEffect(() => {
    const obs = new ResizeObserver(entries => {
      const { width, height } = entries[0].contentRect
      setDims({ w: Math.floor(width), h: Math.max(500, Math.floor(height)) })
    })
    if (containerRef.current) obs.observe(containerRef.current)
    return () => obs.disconnect()
  }, [])

  const toggleType = (type) => {
    setActiveTypes(prev => {
      const next = new Set(prev)
      next.has(type) ? next.delete(type) : next.add(type)
      return next
    })
  }

  const filteredData = graphData
    ? {
        nodes: graphData.nodes.filter(n => activeTypes.has(n.type)),
        links: graphData.links.filter(l => {
          const srcId = l.source?.id ?? l.source
          const tgtId = l.target?.id ?? l.target
          const srcNode = graphData.nodes.find(n => n.id === srcId)
          const tgtNode = graphData.nodes.find(n => n.id === tgtId)
          return srcNode && tgtNode && activeTypes.has(srcNode.type) && activeTypes.has(tgtNode.type)
        }),
      }
    : null

  return (
    <div className="flex flex-col h-[calc(100vh-64px)]">
      <div className="px-4 py-4 border-b border-slate-700 flex flex-wrap items-center gap-4">
        <div>
          <h1 className="text-xl font-bold text-white">Graph Explorer</h1>
          <p className="text-xs text-slate-400">
            {filteredData ? `${filteredData.nodes.length} nodes · ${filteredData.links.length} edges` : 'Loading…'}
          </p>
        </div>
        <div className="flex flex-wrap gap-2 ml-auto">
          {NODE_TYPES.map(type => (
            <button
              key={type}
              onClick={() => toggleType(type)}
              aria-pressed={activeTypes.has(type)}
              aria-label={`Toggle ${type} nodes`}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-all ${
                activeTypes.has(type) ? 'opacity-100' : 'opacity-30'
              }`}
              style={{
                borderColor: NODE_COLORS[type],
                color: NODE_COLORS[type],
                background: activeTypes.has(type) ? `${NODE_COLORS[type]}15` : 'transparent',
              }}
            >
              {type}
            </button>
          ))}
        </div>
        <button
          onClick={() => load({ limit: 200 })}
          disabled={loading}
          className="px-3 py-1 text-xs rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-300 transition-colors disabled:opacity-50"
        >
          Refresh
        </button>
      </div>

      <div ref={containerRef} className="flex-1 overflow-hidden bg-slate-900" aria-label="Medical knowledge graph visualization" role="region">
        {loading && (
          <div className="flex items-center justify-center h-full">
            <LoadingSpinner message="Loading knowledge graph..." />
          </div>
        )}
        {error && (
          <div className="flex items-center justify-center h-full text-red-400">
            Failed to load graph: {error}
          </div>
        )}
        {filteredData && !loading && (
          <GraphVisualization data={filteredData} width={dims.w} height={dims.h} />
        )}
      </div>
    </div>
  )
}
