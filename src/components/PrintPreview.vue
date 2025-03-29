<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center py-8">
    <div class="bg-white rounded-lg max-w-4xl w-full h-[calc(100vh-4rem)] p-6 flex flex-col">
      <!-- Header -->
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Print Preview</h2>
        <div class="text-center text-gray-500">
          Page {{ currentPage + 1 }} of {{ previewPages.length }}
        </div>
        <button 
          @click="$emit('close')" 
          class="text-gray-500 hover:text-gray-700 focus:ring-2 focus:ring-gray-500"
          aria-label="Close Print Preview"
        >
          ✕
        </button>
      </div>

      <!-- Main Content -->
      <div class="flex-grow relative flex items-center justify-center overflow-hidden min-h-0">
        <!-- Navigation Buttons -->
        <button 
          v-if="currentPage > 0"
          @click="currentPage--"
          class="absolute left-2 top-1/2 transform -translate-y-1/2 bg-gray-100 text-gray-800 rounded-full p-2 shadow-lg hover:bg-gray-200 focus:ring-2 focus:ring-gray-500"
          aria-label="Go to previous page"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <button 
          v-if="currentPage < previewPages.length - 1"
          @click="currentPage++"
          class="absolute right-2 top-1/2 transform -translate-y-1/2 bg-gray-100 text-gray-800 rounded-full p-2 shadow-lg hover:bg-gray-200 focus:ring-2 focus:ring-gray-500"
          aria-label="Go to next page"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>

        <!-- Cards Container -->
        <div class="h-full w-full flex items-center justify-center px-16 bg-white max-w-[210mm] mx-auto py-[1cm]">
          <!-- Back Cards Page -->
          <div v-if="currentPage % 2 === 0" class="grid grid-cols-2 gap-4 h-full">
            <template v-for="card in previewPages[currentPage]" :key="card.id">
              <div class="aspect-[63/88] max-h-[calc((100vh-20rem)/3)] w-[6.3cm] h-[8.8cm]">
                <img :src="backCardUrl" alt="Card Back" class="w-full h-full object-contain">
              </div>
            </template>
          </div>

          <!-- Front Cards Page -->
          <div v-else class="grid grid-cols-2 gap-4 h-full">
            <template v-for="card in previewPages[currentPage]" :key="card.id">
              <div class="aspect-[63/88] max-h-[calc((100vh-20rem)/3)] w-[6.3cm] h-[8.8cm]">
                <img :src="getCardImageUrl(card)" :alt="card.name" class="w-full h-full object-contain">
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Footer Controls -->
      <div class="mt-6 flex justify-between items-center">
        <!-- Pagination Indicators -->
        <div class="flex space-x-2">
          <button 
            v-for="pageIdx in previewPages.length" 
            :key="pageIdx"
            @click="currentPage = pageIdx - 1"
            :class="[
              'w-3 h-3 rounded-full transition-all',
              currentPage === pageIdx - 1 ? 'bg-blue-500' : 'bg-gray-300 hover:bg-gray-400'
            ]"
            aria-label="Go to page {{ pageIdx }}"
          ></button>
        </div>

        <!-- Action Buttons -->
        <div class="flex space-x-4">
          <button 
            @click="$emit('close')" 
            class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 focus:ring-2 focus:ring-gray-500"
            aria-label="Cancel Print Preview"
          >
            Cancel
          </button>
          <button 
            @click="generatePDF" 
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:ring-2 focus:ring-blue-500"
            aria-label="Generate PDF for Printing"
          >
            Print
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { jsPDF } from 'jspdf';

// Import the back card image
import backCardImage from '/images/back-card.webp';

const props = defineProps({
  selectedCards: {
    type: Array,
    required: true,
  },
  availableCards: {
    type: Array,
    required: true,
  },
});

// Configurações ajustáveis
const CONFIG = {
  cardWidth: 63,
  cardHeight: 88,
  margin: 10,
  spacing: 10,
  cardsPerPage: 6,
};

// Reactive Data
const backCardUrl = ref(backCardImage);
const currentPage = ref(0);

// Computed: Process cards into individual copies
const allSelectedCards = computed(() => {
  const processed = [];
  for (const selectedCard of props.selectedCards) {
    const cardInfo = props.availableCards.find((c) => c.id === selectedCard.id);
    if (cardInfo) {
      for (let i = 0; i < selectedCard.amount; i++) {
        processed.push(cardInfo);
      }
    }
  }
  return processed;
});

// Computed: Organize cards into pages for preview
const previewPages = computed(() => {
  const cards = allSelectedCards.value;
  const pages = [];

  for (let i = 0; i < cards.length; i += CONFIG.cardsPerPage) {
    const pageCards = cards.slice(i, i + CONFIG.cardsPerPage);
    pages.push(pageCards); // Back page
    pages.push(pageCards); // Corresponding front page
  }

  return pages;
});

// Get card image URL
const getCardImageUrl = (card) => {
  return card ? card.image || '' : '';
};

// Load Image
const loadImage = (url) => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'Anonymous';
    img.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);

      try {
        const dataUrl = canvas.toDataURL('image/png');
        resolve(dataUrl);
      } catch (e) {
        reject(e);
      }
    };
    img.onerror = (e) => {
      console.error('Error loading image:', url, e);
      reject(e);
    };
    img.src = url;
  });
};

// Generate PDF
const generatePDF = async () => {
  try {
    console.log('Starting PDF generation...');
    if (!props.selectedCards || props.selectedCards.length === 0) {
      alert('No cards selected for printing.');
      return;
    }

    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4',
    });

    const { cardWidth, cardHeight, margin, spacing, cardsPerPage } = CONFIG;

    // Load back card image
    console.log('Loading back card image...');
    const backImgUrl = await loadImage(backCardUrl.value);
    console.log('Back card image loaded');

    const cards = allSelectedCards.value;
    const totalPages = Math.ceil(cards.length / cardsPerPage);

    for (let pageNum = 0; pageNum < totalPages; pageNum++) {
      const startIdx = pageNum * cardsPerPage;
      const endIdx = Math.min(startIdx + cardsPerPage, cards.length);
      const pageCards = cards.slice(startIdx, endIdx);

      console.group(`Processing page ${pageNum + 1} (Cards ${startIdx + 1} to ${endIdx})`);
      
      // Add backs
      console.log('Processing back page...');
      for (let i = 0; i < pageCards.length; i++) {
        const row = Math.floor(i / 2);
        const col = i % 2;
        const x = margin + col * (cardWidth + spacing);
        const y = margin + row * (cardHeight + spacing);

        pdf.addImage(backImgUrl, 'PNG', x, y, cardWidth, cardHeight);
      }

      // Add new page for fronts
      pdf.addPage();

      // Add fronts
      console.log('Processing front page...');
      for (let i = 0; i < pageCards.length; i++) {
        const card = pageCards[i];
        const row = Math.floor(i / 2);
        const col = i % 2;
        const x = margin + col * (cardWidth + spacing);
        const y = margin + row * (cardHeight + spacing);

        try {
          const frontImgUrl = await loadImage(getCardImageUrl(card));
          pdf.addImage(frontImgUrl, 'PNG', x, y, cardWidth, cardHeight);
        } catch (imgError) {
          console.error('Error loading front image:', card.name, imgError);
          alert(`Failed to load image for card: ${card.name}`);
        }
      }

      console.groupEnd();

      if (pageNum < totalPages - 1) {
        pdf.addPage();
      }
    }

    pdf.setProperties({
      title: 'Cards.pdf',
      subject: 'Card Deck',
      creator: 'MOP Card Printer',
      author: 'MOP',
      printScaling: 'none',
    });

    console.log('Saving PDF...');
    pdf.save('cards.pdf');
  } catch (error) {
    console.error('Error generating PDF:', error);
    alert('Error generating PDF. Please try again.');
  }
};
</script>


