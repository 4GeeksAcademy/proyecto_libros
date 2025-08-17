import streamlit as st
import numpy as np
from Models.knn_module import load_df_knn, knn_recommend, prepare_knn
from utils.home_style import render_logo, render_sidebar
from utils.inner_pages import apply_inner_styles, set_tab_title, force_sidebar
from utils.cards import show_cards

apply_inner_styles()
render_logo()
render_sidebar()

set_tab_title("ReadMeUp – Smart Match") 
force_sidebar("expanded") 
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

c1, c2, c3 = st.columns([1, 1, 1]) 

with c1:
    exclude_series = st.checkbox("Exclude same series", value=True)

with c2:
    exclude_author = st.checkbox("Exclude same author", value=False)

with c3:
    top_knn = st.slider("Recommendations", 3, 15, 5)
    
if st.button("Find Similar Books", type="primary") and selected_book:
    recs, msg = knn_recommend(
        selected_book, exclude_series, exclude_author, top_knn, df, embedding_matrix, knn_model
    )
    st.markdown(msg)

    if recs.empty:
        st.warning("No recommendations found. Check spelling or try another title.")
    else:
        show_cards(recs)