import { useRef, useCallback } from 'react'
import ForceGraph2D from 'react-force-graph-2d'
import { getNodeColor, getNodeSize } from '../../utils/graphHelpers'

export default function GraphVisualization({ data, width = 800, height = 600 }) {
  const fgRef = useRef()

  const handleNodeClick = useCallback(node => {
    fgRef.current?.centerAt(node.x, node.y, 500)
    fgRef.current?.zoom(3, 500)
  }, [])

  const paintNode = useCallback((node, ctx, globalScale) => {
    const r = getNodeSize(node.type) / globalScale + 2
    ctx.beginPath()
    ctx.arc(node.x, node.y, r, 0, 2 * Math.PI)
    ctx.fillStyle = getNodeColor(node.type)
    ctx.fill()

    if (globalScale > 1.5) {
      const label = node.label || node.id
      const fontSize = 10 / globalScale
      ctx.font = `${fontSize}px Sans-Serif`
      ctx.fillStyle = '#e2e8f0'
      ctx.textAlign = 'center'
      ctx.fillText(label, node.x, node.y + r + fontSize)
    }
  }, [])

  if (!data || data.nodes.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-slate-500">
        No graph data to display
      </div>
    )
  }

  return (
    <div
      role="img"
      aria-label={`Medical knowledge graph with ${data.nodes.length} nodes and ${data.links.length} edges`}
    >
      <ForceGraph2D
        ref={fgRef}
        graphData={data}
        width={width}
        height={height}
        backgroundColor="#0f172a"
        nodeCanvasObject={paintNode}
        nodeCanvasObjectMode={() => 'replace'}
        linkColor={() => '#334155'}
        linkWidth={1}
        linkDirectionalArrowLength={3}
        linkDirectionalArrowRelPos={1}
        onNodeClick={handleNodeClick}
        cooldownTicks={100}
        nodeLabel={node => `${node.type}: ${node.label || node.id}`}
      />
    </div>
  )
}
