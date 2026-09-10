from dotenv import load_dotenv
from openai import OpenAI

from app.knowledge_loader import carregar_documentos, dividir_documentos
from app.embeddings import gerar_embeddings
from app.vector_store import criar_indice
from app.retriever import criar_retriever, buscar

load_dotenv()

documentos = carregar_documentos()
chunks = dividir_documentos(documentos)

embeddings = gerar_embeddings(chunks)

indice = criar_indice(embeddings)

retriever = criar_retriever(indice, chunks)


def responder(mensagem):
    resultados = buscar(retriever, mensagem, k=3)

    resposta = []

    for resultado in resultados:
        resposta.append(resultado["chunk"].page_content)

    return "\n\n".join(resposta)

