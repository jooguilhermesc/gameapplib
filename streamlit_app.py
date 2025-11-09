import tomllib
from utils import to_numeric, multiselect_all, range_from_distinct
import streamlit as st
import pandas as pd

@st.dialog("📘 Detalhes do Jogo")
def show_game_details(r):
    st.subheader(r["Nome do Jogo"])
    st.markdown(
        f"""
**Descrição:** {r['Descrição do Jogo'] or '—'}  

**Categoria:** {r['Categoria'] or '—'}  
**Subcategoria:** {r['Subcategoria'] or '—'}  
**Mecânica Principal:** {r['Mecânica Principal'] or '—'}  
**Tema:** {r['Tema'] or '—'}  

**Idade Mínima:** {int(r['Idade Mínima']) if pd.notna(r['Idade Mínima']) else '—'}  
**Jogadores:** {int(r['Mínimo de Jogadores']) if pd.notna(r['Mínimo de Jogadores']) else '—'}–{int(r['Máximo de Jogadores']) if pd.notna(r['Máximo de Jogadores']) else '—'}  
**Mantenedor:** {r['Mantenedor'] or '—'}  

**Nota da Laura:** {r['Nota da Laura'] if pd.notna(r['Nota da Laura']) else '—'}  
**Nota do João:** {r['Nota do João'] if pd.notna(r['Nota do João']) else '—'}
        """.strip()
    )

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

game_csv_path = config["paths"]["game_csv"]

df = pd.read_csv(game_csv_path)

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

st.set_page_config(page_title="Metagame - Nossa biblioteca de jogos!", page_icon="🎲", layout="wide")

st.title("Bem vindo ao MetaGame - Nossa biblioteca de jogos!")

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
idade_min, idade_max, _ = range_from_distinct("Idade Mínima", df["Idade Mínima"])
jmin_min, jmin_max, _ = range_from_distinct("Mínimo de Jogadores", df["Mínimo de Jogadores"])
jmax_min, jmax_max, _ = range_from_distinct("Máximo de Jogadores", df["Máximo de Jogadores"])

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

# st.dataframe(dff, use_container_width=False, hide_index=True)

# ---- Lista dinâmica de botões a partir do dff ----
# Guardamos a seleção em session_state para persistir após o clique
if "selected_idx" not in st.session_state:
    st.session_state.selected_idx = None

# Grade de botões (3 colunas por linha, ajuste à vontade)
cols_per_row = 3
rows = []
current_row = st.columns(cols_per_row)

for i, (idx, row) in enumerate(dff.iterrows()):
    col = current_row[i % cols_per_row]
    with col:
        clicked = st.button(row["Nome do Jogo"], key=f"btn_{idx}", use_container_width=True)
        if clicked:
            st.session_state.selected_idx = idx
            # abre o diálogo com as informações do jogo clicado
            show_game_details(row)