import os
import zipfile
import re

extract_dir = "extracted"
out_file = "all_texts.txt"

def get_docx_text(path):
    try:
        with zipfile.ZipFile(path) as z:
            xml_content = z.read('word/document.xml').decode('utf-8')
            # Extract text from <w:t> tags
            texts = re.findall(r'<w:t(?: xml:space="preserve")?>(.*?)</w:t>', xml_content)
            return ' '.join(texts)
    except Exception as e:
        return f"Error reading docx: {e}"

with open(out_file, "w", encoding="utf-8") as out:
    for filename in os.listdir(extract_dir):
        if filename.endswith(".docx"):
            filepath = os.path.join(extract_dir, filename)
            text = get_docx_text(filepath)
            out.write(f"--- FILE: {filename} ---\n")
            out.write(text + "\n\n")
