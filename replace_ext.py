import sys
import codecs

with codecs.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_content = content.replace('.docx"', '.pdf"')

with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done")
