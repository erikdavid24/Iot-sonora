// --- VARIABLES GLOBALES ---
let municipioSeleccionado = null;
let modoActual = 'temperatura';
let historialGlobal = {};

function hexToRgba(hex, alpha) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function obtenerConfig(modo) {
    switch(modo) {
        case 'temperatura': return { color: '#dc3545', unidad: '°C' };
        case 'humedad':     return { color: '#0d6efd', unidad: '%' };
        case 'presion':     return { color: '#17a2b8', unidad: ' hPa' };
        case 'radioactividad': return { color: '#ffc107', unidad: ' µSv' };
        default: return { color: '#333', unidad: '' };
    }
}

// --- CREAR GRÁFICA ---
function crearGrafica(id, label, colorHex) {
    const ctx = document.getElementById(id).getContext('2d');
    const colorFondo = hexToRgba(colorHex, 0.2);

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: label,
                data: [],
                borderColor: colorHex,
                backgroundColor: colorFondo,
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { display: false },
                y: { grid: { color: '#f0f0f0', borderDash: [5, 5] }, grace: '5%' }
            },
            interaction: { mode: 'nearest', axis: 'x', intersect: false }
        }
    });
}

// Inicialización
const chartHmo = crearGrafica('chartHermosillo', 'Temperatura', '#dc3545');
const chartGym = crearGrafica('chartGuaymas', 'Temperatura', '#dc3545');
const chartDinamico = crearGrafica('chartDinamico', 'Temperatura', '#333333');


// --- CAMBIO DE MODO ---
function cambiarModo(nuevoModo) {
    modoActual = nuevoModo;
    const config = obtenerConfig(modoActual);

    // Actualizar Botón Dropdown
    const btnLabel = document.getElementById('lbl-variable');
    const btnIcon = document.querySelector('#btnVariable i');
    const estilosBtn = {
        'temperatura': { texto: 'Temperatura', icono: 'bi-thermometer-half', color: 'text-danger' },
        'humedad':     { texto: 'Humedad',     icono: 'bi-droplet-fill',     color: 'text-primary' },
        'presion':     { texto: 'Presión',     icono: 'bi-speedometer',      color: 'text-info' },
        'radioactividad': { texto: 'Radioactividad', icono: 'bi-radioactive', color: 'text-warning' }
    };

    if (btnLabel && btnIcon && estilosBtn[nuevoModo]) {
        btnLabel.innerText = estilosBtn[nuevoModo].texto;
        btnIcon.className = `bi ${estilosBtn[nuevoModo].icono} ${estilosBtn[nuevoModo].color} me-2`;
    }

    // Actualizar colores gráficas
    actualizarEstiloGrafica(chartHmo, config.color, modoActual);
    actualizarEstiloGrafica(chartGym, config.color, modoActual);
    if(municipioSeleccionado) {
        actualizarEstiloGrafica(chartDinamico, config.color, modoActual);
    }

    renderizarInterfaz();
}

function actualizarEstiloGrafica(chart, color, label) {
    const fondo = hexToRgba(color, 0.2);
    chart.data.datasets[0].borderColor = color;
    chart.data.datasets[0].backgroundColor = fondo;
    chart.data.datasets[0].pointBorderColor = color;
    chart.data.datasets[0].label = label;
}

// --- INTERACCIÓN ---
function abrirGrafica(idMunicipio, nombreBonito, colorBase) {
    if (municipioSeleccionado === idMunicipio) {
        cerrarGrafica();
        return;
    }
    const zona = document.getElementById('zona-dinamica');
    zona.style.display = 'block';
    document.getElementById('titulo-dinamico').innerText = 'Historial: ' + nombreBonito;

    municipioSeleccionado = idMunicipio;
    renderizarInterfaz();

    zona.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function cerrarGrafica() {
    document.getElementById('zona-dinamica').style.display = 'none';
    municipioSeleccionado = null;
}

// --- CARGA INICIAL (HISTORIAL COMPLETO) ---
document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/datos/')
        .then(response => response.json())
        .then(data => {
            // Guardamos directamente los arrays que vienen del backend
            historialGlobal = data;
            renderizarInterfaz(); // ¡Pinta todo inmediatamente!
        })
        .catch(console.error);
});

// --- WEBSOCKET (TIEMPO REAL) ---
const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
const sensorSocket = new WebSocket(wsScheme + '://' + window.location.host + '/ws/sensores/');

sensorSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const municipio = data.municipio;
    const now = new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    // Inicializar si no existe
    if (!historialGlobal[municipio]) {
        historialGlobal[municipio] = { temperatura: [], humedad: [], presion: [], radioactividad: [] };
    }

    ['temperatura', 'humedad', 'presion', 'radioactividad'].forEach(variable => {
        if (data[variable]) {
            const valor = parseFloat(data[variable]);

            // Si la lista no existe, crearla
            if (!historialGlobal[municipio][variable]) historialGlobal[municipio][variable] = [];

            // Agregar nuevo dato al final
            historialGlobal[municipio][variable].push({ t: now, v: valor });

            // Mantener solo los últimos 20 puntos
            if (historialGlobal[municipio][variable].length > 20) {
                historialGlobal[municipio][variable].shift();
            }
        }
    });

    renderizarInterfaz();
};

// --- RENDERIZADOR UI ---
function renderizarInterfaz() {
    const config = obtenerConfig(modoActual);
    const tarjetas = document.querySelectorAll('[id^="val-"]');

    tarjetas.forEach(tarjeta => {
        const municipio = tarjeta.id.replace('val-', '');
        const historial = historialGlobal[municipio];
        const arrayDatos = historial ? historial[modoActual] : [];

        tarjeta.classList.remove('text-danger', 'text-warning', 'text-primary', 'text-info', 'text-dark', 'fw-bold', 'text-muted');

        if (arrayDatos && arrayDatos.length > 0) {
            const ultimoDato = arrayDatos[arrayDatos.length - 1].v;
            tarjeta.innerText = ultimoDato + config.unidad;

            // ALERTAS
            if (modoActual === 'temperatura' && ultimoDato >= 38) {
                tarjeta.classList.add('text-danger', 'fw-bold');
                tarjeta.innerText = "🔥 " + ultimoDato + config.unidad;
            }
            else if (modoActual === 'radioactividad' && ultimoDato >= 5.0) {
                tarjeta.classList.add('text-warning', 'fw-bold');
                tarjeta.style.color = '#fd7e14';
                tarjeta.innerText = "☢️ " + ultimoDato + config.unidad;
            }
            else {
                tarjeta.style.color = config.color;
            }

            // ACTUALIZAR GRÁFICAS (Pinta la línea completa)
            if (municipio === 'hermosillo') pintarGraficaCompleta(chartHmo, arrayDatos);
            if (municipio === 'guaymas') pintarGraficaCompleta(chartGym, arrayDatos);
            if (municipio === municipioSeleccionado) pintarGraficaCompleta(chartDinamico, arrayDatos);

        } else {
            // SIN DATOS
            tarjeta.innerText = '--';
            tarjeta.classList.add('text-muted');
            if (municipio === 'hermosillo') pintarGraficaCompleta(chartHmo, []);
            if (municipio === 'guaymas') pintarGraficaCompleta(chartGym, []);
            if (municipio === municipioSeleccionado) pintarGraficaCompleta(chartDinamico, []);
        }
    });
}

function pintarGraficaCompleta(chart, datos) {
    chart.data.labels = datos.map(d => d.t);
    chart.data.datasets[0].data = datos.map(d => d.v);
    chart.update('none');
}