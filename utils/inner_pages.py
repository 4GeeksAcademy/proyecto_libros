import streamlit as st

def apply_inner_styles():
    st.markdown("""
    <style>
    
    /* ====== Sidebar (idéntico al de home) ====== */
    [data-testid="stSidebar"] { background-color: #023047; }
    [data-testid="stSidebar"] * { color: white; }
    .sidebar-footer { padding: 12px 8px; }
    .sidebar-footer p { margin: 0 0 8px 0; font-weight: 600; }
    .sidebar-footer .avatars { display:flex; align-items:center; gap:12px; }
    .sidebar-footer .avatar { position:relative; display:inline-block; }
    .sidebar-footer .avatars img {
        width:50px; height:50px; border-radius:50%; object-fit:cover; display:block; cursor:pointer;
    }
    .sidebar-footer .avatar .tooltip{
        visibility:hidden; opacity:0; position:absolute; bottom:-28px; left:50%;
        transform:translateX(-50%); background:#219EBC; color:#023047; padding:4px 8px;
        border-radius:6px; white-space:nowrap; font-size:13px; font-weight:bold;
        transition:opacity .3s ease; pointer-events:none; z-index:10;
    }
    .sidebar-footer .avatar:hover .tooltip{ visibility:visible; opacity:1; }

    /* ====== Estilos de páginas internas ====== */
    .block-container{
        max-width: 1100px;
        margin: 0 auto;
        padding: 40px 30px 0 30px;
    }
    .block-container h1{
        margin-top: 24px;
        font-size: 28px;
        color: #023047;
    }

    </style>
    """, unsafe_allow_html=True)
