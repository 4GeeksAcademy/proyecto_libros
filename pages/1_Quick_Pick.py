import streamlit as st
import numpy as np
from Models.cribado import load_df, apply_multi_filter
from utils.home_style import render_logo, render_sidebar
from utils.inner_pages import apply_inner_styles
from utils.cards import show_cards
from utils.sorting import sort_df_by_title_lns, sort_lns_iterable

st.set_page_config(page_title="ReadMeUp – Quick_Pick", layout="wide", initial_sidebar_state="expanded")

# Estilos y logo
apply_inner_styles()
render_logo()
render_sidebar()

DATA_CSV = 'data/final_data/df_web.csv'

with st.spinner("Loading data..."):
    df, GENRES, TITLES, AUTHORS = load_df(DATA_CSV)

st.title("Personalized recommendations based on your tastes")

col1, col2, col3 = st.columns(3)
with col1:
    title_kw = st.text_input("Search by title")
with col2:
    author_kw = st.text_input("Search by author")
with col3:
    genre_kw = st.multiselect("Select genre(s)", GENRES)

col4, col5 = st.columns(2)
with col4:
    lang_kw = st.selectbox("Language", [""] + sort_lns_iterable(df["language"].unique()))
with col5:
    pub_kw = st.text_input("Search by publisher")

results = apply_multi_filter(df, title_kw, author_kw, genre_kw, lang_kw, pub_kw)

order_by = st.selectbox("Sort results by", ["rating (high to low)", "title (A-Z)"])
if order_by == "rating (high to low)":
    results = results.sort_values(by="rating", ascending=False)
else:
    results = sort_df_by_title_lns(results)

st.subheader(f"Results ({len(results)})")
page_size = st.selectbox("Results per page", [10, 20, 30], index=1)
n_pages = max(1, int(np.ceil(len(results) / page_size)))
page = st.number_input("Page", 1, n_pages, 1)
start = (page - 1) * page_size
end = start + page_size

show_cards(results.iloc[int(start):int(end)])
