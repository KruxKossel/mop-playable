<template>
  <div class="bg-white rounded-lg shadow-md p-4 mb-6">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Name filter -->
      <div>
        <label class="block text-sm font-medium mb-1">Card Name</label>
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
        <label class="block text-sm font-medium mb-1">Mana Cost</label>
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
        <label class="block text-sm font-medium mb-1">Description</label>
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
      <label class="block text-sm font-medium mb-1">Card Type</label>
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

    <!-- Clear filters button -->
    <div class="mt-4 flex justify-end">
      <button
        @click="clearFilters"
        class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
      >
        Clear Filters
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

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

const toggleType = (type) => {
  const index = filters.value.types.indexOf(type)
  if (index === -1) {
    filters.value.types.push(type)
  } else {
    filters.value.types.splice(index, 1)
  }
  emitFilters()
}

const clearFilters = () => {
  filters.value = {
    name: '',
    costMin: null,
    costMax: null,
    description: '',
    types: []
  }
  emitFilters()
}

const emitFilters = () => {
  emit('filter', { ...filters.value })
}
</script>