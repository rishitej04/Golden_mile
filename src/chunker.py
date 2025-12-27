import os
import json

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    INPUT_DIR = "data/unstructured"
    OUTPUT_PATH = "data/processed/text_chunks.json"

    os.makedirs("data/processed", exist_ok=True)

    all_chunks = []

    print("🔹 Starting text chunking...\n")

    for root, _, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith(".txt") or file.endswith(".md"):
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                chunks = chunk_text(text)

                print(f"📄 {file} → {len(chunks)} chunks")

                for i, chunk in enumerate(chunks):
                    all_chunks.append({
                        "source": file,
                        "chunk_id": i,
                        "text": chunk
                    })

    # Save chunks
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print("\n✅ Chunking completed!")
    print(f"📦 Total chunks created: {len(all_chunks)}")
    print(f"💾 Saved to: {OUTPUT_PATH}")