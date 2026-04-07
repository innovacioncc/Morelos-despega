import os
import json
import pymupdf
from docx import Document

extract_dir = "extracted_all"
out_file = "all_texts_detailed.json"

results = {}

for filename in os.listdir(extract_dir):
    filepath = os.path.join(extract_dir, filename)
    text = ""
    try:
        if filename.endswith(".docx"):
            doc = Document(filepath)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif filename.endswith(".pdf"):
            doc = pymupdf.open(filepath)
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            
        results[filename] = text[:2000] # First 2000 chars are enough for summary and title
    except Exception as e:
        results[filename] = f"Error: {e}"

with open(out_file, "w", encoding="utf-8") as out:
    json.dump(results, out, ensure_ascii=False, indent=2)
