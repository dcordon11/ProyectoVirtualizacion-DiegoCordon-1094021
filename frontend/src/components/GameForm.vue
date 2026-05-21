<script setup>
import { ref } from 'vue'
import StarRating from './StarRating.vue'

const emit = defineEmits(['create-game'])

const form = ref({
  title: '',
  platform: '',
  genre: '',
  status: 'pendiente',
  rating: 0,
  hoursPlayed: 0,
  review: '',
  imageUrl: ''
})

const submitForm = () => {
  if (!form.value.title) return

  emit('create-game', { ...form.value })

  form.value = {
    title: '',
    platform: '',
    genre: '',
    status: 'pendiente',
    rating: 0,
    hoursPlayed: 0,
    review: '',
    imageUrl: ''
    }
}
</script>

<template>
  <section class="form-card">
    <h2>Agregar juego</h2>

    <div class="field">
      <label>Título del juego</label>
      <input v-model="form.title" type="text" />
    </div>

    <div class="field">
      <label>Plataforma</label>
      <input v-model="form.platform" type="text" />
    </div>

    <div class="field">
      <label>Género</label>
      <input v-model="form.genre" type="text" />
    </div>

    <div class="field">
      <label>Estado</label>
      <select v-model="form.status">
        <option value="pendiente">Pendiente</option>
        <option value="jugando">Jugando</option>
        <option value="terminado">Terminado</option>
      </select>
    </div>

    <div class="field">
      <label>Calificación</label>
      <StarRating v-model="form.rating" />
    </div>

    <div class="field">
      <label>Horas jugadas</label>
      <input v-model="form.hoursPlayed" type="number" min="0" />
    </div>

    <div class="field">
      <label>Reseña personal</label>
      <textarea v-model="form.review"></textarea>
    </div>

    <div class="field">
        <label>URL de imagen / portada</label>
        <input v-model="form.imageUrl" type="text" />
    </div>

    <button @click="submitForm">
      Guardar juego
    </button>
  </section>
</template>