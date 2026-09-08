from app.embeddings import gerar_embeddings


def criar_retriever(indice, chunks):
    return {
        "indice": indice,
        "chunks": chunks,
    }


def buscar(retriever, pergunta, k=3):
    indice = retriever["indice"]
    chunks = retriever["chunks"]

    embedding_pergunta = gerar_embeddings([
        type("Documento", (), {"page_content": pergunta})()
    ])

    distancias, indices = indice.search(embedding_pergunta, k)

    resultados = []

    for distancia, indice_chunk in zip(distancias[0], indices[0]):
        resultados.append({
            "chunk": chunks[indice_chunk],
            "distancia": float(distancia),
        })

    return resultados