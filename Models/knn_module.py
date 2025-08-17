import pandas as pd
import numpy as np
import os
import ast
from sklearn.neighbors import NearestNeighbors
import random
import streamlit as st

@st.cache_resource
def load_dataset():
    df = pd.read_csv("data/final_data/df_web.csv")
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')
    df['genres'] = df['genres'].apply(ast.literal_eval if isinstance(df['genres'].iloc[0], str) else lambda x: x)
    df['author'] = df['author'].apply(lambda x: [a.strip() for a in x.split(',')])
    df['normalized_title'] = df['title'].str.strip().str.lower()
    return df

def load_df_knn(csv_path):
    df = pd.read_csv(csv_path)

    def safe_parse_author(x):
        if isinstance(x, str):
            try:
                val = ast.literal_eval(x)
                return val if isinstance(val, list) else [str(val)]
            except:
                return [x]
        elif isinstance(x, list):
            return x
        else:
            return []

    df["author"] = df["author"].apply(safe_parse_author)

    def safe_parse_genres(x):
        if isinstance(x, str):
            try:
                val = ast.literal_eval(x)
                return val if isinstance(val, list) else [str(val)]
            except:
                return [g.strip() for g in x.replace("[","").replace("]","").replace("'", "").split(",")]
        elif isinstance(x, list):
            return x
        else:
            return []

    df["genres"] = df["genres"].apply(safe_parse_genres)

    df["normalized_title"] = df["title"].str.lower().str.strip()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0.0)

    return df

def knn_recommend(book_title, exclude_series, exclude_author, top_n, df, embeddings, knn_model, pool_factor=5):
    """
    Devuelve recomendaciones en orden aleatorio a partir de un pool de vecinos cercanos.
    Siempre devuelve (DataFrame, mensaje).
    """
    book_title = book_title.lower().strip()
    if book_title not in df["normalized_title"].values:
        return pd.DataFrame(), "Book not found in the dataset."

    idx = df[df["normalized_title"] == book_title].index[0]

    # Pool de vecinos (más que top_n) para poder aleatorizar
    # +1 para incluir el propio libro y poder filtrarlo
    pool_n = min(len(df) - 1, max(top_n * pool_factor, top_n + 10))
    _, indices = knn_model.kneighbors([embeddings[idx]], n_neighbors=pool_n + 1)

    candidates = []
    ref_row = df.iloc[idx]

    for i in indices[0]:
        if i == idx:
            continue  # saltar el propio libro
        row = df.iloc[i]

        # Excluir misma serie (maneja NaN/None)
        if exclude_series:
            s_ref = str(ref_row.get("series", "") or "").strip().lower()
            s_row = str(row.get("series", "") or "").strip().lower()
            if s_ref and s_row and s_ref == s_row:
                continue

        # Excluir mismo autor (listas)
        if exclude_author:
            a_ref = set(ref_row["author"]) if isinstance(ref_row["author"], list) else {ref_row["author"]}
            a_row = set(row["author"]) if isinstance(row["author"], list) else {row["author"]}
            if a_ref & a_row:
                continue

        candidates.append(row)

    if not candidates:
        return pd.DataFrame(), "No recommendations found with the current filters."

    # Aleatoriza y corta a top_n
    random.shuffle(candidates)
    results = candidates[:top_n]

    return pd.DataFrame(results), f"Books similar to: **{ref_row['title']}**"

def prepare_knn(df, embedding_matrix):
    model = NearestNeighbors(metric="cosine", algorithm="brute")
    model.fit(embedding_matrix)
    return model

