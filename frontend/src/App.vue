<script setup>
import { ref } from 'vue'
import LoginView from './views/LoginView.vue'
import DashboardView from './views/DashboardView.vue'
import { getToken, clearSession } from './services/api'

const isAuthenticated = ref(!!getToken())

const handleLogin = () => {
  isAuthenticated.value = true
}

const handleLogout = () => {
  clearSession()
  isAuthenticated.value = false
}
</script>

<template>
  <LoginView
    v-if="!isAuthenticated"
    @login-success="handleLogin"
  />

  <DashboardView
    v-else
    @logout="handleLogout"
  />
</template>