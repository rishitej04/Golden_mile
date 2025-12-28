import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Initialize the SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Paths for FAISS index and metadata
INDEX_PATH = "vector_store/faiss.index"
META_PATH = "vector_store/metadata.pkl"

def retrieve_docs(city: str, k: int = 5):
    """
    Retrieve top-k documents relevant to a city using FAISS and SentenceTransformer.
    
    Args:
        city (str): City name to search for.
        k (int): Number of documents to return.

    Returns:
        List[dict]: List of metadata dicts for relevant documents.
    """
    # Check if index and metadata exist
    if not os.path.exists(INDEX_PATH):
        print(f"[Warning] FAISS index not found at {INDEX_PATH}")
        return []
    if not os.path.exists(META_PATH):
        print(f"[Warning] Metadata file not found at {META_PATH}")
        return []

    # Load index and metadata
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)

    if len(metadata) == 0:
        print("[Warning] Metadata is empty")
        return []

    # Encode query
    query_vec = model.encode([f"{city} real estate infrastructure growth"])
    query_vec = query_vec.astype("float32")  # FAISS requires float32

    # Perform FAISS search
    search_k = min(k * 3, len(metadata))
    _, idxs = index.search(query_vec, search_k)

    docs = []
    for i in idxs[0]:
        if i >= len(metadata):
            continue
        meta_city = metadata[i].get("city", "")
        if meta_city and city.lower() in meta_city.lower():  # partial match
            docs.append(metadata[i])
            if len(docs) == k:
                break

    print(f"[Info] Retrieved {len(docs)} documents for city: {city}")
    return docs