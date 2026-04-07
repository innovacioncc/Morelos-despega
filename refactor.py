import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update YouTube iframe
youtube_old = r'<iframe width="560" height="315" src="https://www.youtube.com/embed/xvxuD_XeCmE\?si=shared" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen class="w-full h-full absolute inset-0"></iframe>'
youtube_new = r'''<img src="https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=800&q=80" class="absolute inset-0 w-full h-full object-cover opacity-50 mix-blend-overlay group-hover:scale-105 transition-transform duration-500" alt="Video thumbnail">
                    <a href="https://youtu.be/xvxuD_XeCmE" target="_blank" class="relative z-10 w-20 h-20 bg-red-600 rounded-full flex items-center justify-center text-white shadow-xl hover:scale-110 hover:bg-red-700 transition-all duration-300">
                        <i class="fa-brands fa-youtube text-4xl leading-none" style="margin-top: 2px;"></i>
                    </a>'''
html = re.sub(youtube_old, youtube_new, html)
if '<img src=' not in html:
    print("Warning: YouTube replacement failed.")

# 2. Extract Tutores Section
tutor_pattern = re.compile(r'(    <!-- 4\. Sección de Tutores -->\s*<section id="tutores".*?</section>\n)', re.DOTALL)
match = tutor_pattern.search(html)
if match:
    tutores_html = match.group(0)
    html = html.replace(tutores_html, '')
    
    # 3. Add mention of showcase below
    tutores_html = tutores_html.replace(
        'Súmate a la red de mentores del Campus Morelos. Investigadores, académicos y profesionales guiando a la próxima generación de solucionadores.',
        'Súmate a la red de mentores del Campus Morelos. Investigadores, académicos y profesionales guiando a la próxima generación de solucionadores. <br><br><span class="text-emerald-accent font-semibold">A continuación, te invitamos a explorar los proyectos propuestos por nuestros estudiantes en el Showcase.</span>'
    )

    # 4. Insert Tutores Section before Showcase
    html = html.replace('    <!-- 2. Showcase de Proyectos 2026 -->', tutores_html + '\n    <!-- 2. Showcase de Proyectos 2026 -->')
else:
    print("Warning: Tutores section not found.")

# 5. Update Showcase text
old_showcase_text = 'Conoce las soluciones tecnológicas desarrolladas por los estudiantes de Morelos para resolver problemáticas locales con impacto global.'
new_showcase_text = 'Conoce las soluciones tecnológicas propuestas por los estudiantes de Morelos para resolver problemáticas locales con impacto global. Con la tutoría de investigadoras e investigadores de Morelos, estos proyectos serán semilla de soluciones globales.'
html = html.replace(old_showcase_text, new_showcase_text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Changes applied!")
