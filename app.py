import streamlit as st

# Configuração da Página para ocupar toda a largura e manter o estilo high-tech
st.set_page_config(
    page_title="KRONUS ERP",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada (Estilo High-Tech: Preto fosco e azul neon)
st.markdown("""
    <style>
        /* Fundo geral da aplicação */
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        /* Estilização da barra lateral */
        [data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }
        /* Estilização de títulos e textos */
        h1, h2, h3 {
            color: #58a6ff;
        }
        /* Ajuste finos nos botões do menu lateral para parecerem itens de ERP */
        .stButton button {
            width: 100%;
            text-align: left;
            background-color: #21262d;
            color: #ffffff;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 8px 12px;
            margin-bottom: 4px;
        }
        .stButton button:hover {
            background-color: #30363d;
            border-color: #58a6ff;
            color: #58a6ff;
        }
    </style>
""", unsafe_allow_html=True)

# Inicializa o estado da navegação se não existir
if 'menu_ativo' not in st.session_state:
    st.session_state.menu_ativo = "Início"

# -------------------------------------------------------------
# BARRA LATERAL (SIDEBAR) - NAVEGAÇÃO ESTILO ERP
# -------------------------------------------------------------
st.sidebar.markdown("## ⚡ KRONUS ERP")
st.sidebar.markdown("---")

st.sidebar.markdown("### Navegação Principal")

# Substituindo o selectbox por botões organizados em estilo de lista/acordeão (semelhante ao MarketUP)
if st.sidebar.button("🏠 Início / Dashboard"):
    st.session_state.menu_ativo = "Início"

# Seção de Cadastros Expansível
with st.sidebar.expander("📁 Cadastros", expanded=True):
    if st.button("🏢 Empresas"):
        st.session_state.menu_ativo = "Empresas"
    if st.button("📑 Plano de Contas"):
        st.session_state.menu_ativo = "Plano de Contas"

# Seção de Módulos Expansível
with st.sidebar.expander("⚙️ Módulos do Sistema", expanded=True):
    if st.button("🏛️ Módulo eSocial"):
        st.session_state.menu_ativo = "eSocial"
    if st.button("📊 Módulo Contábil"):
        st.session_state.menu_ativo = "Contábil"

st.sidebar.markdown("---")
st.sidebar.caption("Krono System - High-Tech ERP")

# -------------------------------------------------------------
# CONTEÚDO PRINCIPAL DE ACORDO COM A SELEÇÃO
# -------------------------------------------------------------

if st.session_state.menu_ativo == "Início":
    st.title("⚡ Bem-vindo ao KRONUS ERP")
    st.markdown("Selecione uma opção no menu lateral esquerdo para navegar pelos módulos e cadastros.")

elif st.session_state.menu_ativo == "Empresas":
    st.title("🏢 Gestão de Empresas")
    st.markdown("Painel de gerenciamento e cadastro das empresas parceiras.")
    st.info("Utilize o menu lateral para alternar entre as seções.")

elif st.session_state.menu_ativo == "Plano de Contas":
    st.title("📑 Plano de Contas")
    st.markdown("Estruturação e diretrizes contábeis.")
    st.warning("Área reservada. Aguardando o envio da estrutura completa do plano de contas para importação.")

elif st.session_state.menu_ativo == "eSocial":
    st.title("🏛️ Módulo eSocial")
    st.markdown("Geração e validação de pacotes XML para envio integrado.")
    
    # Seleção de eventos de teste do eSocial limpa
    evento = st.selectbox(
        "Selecione o Evento do eSocial:",
        ["Selecione...", "S-1000 - Informações do Empregador", "S-2230 - Afastamento Temporário", "S-1299 - Fechamento de Eventos Periódicos"]
    )
    
    if evento == "S-2230 - Afastamento Temporário":
        st.write("### Parâmetros para o Evento S-2230")
        st.text_input("CPF do Trabalhador")
        st.date_input("Data de Início do Afastamento")
    elif evento == "S-1299 - Fechamento de Eventos Periódicos":
        st.write("### Parâmetros para o Evento S-1299")
        st.text_input("Período de Apuração (MMAAAA)")

elif st.session_state.menu_ativo == "Contábil":
    st.title("📊 Módulo Contábil & DVA")
    st.markdown("Consolidação de demonstrações financeiras e estruturação contábil.")
