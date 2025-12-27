import os

def load_text_docs(base_dir):
    docs = []

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".txt") or file.endswith(".md"):
                full_path = os.path.join(root, file)

                with open(full_path, "r", encoding="utf-8") as f:
                    docs.append({
                        "source": os.path.relpath(full_path, base_dir),
                        "text": f.read()
                    })

                print(f"📄 Loaded: {os.path.relpath(full_path, base_dir)}")

    return docs


# -----------------------------
# Run directly
# -----------------------------
if __name__ == "__main__":
    BASE_DIR = "data/unstructured"

    documents = load_text_docs(BASE_DIR)

    print(f"\nTotal text documents loaded: {len(documents)}")