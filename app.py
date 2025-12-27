from flask import Flask, render_template, request, jsonify, send_file
from predictor import predict_properties
from retriever import retrieve_docs
from prompt import build_llm_prompt
from llm import generate_report
from pdf_generator import generate_pdf

app = Flask(__name__)

# Store last generated PDF path (simple & safe for single-user demo)
LAST_PDF_PATH = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    global LAST_PDF_PATH

    data = request.json

    user_inputs = {
        "city": data["city"],
        "budget": float(data["budget"]),
        "size": float(data.get("size", 1000)),
        "metro": "Yes",
        "intent": data.get("intent", "Investment")
    }

    # 1. ML
    recommendations = predict_properties(user_inputs)

    # 2. Docs
    documents = retrieve_docs(user_inputs["city"])

    # 3. Prompt (UNCHANGED)
    prompt = build_llm_prompt(recommendations, documents, user_inputs)

    # 4. LLM
    report_text = generate_report(prompt)

    # 5. PDF
    LAST_PDF_PATH = generate_pdf(report_text)

    return jsonify({
        "analysis": report_text
    })

@app.route("/download")
def download():
    if not LAST_PDF_PATH:
        return "No report generated yet", 400

    return send_file(
        LAST_PDF_PATH,
        as_attachment=True,
        download_name="Golden_Mile_Advisory_Report.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)