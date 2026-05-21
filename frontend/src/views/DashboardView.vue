<script setup>
import { ref, onMounted } from 'vue'
import { getGames, createGame, getUsername } from '../services/api'
import Navbar from '../components/Navbar.vue'
import GameForm from '../components/GameForm.vue'
import GameCard from '../components/GameCard.vue'
import '../assets/styles/dashboard.css'
import '../assets/styles/cards.css'

const emit = defineEmits(['logout'])

const games = ref([])
const username = getUsername()

const loadGames = async () => {
  games.value = await getGames()
}

const handleCreateGame = async (game) => {
  await createGame(game)
  await loadGames()
}

const handleDeleted = async () => {
  await loadGames()
}

onMounted(loadGames)
</script>

<template>
  <Navbar
    :username="username"
    @logout="emit('logout')"
  />

  <main class="dashboard">
    <section class="hero">
      <h1>Mi backlog de videojuegos</h1>
      <p>
        Guarda juegos pendientes, registra tus horas y califica tus experiencias.
      </p>
    </section>

    <section class="layout">
      <GameForm @create-game="handleCreateGame" />

      <section class="games-section">
        <h2>Mis juegos</h2>

        <div v-if="games.length === 0" class="empty">
          Todavía no has agregado juegos.
        </div>

        <div v-else class="games-grid">
          <GameCard
            v-for="game in games"
            :key="game.id"
            :game="game"
            @deleted="handleDeleted"
          />
        </div>
      </section>
    </section>
  </main>
</template>