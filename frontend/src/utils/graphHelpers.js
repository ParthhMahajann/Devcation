export const NODE_COLORS = {
  Disease:   '#ef4444',
  Symptom:   '#f59e0b',
  Drug:      '#0ea5e9',
  SideEffect:'#8b5cf6',
  Gene:      '#22c55e',
  Patient:   '#ec4899',
}

export const NODE_SIZES = {
  Disease:   8,
  Symptom:   6,
  Drug:      7,
  SideEffect:5,
  Gene:      6,
  Patient:   9,
}

export function getNodeColor(type) {
  return NODE_COLORS[type] || '#94a3b8'
}

export function getNodeSize(type) {
  return NODE_SIZES[type] || 6
}

// Convert backend graph data to force-graph format
export function toForceGraphData(data) {
  const nodes = (data?.nodes || []).map(n => ({
    id: n.id,
    label: n.label,
    type: n.type,
    color: getNodeColor(n.type),
    size: getNodeSize(n.type),
    ...n.properties,
  }))

  const links = (data?.edges || []).map(e => ({
    source: e.source,
    target: e.target,
    type: e.type,
    ...e.properties,
  }))

  return { nodes, links }
}
