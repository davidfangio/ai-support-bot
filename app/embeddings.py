from sentence_transformers import SentenceTransformer


modelo = SentenceTransformer("all-MiniLM-L6-v2")


def gerar_embeddings(chunks):
    textos = [chunk.page_content for chunk in chunks]

    embeddings = modelo.encode(textos)

    return embeddings