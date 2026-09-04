#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera y reemplaza la sección de proyectos categorizados en web2 cobaem/Morelos-despega/index.html
basado fielmente en Catalogo_Proyectos.md y los PDFs en proyectos_pdf/.
"""

import os
import re
import html

MD_PATH = r"c:\Users\user\Downloads\Airbus COBAEM actualizado\Analisis de proyectos y asesorias\Catalogo_Proyectos.md"
INDEX_PATH = r"c:\Users\user\Downloads\Airbus COBAEM actualizado\web2 cobaem\Morelos-despega\index.html"

# Metadatos visuales para las 6 categorías
CATEGORY_META = {
    "Energías Renovables y Eficiencia Energética": {
        "slug": "energia",
        "icon": "fa-solid fa-solar-panel",
        "color_name": "amber",
        "bg_icon": "bg-amber-500/10 text-amber-500 border border-amber-500/20",
        "badge_bg": "bg-amber-100 text-amber-800 border border-amber-200",
        "card_header_bg": "bg-gradient-to-br from-amber-500/15 via-amber-400/10 to-yellow-500/5",
        "card_icon_color": "text-amber-500",
        "tag": "Energía Limpia",
        "btn_color": "hover:bg-amber-50 text-amber-700 hover:text-amber-900 border-amber-200"
    },
    "Agua, Biofiltración y Tratamiento": {
        "slug": "agua",
        "icon": "fa-solid fa-droplet",
        "color_name": "sky",
        "bg_icon": "bg-sky-500/10 text-sky-500 border border-sky-500/20",
        "badge_bg": "bg-sky-100 text-sky-800 border border-sky-200",
        "card_header_bg": "bg-gradient-to-br from-sky-500/15 via-blue-400/10 to-cyan-500/5",
        "card_icon_color": "text-sky-500",
        "tag": "Gestión Hídrica",
        "btn_color": "hover:bg-sky-50 text-sky-700 hover:text-sky-900 border-sky-200"
    },
    "Biotecnología, Agricultura y Sustentabilidad": {
        "slug": "biotecnologia",
        "icon": "fa-solid fa-seedling",
        "color_name": "emerald",
        "bg_icon": "bg-emerald-500/10 text-emerald-500 border border-emerald-500/20",
        "badge_bg": "bg-emerald-100 text-emerald-800 border border-emerald-200",
        "card_header_bg": "bg-gradient-to-br from-emerald-500/15 via-green-400/10 to-teal-500/5",
        "card_icon_color": "text-emerald-500",
        "tag": "Agro y Bio",
        "btn_color": "hover:bg-emerald-50 text-emerald-700 hover:text-emerald-900 border-emerald-200"
    },
    "Salud y Bienestar": {
        "slug": "salud",
        "icon": "fa-solid fa-heart-pulse",
        "color_name": "rose",
        "bg_icon": "bg-rose-500/10 text-rose-500 border border-rose-500/20",
        "badge_bg": "bg-rose-100 text-rose-800 border border-rose-200",
        "card_header_bg": "bg-gradient-to-br from-rose-500/15 via-red-400/10 to-pink-500/5",
        "card_icon_color": "text-rose-500",
        "tag": "Salud y Comunidad",
        "btn_color": "hover:bg-rose-50 text-rose-700 hover:text-rose-900 border-rose-200"
    },
    "Monitoreo Ambiental y Tecnología": {
        "slug": "tecnologia",
        "icon": "fa-solid fa-satellite-dish",
        "color_name": "indigo",
        "bg_icon": "bg-indigo-500/10 text-indigo-500 border border-indigo-500/20",
        "badge_bg": "bg-indigo-100 text-indigo-800 border border-indigo-200",
        "card_header_bg": "bg-gradient-to-br from-indigo-500/15 via-purple-400/10 to-blue-500/5",
        "card_icon_color": "text-indigo-500",
        "tag": "Tecnología e IoT",
        "btn_color": "hover:bg-indigo-50 text-indigo-700 hover:text-indigo-900 border-indigo-200"
    },
    "Educación Ambiental y Economía Circular": {
        "slug": "economia-circular",
        "icon": "fa-solid fa-recycle",
        "color_name": "teal",
        "bg_icon": "bg-teal-500/10 text-teal-500 border border-teal-500/20",
        "badge_bg": "bg-teal-100 text-teal-800 border border-teal-200",
        "card_header_bg": "bg-gradient-to-br from-teal-500/15 via-emerald-400/10 to-cyan-500/5",
        "card_icon_color": "text-teal-500",
        "tag": "Economía Circular",
        "btn_color": "hover:bg-teal-50 text-teal-700 hover:text-teal-900 border-teal-200"
    }
}

def parse_catalog():
    with open(MD_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    sections = re.split(r'\n##\s+', content)
    categories = []

    for s in sections[1:]:
        lines = s.strip().split('\n')
        cat_title = lines[0].strip()
        rest = '\n'.join(lines[1:])
        m_desc = re.search(r'_(.*?)_', rest)
        desc = m_desc.group(1).strip() if m_desc else ''

        projs_raw = re.split(r'\n###\s+Proyecto\s+', rest)
        projects = []
        for p in projs_raw[1:]:
            p_lines = p.strip().split('\n')
            header_line = p_lines[0].strip()
            parts = header_line.split('–', 1)
            p_num = parts[0].strip()
            p_title = parts[1].strip() if len(parts) > 1 else ''
            p_title = p_title.replace('*(NUEVO)*', '').strip()

            m_plantel = re.search(r'\*\*Plantel:\*\*\s*(.+)', p)
            plantel = m_plantel.group(1).strip() if m_plantel else ''

            p_body = p.split(plantel)[-1].strip() if plantel else p
            p_body = p_body.strip(' -\n\r\t')

            projects.append({
                'num': p_num,
                'title': p_title,
                'plantel': plantel,
                'summary': p_body
            })

        meta = CATEGORY_META.get(cat_title, {
            "slug": "general",
            "icon": "fa-solid fa-lightbulb",
            "color_name": "gray",
            "bg_icon": "bg-gray-500/10 text-gray-500",
            "badge_bg": "bg-gray-100 text-gray-800",
            "card_header_bg": "bg-gray-100",
            "card_icon_color": "text-gray-500",
            "tag": "Iniciativa STEM",
            "btn_color": "hover:bg-gray-50 text-gray-700 border-gray-200"
        })

        categories.append({
            'title': cat_title,
            'desc': desc,
            'meta': meta,
            'projects': projects
        })

    return categories

def build_section_html(categories):
    total_projects = sum(len(c['projects']) for c in categories)
    
    html_parts = []
    html_parts.append('<!-- SECCIONES DE PROYECTOS CATEGORIZADAS -->\n')
    
    # Barra superior de utilidades: Buscador, filtros rápidos y botón de Catálogo Completo
    html_parts.append(f'''
            <!-- Barra de Controles y Descarga de Catálogo -->
            <div class="mb-10 bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                <div class="flex flex-col lg:flex-row items-center justify-between gap-6">
                    <!-- Buscador reactivo -->
                    <div class="w-full lg:w-96 relative">
                        <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                            <i class="fa-solid fa-magnifying-glass"></i>
                        </div>
                        <input type="text" id="project-search-input" placeholder="Buscar por proyecto, plantel o tema..." 
                            class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-accent/50 focus:border-emerald-accent transition-all">
                    </div>

                    <!-- Botones de Acción / Catálogo PDF -->
                    <div class="flex items-center gap-3 w-full lg:w-auto justify-end flex-wrap">
                        <span class="text-xs font-semibold text-gray-500 hidden sm:inline">{total_projects} Proyectos Oficiales • 6 Áreas</span>
                        <a href="Catalogo_Proyectos.pdf" target="_blank" download="Catalogo_Proyectos_Airbus_COBAEM.pdf"
                            class="inline-flex items-center gap-2 px-5 py-2.5 bg-airbus-blue text-white rounded-xl text-sm font-semibold hover:bg-opacity-90 transition-all shadow-sm hover:shadow group">
                            <i class="fa-solid fa-file-pdf text-red-400 group-hover:scale-110 transition-transform"></i>
                            <span>Descargar Catálogo Completo (PDF)</span>
                        </a>
                    </div>
                </div>

                <!-- Filtros rápidos por categoría -->
                <div class="flex items-center gap-2 overflow-x-auto pt-4 mt-4 border-t border-gray-100 pb-1 scrollbar-none text-xs">
                    <span class="text-gray-400 font-semibold uppercase tracking-wider text-[11px] mr-1 shrink-0">Filtrar:</span>
                    <button type="button" class="category-filter-btn active px-3.5 py-1.5 rounded-full font-medium transition-all bg-airbus-blue text-white shadow-xs" data-filter="all">
                        Todos ({total_projects})
                    </button>
    ''')

    for c in categories:
        slug = c['meta']['slug']
        count = len(c['projects'])
        short_name = c['title'].split(' ')[0]
        if short_name in ["Energías", "Educación"]:
            short_name = c['title'].split(' y ')[0]
        html_parts.append(f'''                    <button type="button" class="category-filter-btn px-3.5 py-1.5 rounded-full font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 transition-all shrink-0" data-filter="{slug}">
                        {html.escape(short_name)} ({count})
                    </button>\n''')

    html_parts.append('''                </div>
            </div>

            <!-- Listado de Categorías de Proyectos -->
            <div id="projects-container" class="space-y-6">
    ''')

    for idx, c in enumerate(categories):
        meta = c['meta']
        slug = meta['slug']
        icon = meta['icon']
        bg_icon = meta['bg_icon']
        badge_bg = meta['badge_bg']
        card_header_bg = meta['card_header_bg']
        card_icon_color = meta['card_icon_color']
        btn_color = meta['btn_color']
        count = len(c['projects'])
        
        # Dejamos abiertas las primeras categorías para que sean visibles inmediatamente
        open_attr = "open" if idx < 2 else ""

        html_parts.append(f'''
                <!-- Categoría: {html.escape(c['title'])} -->
                <details class="category-group group bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden open:shadow-md transition-all duration-300" data-category="{slug}" {open_attr}>
                    <summary class="flex items-center gap-4 p-5 md:p-6 cursor-pointer list-none hover:bg-gray-50/80 transition-colors [&::-webkit-details-marker]:hidden focus:outline-none focus:ring-2 focus:ring-inset focus:ring-emerald-accent">
                        <div class="w-12 h-12 rounded-xl {bg_icon} flex items-center justify-center shrink-0 shadow-xs">
                            <i class="{icon} text-2xl"></i>
                        </div>
                        <div class="flex-grow min-w-0">
                            <div class="flex items-center gap-3 flex-wrap">
                                <h3 class="text-xl md:text-2xl font-bold text-airbus-blue leading-snug">{html.escape(c['title'])}</h3>
                                <span class="{badge_bg} text-xs font-bold px-2.5 py-0.5 rounded-full shrink-0 shadow-2xs">
                                    {count} {('proyecto' if count == 1 else 'proyectos')}
                                </span>
                            </div>
                            <p class="text-xs text-gray-500 mt-1 line-clamp-1">{html.escape(c['desc'])}</p>
                        </div>
                        <div class="w-8 h-8 rounded-full bg-gray-50 flex items-center justify-center text-gray-400 group-hover:text-airbus-blue group-open:rotate-180 transition-transform duration-300 shrink-0">
                            <i class="fa-solid fa-chevron-down text-sm"></i>
                        </div>
                    </summary>
                    
                    <div class="p-5 md:p-6 pt-0 border-t border-gray-100 mt-2 bg-slate-50/30">
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 pt-6">
        ''')

        for p in c['projects']:
            p_num = p['num']
            p_title = p['title']
            p_plantel = p['plantel']
            p_summary = p['summary']
            pdf_link = f"proyectos_pdf/Proyecto_{p_num}.pdf"

            html_parts.append(f'''
                            <!-- Tarjeta de Proyecto {p_num} -->
                            <div class="project-card bg-white rounded-2xl overflow-hidden shadow-xs hover:shadow-xl transition-all duration-300 border border-gray-100 flex flex-col h-full hover:-translate-y-1.5 group/card"
                                data-project-num="{p_num}"
                                data-title="{html.escape(p_title.lower())}"
                                data-plantel="{html.escape(p_plantel.lower())}"
                                data-summary="{html.escape(p_summary.lower())}">
                                
                                <div class="h-36 {card_header_bg} overflow-hidden relative shrink-0 flex items-center justify-center group-hover/card:brightness-105 transition-all duration-500 border-b border-gray-100/60">
                                    <i class="{icon} text-5xl {card_icon_color} opacity-75 group-hover/card:scale-115 transition-transform duration-500"></i>
                                    <div class="absolute top-3 left-3 bg-white/95 backdrop-blur-sm text-airbus-blue text-[11px] font-extrabold px-2.5 py-1 rounded-lg shadow-xs border border-gray-100">
                                        PROYECTO {p_num}
                                    </div>
                                    <div class="absolute top-3 right-3 bg-white/90 backdrop-blur-sm text-gray-600 text-[10px] font-semibold px-2 py-0.5 rounded-md shadow-2xs">
                                        {html.escape(meta['tag'])}
                                    </div>
                                </div>

                                <div class="p-5 flex flex-col flex-grow">
                                    <div class="flex items-center gap-1.5 text-emerald-600 text-xs font-semibold mb-2 line-clamp-1">
                                        <i class="fa-solid fa-location-dot text-[11px]"></i>
                                        <span>{html.escape(p_plantel)}</span>
                                    </div>

                                    <h4 class="text-base font-bold text-airbus-blue mb-2.5 leading-snug group-hover/card:text-emerald-600 transition-colors">
                                        {html.escape(p_title)}
                                    </h4>

                                    <p class="text-gray-600 text-xs leading-relaxed mb-5 flex-grow line-clamp-4">
                                        {html.escape(p_summary)}
                                    </p>

                                    <div class="pt-3 border-t border-gray-100 mt-auto flex items-center justify-between">
                                        <a href="{pdf_link}" target="_blank" 
                                            class="inline-flex items-center gap-2 text-xs font-bold text-emerald-accent hover:text-airbus-blue transition-colors group/btn py-1 px-1">
                                            <i class="fa-solid fa-file-pdf text-red-500 text-sm group-hover/btn:scale-110 transition-transform"></i>
                                            <span>Ficha Técnica PDF</span>
                                            <i class="fa-solid fa-arrow-up-right-from-square text-[10px] opacity-70"></i>
                                        </a>
                                        <span class="text-[10px] text-gray-400 font-mono">ID {p_num}</span>
                                    </div>
                                </div>
                            </div>
            ''')

        html_parts.append('''                        </div>
                    </div>
                </details>
        ''')

    html_parts.append(f'''
            </div>

            <div id="no-projects-found" class="hidden text-center py-16 bg-white rounded-2xl border border-gray-100 shadow-sm mt-6">
                <div class="w-16 h-16 rounded-full bg-gray-100 text-gray-400 flex items-center justify-center mx-auto mb-4 text-2xl">
                    <i class="fa-solid fa-magnifying-glass"></i>
                </div>
                <h4 class="text-lg font-bold text-gray-700 mb-1">No se encontraron proyectos</h4>
                <p class="text-sm text-gray-500">Prueba con otra palabra clave o limpia el buscador para ver todos los {total_projects} proyectos.</p>
                <button type="button" id="reset-filter-btn" class="mt-4 px-4 py-2 bg-emerald-accent text-white rounded-xl text-xs font-bold hover:bg-emerald-600 transition-colors">
                    Ver todos los proyectos
                </button>
            </div>''')
    html_parts.append('''
            <script>
            (function() {
                const searchInput = document.getElementById('project-search-input');
                const filterBtns = document.querySelectorAll('.category-filter-btn');
                const categoryGroups = document.querySelectorAll('.category-group');
                const projectCards = document.querySelectorAll('.project-card');
                const noProjectsMsg = document.getElementById('no-projects-found');
                const resetFilterBtn = document.getElementById('reset-filter-btn');

                let currentCategory = 'all';

                function applyFilters() {
                    const query = (searchInput ? searchInput.value : '').toLowerCase().trim();
                    let totalVisible = 0;

                    categoryGroups.forEach(group => {
                        const groupCategory = group.getAttribute('data-category');
                        const isCategoryMatch = (currentCategory === 'all' || currentCategory === groupCategory);

                        if (!isCategoryMatch) {
                            group.classList.add('hidden');
                            return;
                        }

                        let visibleInGroup = 0;
                        const cardsInGroup = group.querySelectorAll('.project-card');

                        cardsInGroup.forEach(card => {
                            const title = card.getAttribute('data-title') || '';
                            const plantel = card.getAttribute('data-plantel') || '';
                            const summary = card.getAttribute('data-summary') || '';
                            const num = card.getAttribute('data-project-num') || '';

                            const matchesQuery = !query || 
                                title.includes(query) || 
                                plantel.includes(query) || 
                                summary.includes(query) || 
                                num.includes(query);

                            if (matchesQuery) {
                                card.classList.remove('hidden');
                                visibleInGroup++;
                                totalVisible++;
                            } else {
                                card.classList.add('hidden');
                            }
                        });

                        if (visibleInGroup > 0) {
                            group.classList.remove('hidden');
                            if (query.length > 0) {
                                group.setAttribute('open', '');
                            }
                        } else {
                            group.classList.add('hidden');
                        }
                    });

                    if (noProjectsMsg) {
                        if (totalVisible === 0) {
                            noProjectsMsg.classList.remove('hidden');
                        } else {
                            noProjectsMsg.classList.add('hidden');
                        }
                    }
                }

                if (searchInput) {
                    searchInput.addEventListener('input', applyFilters);
                }

                filterBtns.forEach(btn => {
                    btn.addEventListener('click', function() {
                        filterBtns.forEach(b => {
                            b.classList.remove('active', 'bg-airbus-blue', 'text-white', 'shadow-xs');
                            b.classList.add('text-gray-600', 'bg-gray-100');
                        });
                        this.classList.add('active', 'bg-airbus-blue', 'text-white', 'shadow-xs');
                        this.classList.remove('text-gray-600', 'bg-gray-100');

                        currentCategory = this.getAttribute('data-filter');
                        applyFilters();
                    });
                });

                if (resetFilterBtn) {
                    resetFilterBtn.addEventListener('click', function() {
                        if (searchInput) searchInput.value = '';
                        currentCategory = 'all';
                        filterBtns.forEach(b => {
                            if (b.getAttribute('data-filter') === 'all') {
                                b.classList.add('active', 'bg-airbus-blue', 'text-white', 'shadow-xs');
                                b.classList.remove('text-gray-600', 'bg-gray-100');
                            } else {
                                b.classList.remove('active', 'bg-airbus-blue', 'text-white', 'shadow-xs');
                                b.classList.add('text-gray-600', 'bg-gray-100');
                            }
                        });
                        applyFilters();
                    });
                }
            })();
            </script>
<!-- END SECCIONES DE PROYECTOS CATEGORIZADAS -->''')

    return "".join(html_parts)

def update_index_html():
    categories = parse_catalog()
    new_section_html = build_section_html(categories)

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Patrón entre <!-- SECCIONES DE PROYECTOS CATEGORIZADAS --> y <!-- END SECCIONES DE PROYECTOS CATEGORIZADAS -->
    pattern = re.compile(
        r'<!-- SECCIONES DE PROYECTOS CATEGORIZADAS -->.*?<!-- END SECCIONES DE PROYECTOS CATEGORIZADAS -->',
        re.DOTALL
    )

    if not pattern.search(html_content):
        # Intentamos con alternativa si el comentario final es distinto
        alt_pattern = re.compile(
            r'<!-- SECCIONES DE PROYECTOS CATEGORIZADAS -->.*?<!-- Interactive Map -->',
            re.DOTALL
        )
        if alt_pattern.search(html_content):
            updated_content = alt_pattern.sub(new_section_html + '\n\n            <!-- Interactive Map -->', html_content)
        else:
            raise ValueError("No se pudo localizar el bloque <!-- SECCIONES DE PROYECTOS CATEGORIZADAS -->")
    else:
        updated_content = pattern.sub(new_section_html, html_content)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"index.html actualizado exitosamente con {len(categories)} categorías y {sum(len(c['projects']) for c in categories)} proyectos.")

if __name__ == "__main__":
    update_index_html()
