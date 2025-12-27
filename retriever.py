from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "vector_store/faiss.index"
META_PATH = "vector_store/metadata.pkl"

def retrieve_docs(city, k=5):
    if not os.path.exists(INDEX_PATH):
        return []

    index = faiss.read_index(INDEX_PATH)
    metadata = pickle.load(open(META_PATH, "rb"))

    query = model.encode([f"{city} real estate infrastructure growth"])
    _, idxs = index.search(query, min(k * 3, len(metadata)))

    docs = []
    for i in idxs[0]:
        meta_city = metadata[i].get("city")
        if meta_city and meta_city.lower() == city.lower():
            docs.append(metadata[i])
            if len(docs) == k:
                break

    return docs