from app.knowledge_loader import carregar_documentos, dividir_documentos
from app.embeddings import gerar_embeddings
from app.vector_store import criar_indice


documentos = carregar_documentos()
chunks = dividir_documentos(documentos)

embeddings = gerar_embeddings(chunks)

indice = criar_indice(embeddings)

print(f"Total de chunks: {len(chunks)}")
print(f"Formato dos embeddings: {embeddings.shape}")
print(f"Total de vetores no FAISS: {indice.ntotal}")
print(f"Dimensão do índice: {indice.d}")