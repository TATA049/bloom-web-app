import json
import unicodedata
from difflib import get_close_matches
import streamlit as st

# -------------------------- Utilidades --------------------------------------
def strip_accents(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def norm(txt: str) -> str:
    return strip_accents(txt.strip().lower())


# ---------------------------- Carga de datos --------------------------------
import json
import unicodedata
from difflib import get_close_matches
from pathlib import Path

# Ruta del directorio donde está este app.py
BASE_DIR = Path(__file__).parent

# Carga segura del JSON siempre relativo a app.py
with open(BASE_DIR / 'data' / 'verbos.json', 'r', encoding='utf-8') as f:
    VERBOS_BLOOM = json.load(f)


# ---------------------------- UI helpers ------------------------------------
def badge(texto: str, bg: str, fg: str = "#0A2540"):
    # Chip/etiqueta en HTML sin llaves literales en CSS
    return (
        f"<span style='display:inline-block; padding:6px 10px; margin:4px; "
        f"border-radius:999px; background:{bg}; color:{fg}; "
        f"font-size:14px; font-weight:600;'>{texto}</span>"
    )

def card(title: str, body_html: str, color: str):
    # Tarjeta con borde izquierdo de color; todo en f-strings bien formados
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

st.markdown("<h1 style='text-align:center; margin-bottom:0;'>Clasificador de Verbos</h1>" "<p style='text-align:center; opacity:0.85;'>Taxonomía de Bloom</p>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; opacity:0.85;">
  Escribe un verbo en español (infinitivo o forma base) y clasifícalo por nivel cognitivo.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    verbo_input = st.text_input("Escribe un verbo", placeholder="p. ej., analizar, definir, crear...")
with col2:
    consultar = st.button("Clasificar", type="primary", use_container_width=True)

if consultar and verbo_input:
    consulta = norm(verbo_input)
    if consulta in MAPA_VERBO_NIVEL:
        nivel = MAPA_VERBO_NIVEL[consulta]
        color = NIVEL_COLOR[nivel]
        st.markdown(card("Resultado", f"El verbo <b>«{verbo_input.strip()}»</b> pertenece al nivel<br><span style='font-size:22px; font-weight:800; color:{color};'>{nivel}</span>", color), unsafe_allow_html=True)
    else:
        sugerencias = get_close_matches(consulta, TODOS_VERBOS, n=6, cutoff=0.73)
        items = []
        for s in sugerencias:
            n = MAPA_VERBO_NIVEL[s]
            # Recuperar forma original con acentos
            original = next((v for v in VERBOS_BLOOM[n] if norm(v) == s), s)
            items.append(badge(f"{original} — {n}", NIVEL_COLOR[n], "#0A2540"))
        suger_html = ("".join(items) if items else "<i>Sin sugerencias cercanas. Revisa ortografía o prueba un sinónimo.</i>")
        st.markdown(card("No encontrado", f"No encontramos <b>«{verbo_input.strip()}»</b> en la base actual.<br><br><b>Sugerencias:</b><br>{suger_html}", "#E57373"), unsafe_allow_html=True)

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
                st.markdown(badge(v, NIVEL_COLOR[nivel], "#0A2540"), unsafe_allow_html=True)
        with col_b:
            for v in lista[mitad:]:
                st.markdown(badge(v, NIVEL_COLOR[nivel], "#0A2540"), unsafe_allow_html=True)

st.caption("Listados de verbos basados en recursos públicos. Puedes ampliar la base en data/verbos.json.")
