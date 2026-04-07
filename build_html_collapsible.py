import json
import re

with open("all_texts_detailed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

categories = {
    "Agua y Conservación Ambiental": {"keywords": ["agua", "residual", "hidroponia", "lluvia", "contaminación", "basura", "ecología", "composta", "río", "hidráulica", "fuga", "filtro", "sanitarios", "sanear"], "icon": "fa-droplet", "img": "https://images.unsplash.com/photo-1582485565167-75055e5e6b5b?auto=format&fit=crop&w=800&q=80", "color": "blue-500"},
    "Energía Sustentable": {"keywords": ["solar", "fotovoltaico", "energía", "electricidad", "generador", "turbina", "bicicleta", "panel", "hidrogeno", "combustión", "calor", "horno", "secador", "híbrido"], "icon": "fa-sun", "img": "https://images.unsplash.com/photo-1509391366360-51548651817c?auto=format&fit=crop&w=800&q=80", "color": "yellow-500"},
    "Agricultura y Agrotecnología": {"keywords": ["agrícola", "huerto", "suelo", "fertilizante", "plantas", "riego", "semilla", "nopal", "biopolímero", "fruta", "cultivo"], "icon": "fa-leaf", "img": "https://images.unsplash.com/photo-1592982537447-6f23342d2f78?auto=format&fit=crop&w=800&q=80", "color": "green-500"},
    "Robótica y Tecnología": {"keywords": ["robótica", "aplicación", "software", "sistema", "plataforma", "automatizado", "mano mecánica", "IoT", "sensor"], "icon": "fa-robot", "img": "https://images.unsplash.com/photo-1485603770141-863a1523b08e?auto=format&fit=crop&w=800&q=80", "color": "purple-500"},
    "Salud y Bienestar": {"keywords": ["salud", "aire", "ovario", "enfermedad", "respiratorio", "síndrome"], "icon": "fa-heart-pulse", "img": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=800&q=80", "color": "red-500"}
}

categorized = {k: [] for k in categories.keys()}
categorized["Otros Iniciativas STEM"] = [] # fallback
categories["Otros Iniciativas STEM"] = {"keywords": [], "icon": "fa-lightbulb", "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80", "color": "gray-500"}

for filename, text in data.items():
    if not text.strip() or "Error:" in text: continue
    text_lower = text.lower()
    
    # Try to extract a title
    lines = [L.strip() for L in text.split('\n') if L.strip() and "Morelos Despega" not in L and "Educación STEM" not in L and "Fundación Airbus" not in L]
    
    title = "Proyecto Innovador"
    for L in lines:
        L_lower = L.lower()
        if "avenida" in L_lower or "c.p." in L_lower or "colonia" in L_lower or "tel:" in L_lower or "@" in L_lower or L.replace(' ', '').replace('-', '').isdigit():
            continue
        if "777" in L or "362" in L: # Hardcode for COBAEM phone
            continue
        if len(L) > 10 and not ("Contexto" in L or "Favorecer" in L or "Formato" in L):
            title = L[:90]
            if title.startswith("TEMA:"):
                title = title[5:].strip()
            break

    # Sentence extraction for better summary
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text.replace('\n', ' '))
    best_sentence = ""
    for s in sentences:
        s_lower = s.lower()
        if ("objetivo" in s_lower or "proyecto" in s_lower or "propuesta" in s_lower or "busca" in s_lower or "consiste" in s_lower) and len(s) > 40:
            best_sentence = s.strip()
            break
            
    if not best_sentence:
        desc_lines = [L for L in lines if len(L) > 50 and "Objetivo" not in L]
        best_sentence = desc_lines[0] if desc_lines else "Proyecto STEM enfocado en brindar soluciones prácticas a problemas de la comunidad, utilizando tecnología y ciencia de forma creativa."
        
    desc = best_sentence[:220] + "..." if len(best_sentence) > 220 else best_sentence
    
    assigned_cat = "Otros Iniciativas STEM"
    max_score = 0
    for cat, meta in categories.items():
        if cat == "Otros Iniciativas STEM": continue
        score = sum(text_lower.count(kw) for kw in meta["keywords"])
        if score > max_score:
            max_score = score
            assigned_cat = cat

    categorized[assigned_cat].append({
        "title": title.title(),
        "desc": desc,
        "tag": assigned_cat.split(" ")[0],
        "link": f"extracted_all/{filename}"
    })

html_output = '<!-- SECCIONES DE PROYECTOS CATEGORIZADAS -->\n'
html_output += '<div class="space-y-6">\n'

for cat, projs in categorized.items():
    if not projs: continue
    
    meta = categories[cat]
    icon = meta["icon"]
    color = meta["color"]
    img = meta["img"]
    
    html_output += f'''
    <!-- Categoría: {cat} -->
    <details class="group bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden open:shadow-md transition-all duration-300">
        <summary class="flex items-center gap-4 p-5 md:p-6 cursor-pointer list-none hover:bg-gray-50 transition-colors [&::-webkit-details-marker]:hidden focus:outline-none focus:ring-2 focus:ring-inset focus:ring-emerald-accent">
            <div class="w-12 h-12 rounded-full bg-{color}/10 flex items-center justify-center text-{color} shrink-0">
                <i class="fa-solid {icon} text-2xl"></i>
            </div>
            <h3 class="text-xl md:text-2xl font-bold text-airbus-blue flex-grow">{cat}</h3>
            <span class="bg-gray-100 text-gray-600 text-sm font-bold px-3 py-1 rounded-full mr-2 md:mr-4 shrink-0">{len(projs)}</span>
            <i class="fa-solid fa-chevron-down text-gray-400 text-xl transform group-open:rotate-180 transition-transform duration-300"></i>
        </summary>
        
        <div class="p-5 md:p-6 pt-0 border-t border-gray-100 mt-2">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 pt-6">
    '''
    
    for p in projs:
        html_output += f'''
                <div class="project-card bg-light-bg rounded-2xl overflow-hidden shadow hover:shadow-lg transition-all duration-300 border border-gray-100 flex flex-col h-full hover:-translate-y-1 group/card">
                    <div class="h-40 bg-{color}/10 overflow-hidden relative shrink-0 flex items-center justify-center group-hover/card:bg-{color}/20 transition-colors duration-500">
                        <i class="fa-solid {icon} text-6xl text-{color} opacity-80 group-hover/card:scale-125 transition-transform duration-500"></i>
                        <div class="absolute top-3 right-3 bg-white/90 backdrop-blur-sm text-airbus-blue text-xs font-bold px-2 py-1 rounded-md shadow-sm">{p['tag']}</div>
                    </div>
                    <div class="p-5 flex flex-col flex-grow">
                        <h4 class="text-lg font-bold text-airbus-blue mb-2 leading-tight">{p['title']}</h4>
                        <p class="text-gray-600 text-xs mb-4 flex-grow line-clamp-4">{p['desc']}</p>
                        <a href="{p['link']}" target="_blank" onclick="window.open(this.href,'targetWindow','toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=800,height=600'); return false;" class="text-emerald-accent font-semibold text-xs hover:underline flex items-center gap-1 mt-auto group-hover/card:text-airbus-blue transition-colors">Ver doc. original <i class="fa-solid fa-file-pdf"></i></a>
                    </div>
                </div>
        '''
        
    html_output += '''
            </div>
        </div>
    </details>
    '''
    
html_output += '</div>\n<!-- FIN SECCIONES -->\n'

with open("generated_sections_details.html", "w", encoding="utf-8") as out:
    out.write(html_output)

print("HTML generado en generated_sections_details.html")
