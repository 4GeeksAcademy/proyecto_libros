import pandas as pd
import numpy as np
import os
import re
import streamlit as st  
from utils.language import lang_to_iso, iso_to_display
from utils.sorting import sort_lns_iterable


@st.cache_resource
def load_dataset():
    df = pd.read_csv("data/final_data/df_web.csv")
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')
    df['genres'] = df['genres'].apply(eval if isinstance(df['genres'].iloc[0], str) else lambda x: x)
    df['author'] = df['author'].apply(lambda x: [a.strip() for a in x.split(',')])
    return df
df_filter_model = load_dataset()

def load_df(csv_path: str):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found at {csv_path}")
    df = pd.read_csv(csv_path)

    expected_cols = ["title", "author", "rating", "description", "genres", "language", "publisher", "coverImg"]
    for c in expected_cols:
        if c not in df.columns:
            df[c] = np.nan

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    text_cols = ["title", "author", "description", "genres", "language", "publisher", "coverImg"]
    for c in text_cols:
        df[c] = df[c].fillna("").astype(str)

    df["genres"] = (
        df["genres"]
        .str.replace(r"^\[|\]$", "", regex=True)
        .str.replace("'", "", regex=False)
        .str.replace('"', "", regex=False)
        .str.replace(";", ",")
        .str.replace("|", ",")
        .str.replace("  +", " ", regex=True)
        .str.strip()
    )

    # Mapeo de idiomas
    df["language_raw"] = df["language"].astype(str)
    df["language_code"] = df["language_raw"].apply(lang_to_iso)
    df["language"] = df["language_code"].apply(iso_to_display)

    all_genres = sort_lns_iterable({g.strip() for s in df["genres"] if s for g in s.split(",") if g.strip()})
    titles = sort_lns_iterable(set(df["title"]))
    authors = sort_lns_iterable(set(df["author"]))

    return df, all_genres, titles, authors

# Filtro múltiple por campos
def apply_multi_filter(
    df: pd.DataFrame,
    title_kw=None,
    author_kw=None,
    genre_kw=None,
    lang_kw=None,
    pub_kw=None,
    shuffle: bool = True,
    seed: int | None = None,
    limit: int | None = None,
):
    res = df.copy()
    if title_kw:
        res = res[res["title"].str.contains(title_kw, case=False, na=False)]
    if author_kw:
        res = res[res["author"].str.contains(author_kw, case=False, na=False)]
    if genre_kw:
        genre_pattern = "|".join([re.escape(g.strip()) for g in genre_kw])
        res = res[res["genres"].str.contains(genre_pattern, case=False, na=False)]
    if lang_kw:
        res = res[res["language"].str.contains(lang_kw, case=False, na=False)]
    if pub_kw:
        res = res[res["publisher"].str.contains(pub_kw, case=False, na=False)]
    if shuffle and not res.empty:
        # seed=None => distinto orden en cada llamada
        res = res.sample(frac=1, random_state=seed)
    if limit is not None:
        res = res.head(limit)

    return res.reset_index(drop=True)
