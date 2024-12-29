<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-semibold">Print Preview</h2>
        <button 
          @click="$emit('close')"
          class="text-gray-500 hover:text-gray-700"
        >
          ✕
        </button>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-3 gap-4 print:grid-cols-3">
        <div 
          v-for="card in flattenedCards" 
          :key="`${card.id}-${card.index}`"
          class="bg-white rounded-lg shadow-md p-4 print:shadow-none"
        >
          <img :src="card.image" :alt="card.name" class="w-full h-48 object-cover rounded mb-2">
          <div class="text-sm font-medium">{{ card.name }}</div>
        </div>
      </div>

      <div class="mt-6 flex justify-end space-x-4 print:hidden">
        <button 
          @click="$emit('close')"
          class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
        >
          Cancel
        </button>
        <button 
          @click="print"
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Print
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  selectedCards: {
    type: Array,
    required: true
  }
})

const flattenedCards = computed(() => {
  return props.selectedCards.flatMap(card => {
    return Array(card.amount).fill().map((_, index) => ({
      ...card,
      index
    }))
  })
})

const print = () => {
  window.print()
}
</script>

<style>
@media print {
  @page {
    size: A4;
    margin: 1cm;
  }
  
  body * {
    visibility: hidden;
  }
  
  .print-preview-content,
  .print-preview-content * {
    visibility: visible;
  }
  
  .print-preview-content {
    position: absolute;
    left: 0;
    top: 0;
  }
}
</style>