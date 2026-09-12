from dotenv import load_dotenv
from openai import OpenAI
from app.brain import carregar_cerebro

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
cerebro = carregar_cerebro()

def montar_contexto(mensagem, resultados):
    contexto = []

    contexto.append("=== CÉREBRO DO ROBBIE ===")
    contexto.append(cerebro)

    contexto.append("\n=== INFORMAÇÕES DA NOVASHOP ===")

    for resultado in resultados:
        contexto.append(resultado["chunk"].page_content)

    contexto.append("\n=== PERGUNTA DO CLIENTE ===")
    contexto.append(mensagem)

    return "\n\n".join(contexto)


def responder(mensagem):
    resultados = buscar(retriever, mensagem, k=3)

    resposta = []

    for resultado in resultados:
        resposta.append(resultado["chunk"].page_content)

    return "\n\n".join(resposta)

