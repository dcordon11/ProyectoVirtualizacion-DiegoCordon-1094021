<script setup>
const model = defineModel()
</script>

<template>
  <div class="stars">
    <button
      v-for="star in 5"
      :key="star"
      type="button"
      class="star"
      :class="{ active: star <= model }"
      @click="model = star"
    >
      ★
    </button>

    <button
      type="button"
      class="clear-rating"
      @click="model = 0"
    >
      Limpiar
    </button>
  </div>
</template>