# Clasificador de Verbos – Taxonomía de Bloom (Web)

Aplicación web en **Streamlit** para clasificar verbos según la **Taxonomía de Bloom**.

## Requisitos locales

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estructura

```
bloom_web_app/
├─ app.py
├─ requirements.txt
├─ .streamlit/
│  └─ config.toml
└─ data/
   └─ verbos.json
```

## Despliegue en Streamlit Community Cloud

1. Sube esta carpeta a un repositorio público en GitHub (por ejemplo, `bloom-web-app`).
2. Ve a https://share.streamlit.io y conecta tu cuenta de GitHub.
3. Crea una **New app** y selecciona el repositorio, rama (main) y archivo `app.py`.
4. (Opcional) En **Advanced settings**, usa `requirements.txt` (ya incluido).
5. Haz clic en **Deploy**. Streamlit construirá y publicará tu app.

## Personalización
- Colores y tema: edita `./.streamlit/config.toml`.
- Base de verbos: edita `./data/verbos.json`.
