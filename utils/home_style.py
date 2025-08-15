import streamlit as st
import base64
from functools import lru_cache


def load_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def apply_css_styles():
    st.markdown("""
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    .logo-top-left {
        position: absolute;
        top: 40px;
        left: 30px;
        z-index: 10;
    }
    .title-block {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 60px 80px 120px 80px;
        position: relative;
    }
    .title-text h1 {
        font-size: 50px;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }
    .reader-img {
        position: relative;
        z-index: 4;
    }
    .bg-shape {
        position: absolute;
        right: 50px;
        top: 0px;
        z-index: 2;
        width: 400px;
    }
    .how-section {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: -150px;
        margin-bottom: 100px;
        gap: 40px;
        padding: 0 40px;
        position: relative;
        z-index: 1;
    }

    .how-box {
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        padding: 30px 40px;
        max-width: 800px;
        margin: auto;
        position: relative;
        z-index: 1;
    }

    .how-content {
        display: flex;
        align-items: center;
        position: relative;
    }

    .how-img {
        width: 300px;
        position: relative;
        z-index: 2;
        margin-left: -150px;
        margin-right: 20px;
        flex-shrink: 0;
    }

    .how-card {
        font-size: 17px;
        max-width: 500px;
    }

    .how-card h3 {
        margin-top: 0;
    }

    .how-box img {
        width: 300px;
        margin-right: 20px;
        flex-shrink: 0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #023047;
    }
    [data-testid="stSidebar"] * {
        color: white;
    }
    [data-testid="stSidebar"] .css-1v3fvcr {
        color: #FFD166 !important;
        font-weight: bold;
    }
    .sidebar-footer .avatars {
    display: flex;
    align-items: center;
    gap: 12px;
}

.sidebar-footer .avatar {
    position: relative;
    display: inline-block;
}
    
    .sidebar-footer .avatars img {
    width: 50px;
    height: 50px;
    cursor: pointer;
    display: block;
}
    .sidebar-footer .avatar .tooltip {
    visibility: hidden;
    opacity: 0;
    position: absolute;
    bottom: -28px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #219EBC;
    color: #023047;
    padding: 4px 8px;
    border-radius: 6px;
    white-space: nowrap;
    font-size: 13px;
    font-weight: bold;
    transition: opacity 0.3s ease;
    pointer-events: none;
    z-index: 10;
}

.sidebar-footer .avatar:hover .tooltip {
    visibility: visible;
    opacity: 1;
}

    </style>
    """, unsafe_allow_html=True)

def render_logo(path="images/logo readmeup.png"):
    logo = load_image_base64(path)
    st.markdown(f"""
    <div class="logo-top-left">
        <img src="data:image/png;base64,{logo}" width="180">
    </div>
    """, unsafe_allow_html=True)

@lru_cache(maxsize=None)
def _img_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def render_sidebar():
    elena = _img_b64("images/Elena.png")
    sami = _img_b64("images/Sami.png")
    noemi = _img_b64("images/Noemi.png")

    st.sidebar.markdown(
    f"""
    <div class="sidebar-footer">
        <p>Designed by</p>
        <div class="avatars">
            <span class="avatar">
                <img src="data:image/png;base64,{noemi}" alt="Noemí">
                <span class="tooltip">Noemí</span>
            </span>
            <span class="avatar">
                <img src="data:image/png;base64,{sami}" alt="Sami">
                <span class="tooltip">Sami</span>
            </span>
            <span class="avatar">
                <img src="data:image/png;base64,{elena}" alt="Elena">
                <span class="tooltip">Elena</span>
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
