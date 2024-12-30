# Masters of Pwnage Playable

Este repositório tem como objetivo manter o código de uma aplicação web capaz de selecionar um conjunto de cartas de uma biblioteca em JSON, montar um baralho de cartas e criar arquivos PDF para serem impressos frente e verso com a imagem das cartas.

Todo o projeto será gerenciado através do Github, isso é: toda comunicação, milestones, releases etc.... Será inteiramente desenvolvido por voluntários e portanto Open source.

## MVP (Minimum viable product).
Não queremos uma aplicação 100% perfeita de começo, vamos seguir uma metodologia de startup e definir um Produto mínimo viável.



### Requisitos do MVP.

* [ ] Ser uma aplicação totalmente web, o mais leve possível e que possa ser utilizada via browser(Chrome/Firefox).

* [ ] Permitir que o usuário filtre as cartas por: Nome, tipo e custo de mana.
* [ ] Permitir que o usuário selecione a carta e envie para um "Deck".
* [ ] Permitir que o usuário analise o deck de cartas, adicionando e removendo cartas, cada deck só pode conter no máximo 60 cartas e no máximo 4 de cada tipo.
* [ ] Permitir que uma vez que o deck esteja definido o usuário possa salvar um arquivo .json com Deck que ele definiu.
* [ ] Permitir que o usuário imprima o deck dele.
    * [ ] A aplicação deverá colocar a página em portrait mode, e colocar 10 fundos de cartas igualmente espaçados,
    * [ ] Na página seguinte a aplicação deverá colocar 10 cartas selecionadas no deck, igualmente espaçadas de forma que ao imprimir frente e verso as cartas fiquem alinhadas.
* [ ] Primeira versão no ar até 01/12/2024. (14 dias antes da H2HC)

## Como contribuir:

1. Faça um fork desse repositório
2. Escolha uma única tarefa/issue para fazer, commit o código no seu repositório e faça um Pull-request para o repositório principal.
2.1 Caso seja uma modificação cosmética, adicione um printscreen explicando a modificação.
3. Todo o código será em Inglês, não por elitismo, mas porque é uma oportunidade para que todos possamos aprender.
4. Toda comunicação pode ser feita em Português mesmo, através de issues, comentários e pull-requests.
5. Seja cordial com o amigo, estamos todos aqui para aprender.

## Techstack
1. Tailwind for CSS.
2. Basic HTML
3. Javascript to be defined (SvelteKit/React)
4. Hosted in Github Pages

## Instalação e Execução

Para rodar o projeto localmente, siga os passos abaixo:

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/masters-of-pwnage-mop-playable.git
cd masters-of-pwnage-mop-playable
```

2. Instale as dependências:
```bash
npm install
```

3. Execute o projeto em modo de desenvolvimento:
```bash
npm run dev
```

4. Para gerar a build de produção:
```bash
npm run build
```

5. Para visualizar a build de produção:
```bash
npm run preview
```

## Arquitetura do Projeto

O projeto é uma aplicação web desenvolvida com Vue.js 3 e Tailwind CSS, utilizando Vite como bundler. Abaixo está a estrutura de arquivos e suas funções:

### Estrutura de Diretórios

```
├── cards/              # Contém os arquivos JSON das cartas do jogo
├── decks/              # Armazena os decks salvos em formato JSON
├── images/             # Imagens das cartas e assets do projeto
├── public/             # Arquivos públicos estáticos
├── src/                # Código fonte da aplicação
│   ├── components/     # Componentes Vue reutilizáveis
│   └── App.vue         # Componente principal da aplicação
└── vite.config.js      # Configuração do Vite
```

### Principais Arquivos

- `src/App.vue`: Componente principal que gerencia o construtor de decks, incluindo:
  - Formulário de informações do deck
  - Sistema de filtragem de cartas
  - Gerenciamento do deck (adicionar/remover cartas)
  - Exportação e importação de decks

- `package.json`: Gerencia as dependências e scripts do projeto, incluindo:
  - Vue.js 3 como framework principal
  - Tailwind CSS para estilização
  - Heroicons para ícones
  - UUID para geração de IDs únicos

- `tailwind.config.js`: Configuração do Tailwind CSS para estilização

- `vite.config.js`: Configuração do bundler Vite, responsável pelo build e desenvolvimento

- `cards/*.json`: Arquivos JSON contendo as informações das cartas do jogo

- `fix.py` e `make_files.py`: Scripts Python auxiliares para manipulação de arquivos

### Tecnologias Utilizadas

- **Vue.js 3**: Framework JavaScript para construção da interface
- **Tailwind CSS**: Framework CSS para estilização
- **Vite**: Build tool e dev server
- **Node.js**: Ambiente de execução JavaScript

### Scripts Python

O projeto possui dois scripts Python que precisam ser executados ao configurar o projeto pela primeira vez ou quando houver alterações nas cartas:

1. `make_files.py`: 
   - Combina todos os arquivos JSON da pasta `cards/` em um único arquivo `public/cards.json`
   - Copia as imagens da pasta `images/` para `public/image/`
   - Execute com: `python make_files.py`

2. `fix.py`:
   - Atualiza os caminhos das imagens nos arquivos JSON das cartas
   - Tenta encontrar correspondências entre os nomes dos arquivos de imagem
   - Execute com: `python fix.py`

### Variáveis de Ambiente

Este projeto não requer nenhum arquivo `.env` ou variáveis de ambiente para funcionar. Todas as configurações necessárias já estão incluídas nos arquivos do projeto.

### Primeira Execução

Para rodar o projeto pela primeira vez, siga esta ordem:

1. Clone o repositório e instale as dependências conforme instruções acima
2. Execute os scripts Python para preparar os arquivos:
```bash
python make_files.py
python fix.py
```
3. Inicie o servidor de desenvolvimento:
```bash
npm run dev
```