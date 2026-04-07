import zipfile
import os

zip_path = "propuestas.zip"
extract_dir = "extracted_all"

os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zf:
    for idx, info in enumerate(zf.infolist()):
        if not info.is_dir():
            filename = os.path.basename(info.filename)
            if not filename: continue
            
            data = zf.read(info.filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext not in ['.docx', '.pdf']:
                continue
                
            safe_name = f"doc_{idx}{ext}"
            safe_path = os.path.join(extract_dir, safe_name)
            
            with open(safe_path, 'wb') as out_f:
                out_f.write(data)
