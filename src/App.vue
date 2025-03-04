<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">Card Deck Builder</h1>

    <!-- Deck Information Form -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">Deck Information</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1">Deck Name</label>
          <input 
            v-model="deckInfo.name"
            type="text"
            class="w-full p-2 border rounded"
            placeholder="Enter deck name"
          >
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Author</label>
          <input 
            v-model="deckInfo.author"
            type="text"
            class="w-full p-2 border rounded"
            placeholder="Enter author name"
          >
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Author Social</label>
          <input 
            v-model="deckInfo.author_social"
            type="text"
            class="w-full p-2 border rounded"
            placeholder="Enter social media handle"
          >
        </div>
      </div>

      <!-- Deck Summary -->
      <div class="lg:col-span-1">
        <DeckSummary
          :deck-info="deckInfo"
          :selected-cards="selectedCards"
          :total-cards="totalCards"
          @export-deck="exportDeck"
          @import-deck="importDeck"
          @print-deck="showPrintPreview = true"
        />
      </div>
    </div>

    <!-- Modal de Importação -->
    <ImportDeckModal 
      :isOpen="isModalOpen"
      @imported="handleImport"
      @close="isModalOpen = false"
    />

    <!-- Outros componentes -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <FilterBar :available-types="availableTypes" @filter="activeFilters = $event" />

      <!-- Card Browser -->
      <div class="lg:col-span-2">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">Available Cards</h2>
          <div class="flex items-center gap-4">
            <label class="text-sm font-medium text-gray-700">Cards per page:</label>
            <select 
              v-model="cardsPerPage" 
              class="p-2 border rounded bg-gray-50 text-gray-800 border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            >
              <option :value="12">12</option>
              <option :value="24">24</option>
              <option :value="48">48</option>
              <option :value="60">60</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          <CardDisplay
            v-for="card in paginatedCards"
            :key="card.id"
            :card="card"
            :copies-in-deck="getCardCopies(card.id)"
            @add-card="addCardToDeck"
            @remove-card="removeCardFromDeck"
          />
        </div>
      </div>
    </div>

    <!-- Print Preview Modal -->
    <PrintPreview
      v-if="showPrintPreview"
      :selected-cards="selectedCards"
      :available-cards="availableCards"
      @close="showPrintPreview = false"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import CardDisplay from './components/CardDisplay.vue'
import DeckSummary from './components/DeckSummary.vue'
import PrintPreview from './components/PrintPreview.vue'
import FilterBar from './components/FilterBar.vue'
import ImportDeckModal from './components/ImportDeckModal.vue'

const availableCards = ref([])
const selectedCards = ref([])
const showPrintPreview = ref(false)

const activeFilters = ref({
  name: '',
  costMin: null,
  costMax: null,
  description: '',
  types: []
})

const deckInfo = ref({
  id: crypto.randomUUID(),
  name: '',
  author: '',
  author_social: ''
})

const totalCards = computed(() => {
  return selectedCards.value.reduce((total, card) => total + card.amount, 0)
})

const getCardCopies = (cardId) => {
  const card = selectedCards.value.find(c => c.id === cardId)
  return card ? card.amount : 0
}

const addCardToDeck = (card) => {
  if (totalCards.value >= 60) return
  const existingCard = selectedCards.value.find(c => c.id === card.id)
  if (existingCard) {
    if (existingCard.amount < 4) {
      existingCard.amount++
    }
  } else {
    selectedCards.value.push({
      id: card.id,
      amount: 1
    })
  }
}

const removeCardFromDeck = (cardId) => {
  const index = selectedCards.value.findIndex(c => c.id === cardId)
  if (index !== -1) {
    const card = selectedCards.value[index]
    if (card.amount > 1) {
      card.amount--
    } else {
      selectedCards.value.splice(index, 1)
    }
  }
}

const exportDeck = () => {
  const deckData = {
    ...deckInfo.value,
    cards: selectedCards.value
  }

  const blob = new Blob([JSON.stringify(deckData, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${deckInfo.value.name.toLowerCase().replace(/\s+/g, '-')}.json`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

// Configuração da importação do deck
const isModalOpen = ref(false)
const decks = ref([])

const importDeck = () => {
  isModalOpen.value = true
}

const handleImport = (deck) => {
  console.log("Deck importado:", deck)
  decks.value.push(deck)

  // Atualizando os campos do formulário com os dados do deck importado
  deckInfo.value.name = deck.name || '';  // Preenche o nome do deck
  deckInfo.value.author = deck.author || '';  // Preenche o autor do deck
  deckInfo.value.author_social = deck.author_social || '';  // Preenche a rede social do autor

  isModalOpen.value = false
}

// Carregar cartas de um JSON externo
fetch('cards.json')
  .then(response => response.json())
  .then(data => {
    availableCards.value = Array.isArray(data) ? data : (Array.isArray(data.cards) ? data.cards : Object.values(data))
  })
  .catch(error => {
    console.error('Erro ao carregar as cartas:', error)
  })
</script>
