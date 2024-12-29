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

      <div class="print-content">
        <div class="preview-container">
          <!-- Back cards page -->
          <div class="back-cards-page grid grid-cols-2 gap-4 mb-8">
            <template v-for="i in 10" :key="`back-${i}`">
              <div class="card-back w-[6.3cm] h-[8.8cm]">
                <img :src="backCardUrl" alt="Card Back" class="w-full h-full object-contain">
              </div>
            </template>
          </div>

          <!-- Front cards page -->
          <div class="front-cards-page grid grid-cols-2 gap-4">
            <template v-for="(card, index) in cardsToDisplay" :key="`front-${index}`">
              <div class="card-front w-[6.3cm] h-[8.8cm]">
                <img :src="getCardImageUrl(card)" :alt="card.name" class="w-full h-full object-contain">
              </div>
            </template>
          </div>
        </div>
      </div>

      <div class="mt-6 flex justify-end space-x-4">
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
</template>

<script setup>
import { computed, ref } from 'vue'
import { jsPDF } from 'jspdf'

// Importar a imagem do verso da carta
import backCardImage from '/public/image/back-card.webp'

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

const cardsToDisplay = computed(() => {
  const processed = []
  for (const selectedCard of props.selectedCards) {
    const cardInfo = props.availableCards.find(c => c.id === selectedCard.id)
    if (cardInfo) {
      console.log('Card Info:', cardInfo) // Log para debug
      for (let i = 0; i < selectedCard.amount; i++) {
        processed.push(cardInfo)
      }
    }
  }
  return processed.slice(0, 10)
})

const getCardImageUrl = (card) => {
  if (!card) return ''
  // O caminho já vem com 'image/' do JSON, então só precisamos adicionar '/'
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
      console.error('Erro ao carregar imagem:', url, e)
      reject(e)
    }
    img.src = url
  })
}

const generatePDF = async () => {
  try {
    console.log('Iniciando geração do PDF...')
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })

    const cardWidth = 63
    const cardHeight = 88
    const margin = 10
    const spacing = 10

    try {
      console.log('Carregando imagem do verso...')
      // Usar a URL da imagem do verso importada
      const backImgUrl = await loadImage(backCardUrl.value)
      console.log('Imagem do verso carregada')
      
      // Página dos versos
      for (let i = 0; i < 10; i++) {
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

      // Nova página para as frentes
      pdf.addPage()

      console.log('Processando frentes das cartas...')
      // Adicionar frentes das cartas
      for (let i = 0; i < cardsToDisplay.value.length; i++) {
        const card = cardsToDisplay.value[i]
        const row = Math.floor(i / 2)
        const col = i % 2
        const x = margin + col * (cardWidth + spacing)
        const y = margin + row * (cardHeight + spacing)

        try {
          console.log(`Carregando imagem frontal ${i + 1}/${cardsToDisplay.value.length}:`, card.name)
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
          console.error('Erro ao carregar imagem frontal:', card.name, imgError)
          continue
        }
      }

      pdf.setProperties({
        title: 'Cards.pdf',
        subject: 'Card Deck',
        creator: 'MOP Card Printer',
        author: 'MOP',
        printScaling: 'none'
      })

      console.log('Gerando PDF...')
      // Em vez de abrir em uma nova janela, vamos fazer o download direto
      pdf.save('cards.pdf')
      
    } catch (imgError) {
      console.error('Erro ao processar imagens:', imgError)
      alert('Erro ao processar imagens. Por favor, tente novamente.')
    }
  } catch (error) {
    console.error('Erro ao gerar PDF:', error)
    alert('Erro ao gerar PDF. Por favor, tente novamente.')
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