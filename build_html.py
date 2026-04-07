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
    title = lines[0][:80] if lines else "Proyecto Innovador"
    if "Contexto" in title or "Favorecer" in title or "Formato" in title:
        title = lines[1][:80] if len(lines) > 1 else "Proyecto Innovador"

    # Try to extract a desc
    desc_lines = [L for L in lines if len(L) > 50 and "Objetivo" not in L]
    desc = desc_lines[0][:180] + "..." if desc_lines else "Desarrollo tecnológico para la comunidad con impacto local."
    
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
        "tag": assigned_cat.split(" ")[0]
    })

html_output = '<!-- SECCIONES DE PROYECTOS CATEGORIZADAS -->\n'
html_output += '<div class="space-y-20">\n'

for cat, projs in categorized.items():
    if not projs: continue
    
    meta = categories[cat]
    icon = meta["icon"]
    color = meta["color"]
    img = meta["img"]
    
    html_output += f'''
    <!-- Categoría: {cat} -->
    <div>
        <div class="flex items-center gap-4 mb-8 border-b border-gray-200 pb-4">
            <div class="w-12 h-12 rounded-full bg-{color}/10 flex items-center justify-center text-{color}">
                <i class="fa-solid {icon} text-2xl"></i>
            </div>
            <h3 class="text-2xl md:text-3xl font-bold text-airbus-blue">{cat}</h3>
            <span class="ml-auto bg-gray-100 text-gray-600 text-sm font-bold px-3 py-1 rounded-full">{len(projs)}</span>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    '''
    
    for p in projs:
        html_output += f'''
            <div class="project-card bg-light-bg rounded-2xl overflow-hidden shadow hover:shadow-lg transition-all duration-300 border border-gray-100 group flex flex-col h-full">
                <div class="h-40 bg-gray-200 overflow-hidden relative shrink-0">
                    <img src="{img}" alt="{p['tag']}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500">
                    <div class="absolute top-3 right-3 bg-white/90 backdrop-blur-sm text-airbus-blue text-xs font-bold px-2 py-1 rounded-md shadow-sm">{p['tag']}</div>
                </div>
                <div class="p-5 flex flex-col flex-grow">
                    <h4 class="text-lg font-bold text-airbus-blue mb-2 leading-tight">{p['title']}</h4>
                    <p class="text-gray-600 text-xs mb-4 flex-grow line-clamp-4">{p['desc']}</p>
                    <a href="#" class="text-emerald-accent font-semibold text-xs hover:underline flex items-center gap-1 mt-auto">Ver detalles <i class="fa-solid fa-arrow-right"></i></a>
                </div>
            </div>
        '''
        
    html_output += '''
        </div>
    </div>
    '''
    
html_output += '</div>\n<!-- FIN SECCIONES -->\n'

with open("generated_sections.html", "w", encoding="utf-8") as out:
    out.write(html_output)

print("HTML generado en generated_sections.html")
