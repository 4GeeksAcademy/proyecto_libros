import pandas as pd
import numpy as np
import streamlit as st

def stars(val):
    try:
        r = float(val)
    except Exception:
        return ""
    full = int(round(r))
    full = max(0, min(5, full))  
    return "⭐" * full 

def show_cards(df: pd.DataFrame):
    for _, row in df.iterrows():
        c1, c2 = st.columns([1, 5], vertical_alignment="top")
        with c1:
            url = row.get("coverImg", "")
            if isinstance(url, str) and url and url.lower() != "nan":
                st.image(url, width=100, clamp=True)
        with c2:
            # título + autor + rating
            title = row.get("title","")
            author = row.get("author","")
            if isinstance(author, list):  # por si viene como lista
                author = ", ".join([str(a) for a in author if a])
            st.markdown(f"### {title}")
            st.markdown(f"**Author:** {author}")
            st.markdown(stars(row.get("rating", np.nan)))

            # descripción
            desc = row.get("description","") or ""
            if desc:
                suffix = "…" if len(desc) > 240 else ""
                st.markdown(
                    f"<div style='color:#666'>{desc[:240]}{suffix}</div>",
                    unsafe_allow_html=True
                )

            # idioma + editorial (si existen en este df)
            language = row.get("language", "")
            publisher = row.get("publisher", "")
            if language:
                st.markdown(
                    f"<div style='font-size:0.9em;color:#888'><strong>Language:</strong> {language}</div>",
                    unsafe_allow_html=True
                )
            if publisher:
                st.markdown(
                    f"<div style='font-size:0.9em;color:#888'><strong>Publisher:</strong> {publisher}</div>",
                    unsafe_allow_html=True
                )

            # géneros: acepta string o lista
            genres_raw = row.get("genres", "")
            if isinstance(genres_raw, list):
                gens = [g.strip() for g in genres_raw if str(g).strip()]
            else:
                gens = [g.strip() for g in str(genres_raw).split(",") if g.strip()]
            if gens:
                st.caption(" · ".join(gens))

            # trofeo/awards
            aw_val = row.get("awards", row.get("AWARDS", 0))
            has_award = False
            try:
                has_award = bool(int(aw_val))
            except Exception:
                s = str(aw_val).strip().lower()
                has_award = s in {"true","yes","y","award","awarded","premiado","premiada","1"}
            if has_award:
                st.markdown("<div style='margin-top:1px;font-size:1.2em'>🏆</div>", unsafe_allow_html=True)

        st.markdown("---")
