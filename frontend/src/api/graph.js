import client from './client'

export const getStats = () => client.get('/api/graph/stats').then(r => r.data)

export const exploreGraph = (params = {}) =>
  client.get('/api/graph/explore', { params }).then(r => r.data)
