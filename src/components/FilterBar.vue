<template>
  <div class="bg-white rounded-lg shadow-md p-4 mb-6">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Name filter -->
      <div>
        <label class="block text-sm font-medium mb-1 text-gray-800">Card Name</label>
        <input 
          v-model="filters.name"
          type="text"
          class="w-full p-2 border rounded"
          placeholder="Search by name..."
          @input="emitFilters"
        >
      </div>

      <!-- Cost filter -->
      <div>
        <label class="block text-sm font-medium mb-1 text-gray-800">Mana Cost</label>
        <div class="flex gap-2">
          <input 
            v-model.number="filters.costMin"
            type="number"
            min="0"
            class="w-full p-2 border rounded"
            placeholder="Min"
            @input="emitFilters"
          >
          <input 
            v-model.number="filters.costMax"
            type="number"
            min="0"
            class="w-full p-2 border rounded"
            placeholder="Max"
            @input="emitFilters"
          >
        </div>
      </div>

      <!-- Description filter -->
      <div>
        <label class="block text-sm font-medium mb-1 text-gray-800">Description</label>
        <input 
          v-model="filters.description"
          type="text"
          class="w-full p-2 border rounded"
          placeholder="Search in description..."
          @input="emitFilters"
        >
      </div>
    </div>

    <!-- Type filter -->
    <div class="mt-4">
      <label class="block text-sm font-medium mb-1 text-gray-800">Card Type</label>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="type in availableTypes"
          :key="type"
          @click="toggleType(type)"
          :class="[ 
            'px-3 py-1 rounded-full text-sm',
            filters.types.includes(type)
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700'
          ]"
        >
          {{ type }}
        </button>
      </div>
    </div>

    <!-- Search and Clear filters buttons -->
    <div class="mt-4 flex justify-end gap-2">
      <button
        @click="searchFilters"
        class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Search
      </button>
      <button
        @click="clearFilters"
        class="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
      >
        Clear Filters
      </button>
    </div>

    <!-- Filtered cards list -->
    <div class="mt-4">
      <div v-for="card in filteredCards" :key="card.id" class="card text-gray-800">
        <h3>
          <strong>
            {{ card.name }}
          </strong>
        </h3>
        <p>Mana cost: {{ card.cost }}</p>
        <p>Type: {{ card.type }}</p>
        <p>Description: {{ card.description }}</p>
        <br>
        <hr>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['filter'])

const props = defineProps({
  availableTypes: {
    type: Array,
    default: () => []
  }
})
const filters = ref({
  name: '',
  costMin: null,
  costMax: null,
  description: '',
  types: []
})

const cards = ref([]) 
const filteredCards = ref([])  

// Função para converter o custo de mana (como {2}{G}) em um valor numérico
function parseManaCost(cost) {
  let totalCost = 0
  const costPattern = /\{(\d+)?([A-Za-z])?\}/g
  let match

  while ((match = costPattern.exec(cost)) !== null) {
    if (match[1]) {
      totalCost += parseInt(match[1], 10)
    } else if (match[2]) {
      totalCost += 1
    }
  }

  return totalCost
}


async function loadCards() {
  try {
    const response = await fetch('cards/cards.json')
    if (!response.ok) {
      throw new Error('Erro ao carregar o arquivo JSON')
    }

    const data = await response.json()
    console.log('Cartas carregadas:', data)
    cards.value = data  
  } catch (error) {
    console.error(error)
  }
}

const clearFilters = () => {
  filters.value = {
    name: '',
    costMin: null,
    costMax: null,
    description: '',
    types: []
  }
  filteredCards.value = []  
  emitFilters()
}

const searchFilters = async () => {
  console.log('Applying filters:', filters.value)
  try {
    if (!filters.value.name && !filters.value.costMin && !filters.value.costMax && !filters.value.description && filters.value.types.length === 0) {
      filteredCards.value = []  
      return
    }

    filteredCards.value = cards.value.filter(card => {

      const nameMatch = card.name && card.name.toLowerCase().includes(filters.value.name.toLowerCase())

      const costMatch = (
        (!filters.value.costMin || parseManaCost(card.cost) >= filters.value.costMin) &&
        (!filters.value.costMax || parseManaCost(card.cost) <= filters.value.costMax)
      )

      const descriptionMatch = card.description && card.description.toLowerCase().includes(filters.value.description.toLowerCase())

      const typeMatch = filters.value.types.length === 0 || filters.value.types.includes(card.type)

      return nameMatch && costMatch && descriptionMatch && typeMatch
    })

    filteredCards.value = filteredCards.value.map(({ id, ...card }) => card)

    console.log('Filtered cards:', filteredCards.value.map(card => card.name))
  } catch (error) {
    console.error('Error filtering cards:', error)
  }
  emitFilters()
}

const emitFilters = () => {
  emit('filter', { ...filters.value })
}

onMounted(loadCards)
</script>
