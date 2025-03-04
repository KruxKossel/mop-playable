import os
import json

'''
Script python para converter os JSONs das cartas em um array de JSON, isso pra ficar melhor de manipula-los.
'''

# Caminho para a pasta onde os arquivos JSON estão localizados
cards_folder = 'cards'
output_file = 'cards.json'

# Lista para armazenar os dados combinados
all_cards = []

# Percorre todos os arquivos na pasta cards
for filename in os.listdir(cards_folder):
    file_path = os.path.join(cards_folder, filename)

    # Verifica se o arquivo é um arquivo JSON
    if os.path.isfile(file_path) and filename.endswith('.json'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                card_data = json.load(file)  # Carrega os dados do arquivo JSON
                all_cards.append(card_data)  # Adiciona o objeto JSON à lista
        except Exception as e:
            print(f"Erro ao ler o arquivo {filename}: {e}")

# Salva o array combinado em um novo arquivo JSON
with open(output_file, 'w', encoding='utf-8') as output:
    json.dump(all_cards, output, ensure_ascii=False, indent=2)

print(f"Arquivo {output_file} gerado com sucesso!")
