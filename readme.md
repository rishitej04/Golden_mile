
# Golden Mile – AI-Powered Real Estate Investment Advisor

Golden Mile is an end-to-end Generative AI application that provides **data-driven real estate investment insights** by combining Machine Learning, document grounding, and Large Language Models (LLMs). The system generates a professional, client-ready advisory report that can also be downloaded as a PDF.

---

## Features

- ML-based price-per-sqft property estimation  
- City-specific market insights  
- Rental yield estimation  
- LLM-generated investment advisory analysis  
- Clean web UI with downloadable PDF reports  

---

## Project Structure

```
Golden_mile/
│
├── app.py
├── predictor.py
├── retriever.py
├── prompt.py
├── llm.py
├── pdf_generator.py
├── stage_1_model.py         
│
├── src/
│   ├── build_vector_index.py
│   ├── data_generation.py
│   ├── text_loader.py
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── vector_store.py
│   └── unstructured_docs.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── app.js
│   └── style.css
│
├── data/
│   ├── raw/
│   └── processed/
│
├── vector_store/
│   ├── faiss.index
│   └── metadata.pkl
│
├── reports/
├── requirements.txt
└── .env            # API key (not committed)
```

---

## Prerequisites

- Python 3.10+
- pip
- Virtual environment support
- OpenAI API key

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository_url>
cd Golden_mile
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate       # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Running the Application

```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5001
```

---

## How It Works

1. User inputs city, budget, property size, and intent.
2. ML model predicts feasible properties.
3. City-specific documents are retrieved.
4. Prompt is constructed using ML + documents.
5. LLM generates a structured advisory report.
6. Report is displayed on the web and downloadable as a PDF.

