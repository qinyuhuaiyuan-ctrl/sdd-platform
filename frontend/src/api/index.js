// frontend/src/api/index.js
const BASE = '/api'

async function request(method, url, body) {
  const opts = { method, headers: {} }
  if (body) {
    opts.headers['Content-Type'] = 'application/json'
    opts.body = JSON.stringify(body)
  }
  const res = await fetch(`${BASE}${url}`, opts)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || res.statusText)
  }
  return res.json()
}

// 路径编码：保留 / 分隔符，只编码每段中的特殊字符
function encodePath(path) {
  return path.split('/').map(encodeURIComponent).join('/')
}

export const api = {
  getStages:     ()       => request('GET', '/stages'),
  advanceStage:  ()       => request('POST', '/stages/next'),

  getFile:       (path)   => request('GET', `/files/${encodePath(path)}`),
  saveFile:      (path, content) => request('PUT', `/files/${encodePath(path)}`, { content }),

  getSkills:     ()       => request('GET', '/skills'),
  getSkillFile:  (stage, path) => request('GET', `/skills/${stage}/${encodePath(path)}`),
  saveSkillFile: (stage, path, content) => request('PUT', `/skills/${stage}/${encodePath(path)}`, { content }),

  getTemplates:  ()       => request('GET', '/templates'),
  getTemplate:   (type)   => request('GET', `/templates/${type}`),
  saveTemplate:  (type, content) => request('PUT', `/templates/${type}`, { content }),

  getGitLog:     ()       => request('GET', '/git/log'),
  getGitStatus:  ()       => request('GET', '/git/status'),
  refreshFiles:  ()       => request('POST', '/git/refresh'),
}
