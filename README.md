# 🤖 AI Support Bot — Robbie

Assistente virtual inteligente para atendimento ao cliente, desenvolvido como projeto de portfólio utilizando **Flask, RAG, embeddings, FAISS e OpenAI**.

O projeto simula o atendimento de uma loja virtual fictícia chamada **NovaShop**, permitindo que o Robbie responda perguntas com base em uma base de conhecimento específica da empresa, mantendo regras de comportamento e utilizando memória de conversa.

## 🚀 Demonstração

**Robbie online:**
https://ai-support-bot-production-8bdc.up.railway.app

O projeto está hospedado em produção utilizando **Railway**.

> A NovaShop é uma empresa fictícia criada exclusivamente para fins educacionais e de demonstração.

---

## 🎯 Objetivo

O objetivo do projeto é demonstrar a construção de um sistema de atendimento com IA capaz de:

* consultar uma base de conhecimento;
* recuperar informações semanticamente relevantes;
* utilizar contexto para gerar respostas;
* manter memória de conversa;
* seguir regras comportamentais específicas;
* evitar a invenção de informações;
* identificar situações que exigem atendimento humano;
* lidar com entradas inválidas;
* funcionar através de uma interface web;
* ser executado em ambiente de produção.

---

## 🧠 Arquitetura

```text
Cliente
   ↓
Interface Web
   ↓
POST /chat
   ↓
Flask
   ↓
responder()
   ↓
Retriever
   ↓
FAISS + Embeddings
   ↓
Contexto relevante
   ↓
Cérebro do Robbie
   ↓
Histórico da conversa
   ↓
Prompt
   ↓
OpenAI
   ↓
Resposta do Robbie
```

---

## 🔎 RAG — Retrieval-Augmented Generation

O Robbie não depende apenas do conhecimento geral do modelo.

Antes de gerar uma resposta, o sistema:

1. carrega os documentos da NovaShop;
2. limpa o conteúdo;
3. divide os documentos em chunks;
4. transforma os chunks em embeddings;
5. armazena os vetores em um índice FAISS;
6. transforma a pergunta do cliente em embedding;
7. recupera os trechos semanticamente mais relevantes;
8. combina esses trechos com o cérebro e o histórico da conversa;
9. envia o contexto para o modelo;
10. gera a resposta final.

Isso permite que o Robbie responda de acordo com as informações específicas da NovaShop.

---

## 🧩 Tecnologias

| Tecnologia              | Função                       |
| ----------------------- | ---------------------------- |
| Python                  | Linguagem principal          |
| Flask                   | API e aplicação web          |
| OpenAI API              | Geração das respostas        |
| LangChain               | Processamento dos documentos |
| Sentence Transformers   | Geração de embeddings        |
| FAISS                   | Busca vetorial               |
| NumPy                   | Manipulação numérica         |
| HTML / CSS / JavaScript | Interface                    |
| pytest                  | Testes automatizados         |
| Gunicorn                | Servidor de produção         |
| Railway                 | Deploy e hospedagem          |

---

## 📁 Estrutura do projeto

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
│   └── js/
│       └── chat.js
│
├── templates/
│   └── chat.html
│
├── tests/
│
├── run.py
├── requirements.txt
└── README.md
```

---

## 🧠 Cérebro do Robbie

O comportamento do Robbie é separado da lógica principal da aplicação.

O arquivo:

```text
knowledge/Cérebro_Robbie.txt
```

define regras relacionadas a:

* personalidade;
* tom de comunicação;
* limites de atuação;
* segurança;
* escalonamento para atendimento humano;
* tratamento de informações ausentes;
* regras de garantia;
* proteção de dados;
* situações em que Robbie não deve assumir que uma ação foi realizada.

Essa separação permite alterar o comportamento do assistente sem modificar a arquitetura principal da aplicação.

---

## 📚 Base de conhecimento

A base da NovaShop funciona como **Single Source of Truth** para as respostas do assistente.

O Robbie deve:

* utilizar as informações disponíveis na base;
* evitar inventar informações;
* deixar explícita a falta de informação quando necessário;
* não afirmar que realizou ações que não foram executadas;
* encaminhar situações que exigem intervenção humana.

A base de conhecimento é composta por:

```text
NovaShop_Base.txt
Cérebro_Robbie.txt
```

---

## 💬 Memória de conversa

O sistema utiliza um `conversation_id` para identificar uma conversa.

O histórico é armazenado durante a execução da aplicação e enviado novamente ao modelo como contexto.

Atualmente, o histórico mantém as últimas **10 entradas**, correspondendo aproximadamente a 5 interações completas entre cliente e Robbie.

### Limitação atual

A memória utiliza armazenamento em processo (`dict`) e, portanto:

* é perdida quando a aplicação reinicia;
* não é compartilhada entre múltiplas instâncias;
* não representa uma solução de persistência para produção em escala.

Uma evolução natural seria utilizar Redis ou um banco de dados.

---

## 🛡️ Validação e segurança

A API valida:

* ausência de mensagem;
* JSON inválido;
* mensagem vazia;
* tipo inválido;
* mensagens acima de 4000 caracteres;
* `conversation_id` inválido;
* isolamento entre conversas.

O frontend também utiliza sanitização de conteúdo antes de renderizar respostas formatadas.

Informações sensíveis, como senhas, CVV, números completos de cartão e códigos de autenticação, não devem ser solicitadas pelo assistente.

---

## 🧪 Testes

O projeto possui testes automatizados utilizando `pytest`.

Estado atual:

```text
12 passed
```

Os testes cobrem:

* validação de entrada;
* mensagens inválidas;
* mensagens válidas;
* criação de conversas;
* reutilização de histórico;
* isolamento de conversas;
* limite de histórico;
* carregamento da página inicial.

---

## ⚙️ Instalação local

Clone o repositório:

```bash
git clone https://github.com/davidfangio/ai-support-bot.git
cd ai-support-bot
```

Crie o ambiente virtual:

```bash
python3 -m venv .venv
```

Ative:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env`:

```text
OPENAI_API_KEY=sua_chave_aqui
```

Execute:

```bash
python run.py
```

A aplicação ficará disponível localmente em:

```text
http://127.0.0.1:5000
```

---

## 🚀 Deploy

O projeto está configurado para execução em produção utilizando **Gunicorn**:

```bash
gunicorn run:app
```

A aplicação está hospedada no Railway.

A versão de produção utiliza:

```text
Python 3.12
```

---

## ⚠️ Limitações atuais

O projeto é uma aplicação de portfólio e possui algumas limitações intencionais:

* memória armazenada apenas em processo;
* ausência de autenticação de usuários;
* ausência de banco de dados;
* ausência de integração com pedidos reais;
* ausência de ferramentas para consulta de estoque em tempo real;
* ausência de integração com sistemas de atendimento humano;
* índice vetorial reconstruído durante a inicialização;
* aplicação configurada para uma única instância.

Esses pontos representam possíveis evoluções futuras.

---

## 🔮 Possíveis evoluções

Entre as próximas evoluções possíveis estão:

* Redis para memória persistente;
* banco de dados para conversas;
* autenticação;
* painel administrativo;
* integração com pedidos;
* consulta de estoque em tempo real;
* integração com sistemas de atendimento;
* observabilidade e métricas;
* rate limiting;
* streaming de respostas;
* avaliação automática da qualidade do RAG;
* testes de integração;
* containerização com Docker.

---

## 🎓 Objetivo de portfólio

Este projeto foi desenvolvido para demonstrar conhecimentos em:

* desenvolvimento backend com Python;
* construção de APIs;
* integração com modelos de linguagem;
* RAG;
* embeddings;
* busca vetorial;
* engenharia de prompts;
* gerenciamento de contexto;
* memória conversacional;
* validação de entradas;
* testes automatizados;
* frontend básico;
* segurança;
* deploy de aplicações;
* arquitetura de software.

---

## 👨‍💻 Autor

**David Fangio**

Projeto desenvolvido como parte da construção de um portfólio profissional em desenvolvimento de software, dados e inteligência artificial.