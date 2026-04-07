import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

with open("generated_sections_details.html", "r", encoding="utf-8") as f:
    sections = f.read()

pattern = re.compile(r'(<!-- SECCIONES DE PROYECTOS CATEGORIZADAS -->\s*).*?(<!-- FIN SECCIONES -->)', re.DOTALL)
new_html = pattern.sub(r'\1\n' + sections + r'\n            \2', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)
print("Injected collapsible sections successfully.")
