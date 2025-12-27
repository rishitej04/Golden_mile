from pypdf import PdfReader
import os

def load_all_city_pdfs(base_pdf_dir):
    documents = []

    for city in os.listdir(base_pdf_dir):
        city_path = os.path.join(base_pdf_dir, city)

        if not os.path.isdir(city_path):
            continue

        print(f"\n📂 Loading PDFs for city: {city}")

        for file in os.listdir(city_path):
            if file.endswith(".pdf"):
                print(f"   📄 Loading PDF: {file}")

                reader = PdfReader(os.path.join(city_path, file))
                text = ""

                for page in reader.pages:
                    text += page.extract_text() or ""

                documents.append({
                    "city": city,
                    "source": file,
                    "text": text
                })

    print(f"\n✅ Total PDFs loaded across all cities: {len(documents)}")
    return documents


# Run directly for testing
if __name__ == "__main__":
    pdf_base_dir = "data/pdfs"
    load_all_city_pdfs(pdf_base_dir)