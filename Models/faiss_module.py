import os
import ast
import faiss
import numpy as np
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
from utils.language import lang_to_iso, iso_to_display

DATA_DIR = "data/final_data"
MODEL_PATH = "models/all-MiniLM-L6-v2"  
IDX_PATH = os.path.join(DATA_DIR, "faiss_index.idx") 
EMB_PATH = os.path.join(DATA_DIR, "embeddings.npy") 

@st.cache_data(show_spinner=False)
def load_dataset():
    df = pd.read_csv(os.path.join(DATA_DIR, "df_web.csv"))
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')
    if isinstance(df['genres'].iloc[0], str):
        df['genres'] = df['genres'].apply(ast.literal_eval)
    df['author'] = df['author'].apply(
        lambda x: [a.strip() for a in x.split(',')] if isinstance(x, str)
        else (x if isinstance(x, list) else [])
    )
    df['description'] = df['description'].fillna("").astype(str)
    df['language'] = df['language'].fillna("").astype(str)
    df['language_code'] = df['language'].apply(lang_to_iso)
    df['language'] = df['language_code'].apply(iso_to_display)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)
    df['genres'] = df['genres'].apply(lambda g: g if isinstance(g, list) else [])
    df['text_for_embedding'] = df['description'].str.strip() + ". Genres: " + df['genres'].apply(lambda g: ", ".join(g))
    return df

@st.cache_resource(show_spinner=True)
def load_embedder():
    # Carga el modelo desde la carpeta local, sin descargar
    return SentenceTransformer(MODEL_PATH)

@st.cache_resource(show_spinner=False)
def load_faiss_artifacts():
    if os.path.exists(IDX_PATH) and os.path.exists(EMB_PATH):
        return faiss.read_index(IDX_PATH), np.load(EMB_PATH)
    return None, None

def semantic_recommend(query, df, embedder, faiss_index, top_n=5, language=None, min_rating=0.0):
    if not query or not query.strip():
        return None, "Please enter a description or idea for the book you want."

    q_vec = embedder.encode([query], convert_to_numpy=True).astype('float32')
    q_vec /= np.clip(np.linalg.norm(q_vec, axis=1, keepdims=True), 1e-12, None)

    sims, idxs = faiss_index.search(q_vec, top_n * 5)
    candidates = df.iloc[idxs[0]].copy()
    candidates['similarity'] = sims[0]

    if language:
        lang_str = str(language).strip()
        candidates = candidates[
            candidates['language_code'].str.lower().eq(lang_str.lower()) |
            candidates['language'].str.casefold().eq(lang_str.casefold())
        ]
    if min_rating and min_rating > 0:
        candidates = candidates[candidates['rating'] >= min_rating]

    results = candidates.head(top_n)
    if results.empty:
        return None, "No results found. Try broadening your query or relaxing filters."
    return results, f"Semantic recommendations for: **{query.strip()}**"
