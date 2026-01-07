import streamlit as st
import pandas as pd
import unicodedata

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Portal Business Intelligence", layout="wide", initial_sidebar_state="collapsed")

# --- CSS PERSONALIZADO:  ---
st.markdown("""
<style>
@import url('https://fonts.com/css2?family=Roboto:wght@300;400;700;900&display=swap');
:root {
--primary-color: #5C1212; /* Color principal (Vino) */
--secondary-color: #212529; /* Fondo de encabezado y botones (Gris Oscuro/Negro) */
--app-bg-color: #f8f9fa; /* Fondo de aplicación claro */
--white: #ffffff;
--text-color: #343a40; /* Texto oscuro formal */
}
body { font-family: 'Roboto', sans-serif; background-color: var(--app-bg-color); color: var(--text-color); }

/* 1. Banner Principal (Título Grande y Centrado) */
.main-header-banner {
    background-color: var(--secondary-color);
    color: var(--white);
    padding: 20px 30px; /* Más padding para que el título respire */
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    margin-bottom: 40px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4); /* Sombra más dramática */
    border-bottom: 7px solid var(--primary-color); /* Línea gruesa */
}
.header-logo {
    position: absolute;
    left: 40px;
    /* CAMBIO 2: Aumento de la longitud para hacerlo rectangular */
    width: 100px; 
    height: 70px;
    object-fit: contain; /* Asegura que la imagen se ajuste dentro de las dimensiones */
    background-color: var(--white);
    padding: 8px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}
.header-title {
    font-size: 4.0em; /* ¡Muy grande! */
    font-weight: 900;
    line-height: 1.1;
    text-transform: uppercase;
    letter-spacing: 3px;
}

/* Ocultar elementos nativos de Streamlit */
[data-testid="stSidebar"] { display: none; }
[data-testid="stHeader"] { display: none; }
[data-testid="stToolbar"] { visibility: hidden;}

/* Estilo para los botones de navegación (Áreas) */
.stButton>button {
    background-color: var(--secondary-color);
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 700;
    padding: 15px 30px;
    margin: 5px;
    transition: all 0.3s ease;
    font-size: 1.05em; /* Ligeramente más grande */
}
/* Estilo del botón seleccionado (activo) */
.selected-button > button {
    background-color: var(--primary-color) !important;
    border: 4px solid #f0f2ff !important;
    box-shadow: 0 0 18px rgba(0, 0, 0, 0.5);
    transform: scale(1.05);
}

/* Estilo para los cards/cuadros de producto */
.product-card {
    background-color: var(--white);
    border-radius: 15px;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    padding: 25px;
    height: 100%;
    /* Reducir la altura mínima para permitir el ajuste natural */
    min-height: 400px; 
    display: flex;
    flex-direction: column;
    transition: transform 0.3s, box-shadow 0.3s;
    text-align: center;
    border: 1px solid #e9ecef; /* Borde muy sutil */
}
.product-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}
.product-link {
    text-decoration: none;
    color: inherit;
    display: block;
    height: 100%;
}
.product-title {
    color: var(--secondary-color);
    font-size: 1.6em; /* Más grande y prominente */
    font-weight: 900;
    margin-bottom: 10px;
}
/* Estilo para el IFRAME/Vista previa del sitio web */
.preview-iframe {
    width: 100%; /* Cubre el ancho del contenedor */
    /* CAMBIO 1: Reducción de la altura del iFrame para que el card se vea menos extendido */
    height: 170px; 
    object-fit: contain;
    border-radius: 10px;
    border: 3px solid var(--primary-color); /* Borde de color principal */
    margin: 15px 0;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #f0f2ff; /* Fondo para si no carga */
}
.description-text {
    font-size: 1.0em;
    color: var(--text-color);
    margin-top: auto;
    padding-top: 10px;
    line-height: 1.4;
}
/* REMOVED: .link-access style (punto 1) */
</style>
""", unsafe_allow_html=True)

# --- DATOS DE NAVEGACIÓN (Con Placeholders de Imagen) ---
ICON_COMERCIAL_1 = "https://i.imgur.com/gK9q0nN.png"
ICON_COMERCIAL_2 = "https://i.imgur.com/t4hDq8Z.png"
ICON_TRASLADOS = "https://i.imgur.com/R8k7Kj0.png"
ICON_SUCURSALES = "https://i.imgur.com/e3lXv2W.png"
ICON_FINANZAS = "https://i.imgur.com/xT5u6Gj.png"

AREAS_DATA = {
    "COMERCIAL": [
        {
            "nombre": "Análisis de Ventas",
            "descripcion": "Pronóstico de ventas, gestión de la demanda y proyecciones clave por canal.",
            "url": "https://pronostico-ventura-lag.streamlit.app/",
            "imagen_preview": ICON_COMERCIAL_1
        },
        {
            "nombre": "Scorecard Comercial",
            "descripcion": "Monitoreo consolidado de los Indicadores Clave de Rendimiento (KPIs) para la dirección Comercial.",
            "url": "https://app.powerbi.com/view?r=eyJrIjoiMGI2M2M4MGItNTczZi00OGI0LWE1N2UtNmVhNTkwYjA5NDE0IiwidCI6ImZiMjhmMWFiLTVkZGQtNGExZC1iNjA2LTM4YWVjNGViMmI0OCJ9",
            "imagen_preview": ICON_COMERCIAL_2
        },
        {
            "nombre": "Benchmarking de Competencia",
            "descripcion": "Análisis comparativo de métricas de precio, costo y valor frente al segmento respectivo de mercado.",
            "url": "https://venturabbenchmarkinlga.streamlit.app/",
            "imagen_preview": ICON_COMERCIAL_1
        },
        {
            "nombre": "Cobranza y Cartera",
            "descripcion": "Control de la cartera de cobranza, eficiencia de cobro y días de crédito superado.",
            "url": "https://app.powerbi.com/view?r=eyJrIjoiZDViNjc0OTUtYmRiZS00YjdjLTgzZGQtYjIyOTFlOTk4ZjAxIiwidCI6ImZiMjhmMWFiLTVkZGQtNGExZC1iNjA2LTM4YWVjNGViMmI0OCJ9",
            "imagen_preview": ICON_COMERCIAL_2
        },
        {
            "nombre": "Índices de Precios",
            "descripcion": "Visualización de tendencias, sensibilidad y comparativas de precios promedio.",
            "url": "https://app.powerbi.com/view?r=eyJrIjoiYzk3NWZhODYtODM4MC00NjMyLTkyNWEtOTQ5YjA3YjAzZmVjIiwidCI6ImZiMjhmMWFiLTVkZGQtNGExZC1iNjA2LTM4YWVjNGViMmI0OCJ9",
            "imagen_preview": ICON_COMERCIAL_1
        },
        {
            "nombre": "Pendientes de Comercializar",
            "descripcion": "Monitoreo de inventario sin asignación comercial y análisis de la rotación.",
            "url": "https://app.powerbi.com/view?r=eyJrIjoiMmJlNjliZWItNmM5Mi00NThjLWE3MWYtMzA2NGEzZmMzZTRkIiwidCI6ImZiMjhmMWFiLTVkZGQtNGExZC1iNjA2LTM4YWVjNGViMmI0OCJ9",
            "imagen_preview": ICON_COMERCIAL_2
        },
        {
            "nombre": "Modelo Econométrico",
            "descripcion": "Análisis predictivo de proyecciones económicas e indicadores Ventura.",
            "url": "https://lagarciav.shinyapps.io/Prub/",
            "imagen_preview": ICON_COMERCIAL_1
        },
         {
            "nombre": "Comercialización de Unidades",
            "descripcion": "Comercializacion anual y estrategi de corralones",
            "url": "https://estrategiacorralones.streamlit.app/",
            "imagen_preview": ICON_COMERCIAL_1
        },
    ],
    "TRASLADOS": [
        {
            "nombre": "Scorecard Traslados",
            "descripcion": "KPIs de rendimiento, eficiencia y costos de la flota de traslados.",
            "url": "https://app.powerbi.com/view?r=eyJrIjoiOTM1MTcyNGEtNWY0Zi00MDYyLTg1ZTQtZTNhNGI2Zjg4N2ZmIiwidCI6ImZiMjhmMWFiLTVkZGQtNGExZC1iNjA2LTM4YWVjNGViMmI0OCJ9",
            "imagen_preview": ICON_TRASLADOS
        },
        {
            "nombre": "Eficiencia Logística",
            "descripcion": "Monitoreo detallado de tiempos de entrega, optimización de rutas y utilización de recursos (Tiempos de Ciclo).",
            "url": "#",
            "imagen_preview": ICON_TRASLADOS
        },
    ],
    "SUCURSALES": [
        {
            "nombre": "Scorecard Sucursales",
            "descripcion": "Métricas de desempeño operativo por punto de región.",
            "url": "https://app.powerbi.com/view?r=eyJrIjoiZWZhYTkzOTctODM5MC00ZDI1LTk4YzItYjJiMWQ4Y2JkYmUxIiwidCI6ImZiMjhmMWFiLTVkZGQtNGExZC1iNjA2LTM4YWVjNGViMmI0OCJ9",
            "imagen_preview": ICON_SUCURSALES
        },
        {
            "nombre": "Desempeño Regional",
            "descripcion": "Análisis comparativo de KPIs de venta y operación a nivel regional y geográfico detallado.",
            "url": "#",
            "imagen_preview": ICON_SUCURSALES
        },
    ],
    "FINANZAS": [
        {
            "nombre": "Flujo de Efectivo",
            "descripcion": "Reportes históricos y proyecciones de cash flow, liquidez y control presupuestario.",
            "url": "#",
            "imagen_preview": ICON_FINANZAS
        },
    ],
}

# --- ESTADO DE SESIÓN PARA LA NAVEGACIÓN ---
if 'area_seleccionada' not in st.session_state:
    st.session_state['area_seleccionada'] = list(AREAS_DATA.keys())[0]

# --- FUNCIÓN PARA EL CUADRO DE PRODUCTO MODIFICADO (con iFrame) ---
def crear_product_card(producto):
    """Genera el HTML para un cuadro de producto usando un iFrame como vista previa."""

    url_to_preview = producto['url'] if producto['url'] != "#" else "about:blank"
    
    # CAMBIO 3: Manejo especial para URLs de Streamlit
    # Streamlit Cloud por defecto no se permite incrustar en IFrames a menos que se use la versión 'embed'
    if "streamlit.app" in url_to_preview:
        # Reemplazamos la URL normal por su versión de incrustación
        # Esto generalmente se logra añadiendo ?embed=true al final
        url_to_preview += "?embed=true"
    
    # Si la URL es '#', usamos un placeholder o una imagen por defecto
    elif producto['url'] == "#":
        url_to_preview = "about:blank"


    # La altura se controla en el CSS (.preview-iframe)
    card_html = f"""
    <a href="{producto['url']}" target="_blank" class="product-link">
        <div class="product-card">
            <div class="product-title">{producto['nombre']}</div>
            <iframe src="{url_to_preview}" class="preview-iframe" title="Vista Previa de {producto['nombre']}" frameborder="0"></iframe>
            <p class="description-text">{producto['descripcion']}</p>
            </div>
    </a>
    """
    return card_html


# --- CUERPO PRINCIPAL DE LA PÁGINA ---

# --- BANNER DEL TÍTULO (Centrado y Grande) ---
st.markdown(
    f"""
    <div class="main-header-banner">
        <img src="https://tse1.mm.bing.net/th/id/OIP.dZs9yNpJVa2kZjoE9rx54gAAAA?cb=12&rs=1&pid=ImgDetMain&o=7&rm=3"
             alt="Logo BI Corporativo" class="header-logo">
        <div class="header-title">PORTAL BUSINESS INTELLIGENCE</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<h3 style="text-align: center; color: var(--text-color); margin-bottom: 35px; font-weight: 400;">Plataforma Centralizada de Analítica Avanzada y Data Science</h3>', unsafe_allow_html=True)


# --- BARRA DE NAVEGACIÓN DE ÁREAS (Horizontal) ---
areas_keys = list(AREAS_DATA.keys())
area_cols = st.columns(len(areas_keys))

# Generar los botones de área
for i, area in enumerate(areas_keys):
    is_selected = area == st.session_state['area_seleccionada']

    with area_cols[i]:
        style_class = "selected-button" if is_selected else ""

        st.markdown(f'<div class="{style_class}">', unsafe_allow_html=True)
        if st.button(area, key=f"btn_area_{area}"):
            st.session_state['area_seleccionada'] = area
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid var(--secondary-color); margin-top: 25px;'>", unsafe_allow_html=True)

# --- CONTENIDO DINÁMICO (Productos del Área Seleccionada) ---

area_actual = st.session_state['area_seleccionada']

st.markdown(f'<h2 style="color: var(--primary-color); margin-bottom: 30px; border-left: 5px solid var(--primary-color); padding-left: 15px; font-weight: 700;">{area_actual} – Catálogo de Soluciones Analíticas</h2>', unsafe_allow_html=True)

productos = AREAS_DATA.get(area_actual, [])

if productos:
    # Mostrar 3 productos por fila
    num_productos = len(productos)
    cols = st.columns(3)

    for i, producto in enumerate(productos):
        with cols[i % 3]:
            # **Importante:** La vista previa incrustada (iframe) solo funcionará si
            # la URL del tablero permite ser incrustada (no tiene restricciones de X-Frame-Options).
            st.markdown(crear_product_card(producto), unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
else:
    st.info(f"Actualmente no hay soluciones de Business Intelligence disponibles para el área de **{area_actual}**. Contacte al equipo de BI para solicitar un desarrollo.")

# --- FOOTER ---
st.markdown("<hr style='border: 1px solid #ced4da; margin-top: 50px;'>", unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #6c757d; font-size: 0.85em;">Portal de Inteligencia de Negocios Ventura | Desarrollado por BI </p>', unsafe_allow_html=True)
