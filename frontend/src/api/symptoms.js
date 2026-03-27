import client from './client'

export const listSymptoms = () => client.get('/api/symptoms/list').then(r => r.data)

export const diagnose = (symptoms) =>
  client.post('/api/symptoms/diagnose', { symptoms }).then(r => r.data)
