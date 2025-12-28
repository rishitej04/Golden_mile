import os
import json
import pickle
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss

# -----------------------------
# Paths
# -----------------------------
PDF_DIR = "data/pdfs"              # PDFs per city (folders: Hyderabad, Bengaluru, Pune)
TXT_DIR = "data/unstructured"      # .txt/.md files organized by city folder
CHUNKS_PATH = "data/processed/text_chunks.json"
VECTOR_DIR = "vector_store"
EMBED_PATH = os.path.join(VECTOR_DIR, "embeddings.npy")
META_PATH = os.path.join(VECTOR_DIR, "metadata.pkl")
FAISS_INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")

os.makedirs(VECTOR_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CHUNKS_PATH), exist_ok=True)

# -----------------------------
# Load PDFs
# -----------------------------
def load_pdfs(base_pdf_dir):
    docs = []
    for city in os.listdir(base_pdf_dir):
        city_path = os.path.join(base_pdf_dir, city)
        if not os.path.isdir(city_path):
            continue
        for file in os.listdir(city_path):
            if file.endswith(".pdf"):
                reader = PdfReader(os.path.join(city_path, file))
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                docs.append({
                    "city": city,
                    "source": file,
                    "text": text
                })
    return docs

# -----------------------------
# Load text files
# -----------------------------
def load_text_files(base_dir):
    docs = []
    for root, _, files in os.walk(base_dir):
        city = os.path.basename(root)  # infer city from folder name
        for file in files:
            if file.endswith(".txt") or file.endswith(".md"):
                full_path = os.path.join(root, file)
                with open(full_path, "r", encoding="utf-8") as f:
                    docs.append({
                        "city": city,  # assign city from folder
                        "source": os.path.relpath(full_path, base_dir),
                        "text": f.read()
                    })
    return docs

# -----------------------------
# Chunking function with optional overlap
# -----------------------------
def chunk_text(text, max_len=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunk = words[start:start+max_len]
        chunks.append(" ".join(chunk))
        start += max_len - overlap
    return chunks

# -----------------------------
# Main pipeline
# -----------------------------
if __name__ == "__main__":
    print("🔹 Loading PDFs and text files...")
    pdf_docs = load_pdfs(PDF_DIR)
    txt_docs = load_text_files(TXT_DIR)

    all_docs = pdf_docs + txt_docs
    print(f"📄 Total documents loaded: {len(all_docs)}")

    # -----------------------------
    # Split into chunks
    # -----------------------------
    chunks = []
    for doc in all_docs:
        for c in chunk_text(doc["text"]):
            chunks.append({
                "city": doc["city"],
                "source": doc["source"],
                "text": c
            })

    print(f"📝 Total chunks created: {len(chunks)}")

    # Save chunks JSON
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"✅ Chunks saved to {CHUNKS_PATH}")

    # -----------------------------
    # Create embeddings
    # -----------------------------
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [c["text"] for c in chunks]
    print("🔹 Encoding embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")  # Ensure float32

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    # Save embeddings
    np.save(EMBED_PATH, embeddings)

    # -----------------------------
    # Build FAISS index
    # -----------------------------
    index = faiss.IndexFlatIP(embeddings.shape[1])  # Cosine similarity
    index.add(embeddings)
    faiss.write_index(index, FAISS_INDEX_PATH)
    print(f"✅ FAISS index saved to {FAISS_INDEX_PATH}")

    # -----------------------------
    # Save metadata
    # -----------------------------
    with open(META_PATH, "wb") as f:
        pickle.dump(chunks, f)
    print(f"✅ Metadata saved to {META_PATH}")

    print("🎉 Vector store ready for querying!")