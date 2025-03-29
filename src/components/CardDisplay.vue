<template>
  <div class="bg-white shadow-md p-4 rounded flex flex-col h-[500px]">
    <!-- Imagem da Carta -->
    <div 
      class="bg-gray-200 mb-6 mx-auto flex items-center justify-center h-48 rounded overflow-hidden relative group"
      @click="openImage = true"
    >
      <img 
        v-if="card.image && !imageError"
        :src="card.image" 
        :alt="card.name || 'Unnamed Card'"
        class="w-full h-full object-contain rounded transition-transform duration-300 cursor-pointer"
        @error="handleImageError"
      >
      <div v-else class="text-gray-500">No Image Available</div>
    </div>

    <!-- Informações da Carta -->
    <h3 class="text-lg font-semibold mb-3 text-black text-center">{{ card.name || 'Unnamed Card' }}</h3>
    <div class="grid grid-cols-2 gap-4 mb-4 text-sm text-black">
      <div class="text-center font-semibold">Mana Cost</div>
      <div class="text-center font-semibold">Type</div>
      <div class="text-center">{{ typeof card.cost !== 'undefined' ? card.cost : 'N/A' }}</div>
      <div class="text-center">{{ card.type || 'Unknown' }}</div>
    </div>

    <!-- Descrição exibida apenas no modo de filtro -->
    <p v-if="isFilterMode" class="text-sm text-black overflow-y-auto max-h-[120px] pr-2">
      {{ card.description || 'No description available' }}
    </p>

    <!-- Botões -->
    <div class="flex justify-between items-center text-black mt-auto gap-4">
      <div class="flex items-center space-x-2">
        <button 
          @click="$emit('remove-card', card.id)"
          :disabled="copiesInDeck === 0"
          class="w-12 h-12 bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50"
          aria-label="Remove card"
        >
          -
        </button>
        <span class="text-lg font-semibold" aria-live="polite">{{ copiesInDeck }}</span>
        <button 
          @click="$emit('add-card', card)"
          :disabled="copiesInDeck >= 4"
          class="w-12 h-12 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50"
          aria-label="Add card"
        >
          +
        </button>
      </div>
      <div class="text-lg font-semibold">
        {{ copiesInDeck }}/4
      </div>
    </div>

    <!-- Modal de Imagem Ampliada -->
    <div 
      v-if="openImage" 
      class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
      @click="openImage = false"
    >
      <div class="bg-white rounded p-6 max-w-lg shadow-lg flex flex-col items-center">
        <img 
          :src="card.image" 
          :alt="card.name || 'Unnamed Card'"
          class="w-full h-auto object-contain rounded mb-4"
        >
        <p class="text-sm text-black text-center">
          {{ card.description || 'No description available' }}
        </p>
        <button
          class="mt-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          @click="openImage = false"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Props recebidas
const props = defineProps({
  card: {
    type: Object,
    required: true,
  },
  copiesInDeck: {
    type: Number,
    default: 0,
  },
  isFilterMode: {
    type: Boolean,
    default: false, // Não exibir a descrição por padrão
  },
});

// Variáveis reativas
const imageError = ref(false);
const openImage = ref(false);

// Função para tratar erro de carregamento de imagem
const handleImageError = () => {
  imageError.value = true;
  console.warn(`Failed to load image for card: ${props.card.name}`);
};
</script>

<style scoped>
.bg-opacity-75 {
  backdrop-filter: blur(5px); /* Adiciona um leve desfoque ao fundo */
}
</style>