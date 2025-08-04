# app.py
import streamlit as st
import pandas as pd
import numpy as np
import os

# ----------------------- CONFIG ----------------------- #
st.set_page_config(page_title="Buscador de Libros", layout="wide")
DATA_CSV = "../data/final_data/df_web.csv"

# --------------------- UTILIDADES --------------------- #
@st.cache_data(show_spinner=True)
def load_df(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No se encontró el CSV en {csv_path}")

    df = pd.read_csv(csv_path)

    # Normalizaciones mínimas
    expected_cols = ["title","author","rating","description","genres",
                     "language","publisher","coverImg"]
    for c in expected_cols:
        if c not in df.columns:
            df[c] = np.nan

    # rating a numérico (0-5); si no viene en ese rango, lo dejamos como esté
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    # Asegurar strings
    text_cols = ["title","author","description","genres","language","publisher","coverImg"]
    for c in text_cols:
        df[c] = df[c].fillna("").astype(str)

    # Limpiar y normalizar géneros a "A, B, C"
    df["genres"] = (
        df["genres"]
        .str.replace(r"^\[|\]$", "", regex=True)   # quitar corchetes si quedaron
        .str.replace("'", "", regex=False)
        .str.replace('"', "", regex=False)
        .str.replace(";", ",")                     # por si hay ;
        .str.replace("|", ",")                     # por si hay |
        .str.replace("  +", " ", regex=True)
        .str.strip()
    )

    # Lista de todos los géneros únicos
    all_genres = sorted(
        {g.strip() for s in df["genres"] if s for g in s.split(",") if g.strip()}
    )

    # Listas únicas para autocompletar
    titles = sorted({t for t in df["title"] if t})
    authors = sorted({a for a in df["author"] if a})
    languages = sorted({l for l in df["language"] if l})
    publishers = sorted({p for p in df["publisher"] if p})

    return df, titles, authors, all_genres, languages, publishers


def stars(rating: float) -> str:
    if pd.isna(rating):
        return ""
    r = int(round(float(rating)))
    r = max(0, min(5, r))
    return "⭐" * r + "✩" * (5 - r)


def show_cards(df: pd.DataFrame):
    for _, row in df.iterrows():
        c1, c2 = st.columns([1, 5], vertical_alignment="top")
        with c1:
            url = row.get("coverImg", "")
            if isinstance(url, str) and url and url.lower() != "nan":
                # Mostrar imagen solo si parece URL o ruta válida
                try:
                    st.image(url, width=100, clamp=True)
                except Exception:
                    st.empty()
        with c2:
            st.markdown(f"### {row.get('title','')}")
            st.markdown(f"**Autor:** {row.get('author','')}")
            rt = row.get("rating", np.nan)
            st.markdown(stars(rt))
            desc = row.get("description","")
            if desc:
                st.markdown(f"<div style='color:#666'>{desc[:240]}{'…' if len(desc)>240 else ''}</div>",
                            unsafe_allow_html=True)
            # Chips sencillos de géneros
            gens = [g.strip() for g in row.get("genres","").split(",") if g.strip()]
            if gens:
                st.caption(" · ".join(gens[:6]))
        st.markdown("---")


def apply_filter(df: pd.DataFrame, field: str, value_exact: str, value_contains: str):
    """Permite filtrar por coincidencia exacta (selectbox) o por 'contiene' (text_input)."""
    res = df
    if value_exact:
        res = res[res[field] == value_exact]
    elif value_contains:
        # para 'genres' usamos contains sobre cadena completa
        res = res[res[field].str.contains(value_contains, case=False, na=False)]
    return res


# ------------------------- APP ------------------------ #
st.title("📚 Buscador de Libros (CSV)")

with st.sidebar:
    st.subheader("Fuente de datos")
    st.write(f"Usando: `{DATA_CSV}`")

with st.spinner("Cargando datos…"):
    df, TITLES, AUTHORS, GENRES, LANGS, PUBLISHERS = load_df(DATA_CSV)

# --- Botones (opciones) --- #
st.subheader("Búsqueda rápida")
option = st.radio(
    "Elige un campo de búsqueda",
    ["Título", "Autor", "Género", "Idioma", "Editorial"],
    horizontal=True
)

# Mapeo de columnas
field_map = {
    "Título": "title",
    "Autor": "author",
    "Género": "genres",
    "Idioma": "language",
    "Editorial": "publisher",
}

# Controles dinámicos con autocompletado + texto libre
exact_value = ""
contains_value = ""

if option:
    col_exact, col_contains = st.columns([2, 2])

    if option == "Título":
        with col_exact:
            titulo_indices = [None] + list(range(len(TITLES)))
            titulo_idx = st.selectbox(
                "Selecciona un título:",
                options=titulo_indices,
                format_func=lambda i: "" if i is None else TITLES[i]
            )
            exact_value = TITLES[titulo_idx] if titulo_idx is not None else ""
        with col_contains:
            contains_value = st.text_input("O buscar títulos que contengan…")

    elif option == "Autor":
        with col_exact:
            autor_indices = [None] + list(range(len(AUTHORS)))
            autor_idx = st.selectbox(
                "Selecciona un autor:",
                options=autor_indices,
                format_func=lambda i: "" if i is None else AUTHORS[i]
            )
            exact_value = AUTHORS[autor_idx] if autor_idx is not None else ""
        with col_contains:
            contains_value = st.text_input("O buscar autores que contengan…")

    elif option == "Género":
        with col_exact:
            exact_value = st.selectbox("Selecciona un género:", [""] + GENRES)
        with col_contains:
            contains_value = st.text_input("O buscar géneros que contengan…")

    elif option == "Idioma":
        with col_exact:
            exact_value = st.selectbox("Selecciona un idioma:", [""] + LANGS)
        with col_contains:
            contains_value = st.text_input("O buscar idiomas que contengan…")

    elif option == "Editorial":
        with col_exact:
            exact_value = st.selectbox("Selecciona una editorial:", [""] + PUBLISHERS)
        with col_contains:
            contains_value = st.text_input("O buscar editoriales que contengan…")

# --- Filtrado --- #
results = df.copy()
if option:
    field = field_map[option]
    results = apply_filter(results, field, exact_value, contains_value)

# --- Orden y paginación --- #
st.divider()
st.subheader(f"Resultados ({len(results)})")

# Ordenar por rating desc por defecto (si existe)
if "rating" in results.columns:
    results = results.sort_values(by="rating", ascending=False, na_position="last")

# Paginación simple
page_size = st.selectbox("Resultados por página", [10, 20, 30, 50], index=1)
n_pages = max(1, int(np.ceil(len(results) / page_size)))
page = st.number_input("Página", 1, n_pages, 1)
start = (page - 1) * page_size
end = start + page_size

show_cards(results.iloc[int(start):int(end)])
