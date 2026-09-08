from sentence_transformers import SentenceTransformer


modelo = SentenceTransformer("all-MiniLM-L6-v2")

texto = "Quero trocar meu produto."

embedding = modelo.encode(texto)

print(f"Tipo: {type(embedding)}")
print(f"Dimensões: {embedding.shape}")
print(f"Primeiros valores: {embedding[:10]}")