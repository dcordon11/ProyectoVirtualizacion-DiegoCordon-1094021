const API_URL = 'http://34.27.143.250:5000'

export const getToken = () => {
  return localStorage.getItem('token')
}

export const getUsername = () => {
  return localStorage.getItem('username')
}

export const saveSession = (token, username) => {
  localStorage.setItem('token', token)
  localStorage.setItem('username', username)
}

export const clearSession = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
}

const authHeaders = () => ({
  'Content-Type': 'application/json',
  Authorization: `Bearer ${getToken()}`
})

export const login = async (username, password) => {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })

  return response.json()
}

export const register = async (username, password) => {
  const response = await fetch(`${API_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })

  return response.json()
}

export const getGames = async () => {
  const response = await fetch(`${API_URL}/games`, {
    headers: authHeaders()
  })

  return response.json()
}

export const createGame = async (game) => {
  const response = await fetch(`${API_URL}/games`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(game)
  })

  return response.json()
}

export const deleteGame = async (id) => {
  const response = await fetch(`${API_URL}/games/${id}`, {
    method: 'DELETE',
    headers: authHeaders()
  })

  return response.json()
}