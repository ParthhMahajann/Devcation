import client from './client'

export const getPatient = (id) =>
  client.get(`/api/patients/${id}`).then(r => r.data)

export const getPatientRisk = (id) =>
  client.get(`/api/patients/${id}/risk`).then(r => r.data)

export const addPatient = (data) =>
  client.post('/api/patients', data).then(r => r.data)
