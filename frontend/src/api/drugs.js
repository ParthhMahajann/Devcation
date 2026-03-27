import client from './client'

export const listDrugs = () => client.get('/api/drugs/list').then(r => r.data)

export const checkInteractions = (drug_names) =>
  client.post('/api/drugs/interactions', { drug_names }).then(r => r.data)

export const getDrug = (id) => client.get(`/api/drugs/${id}`).then(r => r.data)
