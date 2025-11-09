import pandas as pd
import streamlit as st

def to_numeric(df, cols):
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def multiselect_all(label, options):
    options = sorted([o for o in options if pd.notna(o)])
    return st.sidebar.multiselect(label, options, default=options)

def range_from_distinct(label, series):
    opts = sorted([int(x) for x in pd.Series(series).dropna().unique().tolist()])
    if not opts:
        return None, None, []
    if len(opts) == 1:
        sel = (opts[0], opts[0])
    else:
        sel = st.sidebar.select_slider(label, options=opts, value=(opts[0], opts[-1]))
    return sel[0], sel[1], opts

def render_game_thumbnail(nome_jogo, img_url):
    """Renderiza a miniatura do jogo — imagem se existir, senão iniciais."""
    # Imagem válida
    st.markdown(
        f"""
        <div style="text-align:center;">
            <img src="{img_url}" 
                width="70" 
                height="70"
                style="border-radius:10px;
                        margin-bottom:8px;
                        object-fit:cover;
                        max-height:70px;">
            <p style="font-size:0.8em; font-weight:600; margin:0;">{nome_jogo}</p>
        </div>
        """,
        unsafe_allow_html=True
    )