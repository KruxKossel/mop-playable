<template>
  <!-- Grade principal: 8 linhas com colunas dinâmicas -->
  <div class="grid auto-rows-min grid-cols-12 gap-4 container mx-auto px-4 py-8">

    <!-- App Header e Deck Information Section -->
    <section class="col-span-12 bg-slate-800 rounded-lg shadow-md p-3">
      <header class="flex items-center justify-center mb-3">
        <h1 class="text-2xl font-bold">Card Deck Builder</h1>
      </header>
      <div>
        <h2 class="text-lg font-semibold mb-3">Deck Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
          <!-- Deck Name -->
          <div>
            <label for="deckName" class="block text-sm font-medium mb-1">Deck Name</label>
            <input
              id="deckName"
              v-model="deckInfo.name"
              type="text"
              class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="Enter deck name"
              aria-label="Deck Name"
            >
          </div>

          <!-- Author -->
          <div>
            <label for="authorName" class="block text-sm font-medium mb-1">Author</label>
            <input
              id="authorName"
              v-model="deckInfo.author"
              type="text"
              class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="Enter author name"
              aria-label="Author Name"
            >
          </div>

          <!-- Author Social -->
          <div>
            <label for="authorSocial" class="block text-sm font-medium mb-1">Author Social</label>
            <input
              id="authorSocial"
              v-model="deckInfo.author_social"
              type="text"
              class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="Enter social media handle"
              aria-label="Author Social Media Handle"
            >
          </div>
        </div>

        <!-- Deck Summary -->
        <DeckSummary
        class="mt-4"
        :deck-info="deckInfo"
        :selected-cards="selectedCards"
        :total-cards="totalCards"
        @export-deck="exportDeck"
        @import-deck="importDeck"
        @print-deck="showPrintPreview = true"
      />
      </div>
    </section>

    <!-- Import Deck Modal -->
    <ImportDeckModal
      class="row-span-1 col-span-12"
      :isOpen="isModalOpen"
      @imported="handleImport"
      @close="isModalOpen = false"
    />

    <!-- Filter Bar e Filtered Cards List -->
    <section class="col-span-12 lg:col-span-4 bg-slate-800 p-3 rounded shadow">
      <FilterBar
        :available-types="availableTypes"
        :available-manas="availableManas"
        @filter="activeFilters = $event"
      />
      <div class="mt-4 bg-gray-100 p-2 rounded shadow max-h-[815px] overflow-y-auto">
        <h2 class="text-sm font-semibold mb-2">Filtered Cards</h2>
        <div v-if="filteredCards.length" class="grid grid-cols-1 sm:grid-cols-2 gap-2">
          <!-- Exibindo cartas no filtro -->
          <div
            v-for="card in filteredCards"
            :key="card.id"
            class="text-gray-800 p-2 border rounded shadow"
          >
            <h3 class="text-sm font-bold">{{ card.name }}</h3>
            <p class="text-xs">Mana Cost: {{ card.cost }}</p>
            <p class="text-xs">Type: {{ card.type }}</p>
            <p class="text-xs">Description: {{ card.description }}</p>
          </div>
        </div>
        <div v-else class="text-center text-gray-500">
          No cards found. Adjust your filters.
        </div>
      </div>
    </section>

    <!-- Card Browser -->
    <section class="col-span-12 lg:col-span-8 bg-slate-800 p-3 rounded shadow">
      <div class="flex justify-between items-center mb-3">
        <h2 class="text-lg font-semibold">Available Cards</h2>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <!-- Exibindo cartas no navegador sem descrição -->
        <CardDisplay
          v-for="card in paginatedCards"
          :key="card.id"
          :card="card"
          :copies-in-deck="getCardCopies(card.id)"
          :is-filter-mode="false" 
          @add-card="addCardToDeck"
          @remove-card="removeCardFromDeck"
        />
      </div>
      <div class="flex justify-between items-center mt-4">
        <button
          @click="prevPage"
          :disabled="currentPage === 1"
          class="px-3 py-2 bg-gray-300 rounded hover:bg-gray-400 disabled:opacity-50 text-xs"
        >
          Previous
        </button>
        <span class="text-xs">Page {{ currentPage }} of {{ totalPages }}</span>
        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="px-3 py-2 bg-gray-300 rounded hover:bg-gray-400 disabled:opacity-50 text-xs"
        >
          Next
        </button>
      </div>
    </section>

    <!-- Print Preview Modal -->
    <PrintPreview
      v-if="showPrintPreview"
      :selected-cards="selectedCards"
      :available-cards="availableCards"
      @close="showPrintPreview = false"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import CardDisplay from './components/CardDisplay.vue';
import DeckSummary from './components/DeckSummary.vue';
import PrintPreview from './components/PrintPreview.vue';
import FilterBar from './components/FilterBar.vue';
import ImportDeckModal from './components/ImportDeckModal.vue';

/**
 * Reactive States:
 * - availableCards: Lista de cartas disponíveis (carregadas via JSON).
 * - selectedCards: Lista de cartas selecionadas para o deck.
 * - showPrintPreview: Define se o modal de visualização de impressão está ativo.
 */
const availableCards = ref([]);
const selectedCards = ref([]);
const showPrintPreview = ref(false);

/**
 * Tipos disponíveis:
 * - Lista fixa de tipos para uso no filtro.
 */
 const availableTypes = ref([
  "Criatura",
  "Mágica Instantânea",
  "Encantamento",
  "Artefato",
  "Feitiço",
  "Terreno",
]);

const availableManas = ref([
  "{W}",
  "{U}",
  "{B}",
  "{R}",
  "{G}",
  "{C}",
]);

/**
 * Filtros ativos:
 * - Define os critérios de pesquisa para exibição de cartas (nome, custo, etc.).
 */
const activeFilters = ref({
  name: '',
  costMin: null,
  costMax: null,
  description: '',
  types: [],
  manas: [],
});

/**
 * Informações do Deck:
 * - Detalhes do deck atual, incluindo nome, autor, etc.
 */
const deckInfo = ref({
  id: crypto.randomUUID(),
  name: '',
  author: '',
  author_social: '',
});

/**
 * Computed: totalCards
 * - Calcula o total de cartas no deck.
 */
const totalCards = computed(() => {
  return selectedCards.value.reduce((total, card) => total + card.amount, 0)
})

/**
 * Paginação:
 * - Define o número de cartas por página e a página atual.
 */
const cardsPerPage = 8; // Limite fixo de cartas por página.
const currentPage = ref(1);

/**
 * Computed: Filtragem de Cartas
 * - Aplica os critérios de `activeFilters` à lista de `availableCards`.
 */
// Função para interpretar o custo de mana
const parseManaCost = (cost) => {
  if (!cost) return 0; // Retorna 0 para cartas sem custo de mana
  
  let totalCost = 0;
  
  // Encontra todos os padrões dentro de chaves {}
  const manaSymbols = cost.match(/\{[^}]+\}/g) || [];
  
  manaSymbols.forEach(symbol => {
    // Remove as chaves
    const manaType = symbol.replace(/[{}]/g, '');
    
    // Se for um número, adiciona esse valor
    if (/^\d+$/.test(manaType)) {
      totalCost += parseInt(manaType, 10);
    } 
    // Se for um símbolo de mana colorido ou incolor, adiciona 1
    else {
      totalCost += 1;
    }
  });
  
  return totalCost;
};

const filteredCards = computed(() => {
  return availableCards.value.filter((card) => {
    const matchesName = activeFilters.value.name
      ? card.name && card.name.toLowerCase().includes(activeFilters.value.name.toLowerCase())
      : true;

    const cardGenericCost = parseManaCost(card.cost);

    const matchesCost =
      (activeFilters.value.costMin === null || cardGenericCost >= activeFilters.value.costMin) &&
      (activeFilters.value.costMax === null || cardGenericCost <= activeFilters.value.costMax);

    const matchesDescription = activeFilters.value.description
      ? card.description && card.description.toLowerCase().includes(activeFilters.value.description.toLowerCase())
      : true;

    const matchesType =
      activeFilters.value.types.length > 0
        ? activeFilters.value.types.some(
            (filterType) => card.type && filterType && card.type.toLowerCase().includes(filterType.toLowerCase())
          )
        : true;
        
    const matchesMana =
      activeFilters.value.manas && activeFilters.value.manas.length > 0
        ? activeFilters.value.manas.every(
            (manaType) => card.cost && card.cost.includes(manaType)
          )
        : true;

    return matchesName && matchesCost && matchesDescription && matchesType && matchesMana;
  });
});


/**
 * Computed: Paginação
 * - Calcula as cartas exibidas na página atual.
 */
const paginatedCards = computed(() => {
  const startIdx = (currentPage.value - 1) * cardsPerPage;
  const endIdx = startIdx + cardsPerPage;
  return filteredCards.value.slice(startIdx, endIdx);
});

/**
 * Computed: Total de Páginas
 * - Calcula o número total de páginas baseado nas cartas filtradas.
 */
const totalPages = computed(() => {
  return Math.ceil(filteredCards.value.length / cardsPerPage);
});

/**
 * Função: Próxima Página
 * - Avança para a próxima página de cartas, caso possível.
 */
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

/**
 * Função: Página Anterior
 * - Retorna à página anterior de cartas, caso possível.
 */
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

/** 
 * Função: getCardCopies
 * - Obtém o número de cópias de uma carta no deck.
 * @param {string} cardId - ID da carta.
 * @returns {number} - Número de cópias da carta.
 */
 const getCardCopies = (cardId) => {
  const card = selectedCards.value.find((c) => c.id === cardId);
   return card ? card.amount : 0;
};

/** 
 * Função: addCardToDeck
 * - Adiciona uma carta ao deck, respeitando os limites de 60 cartas no total e 4 cópias por carta.
 * @param {object} card - Carta a ser adicionada.
 */
 const addCardToDeck = (card) => {
  if (totalCards.value >= 60) return;

  // Procura se a carta já existe no deck
  const existingCard = selectedCards.value.find((c) => c.id === card.id);

  if (existingCard) {
    if (existingCard.amount < 4) {
      // Incrementa a quantidade
      existingCard.amount++;
      // Força Vue a atualizar o estado
      selectedCards.value = [...selectedCards.value];
    }
  } else {
    // Adiciona uma nova carta ao deck
    selectedCards.value.push({
      id: card.id,
      name: card.name,
      description: card.description || 'No description available',
      amount: 1,
    });
   }
};

/** 
 * Função: removeCardFromDeck
 * - Remove uma cópia de uma carta do deck ou a exclui completamente, caso tenha apenas uma cópia.
 * @param {string} cardId - ID da carta a ser removida.
 */
 const removeCardFromDeck = (cardId) => {
  const index = selectedCards.value.findIndex((c) => c.id === cardId);
  if (index !== -1) {
    const card = selectedCards.value[index];
    if (card.amount > 1) {
      // Diminui a quantidade
      card.amount--;
      // Força Vue a atualizar o estado
      selectedCards.value = [...selectedCards.value];
    } else {
      // Remove completamente a carta
      selectedCards.value.splice(index, 1);
    }
  }
};

/**
 * Função: importDeck
 * - Abre o modal de importação de deck.
 */
const isModalOpen = ref(false);

const importDeck = () => {
  isModalOpen.value = true;
};

/**
 * Função: handleImport
 * - Processa um deck importado e atualiza o estado.
 * @param {object} deck - Deck importado.
 */
const handleImport = (deck) => {
  deckInfo.value.name = deck.name || '';
  deckInfo.value.author = deck.author || '';
  deckInfo.value.author_social = deck.author_social || '';
  selectedCards.value = deck.cards.map((card) => ({
    id: card.id,
    amount: card.amount || 0,
  }));
  isModalOpen.value = false;
};

/**
 * Função: exportDeck
 * - Exporta o deck atual como um arquivo JSON.
 */
const exportDeck = () => {
  const deckData = {
    ...deckInfo.value,
    cards: selectedCards.value,
  };

  const blob = new Blob([JSON.stringify(deckData, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${deckInfo.value.name.toLowerCase().replace(/\s+/g, '-')}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

/**
 * Carregamento de Cartas:
 * - Busca cartas de um arquivo JSON e atualiza o estado.
 */
fetch('cards.json')
  .then((response) => response.json())
  .then((data) => {
    availableCards.value = Array.isArray(data)
      ? data
      : Array.isArray(data.cards)
      ? data.cards
      : Object.values(data);
  })
  .catch((error) => {
    console.error('Failed to load cards:', error);
  });
</script>