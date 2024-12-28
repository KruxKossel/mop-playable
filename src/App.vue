<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">Card Deck Selector</h1>
      </div>
    </header>
    <main>
      <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <CardDeckSelector/>
      </div>
    </main>
  </div>
</template>

<script>
import CardDeckSelector from './components/CardDeckSelector.vue'
import Card from './components/Card.vue'
import CardSelector from './components/CardSelector.vue'
import DeckBuilder from './components/DeckBuilder.vue'


export default {
  name: 'App',
  components: {
    CardDeckSelector,
    Card,
    CardSelector,
    DeckBuilder
  }
}
</script>
