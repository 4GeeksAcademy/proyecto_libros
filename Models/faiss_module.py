import os
import ast
import faiss
import numpy as np
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
from utils.language import lang_to_iso, iso_to_display


@st.cache_resource
def load_dataset():
    df = pd.read_csv("data/final_data/df_web.csv")
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')
    # Ensure lists for genres and authors
    df['genres'] = df['genres'].apply(ast.literal_eval if isinstance(df['genres'].iloc[0], str) else lambda x: x)
    df['author'] = df['author'].apply(lambda x: [a.strip() for a in x.split(',')] if isinstance(x, str) else (x if isinstance(x, list) else []))
    # Robust text fields
    df['description'] = df['description'].fillna("").astype(str)
    df['language'] = df['language'].fillna("missing").astype(str)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)
    # Compose the field used for embeddings
    df['genres'] = df['genres'].apply(lambda g: g if isinstance(g, list) else [])
    df['text_for_embedding'] = df['description'].str.strip() + ". Genres: " + df['genres'].apply(lambda g: ", ".join(g))
    return df

# 1) Load and preprocess dataset
def load_dataset():
    df = pd.read_csv("data/final_data/df_web.csv")
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')

    df['genres'] = df['genres'].apply(ast.literal_eval if isinstance(df['genres'].iloc[0], str) else lambda x: x)
    df['author'] = df['author'].apply(lambda x: [a.strip() for a in x.split(',')] if isinstance(x, str) else (x if isinstance(x, list) else []))
    df['description'] = df['description'].fillna("").astype(str)
    df['language'] = df['language'].fillna("").astype(str)
    df['language_raw'] = df['language']
    df['language_code'] = df['language_raw'].apply(lang_to_iso)
    df['language_display'] = df['language_code'].apply(iso_to_display)
    df['language'] = df['language_display']
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)
    df['genres'] = df['genres'].apply(lambda g: g if isinstance(g, list) else [])
    df['text_for_embedding'] = df['description'].str.strip() + ". Genres: " + df['genres'].apply(lambda g: ", ".join(g))
    return df

# 2) Load embedder
def load_embedder(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    return SentenceTransformer(model_name)

# 3) Build FAISS index
def build_faiss_index(df, embedder):
    texts = df['text_for_embedding'].tolist()
    embeddings = embedder.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    embeddings = embeddings.astype('float32')
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / np.clip(norms, 1e-12, None)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index, embeddings

# 4) Save/load FAISS artifacts
def save_faiss_artifacts(index, embeddings, base_path="data/final_data"):
    os.makedirs(base_path, exist_ok=True)
    faiss.write_index(index, os.path.join(base_path, "faiss_index_ip.idx"))
    np.save(os.path.join(base_path, "embeddings_ip.npy"), embeddings)

def load_faiss_artifacts(base_path="data/final_data"):
    idx_path = os.path.join(base_path, "faiss_index_ip.idx")
    emb_path = os.path.join(base_path, "embeddings_ip.npy")
    if os.path.exists(idx_path) and os.path.exists(emb_path):
        index = faiss.read_index(idx_path)
        embeddings = np.load(emb_path)
        return index, embeddings
    return None, None

# 5) Recommender
def semantic_recommend(query, df, embedder, faiss_index, top_n=5, language=None, min_rating=0.0):
    if not query or not query.strip():
        return None, "Please enter a description or idea for the book you want."

    q_vec = embedder.encode([query], convert_to_numpy=True).astype('float32')
    q_vec = q_vec / np.clip(np.linalg.norm(q_vec, axis=1, keepdims=True), 1e-12, None)

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
