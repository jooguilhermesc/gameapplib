# streamlit_app.py
import streamlit as st
from uuid import uuid4
import pandas as pd

st.set_page_config(page_title="Placar", page_icon="🎯", layout="wide")

# ---------- Estado inicial ----------
if "players" not in st.session_state:
    pid = str(uuid4())
    st.session_state.players = {pid: {"name": "Jogador 1", "score": 0, "rounds": []}}  # NEW: rounds

if "game_name" not in st.session_state:
    st.session_state.game_name = ""

# NEW: controle de rodada e baseline de totais
if "round" not in st.session_state:
    st.session_state.round = 1
if "last_totals" not in st.session_state:
    # baseline inicial: total atual de cada jogador
    st.session_state.last_totals = {pid: data.get("score", 0) for pid, data in st.session_state.players.items()}

# utilitário
def add_player(name: str | None = None):
    pid = str(uuid4())
    base_name = name.strip() if name and name.strip() else f"Jogador {len(st.session_state.players)+1}"
    # joga com rounds zerados até a rodada atual - 1
    st.session_state.players[pid] = {"name": base_name, "score": 0, "rounds": [0] * (st.session_state.round - 1)}  # NEW
    st.session_state.last_totals[pid] = 0  # baseline começa do total atual (0)

def remove_player(pid: str):
    if len(st.session_state.players) > 1:
        st.session_state.players.pop(pid, None)
        st.session_state.last_totals.pop(pid, None)

def bump(pid: str, delta: int):
    st.session_state.players[pid]["score"] += delta

# NEW: fechar rodada = calcular deltas e avançar o contador
def close_round():
    for pid, data in st.session_state.players.items():
        # garante chave rounds
        if "rounds" not in data:
            data["rounds"] = []
        prev = st.session_state.last_totals.get(pid, 0)
        cur = int(data.get("score", 0))
        delta = cur - prev
        data["rounds"].append(delta)
        st.session_state.last_totals[pid] = cur
    st.session_state.round += 1

st.title("🎯 Placar")

# ---------- nome do jogo ----------
with st.container(border=True):
    st.text_input(
        "Nome do jogo",
        value=st.session_state.game_name,
        key="game_name",
        placeholder="Ex.: Carcassonne, Azul, Catan..."
    )

# ---------- lista de jogadores ----------
st.subheader("Jogadores")
for pid, data in list(st.session_state.players.items()):
    # retrocompat: garante rounds
    data.setdefault("rounds", [])

    name = data["name"]
    score = data["score"]

    box = st.container(border=True)
    with box:
        top = st.columns([3, 2, 1])
        with top[0]:
            novo_nome = st.text_input(
                "Nome",
                value=name,
                key=f"name_{pid}",
                label_visibility="visible",
            )
            st.session_state.players[pid]["name"] = novo_nome if novo_nome.strip() else name

        with top[1]:
            novo_valor = st.number_input(
                "Pontos (edição manual)",
                value=int(score),
                step=1,
                key=f"score_input_{pid}",
            )
            st.session_state.players[pid]["score"] = int(novo_valor)

        with top[2]:
            st.write("")
            disabled = len(st.session_state.players) <= 1
            if st.button("Remover", key=f"remove_{pid}", disabled=disabled, use_container_width=True):
                remove_player(pid)
                st.rerun()

        # display do total atual (mantido)
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        with col3:
            st.markdown(
                f"""
                <div style="text-align:center;font-size:2rem;font-weight:700;line-height:2.2rem;">
                    {st.session_state.players[pid]["score"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

# ---------- barra inferior ----------
st.divider()
cA, cB, cC = st.columns([1, 1, 6])
with cA:
    if st.button("Zerar todos", use_container_width=True):
        for pid in st.session_state.players:
            st.session_state.players[pid]["score"] = 0
        # zera baselines também
        st.session_state.last_totals = {pid: 0 for pid in st.session_state.players}
        # opcional: zerar rounds/rodada
        # for pid in st.session_state.players: st.session_state.players[pid]["rounds"] = []
        # st.session_state.round = 1
        st.rerun()
with cB:
    if st.button("Adicionar jogador rápido", use_container_width=True):
        add_player(None)
        st.rerun()
with cC:
    if st.button(f"Fechar rodada #{st.session_state.round}", use_container_width=True):  # NEW
        close_round()
        st.rerun()

# ---------- classificação ----------
titulo_class = "Classificação"
if st.session_state.game_name.strip():
    titulo_class += f" — {st.session_state.game_name.strip()}"
st.subheader(titulo_class + f"  |  Rodada atual: {st.session_state.round}")  # NEW

# ordena por total atual
ranking_items = sorted(st.session_state.players.items(), key=lambda kv: kv[1]["score"], reverse=True)

# colunas dinâmicas por rodada
max_rounds = max((len(data.get("rounds", [])) for _, data in ranking_items), default=0)
round_cols = [f"R{i}" for i in range(1, max_rounds + 1)]

rows = []
for pos, (pid, data) in enumerate(ranking_items, start=1):
    rounds = data.get("rounds", [])
    # padding pra alinhar com quem tem mais rodadas
    if len(rounds) < max_rounds:
        rounds = rounds + [0] * (max_rounds - len(rounds))
    row = {
        "Posição": pos,
        "Jogador": data["name"],
        **{col: rounds[i] for i, col in enumerate(round_cols)},
        "Pontuação": int(data["score"]),
    }
    rows.append(row)

df_ranking = pd.DataFrame(rows)

# Tabela interativa sem índice
st.dataframe(df_ranking, hide_index=True, use_container_width=True)