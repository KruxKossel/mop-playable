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
          @print-deck="showPrintPreview = true"
        />
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <FilterBar 
    :available-types="availableTypes"
    @filter="activeFilters = $event"
  />
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

        <!-- Pagination -->
        <div class="mt-6 flex justify-center items-center gap-4">
          <button 
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="px-4 py-2 border rounded bg-gray-50 text-gray-800 border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Previous
          </button>
          
          <span class="text-sm text-gray-700">
            Page {{ currentPage }} of {{ totalPages }}
          </span>

          <button 
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="px-4 py-2 border rounded bg-gray-50 text-gray-800 border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Next
          </button>
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

  <span class="text-center font-medium">Designed with love by Masters of Pwnage community: <a href="https://github.com/fguisso"> @fguisso</a></span>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import CardDisplay from './components/CardDisplay.vue'
import DeckSummary from './components/DeckSummary.vue'
import PrintPreview from './components/PrintPreview.vue'
import FilterBar from './components/FilterBar.vue'

const availableCards = ref([]) // Will be populated from cards.json
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
  author_social: '',
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
  const cardIndex = selectedCards.value.findIndex(c => c.id === cardId)
  if (cardIndex !== -1) {
    const card = selectedCards.value[cardIndex]
    if (card.amount > 1) {
      card.amount--
    } else {
      selectedCards.value.splice(cardIndex, 1)
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

const filteredCards = computed(() => {
  return availableCards.value.filter(card => {
    // Name filter
    if (activeFilters.value.name && !card.name.toLowerCase().includes(activeFilters.value.name.toLowerCase())) {
      return false
    }
    
    // Cost filter
    if (activeFilters.value.costMin !== null && card.cost < activeFilters.value.costMin) {
      return false
    }
    if (activeFilters.value.costMax !== null && card.cost > activeFilters.value.costMax) {
      return false
    }
    
    // Description filter
    if (activeFilters.value.description && 
        !card.description.toLowerCase().includes(activeFilters.value.description.toLowerCase())) {
      return false
    }
    
    // Type filter
    if (activeFilters.value.types.length > 0 && !activeFilters.value.types.includes(card.type)) {
      return false
    }
    
    return true
  })
})

const availableTypes = computed(() => {
  const types = new Set(availableCards.value.map(card => card.type))
  return Array.from(types).sort()
})

const cardsPerPage = ref(12)
const currentPage = ref(1)

// Reset page when filters change
watch([activeFilters, cardsPerPage], () => {
  currentPage.value = 1
})

const totalPages = computed(() => {
  return Math.ceil(filteredCards.value.length / cardsPerPage.value)
})

const paginatedCards = computed(() => {
  const startIndex = (currentPage.value - 1) * cardsPerPage.value
  const endIndex = startIndex + cardsPerPage.value
  return filteredCards.value.slice(startIndex, endIndex)
})

// Validation functions
const validateDeckStructure = (deck) => {
  const errors = []
  
  // Check required fields
  if (!deck.name) errors.push('Deck name is required')
  if (!deck.cards || !Array.isArray(deck.cards)) {
    errors.push('Deck must contain a valid cards array')
    return errors
  }
  
  // Validate card entries
  let totalCards = 0
  const cardCounts = new Map()
  
  for (const card of deck.cards) {
    if (!card.id) {
      errors.push(`Invalid card entry: missing card ID`)
      continue
    }
    
    if (!card.amount || typeof card.amount !== 'number' || card.amount < 1) {
      errors.push(`Invalid amount for card ${card.id}`)
      continue
    }
    
    // Check if card exists in available cards
    const cardExists = availableCards.value.some(c => c.id === card.id)
    if (!cardExists) {
      errors.push(`Card with ID ${card.id} does not exist in the card pool`)
      continue
    }
    
    // Get the card details
    const cardDetails = availableCards.value.find(c => c.id === card.id)
    if (!cardDetails) {
      errors.push(`Card with ID ${card.id} not found in available cards`)
      continue
    }
    
    // Track card counts - skip limit for mana cards (cards with no cost)
    const isManaCard = cardDetails.cost === undefined || cardDetails.cost === null
    const currentCount = cardCounts.get(card.id) || 0
    const newCount = currentCount + card.amount
    
    if (!isManaCard && newCount > 4) {
      errors.push(`Card ${cardDetails.name || card.id} exceeds maximum of 4 copies (has ${newCount})`)
    }
    cardCounts.set(card.id, newCount)
    
    totalCards += card.amount
  }
  
  // Check total cards
  if (totalCards > 60) {
    errors.push(`Deck exceeds maximum size of 60 cards (has ${totalCards})`)
  }
  
  return errors
}

const loadDeck = (deck) => {
  try {
    // Validate deck structure
    const validationErrors = validateDeckStructure(deck)
    
    if (validationErrors.length > 0) {
      throw new Error('Deck validation failed:\n' + validationErrors.join('\n'))
    }

    // Update deck info
    deckInfo.value = {
      id: deck.id || crypto.randomUUID(),
      name: deck.name,
      author: deck.author || '',
      author_social: deck.author_social || ''
    }

    // Load cards with validated amounts
    selectedCards.value = deck.cards.map(card => ({
      id: card.id,
      amount: Math.min(Math.max(1, card.amount), 4) // Ensure amount is between 1 and 4
    }))

  } catch (error) {
    console.error('Error loading deck:', error)
    alert(error.message)
    return false
  }
  
  return true
}


// Load cards from JSON file
fetch('cards.json')
  .then(response => response.json())
  .then(data => {
    console.log('Loaded cards:', data); // Debug log
    availableCards.value = Array.isArray(data) ? data : 
                          Array.isArray(data.cards) ? data.cards : 
                          Object.values(data);
  })
  .catch(error => {
    console.error('Error loading cards:', error);
  })
</script>