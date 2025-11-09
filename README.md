Perfeito — aqui está o markdown completo, agora com uma seção de **exemplos visuais e explicação das colunas e filtros**. Fica pronto para virar o `README.md` do teu app:

---

# 🎲 Biblioteca de Jogos

Um aplicativo interativo feito com **Streamlit** para gerenciar e explorar sua coleção de jogos de tabuleiro.
A ideia é simples: centralizar suas informações sobre jogos — o que você tem, o que já jogou, e o que ainda quer conhecer — de forma bonita, filtrável e fácil de navegar.

[![Abrir no Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://biblioteca-de-jogos.streamlit.app/)

---

## 🧩 Principais Funcionalidades

* Exibição de uma **tabela dinâmica** com informações completas sobre cada jogo.
* **Filtros interativos** por nome, categoria, subcategoria, mecânica principal, tema, faixa etária e número de jogadores.
* Busca rápida por texto e listas suspensas com valores únicos de cada coluna.
* Interface intuitiva e leve, ideal para organizar e explorar sua ludoteca pessoal.

---

## 🧠 Estrutura das Colunas

| Coluna                  | Descrição                                                                                                                                                                                                                                                                                                                                       |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nome do Jogo**        | Título completo do jogo de tabuleiro.                                                                                                                                                                                                                                                                                                           |
| **Já Foi Jogado?**      | Indica se o jogo já foi jogado por você ou pelo grupo.                                                                                                                                                                                                                                                                                          |
| **Categoria**           | Classificação geral (ex: Estratégia, Família, Festivo, Cooperativo).                                                                                                                                                                                                                                                                            |
| **Subcategoria**        | Categoria mais específica dentro do tipo principal (ex: Eurogame, Party Game).                                                                                                                                                                                                                                                                  |
| **Mecânica Principal**  | O tipo de dinâmica central do jogo. Exemplos: <br>• *Alocação de Recursos* – depende de gerir recursos de forma eficiente.<br>• *Apostas* – baseia-se em sorte e blefe.<br>• *Deck Building* – construção de baralhos.<br>• *Dungeon Crawler* – exploração de tabuleiro.<br>• *Gerenciamento de Mãos* – exige combinar cartas estrategicamente. |
| **Tema**                | Ambientação ou narrativa central (ex: Fantasia, Espaço, História, Mistério).                                                                                                                                                                                                                                                                    |
| **Idade Mínima**        | Idade recomendada pelos criadores.                                                                                                                                                                                                                                                                                                              |
| **Mínimo de Jogadores** | Quantidade mínima necessária para jogar.                                                                                                                                                                                                                                                                                                        |
| **Máximo de Jogadores** | Limite máximo de jogadores.                                                                                                                                                                                                                                                                                                                     |
| **Mantenedor**          | Pessoa ou grupo responsável por manter o cadastro no app.                                                                                                                                                                                                                                                                                       |

---

## 🔍 Filtros Disponíveis

| Filtro                  | Tipo           | Descrição                                                |
| ----------------------- | -------------- | -------------------------------------------------------- |
| **Nome do Jogo**        | Campo de texto | Busca parcial por nome.                                  |
| **Já Foi Jogado?**      | Lista suspensa | Exibe as opções distintas (“Sim”, “Não”).                |
| **Categoria**           | Lista suspensa | Filtra pelos tipos de jogos cadastrados.                 |
| **Subcategoria**        | Lista suspensa | Refinamento dentro da categoria principal.               |
| **Mecânica Principal**  | Lista suspensa | Permite focar em jogos com a mesma mecânica central.     |
| **Tema**                | Lista suspensa | Filtra por ambientação ou tema.                          |
| **Idade Mínima**        | Intervalo      | Seleciona jogos adequados à faixa etária desejada.       |
| **Mínimo de Jogadores** | Intervalo      | Permite escolher o número mínimo de jogadores suportado. |
| **Máximo de Jogadores** | Intervalo      | Filtra o número máximo de participantes.                 |
| **Mantenedor**          | Lista suspensa | Exibe jogos por responsável pelo cadastro.               |

---

## 🖼️ Exemplos Visuais

### Tela principal

> Visualização da tabela de jogos com filtros aplicáveis no topo da página.

![Exemplo de Tabela](https://user-images.githubusercontent.com/placeholder/tabela-jogos.png)

### Filtros ativos

> Interface intuitiva com menus suspensos e campos de busca.

![Exemplo de Filtros](https://user-images.githubusercontent.com/placeholder/filtros-jogos.png)

---

## 🚀 Como Executar Localmente

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Rode o aplicativo:

   ```bash
   streamlit run streamlit_app.py
   ```

3. Acesse no navegador:

   ```
   http://localhost:8501
   ```

---

## 💾 Dica

Adicione seu arquivo CSV com os jogos em `data/jogos.csv` e atualize o caminho dentro do script principal para começar a explorar sua coleção.

---

Quer que eu adicione também um **exemplo de dataset fictício (`jogos.csv`)** com umas 10 linhas simulando dados reais de jogos pra quem quiser testar o app localmente? Isso deixaria o README 100% funcional.