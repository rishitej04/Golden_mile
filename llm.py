import os
from dotenv import load_dotenv
from openai import OpenAI
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_report(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a real estate investment advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1200
    )

    text = response.choices[0].message.content

    # 🔹 CLEAN MARKDOWN (minimal post-processing)
    text = re.sub(r"\*\*+", "", text)   # remove **
    text = re.sub(r"#+", "", text)      # remove ###
    text = re.sub(r"- ", "", text)      # remove bullets

    return text.strip()