<template>
   <div class="min-h-screen bg-gray-900 text-white p-8">
     <!-- Filtros de Busca -->
     <div class="mb-8 bg-gray-800 p-6 rounded-lg shadow-lg">
       <h2 class="text-2xl font-bold mb-4 text-gray-200">Buscar Cartas</h2>
       <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
         <input
             v-model="filters.name"
           placeholder="Buscar por nome"
           class="p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
         />
         <input
             v-model="filters.cost"
           placeholder="Buscar por custo"
           class="p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
         />
         <input
             v-model="filters.type"
           placeholder="Buscar por tipo"
           class="p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
         />
         <input
             v-model="filters.edition"
           placeholder="Buscar por edição"
           class="p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
         />
         <input
             v-model="filters.description"
           placeholder="Buscar na descrição"
           class="p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
         />
       </div>
     </div>
 
     <!-- Card Destaque -->
     <div class="bg-gray-800 rounded-lg shadow-lg p-6 mb-8 text-center">
       <h2 class="text-xl font-bold mb-4 text-blue-400">Carta em Destaque</h2>
       <div v-if="filteredCards.length > 0">
         <img
             :src="getCardImage(filteredCards[0].image)"
           :alt="filteredCards[0].name"
           class="w-48 h-64 mx-auto object-cover rounded-lg border-4 border-blue-500 shadow-lg mb-4"
         />
         <h3 class="text-2xl font-bold text-white">{{ filteredCards[0].name }}</h3>
         <p class="text-gray-400">{{ filteredCards[0].type }}</p>
         <p class="text-gray-300 text-sm mt-2">{{ filteredCards[0].description }}</p>
         <button
           @click="addToDeck(filteredCards[0])"
           :disabled="!canAddCard(filteredCards[0])"
           class="mt-4 w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 disabled:bg-gray-700"
         >
           Adicionar ao Deck
         </button>
       </div>
       <div v-else class="text-center text-gray-500">Nenhuma carta encontrada.</div>
     </div>
 
     <!-- Lista de Cartas -->
     <div v-if="filteredCards.length >= 2" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
       <div
         v-for="(card, index) in filteredCards.slice(1)"
         :key="card.id || index"
         class="bg-gray-700 p-4 rounded-lg shadow hover:bg-gray-600 transition-all duration-200 ease-in-out"
       >
         <img
           :src="getCardImage(card.image)"
           :alt="card.name"
           class="w-32 h-40 object-cover rounded mb-2 mx-auto"
         />
         <h4 class="text-white font-bold text-center">{{ card.name }}</h4>
         <p class="text-sm text-gray-400 text-center">{{ card.cost }}</p>
         <button
           @click="addToDeck(card)"
           :disabled="!canAddCard(card)"
           class="mt-2 w-full bg-blue-500 text-white py-1 rounded hover:bg-blue-600 disabled:bg-gray-600"
         >
           Adicionar
         </button>
       </div>
     </div>
     <div v-else class="text-center text-gray-500">
       Nenhuma carta adicional encontrada.
     </div>
 
     <!-- Deck Atual -->
     <div class="mt-8 bg-gray-800 p-6 rounded-lg shadow-lg">
       <h2 class="text-2xl font-bold mb-4 text-blue-400">
         Deck Atual ({{ currentDeck.length }}/60)
       </h2>
       <div class="grid grid-cols-1 gap-4">
         <div
           v-for="(card, index) in currentDeck"
           :key="index"
           class="flex justify-between items-center bg-gray-700 p-2 rounded"
         >
           <div>
             <span class="font-bold text-white">{{ card.name }}</span>
             <span class="text-gray-400 text-sm ml-2">{{ card.cost }}</span>
           </div>
           <button
             @click="removeFromDeck(index)"
             class="text-red-400 hover:text-red-500"
           >
             Remover
           </button>
         </div>
       </div>
     </div>
   </div>
 </template>
 
 <script>
 export default {
   name: 'CardDeckSelector',
   data() {
     return {
       cards: [], // Todas as cartas carregadas
       currentDeck: [], // Deck atual
       filters: {
         name: '',
         cost: '',
         type: '',
         edition: '',
         description: ''
       }
     };
   },
   computed: {
     filteredCards() {
       return this.cards.filter(card => {
         const nameMatch = card.name.toLowerCase().includes(this.filters.name.toLowerCase());
         const costMatch = card.cost.toLowerCase().includes(this.filters.cost.toLowerCase());
         const typeMatch = card.type.toLowerCase().includes(this.filters.type.toLowerCase());
         const editionMatch = card.edition.toLowerCase().includes(this.filters.edition.toLowerCase());
         const descriptionMatch = card.description.toLowerCase().includes(this.filters.description.toLowerCase());
         return nameMatch && costMatch && typeMatch && editionMatch && descriptionMatch;
       });
     }
   },
   methods: {
     getCardImage(image) {
       try {
         return `${import.meta.env.BASE_URL}images/${image}`;
       } catch {
         return '/default-placeholder.webp';
       }
     },
     canAddCard(card) {
       if (this.currentDeck.length >= 60) return false;
       const cardCount = this.currentDeck.filter(c => c.name === card.name).length;
       return cardCount < 4;
     },
     addToDeck(card) {
       if (this.canAddCard(card)) {
         this.currentDeck.push(card);
         console.log(this.currentDeck);
       }
     },
     removeFromDeck(index) {
       this.currentDeck.splice(index, 1);
     }
   },
   mounted() {
     fetch(`${import.meta.env.BASE_URL}cards.json`)
       .then(response => response.json())
       .then(data => {
         this.cards = [...data.cards]; // Garante reatividade
       })
       .catch(error => console.error("Erro ao carregar o JSON:", error));
   }
 };
 </script>
