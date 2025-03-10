<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center py-8">
    <div class="bg-white rounded-lg max-w-4xl w-full h-[calc(100vh-4rem)] p-6 flex flex-col">
      <div class="flex justify-between items-center mb-2">
        <h2 class="text-xl font-semibold">Print Preview</h2>
        <div class="text-center text-gray-500">
          Page {{ currentPage + 1 }} of {{ previewPages.length }}
        </div>
        <button 
          @click="$emit('close')"
          class="text-gray-500 hover:text-gray-700"
        >
          ✕
        </button>
      </div>

      <div class="flex-grow relative flex items-center justify-center overflow-hidden min-h-0">
        <!-- Navigation buttons -->
        <button 
          v-if="currentPage > 0"
          @click="currentPage--"
          class="absolute left-2 top-1/2 transform -translate-y-1/2 bg-gray-100 text-gray-800 rounded-full p-2 shadow-lg hover:bg-gray-200 z-10"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <button 
          v-if="currentPage < previewPages.length - 1"
          @click="currentPage++"
          class="absolute right-2 top-1/2 transform -translate-y-1/2 bg-gray-100 text-gray-800 rounded-full p-2 shadow-lg hover:bg-gray-200 z-10"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>

        <!-- Cards Container -->
        <div class="preview-container h-full w-full flex items-center justify-center px-16 overflow-hidden">
          <!-- Back cards page -->
          <div v-if="currentPage % 2 === 0" class="back-cards-page grid grid-cols-2 gap-4 h-full">
            <template v-for="card in previewPages[currentPage]" :key="card.id">
              <div class="card-back aspect-[63/88] max-h-[calc((100vh-20rem)/3)]">
                <img :src="backCardUrl" alt="Card Back" class="w-full h-full object-contain">
              </div>
            </template>
          </div>

          <!-- Front cards page -->
          <div v-else class="front-cards-page grid grid-cols-2 gap-4 h-full">
            <template v-for="card in previewPages[currentPage]" :key="card.id">
              <div class="card-front aspect-[63/88] max-h-[calc((100vh-20rem)/3)]">
                <img :src="getCardImageUrl(card)" :alt="card.name" class="w-full h-full object-contain">
              </div>
            </template>
          </div>
        </div>
      </div>

      <div class="mt-6 flex justify-between items-center">
        <div class="flex space-x-2">
          <button 
            v-for="pageIdx in previewPages.length" 
            :key="pageIdx"
            @click="currentPage = pageIdx - 1"
            :class="[
              'w-2 h-2 rounded-full',
              currentPage === pageIdx - 1 ? 'bg-blue-500' : 'bg-gray-300'
            ]"
          />
        </div>

        <div class="flex space-x-4">
          <button 
            @click="$emit('close')"
            class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
          >
            Cancel
          </button>
          <button 
            @click="generatePDF"
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Print
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { jsPDF } from 'jspdf'

// Import the back card image
import backCardImage from '/image/back-card.webp'

const props = defineProps({
  selectedCards: {
    type: Array,
    required: true
  },
  availableCards: {
    type: Array,
    required: true
  }
})

const backCardUrl = ref(backCardImage)
const currentPage = ref(0)

const allSelectedCards = computed(() => {
  const processed = []
  for (const selectedCard of props.selectedCards) {
    const cardInfo = props.availableCards.find(c => c.id === selectedCard.id)
    if (cardInfo) {
      for (let i = 0; i < selectedCard.amount; i++) {
        processed.push(cardInfo)
      }
    }
  }
  return processed
})

// Organize cards into pages of 6 for preview
const previewPages = computed(() => {
  const cards = allSelectedCards.value
  const pages = []
  const cardsPerPage = 6

  // Create back pages
  for (let i = 0; i < cards.length; i += cardsPerPage) {
    const pageCards = cards.slice(i, i + cardsPerPage)
    pages.push(pageCards) // Back page
    pages.push(pageCards) // Corresponding front page
  }

  return pages
})

const getCardImageUrl = (card) => {
  if (!card) return ''
  return `${card.image}`
}

const loadImage = (url) => {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.crossOrigin = 'Anonymous'
    img.onload = () => {
      const canvas = document.createElement('canvas')
      canvas.width = img.width
      canvas.height = img.height
      const ctx = canvas.getContext('2d')
      ctx.drawImage(img, 0, 0)
      
      try {
        const dataUrl = canvas.toDataURL('image/png')
        resolve(dataUrl)
      } catch (e) {
        reject(e)
      }
    }
    img.onerror = (e) => {
      console.error('Error loading image:', url, e)
      reject(e)
    }
    img.src = url
  })
}

const generatePDF = async () => {
  try {
    console.log('Starting PDF generation...')
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })

    const cardWidth = 63
    const cardHeight = 88
    const margin = 10
    const spacing = 10
    const cardsPerPage = 6

    try {
      console.log('Loading back card image...')
      const backImgUrl = await loadImage(backCardUrl.value)
      console.log('Back card image loaded')
      
      // Process cards alternating between back and front
      const cards = allSelectedCards.value
      const totalPages = Math.ceil(cards.length / cardsPerPage)

      for (let pageNum = 0; pageNum < totalPages; pageNum++) {
        // Start and end index for this set of cards
        const startIdx = pageNum * cardsPerPage
        const endIdx = Math.min(startIdx + cardsPerPage, cards.length)
        const pageCards = cards.slice(startIdx, endIdx)

        // Back page (odd pages: 1, 3, 5...)
        console.log(`Processing backs for cards ${startIdx + 1} to ${endIdx}`)
        for (let i = 0; i < pageCards.length; i++) {
          const row = Math.floor(i / 2)
          const col = i % 2
          const x = margin + col * (cardWidth + spacing)
          const y = margin + row * (cardHeight + spacing)
          
          pdf.addImage(
            backImgUrl,
            'PNG',
            x,
            y,
            cardWidth,
            cardHeight
          )
        }

        // Add new page for fronts
        pdf.addPage()

        // Front page (even pages: 2, 4, 6...)
        console.log(`Processing fronts for cards ${startIdx + 1} to ${endIdx}`)
        for (let i = 0; i < pageCards.length; i++) {
          const card = pageCards[i]
          const row = Math.floor(i / 2)
          const col = i % 2
          const x = margin + col * (cardWidth + spacing)
          const y = margin + row * (cardHeight + spacing)

          try {
            console.log(`Loading front image ${startIdx + i + 1}/${cards.length}:`, card.name)
            const frontImgUrl = await loadImage(getCardImageUrl(card))
            pdf.addImage(
              frontImgUrl,
              'PNG',
              x,
              y,
              cardWidth,
              cardHeight
            )
          } catch (imgError) {
            console.error('Error loading front image:', card.name, imgError)
            continue
          }
        }

        // Add new page for the next set (except on the last iteration)
        if (pageNum < totalPages - 1) {
          pdf.addPage()
        }
      }

      pdf.setProperties({
        title: 'Cards.pdf',
        subject: 'Card Deck',
        creator: 'MOP Card Printer',
        author: 'MOP',
        printScaling: 'none'
      })

      console.log('Generating PDF...')
      pdf.save('cards.pdf')
      
    } catch (imgError) {
      console.error('Error processing images:', imgError)
      alert('Error processing images. Please try again.')
    }
  } catch (error) {
    console.error('Error generating PDF:', error)
    alert('Error generating PDF. Please try again.')
  }
}

</script>

<style>
.preview-container {
  max-width: 210mm;
  margin: 0 auto;
  background: white;
  padding: 1cm;
}

.card-back img,
.card-front img {
  object-fit: contain;
  width: 100%;
  height: 100%;
}

@media print {
  .preview-container {
    padding: 1cm;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    justify-items: center;
    align-items: center;
  }

  .card-back,
  .card-front {
    width: 6.3cm;
    height: 8.8cm;
    margin: 0;
    padding: 0;
  }
}
</style>
