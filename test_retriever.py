from app.knowledge_loader import carregar_documentos, dividir_documentos
from app.embeddings import gerar_embeddings
from app.vector_store import criar_indice
from app.retriever import criar_retriever, buscar


documentos = carregar_documentos()
chunks = dividir_documentos(documentos)

embeddings = gerar_embeddings(chunks)

indice = criar_indice(embeddings)

retriever = criar_retriever(indice, chunks)

pergunta = "Quero é o prazo para solicitar devolução por arrependimento?"

resultados = buscar(retriever, pergunta, k=3)

for i, resultado in enumerate(resultados, start=1):
    print(f"\n--- Resultado {i} ---")
    print(f"Distância: {resultado['distancia']}")
    print(resultado["chunk"].page_content)