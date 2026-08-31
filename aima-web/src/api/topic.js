import http from './http'

/** 选题池分页查询 */
export const getTopics = (params) => http.get('/topics', { params })

/** 从选题发起生成(主题取热点标题,只需传风格) */
export const createArticleFromTopic = (id, stylePrompt) =>
  http.post(`/topics/${id}/create-article`, { stylePrompt })
