import streamlit as st
import numpy as np
from Models.knn_module import load_df_knn, knn_recommend, prepare_knn
from utils.home_style import render_logo, render_sidebar
from utils.inner_pages import apply_inner_styles
from utils.cards import show_cards

st.set_page_config(page_title="ReadMeUp – Smart Match", layout="wide", initial_sidebar_state="expanded")
apply_inner_styles()
render_logo()
render_sidebar()

st.title("Which book did you like? Find other similar ones.")

DATA_CSV = 'data/final_data/df_web.csv'
EMBEDDING_PATH = 'data/final_data/embeddings.npy'

df = load_df_knn(DATA_CSV)
embedding_matrix = np.load(EMBEDDING_PATH)
knn_model = prepare_knn(df, embedding_matrix)

book_query = st.text_input("Type a book title:")

if book_query:
    filtered_titles = df[df["normalized_title"].str.contains(book_query.strip().lower())]["title"].tolist()
else:
    filtered_titles = []

selected_book = st.selectbox("Select a book from the list:", filtered_titles) if filtered_titles else None

exclude_series = st.checkbox("Exclude same series", value=True)
exclude_author = st.checkbox("Exclude same author", value=False)
top_knn = st.slider("How many recommendations?", 3, 15, 5)

if st.button("Find Similar Books", type="primary") and selected_book:
    recs, msg = knn_recommend(
        selected_book, exclude_series, exclude_author, top_knn, df, embedding_matrix, knn_model
    )
    st.markdown(msg)

    if recs.empty:
        st.warning("No recommendations found. Check spelling or try another title.")
    else:
        show_cards(recs)