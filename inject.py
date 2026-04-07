import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

with open("generated_sections.html", "r", encoding="utf-8") as f:
    sections = f.read()

pattern = re.compile(r'(<!-- Project Cards Grid -->\s*).*?(<!-- Interactive Map -->)', re.DOTALL)
new_html = pattern.sub(r'\1\n' + sections + r'\n            \2', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)
print("Injected successfully.")
