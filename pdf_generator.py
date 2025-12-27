from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import LETTER
import os
import time

def generate_pdf(text):
    os.makedirs("reports", exist_ok=True)
    path = f"reports/Golden_Mile_Report_{int(time.time())}.pdf"

    doc = SimpleDocTemplate(path, pagesize=LETTER)
    styles = getSampleStyleSheet()

    heading = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        spaceAfter=12
    )

    normal = styles["Normal"]
    story = []

    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("###"):
            story.append(Paragraph(line.replace("###", ""), heading))
        elif line == "":
            story.append(Spacer(1, 10))
        else:
            story.append(Paragraph(line.replace("₹", "Rs."), normal))

    doc.build(story)
    return path