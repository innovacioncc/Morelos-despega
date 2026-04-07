document.addEventListener('DOMContentLoaded', () => {

    /* --- Mobile Menu Toggle --- */
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Close mobile menu when clicking a link
    const mobileLinks = mobileMenu.querySelectorAll('a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
        });
    });

    /* --- Animated Counters --- */
    const counters = document.querySelectorAll('.counter');
    const speed = 200; // The lower the slower

    const animateCounters = () => {
        counters.forEach(counter => {
            const updateCount = () => {
                const target = +counter.getAttribute('data-target');
                let count = +counter.innerText.replace(/,/g, '');

                // Lower inc to slow and higher to speed up
                const inc = target / speed;

                // Check if target is reached
                if (count < target) {
                    // Add inc to count and output in counter
                    counter.innerText = Math.ceil(count + inc).toLocaleString();
                    // Call function every ms
                    setTimeout(updateCount, 10);
                } else {
                    counter.innerText = target.toLocaleString();
                }
            };
            updateCount();
        });
    };

    // Use Intersection Observer to trigger counter animation when section is in view
    const statsSection = document.querySelector('.mt-16.grid'); // parent of counters
    if (statsSection) {
        const observer = new IntersectionObserver((entries, observer) => {
            const [entry] = entries;
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(statsSection);
            }
        }, { threshold: 0.5 });
        observer.observe(statsSection);
    }

    /* --- Tabs Logic (Wiki Section) --- */
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all buttons
            tabBtns.forEach(b => {
                b.classList.remove('border-emerald-accent', 'text-white', 'active');
                b.classList.add('border-transparent', 'text-gray-400');
            });
            // Hide all tab contents
            tabContents.forEach(content => {
                content.classList.remove('active');
                content.classList.add('hidden');
            });

            // Set active to current button
            btn.classList.add('border-emerald-accent', 'text-white', 'active');
            btn.classList.remove('border-transparent', 'text-gray-400');

            // Show corresponding tab content
            const targetId = btn.getAttribute('data-tab');
            const targetContent = document.getElementById(targetId);
            if (targetContent) {
                targetContent.classList.remove('hidden');
                targetContent.classList.add('active');
            }
        });
    });

    /* --- Interactive Map (Leaflet.js) --- */
    // Ensure the container exists before initializing
    const mapElement = document.getElementById('map');
    if (mapElement && typeof L !== 'undefined') {
        // Init map centered in Morelos (Cuernavaca approx)
        const map = L.map('map').setView([18.9215, -99.2346], 9);

        // Add standard OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        // Custom icon design (Optional, using default for now or a custom divIcon for better look)
        const greenIcon = new L.Icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });

        const blueIcon = new L.Icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });

        const locations = [
            // Planteles
            { name: "Plantel 01 Cuernavaca", coords: [18.9215, -99.2346], type: "plantel" },
            { name: "Plantel 02 Jiutepec", coords: [18.8833, -99.1667], type: "plantel" },
            { name: "Plantel 03 Oacalco", coords: [18.8894, -99.0430], type: "plantel" },
            { name: "Plantel 04 Cuautla", coords: [18.8105, -98.9535], type: "plantel" },
            { name: "Plantel 05 Amacuzác", coords: [18.6015, -99.3705], type: "plantel" },
            { name: "Plantel 06 Tlaltizapan", coords: [18.6853, -99.1171], type: "plantel" },
            { name: "Plantel 07 Tepalcingo", coords: [18.5950, -98.8471], type: "plantel" },
            { name: "Plantel 08 Tehuixtla", coords: [18.5367, -99.2789], type: "plantel" },
            { name: "Plantel 09 Atlatlahucan", coords: [18.9329, -98.8993], type: "plantel" },
            { name: "Plantel 10 Santa Rosa 30", coords: [18.7291, -99.1830], type: "plantel" },
            { name: "Plantel 11 Jantetelco", coords: [18.7180, -98.7667], type: "plantel" },
            { name: "Plantel 12 Xochitepec", coords: [18.7831, -99.2307], type: "plantel" },
            { name: "Plantel 13 Chinameca", coords: [18.6186, -98.9950], type: "plantel" },
            { name: "Plantel 14 Ahuatepec", coords: [18.9619, -99.2086], type: "plantel" },
            // EMSaDs
            { name: "EMSaD 01 Valle de Vázquez", coords: [18.5284, -99.0715], type: "emsad" },
            { name: "EMSaD 02 Cuentepec", coords: [18.8471, -99.3094], type: "emsad" },
            { name: "EMSaD 03 Huautla", coords: [18.4552, -99.0348], type: "emsad" },
            { name: "EMSaD 04 Chinameca", coords: [18.6256, -99.0050], type: "emsad" }, // Offset slightly from Plantel 13
            { name: "EMSaD 05 Hueyapan", coords: [18.8893, -98.6844], type: "emsad" },
            { name: "EMSaD 06 Tlacotepec", coords: [18.7892, -98.7753], type: "emsad" },
            { name: "EMSaD 07 Jumiltepec", coords: [18.8787, -98.8166], type: "emsad" },
            { name: "EMSaD 08 Totolapan", coords: [18.9833, -98.9167], type: "emsad" },
            { name: "EMSaD 09 Michapa", coords: [18.7565, -99.4182], type: "emsad" }
        ];

        locations.forEach(loc => {
            const elIcon = loc.type === 'emsad' ? greenIcon : blueIcon;
            L.marker(loc.coords, {icon: elIcon}).addTo(map)
                .bindPopup(`<b>${loc.name}</b><br>Participante del Programa Morelos Despega.`);
        });
    }

});
