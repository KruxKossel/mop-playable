<template>
  <!-- Modal Overlay -->
  <div v-if="isOpen" class="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex justify-center items-center">
    <!-- Modal Content -->
    <div class="bg-white p-6 rounded shadow-lg text-center w-96">
      
      <!-- Input para Upload de Arquivo -->
      <input 
        type="file" 
        @change="handleFileUpload" 
        accept=".json" 
        class="mb-4 border border-gray-300 rounded px-2 py-1 w-full"
        aria-label="Upload a JSON file to import deck"
      />

      <!-- Mensagem de Erro -->
      <p v-if="error" class="text-red-500 text-sm mb-4">{{ error }}</p>

      <!-- Botões de Ação -->
      <div class="flex justify-between">
        <!-- Botão para Importar o Deck -->
        <button 
          @click="importDeck" 
          :disabled="isProcessing" 
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          aria-label="Import Deck"
        >
          {{ isProcessing ? 'Importing...' : 'Import' }}
        </button>

        <!-- Botão para Fechar/Cancelar -->
        <button 
          @click="closeModal" 
          class="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
          aria-label="Cancel"
        >
          Cancel
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Props recebidas do pai
defineProps({
  isOpen: {
    type: Boolean,
    required: true, // Define se o modal está aberto
  },
});

// Declaração dos eventos que o componente pode emitir
const emit = defineEmits(['imported', 'close']);

// Variáveis reativas para manipulação de estado
const file = ref(null); // Armazena o arquivo carregado
const error = ref(""); // Mensagem de erro exibida ao usuário
const isProcessing = ref(false); // Indica se a importação está em progresso

// Método para lidar com o upload do arquivo
const handleFileUpload = (event) => {
  file.value = event.target.files[0]; // Armazena o arquivo selecionado
  error.value = ""; // Reseta qualquer mensagem de erro
};

// Validações do conteúdo do arquivo
const validateFileContent = (json) => {
  if (
    !json.id || // O deck precisa de um ID
    !json.name || // O deck precisa de um nome
    !Array.isArray(json.cards) || // O deck precisa ser um array de cartas
    json.cards.length === 0 || // O deck não pode estar vazio
    json.cards.some(
      (card) =>
        !card.id || typeof card.amount !== "number" || card.amount <= 0 // Valida as cartas do deck
    )
  ) {
    throw new Error("Invalid file format."); // Lança um erro se as validações falharem
  }
};

// Método principal para importar o deck
const importDeck = async () => {
  if (!file.value) {
    error.value = "No file selected."; // Erro se nenhum arquivo for carregado
    return;
  }

  if (!file.value.name.endsWith(".json")) {
    error.value = "The file extension must be .json."; // Erro se o arquivo não for JSON
    return;
  }

  isProcessing.value = true; // Seta o estado de processamento

  try {
    const text = await file.value.text(); // Lê o conteúdo do arquivo como texto
    const json = JSON.parse(text); // Converte o texto para JSON

    validateFileContent(json); // Valida o conteúdo do JSON

    const validAmountValue = 60; // Limite de cartas no deck
    const totalAmount = json.cards.reduce(
      (total, card) => total + card.amount,
      0
    );

    if (totalAmount > validAmountValue) {
      throw new Error("The deck must have 60 cards or fewer."); // Erro se exceder o limite
    }

    // Emite o evento para enviar os dados do deck ao pai
    emit("imported", json);
    closeModal(); // Fecha o modal após a importação
  } catch (e) {
    error.value = "The file can't be processed: " + e.message; // Exibe a mensagem de erro
  } finally {
    isProcessing.value = false; // Reseta o estado de processamento
  }
};

// Método para fechar o modal
const closeModal = () => {
  emit("close"); // Emite o evento de fechamento
};
</script>