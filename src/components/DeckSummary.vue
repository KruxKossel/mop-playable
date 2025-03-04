<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-xl font-semibold mb-4 text-gray-800">Deck Summary</h2>
    
    <div class="mb-4">
      <div class="text-lg font-medium">{{ deckInfo.name || 'Unnamed Deck' }}</div>
      <div class="text-sm text-gray-600">by {{ deckInfo.author || 'Anonymous' }}</div>
    </div>

    <div class="mb-6">
      <div class="flex justify-between mb-2 text-gray-800">
        <span>Total Cards:</span>
        <span class="font-medium">{{ totalCards }}/60</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div 
          class="bg-blue-500 rounded-full h-2"
          :style="{ width: `${(totalCards / 60) * 100}%` }"
        ></div>
      </div>
    </div>

    <div class="space-y-4">
      <button 
        @click="$emit('export-deck')"
        class="w-full py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Export Deck
      </button>
      
      <button 
        @click="$emit('import-deck')"
        class="w-full py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
      >
        Import Deck
      </button>
      
      <button 
        @click="$emit('print-deck')"
        class="w-full py-2 bg-green-500 text-white rounded hover:bg-green-600"
      >
        Print Cards
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  deckInfo: {
    type: Object,
    required: true
  },
  totalCards: {
    type: Number,
    required: true
  }
})
</script>