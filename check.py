import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Paths
INDEX_PATH = "vector_store/faiss.index"
META_PATH = "vector_store/metadata.pkl"

# Initialize model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
if not os.path.exists(INDEX_PATH):
    raise FileNotFoundError(f"FAISS index not found: {INDEX_PATH}")
index = faiss.read_index(INDEX_PATH)

# Load metadata
if not os.path.exists(META_PATH):
    raise FileNotFoundError(f"Metadata file not found: {META_PATH}")
with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)

if len(metadata) == 0:
    raise ValueError("Metadata is empty")

print(f"FAISS index has {index.ntotal} vectors")
print(f"Metadata has {len(metadata)} entries")

# Check that index size matches metadata length
if index.ntotal != len(metadata):
    print("[Warning] Number of vectors in FAISS index does not match metadata length!")

# Test retrieval for all supported cities
SUPPORTED_CITIES = ["Hyderabad", "Bengaluru", "Pune"]

for city in SUPPORTED_CITIES:
    query_vec = model.encode([f"{city} real estate infrastructure growth"]).astype("float32")
    k = min(5 * 3, len(metadata))
    _, idxs = index.search(query_vec, k)

    found = 0
    for i in idxs[0]:
        if i >= len(metadata):
            continue
        meta_city = metadata[i].get("city", "")
        if meta_city and city.lower() in meta_city.lower():
            found += 1
    print(f"City: {city}, Documents matching: {found}")