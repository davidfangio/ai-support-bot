import faiss
import numpy as np


def criar_indice(embeddings):
    embeddings = np.asarray(embeddings).astype("float32")

    dimensao = embeddings.shape[1]

    indice = faiss.IndexFlatL2(dimensao)

    indice.add(embeddings)

    return indice