import streamlit as st
import pandas as pd
import faiss
import unicodedata
from utils.cards import show_cards
from utils.sorting import sort_lns_iterable
from utils.language import lang_to_iso, iso_to_display
from sentence_transformers import SentenceTransformer
from Models.faiss_module import (
    load_dataset,
    load_embedder,
    build_faiss_index,
    load_faiss_artifacts,
    semantic_recommend
)
from utils.home_style import render_logo, render_sidebar
from utils.inner_pages import apply_inner_styles
@st.cache_resource
def load_embedder():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
@st.cache_resource
def load_faiss_index():
    return faiss.read_index("data/final_data/faiss_index.idx")
EMBEDDER = load_embedder()
FAISS_INDEX = load_faiss_index()


st.set_page_config(page_title="ReadMeUp – Deep Dive", layout="wide", initial_sidebar_state="expanded")
apply_inner_styles()
render_logo()
render_sidebar()

st.title("Discover your next favorite book")

# Load everything (con caché opcional)
@st.cache_resource
def load_all():
    df = load_dataset()
    embedder = load_embedder()
    index, embs = load_faiss_artifacts()
    if index is None or embs is None:
        index, embs = build_faiss_index(df, embedder)
    if 'language_code' not in df.columns:
        df['language_raw'] = df['language'].astype(str)
        df['language_code'] = df['language_raw'].apply(lang_to_iso)
    # Muestra legible en df["language"] para la UI
    df['language'] = df['language_code'].apply(iso_to_display)  
    
    return df, embedder, index

df_semantic, embedder, faiss_index = load_all()

# UI inputs
query = st.text_area("Describe what you'd like to read", placeholder="e.g., A cozy fantasy adventure with dragons")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    top_n = st.slider("Results", 3, 15, 6)
with col2:
    rating = st.slider("Min rating", 0, 5, 4, 1)
with col3:
    lang_codes = sorted(df_semantic['language_code'].dropna().unique().tolist())
    name_by_code = {code: iso_to_display(code) for code in lang_codes}
    lang_labels_sorted = sort_lns_iterable([name_by_code[c] for c in lang_codes])

    lang_choice = st.selectbox("Language", options=["(any)"] + lang_labels_sorted)
    selected_lang_code = None if lang_choice == "(any)" else {v: k for k, v in name_by_code.items()}[lang_choice]

# Run search
if st.button("Search semantically", type="primary"):
    results, msg = semantic_recommend(
        query=query,
        df=df_semantic,
        embedder=embedder,
        faiss_index=faiss_index,
        top_n=top_n,
        language=selected_lang_code,
        min_rating=rating
    )
    st.markdown(msg)

    if results is None or results.empty:
        st.info("Try a different prompt or remove filters.")
    else:
        show_cards(results)

