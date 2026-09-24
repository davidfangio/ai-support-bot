# 🤖 AI Support Bot — Robbie

Assistente virtual inteligente desenvolvido para atendimento ao cliente da **NovaShop**, uma empresa fictícia de tecnologia criada para fins de demonstração e portfólio.

O projeto combina **Flask, Retrieval-Augmented Generation (RAG), embeddings, busca vetorial com FAISS e modelos da OpenAI** para criar um assistente capaz de responder perguntas com base em uma base de conhecimento controlada, mantendo também um histórico de conversa por sessão.

---

## 📌 Sobre o projeto

O Robbie foi desenvolvido com o objetivo de simular um sistema real de atendimento ao cliente utilizando Inteligência Artificial.

Em vez de depender exclusivamente do conhecimento geral de um modelo de linguagem, o sistema recupera informações relevantes da base de conhecimento da NovaShop e utiliza esse conteúdo como contexto para gerar a resposta.

Isso permite maior controle sobre as informações utilizadas pelo assistente e reduz o risco de respostas inventadas.

### Principais características

* 💬 Interface web de chat
* 🧠 Base de comportamento do Robbie
* 📚 Base de conhecimento da NovaShop
* 🔎 Retrieval-Augmented Generation (RAG)
* 🧩 Divisão da base em chunks
* 🔢 Geração de embeddings
* 🗂️ Busca vetorial com FAISS
* 🧠 Memória de conversação
* 🔐 Sanitização de conteúdo Markdown
* 🛡️ Validação de entradas
* ⚠️ Tratamento de erros da API
* 🧪 Testes automatizados com pytest

---

# 🏗️ Arquitetura

O fluxo principal do sistema funciona da seguinte maneira:

```text
                    ┌──────────────────┐
                    │     Cliente      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Interface Web   │
                    │ HTML / CSS / JS  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Flask / API    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Retriever     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      FAISS       │
                    │ Busca vetorial   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Contexto + RAG   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  OpenAI Model    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Robbie       │
                    └──────────────────┘
```

---

# 🧠 Como funciona o RAG

O Robbie não utiliza simplesmente a pergunta do cliente para gerar uma resposta.

Primeiro, a pergunta passa pelo processo de recuperação de informação.

### 1. Carregamento

A base de conhecimento da NovaShop é carregada pelo sistema.

### 2. Limpeza

O conteúdo é normalizado para reduzir espaços e quebras de linha desnecessárias.

### 3. Chunking

O conteúdo é dividido em partes menores utilizando `RecursiveCharacterTextSplitter`.

```text
Documento
    ↓
Seções
    ↓
Chunks
    ↓
Embeddings
```

O projeto utiliza:

* `chunk_size = 1000`
* `chunk_overlap = 200`

### 4. Embeddings

Cada chunk é transformado em uma representação vetorial utilizando:

```text
sentence-transformers
```

com o modelo:

```text
all-MiniLM-L6-v2
```

### 5. Busca vetorial

Os embeddings são armazenados em um índice FAISS.

Quando o cliente faz uma pergunta, ela também é transformada em embedding e comparada com os vetores existentes.

Os chunks mais relevantes são recuperados.

### 6. Construção do contexto

O sistema combina:

```text
Cérebro do Robbie
        +
Histórico da conversa
        +
Informações relevantes da NovaShop
        +
Pergunta atual
```

Esse contexto é enviado ao modelo de linguagem.

### 7. Geração da resposta

O modelo gera a resposta respeitando as regras definidas para o Robbie e utilizando as informações recuperadas.

---

# 🧩 Tecnologias

| Tecnologia            | Utilização                                    |
| --------------------- | --------------------------------------------- |
| Python                | Linguagem principal                           |
| Flask                 | Backend e API                                 |
| OpenAI API            | Geração das respostas                         |
| LangChain             | Processamento e divisão dos documentos        |
| Sentence Transformers | Geração de embeddings                         |
| FAISS                 | Busca vetorial                                |
| NumPy                 | Manipulação dos vetores                       |
| HTML                  | Estrutura da interface                        |
| CSS                   | Estilização                                   |
| JavaScript            | Comunicação com a API e comportamento do chat |
| pytest                | Testes automatizados                          |

---

# 📁 Estrutura do projeto

```text
ai-support-bot/
│
├── app/
│   ├── __init__.py
│   ├── brain.py
│   ├── chatbot.py
│   ├── embeddings.py
│   ├── knowledge_loader.py
│   ├── retriever.py
│   ├── routes.py
│   └── vector_store.py
│
├── knowledge/
│   ├── NovaShop_Base.txt
│   └── Cérebro_Robbie.txt
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── chat.js
│
├── templates/
│   └── chat.html
│
├── tests/
│   └── test_routes.py
│
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

> O arquivo `.env` contém configurações locais e não deve ser versionado.

---

# ⚙️ Instalação

Clone o repositório:

```bash
git clone https://github.com/davidfangio/ai-support-bot.git
```

Entre no diretório:

```bash
cd ai-support-bot
```

Crie um ambiente virtual:

```bash
python3 -m venv .venv
```

Ative o ambiente virtual:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

# 🔑 Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_aqui
```

A chave da API deve ser mantida em segredo e nunca deve ser publicada no GitHub.

---

# ▶️ Executando o projeto

Com o ambiente virtual ativado:

```bash
python run.py
```

O servidor Flask será iniciado localmente.

Abra o endereço informado pelo Flask no navegador para acessar a interface do Robbie.

---

# 🧪 Testes

O projeto possui testes automatizados para validar o comportamento da API.

Execute:

```bash
pytest
```

O conjunto atual possui **12 testes automatizados** cobrindo, entre outros pontos:

* mensagens ausentes;
* mensagens vazias;
* tipos inválidos;
* limite de caracteres;
* respostas válidas;
* criação de identificadores de conversa;
* reutilização do histórico;
* isolamento entre conversas;
* limite do histórico.

Resultado atual:

```text
12 passed
```

---

# 🛡️ Validações e tratamento de erros

A API possui algumas proteções básicas para evitar entradas inválidas.

Entre elas:

* validação do JSON recebido;
* validação do campo `mensagem`;
* rejeição de mensagens vazias;
* limite de 4000 caracteres;
* identificação de conversas;
* isolamento do histórico;
* tratamento de erros de conexão;
* tratamento de timeout;
* tratamento de limite de requisições;
* tratamento de autenticação da API.

O frontend também utiliza sanitização de HTML para reduzir riscos ao renderizar respostas em Markdown.

---

# 🧠 Memória de conversação

Cada conversa recebe um identificador:

```text
conversation_id
```

Esse identificador permite que o backend mantenha o histórico associado àquela conversa.

O histórico é limitado às últimas **10 entradas**, evitando crescimento indefinido da memória durante uma sessão.

A implementação atual utiliza memória em processo (`dict`), sendo adequada para demonstração e desenvolvimento, mas não para uma arquitetura distribuída de produção.

---

# ⚠️ Limitações atuais

Este projeto foi desenvolvido como demonstração técnica e projeto de portfólio.

Algumas limitações são intencionais:

* A memória das conversas é mantida apenas em memória.
* O histórico é perdido quando a aplicação é reiniciada.
* O sistema ainda não utiliza banco de dados.
* Não existe autenticação de usuários.
* O escalonamento para atendimento humano é representado pelas regras do assistente, não por uma integração real com uma equipe de suporte.
* O índice vetorial é criado durante a inicialização da aplicação.
* O projeto utiliza uma única instância do processo para manter o estado das conversas.

Esses pontos representam possíveis evoluções futuras.

---

# 🚀 Possíveis evoluções

Entre as próximas melhorias possíveis estão:

* Persistência de conversas em banco de dados.
* Autenticação de usuários.
* Sistema real de escalonamento para atendimento humano.
* Interface administrativa.
* Observabilidade e logging estruturado.
* Cache do índice vetorial.
* Pipeline separado para ingestão da base de conhecimento.
* Deploy com múltiplos workers.
* Streaming das respostas do modelo.
* Sistema de avaliação automática das respostas.
* Métricas de qualidade do RAG.

---

# 🎯 Objetivo do projeto

O objetivo principal deste projeto é demonstrar, de forma prática, a construção de uma aplicação de atendimento baseada em Inteligência Artificial utilizando técnicas modernas de recuperação de conhecimento e geração de linguagem.

Mais do que apenas integrar uma API de LLM, o projeto busca demonstrar conceitos como:

```text
Backend
   +
APIs
   +
RAG
   +
Embeddings
   +
Busca vetorial
   +
Memória
   +
Validação
   +
Testes
   +
Interface Web
```

---

# 📄 Observação

A **NovaShop** e o personagem **Robbie** são fictícios e foram criados exclusivamente para este projeto de demonstração e portfólio.

Nenhuma informação comercial apresentada pela NovaShop representa uma empresa real.

---

## 👨‍💻 Autor

**David Fangio**

Projeto desenvolvido como parte do portfólio de desenvolvimento e Ciência de Dados.