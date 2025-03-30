<template>
  <!-- Componente principal do resumo do deck -->
  <div class="bg-slate-300 rounded-lg shadow-md p-6">
    <!-- Título do Resumo do Deck -->
    <h2 class="text-xl font-semibold mb-4 text-gray-800">Deck Summary</h2>
    
    <!-- Informações do Deck -->
    <div class="mb-4">
      <div class="text-lg  text-gray-600 font-medium">{{ deckInfo.name || 'Unnamed Deck' }}</div>
      <div class="text-sm text-gray-600">by {{ deckInfo.author || 'Anonymous' }}</div>
    </div>

    <!-- Barra de Progresso do Total de Cartas -->
    <div class="mb-6">
      <div class="flex justify-between mb-2 text-gray-800">
        <span>Total Cards:</span>
        <span class="font-medium">{{ totalCards }}/60</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div 
          class="bg-purple-700 rounded-full h-2 transition-all"
          :style="{ width: `${(totalCards / 60) * 100}%` }"
        ></div>
      </div>
    </div>

    <!-- Botões de Ação -->
    <div class="space-y-4">
      <button 
        @click="$emit('export-deck')" 
        class="w-full py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        aria-label="Export Deck"
      >
        Export Deck
      </button>
      
      <button 
        @click="$emit('import-deck')" 
        class="w-full py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
        aria-label="Import Deck"
      >
        Import Deck
      </button>
      
      <button 
        @click="$emit('print-deck')" 
        class="w-full py-2 bg-green-500 text-white rounded hover:bg-green-600"
        aria-label="Print Deck"
      >
        Print Cards
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

// Props recebidas do componente pai
defineProps({
  deckInfo: {
    type: Object,
    required: true,
    default: () => ({ name: 'Unnamed Deck', author: 'Anonymous' }), // Valores padrão
  },
  totalCards: {
    type: Number,
    required: true,
    default: 0, // Valor padrão caso não seja passado
  },
});
</script>

<style scoped>
/* Estilos adicionais para melhorar aparência e acessibilidade */
.bg-blue-500:hover {
  transition: background-color 0.3s ease-in-out;
}
.bg-yellow-500:hover {
  transition: background-color 0.3s ease-in-out;
}
.bg-green-500:hover {
  transition: background-color 0.3s ease-in-out;
}
</style>