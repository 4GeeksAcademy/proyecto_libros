import streamlit as st
from utils.home_style import apply_css_styles, render_logo, load_image_base64, render_sidebar

st.set_page_config(page_title="ReadMeUp", layout="wide", initial_sidebar_state="expanded")

# Estilos y logo
apply_css_styles()
render_logo()
render_sidebar() 

# Imágenes
reader = load_image_base64("images/background-1.png")
how = load_image_base64("images/pila-libros.png")
bg = load_image_base64("images/Vector.png")
flechas = load_image_base64("images/flechas.png")
lupa = load_image_base64("images/lupa.png")
check = load_image_base64("images/check.png")


# TITULAR Y LECTORA
st.markdown(f"""
<div class="title-block">
    <div class="title-text">
        <h1>Let ReadMeUp help<br>you find your next favorite story.</h1>
    </div>
    <img src="data:image/png;base64,{bg}" class="bg-shape">
    <img src="data:image/png;base64,{reader}" width="320" class="reader-img">
</div>
""", unsafe_allow_html=True)

# SECCIÓN HOW IT WORKS
st.markdown(f"""
<div class="how-section">
    <div class="how-box">
        <div class="how-content">
            <img src="data:image/png;base64,{how}" class="how-img">
            <div class="how-card">
                <h3>How it works:</h3>
                <ul style="line-height: 1.8; list-style: none; padding-left: 0;">
                    <li><img src="data:image/png;base64,{flechas}" style="width: 24px; height: 24px; vertical-align: middle; margin-right: 6px;"> Tap the menu in the top right corner</li>
                    <li><img src="data:image/png;base64,{lupa}" style="width: 24px; height: 24px; vertical-align: middle; margin-right: 6px;"> Choose how you'd like to search for your next book</li>
                    <li><img src="data:image/png;base64,{check}" style="width: 24px; height: 24px; vertical-align: middle; margin-right: 6px;"> Click the search button — and you're all set!</li>
                </ul>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)