<script setup>
defineProps({
  username: String
})

const emit = defineEmits(['logout'])
</script>

<template>
  <nav class="navbar">
    <div class="brand">🎮 GameLog</div>

    <div class="nav-user">
      <span>{{ username }}</span>
      <button @click="emit('logout')">Cerrar sesión</button>
    </div>
  </nav>
</template>