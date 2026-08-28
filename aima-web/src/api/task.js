import http from './http'

export const submitGeneration = (topic, stylePrompt) =>
  http.post('/articles/generate', { topic, stylePrompt })

export const getTask = (id) => http.get(`/tasks/${id}`)
