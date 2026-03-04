# =======================
# Clasificador de Verbos – Taxonomía de Bloom (Streamlit)
# =======================

import json
import unicodedata
from difflib import get_close_matches
from pathlib import Path
import streamlit as st

# ---------------------------- Utilidades ------------------------------------
def strip_accents(s: str) -> str:
    """Quita acentos para comparar sin tildes."""
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def norm(txt: str) -> str:
    """Normaliza texto a minúsculas y sin acentos."""
    return strip_accents(txt.strip().lower())

# ---------------------------- Carga de datos --------------------------------
BASE_DIR = Path(__file__).parent  # directorio donde está este app.py

# Cargamos el JSON SIEMPRE relativo a app.py para evitar FileNotFoundError
with open(BASE_DIR / "data" / "verbos.json", "r", encoding="utf-8") as f:
    VERBOS_BLOOM = json.load(f)

# Mapa color por nivel (debe estar DEFINIDO antes de usarse)
NIVEL_COLOR = {
    "Recordar":   "#64B5F6",
    "Comprender": "#4FC3F7",
    "Aplicar":    "#4DD0E1",
    "Analizar":   "#4DB6AC",
    "Evaluar":    "#81C784",
    "Crear":      "#BA68C8",
}

# Mapa inverso verbo → nivel (normalizado)
MAPA_VERBO_NIVEL = {norm(v): nivel for nivel, lista in VERBOS_BLOOM.items() for v in lista}
TODOS_VERBOS = list(MAPA_VERBO_NIVEL.keys())

# ---------------------------- UI helpers ------------------------------------
def badge(texto: str, bg: str, fg: str = "#0A2540"):
    # Etiqueta tipo “chip” (sin llaves literales de CSS)
    return (
        f"<span style='display:inline-block; padding:6px 10px; margin:4px; "
        f"border-radius:999px; background:{bg}; color:{fg}; "
        f"font-size:14px; font-weight:600;'>{texto}</span>"
    )

def card(title: str, body_html: str, color: str):
    # Tarjeta con borde izquierdo de color
    return (
        f"<div style='border:1px solid rgba(255,255,255,0.15); "
        f"border-left:6px solid {color}; "
        f"background:rgba(255,255,255,0.05); border-radius:10px; "
        f"padding:16px; margin-top:12px;'>"
        f"<div style='font-size:18px; font-weight:700; color:{color};'>{title}</div>"
        f"<div style='margin-top:8px; line-height:1.5;'>{body_html}</div>"
        f"</div>"
    )

# ----------------------------- APP ------------------------------------------
st.set_page_config(page_title="Clasificador Bloom (Web)", page_icon="🧠", layout="centered")

st.markdown(
    "<h1 style='text-align:center; margin-bottom:0;'>Clasificador de Verbos</h1>"
    "<p style='text-align:center; opacity:0.85;'>Taxonomía de Bloom</p>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align:center; opacity:0.85;">
      Escribe un verbo en español (infinitivo o forma base) y clasifícalo por nivel cognitivo.
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([3, 1])  # evitamos parámetros no soportados
with col1:
    verbo_input = st.text_input("Escribe un verbo", placeholder="p. ej., analizar, definir, crear...")
with col2:
    consultar = st.button("Clasificar", type="primary", use_container_width=True)

if consultar and verbo_input:
    consulta = norm(verbo_input)
    if consulta in MAPA_VERBO_NIVEL:
        nivel = MAPA_VERBO_NIVEL[consulta]
        color = NIVEL_COLOR.get(nivel, "#64B5F6")
        st.markdown(
            card(
                "Resultado",
                (
                    f"El verbo <b>«{verbo_input.strip()}»</b> pertenece al nivel<br>"
                    f"<span style='font-size:22px; font-weight:800; color:{color};'>{nivel}</span>"
                ),
                color,
            ),
            unsafe_allow_html=True,
        )
    else:
        sugerencias = get_close_matches(consulta, TODOS_VERBOS, n=6, cutoff=0.73)
        chips = []
        for s in sugerencias:
            n = MAPA_VERBO_NIVEL[s]
            original = next((v for v in VERBOS_BLOOM[n] if norm(v) == s), s)
            chips.append(badge(f"{original} — {n}", NIVEL_COLOR.get(n, "#64B5F6"), "#0A2540"))
        suger_html = "".join(chips) if chips else "<i>Sin sugerencias cercanas. Revisa ortografía o prueba un sinónimo.</i>"
        st.markdown(
            card(
                "No encontrado",
                f"No encontramos <b>«{verbo_input.strip()}»</b> en la base actual.<br><br>"
                f"<b>Sugerencias:</b><br>{suger_html}",
                "#E57373",
            ),
            unsafe_allow_html=True,
        )

st.markdown("---")
st.subheader("Explorar verbos por nivel")

niveles = list(VERBOS_BLOOM.keys())
tabs = st.tabs(niveles)

for i, nivel in enumerate(niveles):
    with tabs[i]:
        lista = VERBOS_BLOOM[nivel]
        col_a, col_b = st.columns(2)
        mitad = (len(lista) + 1) // 2
        with col_a:
            for v in lista[:mitad]:
                st.markdown(badge(v, NIVEL_COLOR.get(nivel, "#64B5F6"), "#0A2540"), unsafe_allow_html=True)
        with col_b:
            for v in lista[mitad:]:
                st.markdown(badge(v, NIVEL_COLOR.get(nivel, "#64B5F6"), "#0A2540"), unsafe_allow_html=True)

st.caption("Base de verbos editable en data/verbos.json. Ruta del archivo cargada de forma robusta con pathlib.")
