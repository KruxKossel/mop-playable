<template>
  <div class="bg-slate-300 rounded-lg shadow-md p-4 mb-6">
    <!-- Grid Filters -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Name Filter -->
      <div>
        <label class="block text-sm font-medium mb-1 text-gray-800" aria-label="Filter cards by name">Card Name</label>
        <input 
          v-model="filters.name"
          type="text"
          class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
          placeholder="Search by name..."
          @input="emitFilters"
        >
      </div>

      <!-- Mana Cost Filter -->
      <div>
        <label class="block text-sm font-medium mb-1 text-gray-800" aria-label="Filter cards by mana cost">Mana Cost</label>
        <div class="flex gap-2">
          <input 
            v-model.number="filters.costMin"
            type="number"
            min="0"
            class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
            placeholder="Min"
            @input="emitFilters"
          >
          <input 
            v-model.number="filters.costMax"
            type="number"
            min="0"
            class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
            placeholder="Max"
            @input="emitFilters"
          >
        </div>
      </div>

      <!-- Description Filter -->
      <div>
        <label class="block text-sm font-medium mb-1 text-gray-800" aria-label="Filter cards by description">Description</label>
        <input 
          v-model="filters.description"
          type="text"
          class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
          placeholder="Search in description..."
          @input="emitFilters"
        >
      </div>
    </div>

    <!-- Type Filter -->
    <div class="mt-4">
      <label class="block text-sm font-medium mb-1 text-gray-800" aria-label="Filtrar cartas por tipo">Tipo de Carta</label>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="type in availableTypes"
          :key="type"
          @click="toggleType(type)"
          :class="[ 
            'px-3 py-1 rounded-full text-sm transition-all duration-150',
            filters.types.includes(type)
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          ]"
          aria-pressed="filters.types.includes(type)"
        >
          {{ type }}
        </button>
      </div>
    </div>

    <!-- Mana Type Filter -->
    <div class="mt-4">
      <label class="block text-sm font-medium mb-1 text-gray-800" aria-label="Filter cards by mana type">Mana Type</label>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="mana in availableManas"
          :key="mana"
          @click="toggleMana(mana)"
          :class="[ 
            'px-3 py-1 rounded-full text-sm transition-all duration-150',
            filters.manas.includes(mana)
              ? getManaButtonStyle(mana)
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          ]"
          aria-pressed="filters.manas.includes(mana)"
        >
          {{ mana }}
        </button>
      </div>
    </div>

    <!-- Search and Clear Filters -->
    <div class="mt-4 flex justify-end gap-2">
      <button
        @click="searchFilters"
        class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 focus:ring-2 focus:ring-blue-500"
        aria-label="Apply search filters"
      >
        Search
      </button>
      <button
        @click="clearFilters"
        class="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 focus:ring-2 focus:ring-gray-500"
        aria-label="Clear all search filters"
      >
        Clear Filters
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Define o evento que o componente emitirá para o pai
const emit = defineEmits(['filter']);

/**
 * Props:
 * - availableTypes: Array de tipos de cartas disponíveis.
 * - availableManas: Array de tipos de mana disponíveis.
 */
 const props = defineProps({
  availableTypes: {
    type: Array,
    default: () => ["Criatura", "Mágica Instantânea", "Encantamento", "Artefato", "Feitiço", "Terreno"],
  },
  availableManas: {
    type: Array,
    default: () => ["{R}", "{G}", "{B}", "{U}", "{W}"],
  },
});

/**
 * Estado reativo dos filtros:
 * - name: Nome da carta.
 * - costMin: Custo mínimo.
 * - costMax: Custo máximo.
 * - description: Texto de busca na descrição.
 * - types: Lista de tipos selecionados.
 * - manas: Lista de tipos de mana selecionados.
 */
const filters = ref({
  name: '',
  costMin: null,
  costMax: null,
  description: '',
  types: [],
  manas: [],
});

/**
 * Função: emitFilters
 * - Emite os filtros atualizados para o componente pai.
 */
const emitFilters = () => {
  emit('filter', { ...filters.value });
};

/**
 * Função: toggleType
 * - Adiciona ou remove um tipo da lista de tipos selecionados.
 * @param {string} type - Tipo a ser alternado.
 */
const toggleType = (type) => {
  // Certifique-se de que filters.types existe e é um array
  if (!Array.isArray(filters.value.types)) {
    filters.value.types = [];
  }

  if (filters.value.types.includes(type)) {
    filters.value.types = filters.value.types.filter((t) => t !== type);
  } else {
    filters.value.types.push(type);
  }
  emitFilters(); // Emite os filtros atualizados
};

/**
 * Função: toggleMana
 * - Adiciona ou remove um tipo de mana da lista de manas selecionados.
 * @param {string} mana - Tipo de mana a ser alternado.
 */
const toggleMana = (mana) => {
  // Certifique-se de que filters.manas existe e é um array
  if (!Array.isArray(filters.value.manas)) {
    filters.value.manas = [];
  }

  if (filters.value.manas.includes(mana)) {
    filters.value.manas = filters.value.manas.filter((m) => m !== mana);
  } else {
    filters.value.manas.push(mana);
  }
  emitFilters(); // Emite os filtros atualizados
};

/**
 * Função: getManaButtonStyle
 * - Retorna as classes CSS para o botão de mana com base no tipo.
 * @param {string} mana - Tipo de mana.
 * @returns {string} - Classes CSS.
 */
const getManaButtonStyle = (mana) => {
  const styles = {
    "{R}": "bg-red-500 text-white",
    "{G}": "bg-green-500 text-white",
    "{B}": "bg-black text-white",
    "{U}": "bg-blue-500 text-white",
    "{W}": "bg-yellow-100 text-gray-800",
  };
  
  return styles[mana] || "bg-blue-500 text-white";
};

/**
 * Função: clearFilters
 * - Reseta todos os filtros para os valores padrão e os emite para o pai.
 */
const clearFilters = () => {
  filters.value = {
    name: '',
    costMin: null,
    costMax: null,
    description: '',
    types: [],
    manas: [],
  };
  emitFilters(); // Reaplica filtros limpos
};

/**
 * Função: searchFilters
 * - Aplica explicitamente os filtros no clique do botão "Search".
 */
const searchFilters = () => {
  emitFilters(); // Reutiliza a função emitFilters
};
</script>