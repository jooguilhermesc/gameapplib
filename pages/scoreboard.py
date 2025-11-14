# streamlit_app.py
import streamlit as st
from uuid import uuid4
import pandas as pd
import tomllib
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests

st.set_page_config(page_title="Placar", page_icon="🎯", layout="wide")

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
    "Nota do João",
    "Imagem Capa"
]

# ---------- Estado inicial ----------
if "players" not in st.session_state:
    pid = str(uuid4())
    st.session_state.players = {pid: {"name": "Jogador 1", "score": 0, "rounds": []}}

if "game_name" not in st.session_state:
    st.session_state.game_name = ""

if "round" not in st.session_state:
    st.session_state.round = 1

# ---------- Utilitários ----------
def add_player(name: str | None = None):
    pid = str(uuid4())
    base_name = name.strip() if name and name.strip() else f"Jogador {len(st.session_state.players)+1}"
    completed_rounds = max((len(p["rounds"]) for p in st.session_state.players.values()), default=0)
    st.session_state.players[pid] = {
        "name": base_name,
        "score": 0,
        "rounds": [0] * completed_rounds,  # entra com 0 nas rodadas já concluídas
    }
    # inicializa o valor do widget ANTES da criação do widget (vai ser usado mais abaixo)
    st.session_state[f"score_input_{pid}"] = 0

def remove_player(pid: str):
    if len(st.session_state.players) > 1:
        st.session_state.players.pop(pid, None)
        st.session_state.pop(f"score_input_{pid}", None)

def close_round():
    """Fecha a rodada: grava o placar atual como Rn e zera o contador para a próxima."""
    for pid, data in st.session_state.players.items():
        data.setdefault("rounds", [])
        current = int(data.get("score", 0))
        data["rounds"].append(current)
        data["score"] = 0
        # como estamos chamando isso ANTES de criar widgets, podemos setar o valor do input aqui
        st.session_state[f"score_input_{pid}"] = 0
    st.session_state.round += 1

def reset_all(reset_rounds: bool = False):
    """Zera contadores e widgets. Se reset_rounds=True, limpa histórico e volta à rodada 1."""
    for pid in list(st.session_state.players.keys()):
        st.session_state.players[pid]["score"] = 0
        st.session_state[f"score_input_{pid}"] = 0
        if reset_rounds:
            st.session_state.players[pid]["rounds"] = []
    if reset_rounds:
        st.session_state.round = 1

def measure(text, font):
    """Retorna (largura, altura) usando getbbox, compatível com Pillow 10+."""
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    return w, h

def gerar_imagem_resultado(
    game_name: str,
    df_ranking: pd.DataFrame,
    capa_url: str | None,
    template_path: str,
) -> Image.Image:

    base = Image.open(template_path).convert("RGBA")
    W, H = base.size
    draw = ImageDraw.Draw(base)

    # ------ função de medição compatível com Pillow 10 ------
    def measure(text: str, font: ImageFont.ImageFont):
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    # ------ tamanhos proporcionais à LARGURA ------
    font_title  = ImageFont.truetype(r'pages/font/PressStart2P-Regular.ttf', size=30)   # título
    font_winner = ImageFont.truetype(r'pages/font/PressStart2P-Regular.ttf', size=20)    # vencedor
    font_score  = ImageFont.truetype(r'pages/font/PressStart2P-Regular.ttf', size=20)    # placar

    thumb_size  = int(W * 0.8)  # tamanho da capa do jogo

    # ------------------------------------------------------------
    # 1. Nome do jogo acima do "VENCEDOR!"
    # ------------------------------------------------------------
    texto_jogo = game_name or "Jogo não informado"
    tw, th = measure(texto_jogo, font_title)
    x = (W - tw) // 2
    y = int(H * 0.05)
    draw.text((x, y), texto_jogo, font=font_title, fill="white")

    # ------------------------------------------------------------
    # 2. Capa do jogo abaixo do troféu
    # ------------------------------------------------------------
    trophy_x = int(W * 0.35)
    trophy_y = int(H * 0.25)

    if capa_url:
        try:
            if capa_url.startswith("http"):
                r = requests.get(capa_url, timeout=5)
                r.raise_for_status()
                capa = Image.open(BytesIO(r.content)).convert("RGBA")
            else:
                capa = Image.open(capa_url).convert("RGBA")

            capa.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)
            capa_x = trophy_x
            capa_y = trophy_y + int(H * 0.12)
            base.paste(capa, (capa_x, capa_y), capa)
        except:
            pass

    # ------------------------------------------------------------
    # 3. Nome do vencedor
    # ------------------------------------------------------------
    vencedor = ""
    if not df_ranking.empty:
        vencedor = str(df_ranking.iloc[0]["Jogador"])

    txt = vencedor or "Sem vencedor"
    tw, th = measure(txt, font_winner)

    nome_x = trophy_x + int(W * 0.15)
    nome_y = trophy_y + int(H * 0.03)

    draw.text((nome_x, nome_y), txt, font=font_winner, fill="black")

    # ------------------------------------------------------------
    # 4. Placar final
    # ------------------------------------------------------------
    start_y = int(H * 0.72)
    line_spacing = int(H * 0.015)

    for idx, row in df_ranking.iterrows():
        pos = row.get("Posição", "")
        nome = str(row.get("Jogador", ""))
        pts = row.get("Pontuação", "")
        linha = f"{pos}º  {nome} — {pts} pts"

        tw, th = measure(linha, font_score)
        x = (W - tw) // 2
        draw.text((x, start_y), linha, font=font_score, fill="white")
        start_y += th + line_spacing

    return base

# ---------- PROCESSADOR DE AÇÕES PENDENTES (antes de renderizar widgets) ----------
# Quando clicar no botão, setamos um flag e damos st.rerun().
# Aqui no topo, consumimos esse flag e executamos a ação com segurança.

if st.session_state.pop("_do_reset_all", False):
    reset_all(reset_rounds=False)  # mude pra True se quiser limpar R1, R2, ...
    # não chama st.rerun aqui; deixamos seguir o fluxo já com estado atualizado

if st.session_state.pop("_do_close_round", False):
    close_round()
    # idem: sem rerun aqui; a UI já vai nascer com tudo zerado

# ---------- UI ----------
st.title("🎯 Placar")

# Nome do jogo
with st.container(border=True):
    # extrai os nomes da coluna
    lista_jogos = df["Nome do Jogo"].dropna().unique().tolist()

    # mantém seleção anterior se existir
    if st.session_state.game_name in lista_jogos:
        idx = lista_jogos.index(st.session_state.game_name)
    else:
        idx = 0

    escolha = st.selectbox(
        "Nome do jogo",
        options=lista_jogos,
        index=idx,
        key="game_name_select"
    )

    # salva no session_state com o mesmo nome que você usa em todo o app
    st.session_state.game_name = escolha

# Lista de jogadores
st.subheader("Jogadores")
for pid, data in list(st.session_state.players.items()):
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
            # garante que o widget nasce com o valor do estado
            if f"score_input_{pid}" not in st.session_state:
                st.session_state[f"score_input_{pid}"] = int(score)
            novo_valor = st.number_input(
                "Pontos (edição manual)",
                value=int(st.session_state[f"score_input_{pid}"]),
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

        # display do placar da rodada atual
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

# Barra inferior
st.divider()
cA, cB, cC, cD = st.columns([1, 1, 3, 4])
with cA:
    if st.button("Zerar todos", use_container_width=True):
        st.session_state._do_reset_all = True
        st.rerun()
with cB:
    if st.button("Adicionar jogador rápido", use_container_width=True):
        add_player(None)
        st.rerun()
with cC:
    if st.button(f"Fechar rodada #{st.session_state.round}", use_container_width=True):
        st.session_state._do_close_round = True
        st.rerun()
with cD:
    st.caption("Ao fechar, o contador zera e a próxima rodada começa do 0. A pontuação total é a soma de todas as rodadas.")

# Classificação
titulo_class = "Classificação"
if st.session_state.game_name.strip():
    titulo_class += f" — {st.session_state.game_name.strip()}"
st.subheader(titulo_class + f"  |  Rodada atual: {st.session_state.round}")

# Ordena por total (soma das rodadas)
def total_points(data: dict) -> int:
    return int(sum(data.get("rounds", [])))

ranking_items = sorted(
    st.session_state.players.items(),
    key=lambda kv: total_points(kv[1]),
    reverse=True
)

# Colunas dinâmicas por rodada
max_rounds = max((len(data.get("rounds", [])) for _, data in ranking_items), default=0)
round_cols = [f"Rodada {i}" for i in range(1, max_rounds + 1)]

rows = []
for pos, (pid, data) in enumerate(ranking_items, start=1):
    rounds = list(data.get("rounds", []))
    if len(rounds) < max_rounds:
        rounds += [0] * (max_rounds - len(rounds))
    row = {
        "Posição": pos,
        "Jogador": data["name"],
        **{col: int(rounds[i]) for i, col in enumerate(round_cols)},
        "Pontuação": int(sum(rounds)),  # soma das rodadas
    }
    rows.append(row)

df_ranking = pd.DataFrame(rows)

# Tabela interativa sem índice
st.dataframe(df_ranking, hide_index=True, use_container_width=True)

st.divider()
st.subheader("📤 Compartilhar resultado da partida")

if st.button("Gerar imagem do resultado", use_container_width=True):
    # pega capa do jogo a partir do df_jogos
    jogo_atual = st.session_state.game_name
    capa_url = None
    try:
        linha_jogo = df.loc[df["Nome do Jogo"] == jogo_atual]
        if not linha_jogo.empty:
            capa_url = str(linha_jogo.iloc[0]["Imagem Capa"])
    except Exception:
        capa_url = None

    img = gerar_imagem_resultado(
        game_name=jogo_atual,
        df_ranking=df_ranking,
        capa_url=capa_url,
        template_path="pages/img/template.png",  # ajusta o caminho
    )

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    img_bytes = buf.getvalue()

    st.image(img, caption="Prévia do resultado", use_container_width=True)

    st.download_button(
        "Baixar imagem do resultado",
        data=img_bytes,
        file_name=f"resultado_{jogo_atual or 'partida'}.png",
        mime="image/png",
        use_container_width=True,
    )
