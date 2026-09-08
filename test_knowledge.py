from app.knowledge_loader import carregar_documentos, dividir_documentos


documentos = carregar_documentos()
chunks = dividir_documentos(documentos)


print(f"Total de páginas: {len(documentos)}")
print(f"Total de chunks: {len(chunks)}")

tamanhos = [len(chunk.page_content) for chunk in chunks]

print(f"Tamanho mínimo: {min(tamanhos)} caracteres")
print(f"Tamanho máximo: {max(tamanhos)} caracteres")
print(f"Tamanho médio: {sum(tamanhos) / len(tamanhos):.0f} caracteres")

vazios = [chunk for chunk in chunks if not chunk.page_content.strip()]
pequenos = [chunk for chunk in chunks if len(chunk.page_content.strip()) < 100]

print(f"Chunks vazios: {len(vazios)}")
print(f"Chunks com menos de 100 caracteres: {len(pequenos)}")


print("\n--- EXEMPLO DE CHUNK 1 ---")
print(chunks[0].page_content[:500])

print("\n--- EXEMPLO DE CHUNK DO MEIO ---")
meio = len(chunks) // 2
print(chunks[meio].page_content[:500])

print("\n--- EXEMPLO DE CHUNK FINAL ---")
print(chunks[-1].page_content[:500])