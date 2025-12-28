from flask import Flask, render_template, request, jsonify, send_file
import os
import time
import json

from predictor import predict_properties
from retriever import retrieve_docs
from prompt import build_llm_prompt
from llm import generate_report
from pdf_generator import generate_pdf

app = Flask(__name__)

# Store last generated PDF path
LAST_PDF_PATH = None

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    global LAST_PDF_PATH

    data = request.json

    # --- Dynamic user inputs ---
    user_inputs = {
        "city": data["city"],
        "budget": float(data["budget"]),
        "size": float(data["size"]),
        "metro": data.get("metro", "Yes"),  # Yes/No from UI
        "intent": data.get("intent", "Investment")
    }

    print("User Inputs:", user_inputs)

    # --- 1️⃣ ML predictions ---
    print("Running ML predictions...")
    recommendations = predict_properties(user_inputs)
    print("ML done, rows:", len(recommendations))

    # --- 2️⃣ Retrieve documents ---
    print("Retrieving documents...")
    documents = retrieve_docs(user_inputs["city"])
    print("Docs retrieved:", len(documents))

    # --- 3️⃣ Build prompt ---
    print("Building prompt...")
    prompt = build_llm_prompt(recommendations, documents, user_inputs)

    # --- 4️⃣ LLM call ---
    print("Calling LLM...")
    report_text = generate_report(prompt)
    print("LLM done")

    # --- 5️⃣ Save JSON ---
    os.makedirs("reports/json", exist_ok=True)
    json_path = f"reports/json/report_{int(time.time())}.json"
    with open(json_path, "w") as f:
        json.dump({
            "user_inputs": user_inputs,
            "recommendations": recommendations.to_dict(orient="records"),
            "analysis": report_text
        }, f, indent=2)
    print(f"JSON saved: {json_path}")

    # --- 6️⃣ Generate PDF ---
    LAST_PDF_PATH = generate_pdf(report_text)
    print("PDF generated:", LAST_PDF_PATH)

    return jsonify({
        "analysis": report_text,
        "pdf_path": LAST_PDF_PATH,
        "json_path": json_path
    })


@app.route("/download")
def download():
    if not LAST_PDF_PATH or not os.path.exists(LAST_PDF_PATH):
        return "No report generated yet", 404

    return send_file(
        LAST_PDF_PATH,
        as_attachment=True,
        download_name="Golden_Mile_Report.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)