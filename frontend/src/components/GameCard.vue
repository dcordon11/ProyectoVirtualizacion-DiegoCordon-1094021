<script setup>
import { deleteGame } from '../services/api'

const props = defineProps({
  game: Object
})

const emit = defineEmits(['deleted'])

const handleDelete = async () => {
  await deleteGame(props.game.id)
  emit('deleted')
}
</script>

<template>
  <article class="game-card">
    <img
      v-if="game.imageUrl"
      :src="game.imageUrl"
      :alt="game.title"
      class="game-cover"
    />

    <div v-else class="game-cover placeholder">
      🎮
    </div>

    <div class="card-header">
      <h3>{{ game.title }}</h3>
      <span class="rating">
        {{ '★'.repeat(game.rating) }}{{ '☆'.repeat(5 - game.rating) }}
      </span>
    </div>

    <p><strong>Plataforma:</strong> {{ game.platform || 'No especificada' }}</p>
    <p><strong>Género:</strong> {{ game.genre || 'No especificado' }}</p>

    <p>
      <strong>Estado:</strong>
      <span class="status">{{ game.status }}</span>
    </p>

    <p><strong>Horas jugadas:</strong> {{ game.hoursPlayed }}</p>

    <p class="review">
      {{ game.review || 'Sin reseña todavía.' }}
    </p>

    <button class="delete-btn" @click="handleDelete">
      Eliminar
    </button>
  </article>
</template>