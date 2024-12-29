<template>
  <div class="bg-white shadow-md p-4">
    
    <!-- Use default image if card.image is not available -->
    <div class="bg-gray-200 mb-4 mx-auto">
      <img 
        v-if="card.image"
        :src="card.image" 
        :alt="card.name"
        class="w-full h-full object-contain "
        @error="handleImageError"
      >
      <div v-else class="w-full h-full flex items-center justify-center text-gray-500">
        No Image
      </div>
    </div>
    
    <h3 class="text-lg font-semibold mb-2 text-black">{{ card.name || 'Unnamed Card' }}</h3>
    <div class="grid grid-cols-2 gap-2 mb-2 text-sm text-black">
      <div>{{ typeof card.cost !== 'undefined' ? card.cost : 'N/A' }}</div>
      <div>{{ card.type || 'Unknown' }}</div>
    </div>
    <p class="text-sm mb-4 text-black">{{ card.description || 'No description available' }}</p>
    <div class="flex justify-between items-center">
      <div class="flex items-center space-x-2">
        <button 
          @click="$emit('remove-card', card.id)"
          :disabled="copiesInDeck === 0"
          class="px-2 py-1 bg-red-500 text-white rounded disabled:opacity-50"
        >
          -
        </button>
        <span>{{ copiesInDeck }}</span>
        <button 
          @click="$emit('add-card', card)"
          :disabled="copiesInDeck >= 4"
          class="px-2 py-1 bg-green-500 text-white rounded disabled:opacity-50"
        >
          +
        </button>
      </div>
      <div class="text-sm">
        {{ copiesInDeck }}/4
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  card: {
    type: Object,
    required: true
  },
  copiesInDeck: {
    type: Number,
    default: 0
  }
})

const imageError = ref(false)

const handleImageError = () => {
  imageError.value = true
  console.error(`Failed to load image for card: ${props.card.name}`);
}
</script>