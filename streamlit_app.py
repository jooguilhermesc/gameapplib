import streamlit as st
import pandas as pd

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



df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQG4C5rdmrOOERNB0ICvSSI3GXBICH2z_Vwj-ojGY7l-3PuC9WkvkdLsxFaOMlM7dUp3pqXLQaEh680/pub?gid=0&single=true&output=csv")

df.columns = [
    "Nome do Jogo",
    "Já Foi Jogado?",
    "Categoria",
    "Subcategoria",
    "Mecânica Principal",
    "Tema",
    "Idade Mínima",
    "Mínimo de Jogadores",
    "Máximo de Jogadores",
    "Mantenedor",
    "Descrição do Jogo",
    "Nota da Laura",
    "Nota do João"
]

df = to_numeric(df, ["Idade Mínima", "Mínimo de Jogadores", "Máximo de Jogadores"])

st.title("Bem ao vindo MetaGame - Nossa biblioteca de jogos!")

st.markdown("""
    **Categoria (`dsc_categoria`):**
    - **Tabuleiro:** Jogos cujo foco principal é o tabuleiro.  
    - **Cartas:** Jogos que giram em torno de cartas como elemento central.  
    - **Dados:** Jogos baseados em rolagem de dados.

    **Subcategoria (`dsc_subcategoria`):**
    - **Clássico:** Jogos tradicionais, com mecânicas simples.  
    - **Cozy:** Jogos leves e divertidos para poucas pessoas.  
    - **Dupla:** Projetados exclusivamente para duas pessoas.  
    - **Party:** Jogos festivos e sociais, para grupos grandes.  
    - **Eurogame:** Jogos modernos com mecânicas estratégicas e pouca sorte envolvida.  
    - **RPG:** Jogos com narrativa ou progressão de personagem, mas sem mestre fixo.

    **Mecânica Principal (`dsc_mecanica_principal`):**
    - **Alocação de Recursos:** Envolve gerenciar e distribuir recursos limitados.  
    - **Apostas:** Baseados em sorte, blefe ou risco calculado.  
    - **Deck Building:** Construção e otimização de baralhos.  
    - **Dungeon Crawler:** Exploração de tabuleiros e combate em fases.  
    - **Gerenciamento de Mãos:** Combinações estratégicas de cartas ou peças.  
    - **Quebra-Cabeça:** Requer raciocínio lógico, memória ou reflexos.  
    - **Quiz:** Perguntas e respostas como base da jogabilidade.  
    - **Vários:** Mistura de várias mecânicas dentro de um mesmo jogo.
    """)

st.sidebar.header("Filtros")

# Texto
busca_nome = st.sidebar.text_input("Nome do Jogo (contém)")

# Listas (opções distintas)
sel_jogado = multiselect_all("Já Foi Jogado?", df["Já Foi Jogado?"].unique())
sel_categoria = multiselect_all("Categoria", df["Categoria"].unique())
sel_subcat = multiselect_all("Subcategoria", df["Subcategoria"].unique())
sel_mecanica = multiselect_all("Mecânica Principal", df["Mecânica Principal"].unique())
sel_tema = multiselect_all("Tema", df["Tema"].unique())
sel_mantenedor = multiselect_all("Mantenedor", df["Mantenedor"].unique())

# Intervalos com valores distintos
idade_min, idade_max, _ = range_from_distinct("Idade Mínima (intervalo por valores distintos)", df["Idade Mínima"])
jmin_min, jmin_max, _ = range_from_distinct("Mínimo de Jogadores (intervalo)", df["Mínimo de Jogadores"])
jmax_min, jmax_max, _ = range_from_distinct("Máximo de Jogadores (intervalo)", df["Máximo de Jogadores"])

# ===== Aplica filtros =====
dff = df.copy()

if busca_nome:
    dff = dff[dff["Nome do Jogo"].str.contains(busca_nome, case=False, na=False)]

if sel_jogado:
    dff = dff[dff["Já Foi Jogado?"].isin(sel_jogado)]
if sel_categoria:
    dff = dff[dff["Categoria"].isin(sel_categoria)]
if sel_subcat:
    dff = dff[dff["Subcategoria"].isin(sel_subcat)]
if sel_mecanica:
    dff = dff[dff["Mecânica Principal"].isin(sel_mecanica)]
if sel_tema:
    dff = dff[dff["Tema"].isin(sel_tema)]
if sel_mantenedor:
    dff = dff[dff["Mantenedor"].isin(sel_mantenedor)]

if idade_min is not None and idade_max is not None:
    dff = dff[dff["Idade Mínima"].between(idade_min, idade_max, inclusive="both")]
if jmin_min is not None and jmin_max is not None:
    dff = dff[dff["Mínimo de Jogadores"].between(jmin_min, jmin_max, inclusive="both")]
if jmax_min is not None and jmax_max is not None:
    dff = dff[dff["Máximo de Jogadores"].between(jmax_min, jmax_max, inclusive="both")]

# ===== Resultado =====
st.caption(f"Mostrando {len(dff)} de {len(df)} jogos")

st.dataframe(dff, use_container_width=True, hide_index=True)