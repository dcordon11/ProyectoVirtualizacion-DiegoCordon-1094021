<script setup>
import { ref } from 'vue'
import { login, register, saveSession } from '../services/api'
import '../assets/styles/auth.css'

const emit = defineEmits(['login-success'])

const username = ref('')
const password = ref('')
const isRegisterMode = ref(false)
const message = ref('')

const handleSubmit = async () => {
  message.value = ''

  if (!username.value || !password.value) {
    message.value = 'Debes ingresar usuario y contraseña.'
    return
  }

  const response = isRegisterMode.value
    ? await register(username.value, password.value)
    : await login(username.value, password.value)

  if (response.token) {
    saveSession(response.token, response.username)
    emit('login-success')
  } else {
    message.value = response.message || 'Ocurrió un error.'
  }
}
</script>

<template>
  <main class="auth-page">
    <section class="auth-card">
      <h1>🎮 GameLog</h1>

      <p class="subtitle">
        Tu backlog personal de videojuegos
      </p>

      <div class="field">
        <label>Usuario</label>
        <input v-model="username" type="text" />
      </div>

      <div class="field">
        <label>Contraseña</label>
        <input v-model="password" type="password" />
      </div>

      <button @click="handleSubmit">
        {{ isRegisterMode ? 'Registrarme' : 'Iniciar sesión' }}
      </button>

      <p v-if="message" class="error">
        {{ message }}
      </p>

      <p class="switch">
        {{ isRegisterMode ? '¿Ya tienes cuenta?' : '¿No tienes cuenta?' }}
        <span @click="isRegisterMode = !isRegisterMode">
          {{ isRegisterMode ? 'Inicia sesión' : 'Regístrate' }}
        </span>
      </p>
    </section>
  </main>
</template>