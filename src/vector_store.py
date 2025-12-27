from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_vector_store(docs):
    texts = [d["text"] for d in docs]
    embeddings = model.encode(texts)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return index, texts