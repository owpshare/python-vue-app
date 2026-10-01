<template>
  <div class="page-container">
    <h2>Data from SQLite</h2>
    <p class="subtitle">This view communicates directly with your Flask API endpoints.</p>

    <section class="random-number-section" aria-labelledby="random-number-heading">
      <h3 id="random-number-heading">Random number from server</h3>
      <div class="random-number-controls">
        <button type="button" :disabled="isGenerating" @click="generateRandomNumber">
          {{ isGenerating ? 'Generating...' : 'Get random number' }}
        </button>
        <output v-if="randomNumber !== null" class="random-number" aria-live="polite">
          {{ randomNumber }}
        </output>
      </div>
      <p v-if="randomNumberError" class="request-error" role="alert">
        {{ randomNumberError }}
      </p>
    </section>
    
    <div class="card">
      <ul v-if="items.length" class="item-list">
        <li v-for="item in items" :key="item.id" class="item-row">
          <span class="badge">ID: {{ item.id }}</span> {{ item.name }}
        </li>
      </ul>
      <p v-else class="empty-state">Loading items from database or table is empty...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const items = ref([])
const randomNumber = ref(null)
const isGenerating = ref(false)
const randomNumberError = ref('')

const generateRandomNumber = async () => {
  isGenerating.value = true
  randomNumberError.value = ''
  try {
    const response = await fetch('/api/random-number')
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`)
    }
    const result = await response.json()
    randomNumber.value = result.number
  } catch (error) {
    randomNumberError.value = 'Could not get a random number from the server.'
  } finally {
    isGenerating.value = false
  }
}

const fetchItems = async () => {
  try {
    const response = await fetch('/api/items')
    if (response.ok) {
      items.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching data from Flask backend:', error)
  }
}

onMounted(() => {
  fetchItems()
})
</script>

<style scoped>
.page-container {
  padding: 1rem 0;
}
.random-number-section {
  margin: 0 0 1.5rem;
}
.random-number-section h3 {
  margin: 0 0 0.75rem;
}
.random-number-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.random-number-controls button {
  padding: 0.6rem 0.9rem;
  border: 0;
  border-radius: 4px;
  background: #237a57;
  color: white;
  font: inherit;
  cursor: pointer;
}
.random-number-controls button:disabled {
  cursor: wait;
  opacity: 0.65;
}
.random-number {
  font-size: 1.5rem;
  font-weight: 700;
}
.request-error {
  color: #b42318;
}
.subtitle {
  color: #666;
  margin-bottom: 1.5rem;
}
.card {
  background: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
}
.item-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.item-row {
  padding: 0.75rem 0;
  border-bottom: 1px solid #eaeaea;
  display: flex;
  align-items: center;
}
.item-row:last-child {
  border-bottom: none;
}
.badge {
  background: #42b983;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  margin-right: 1rem;
  font-weight: bold;
}
.empty-state {
  color: #999;
  font-style: italic;
  text-align: center;
}
</style>
