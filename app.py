import streamlit as st

# Configuração da Página para ocupar toda a largura e manter o estilo high-tech
st.set_page_config(
    page_title="KRONUS ERP",
    page_icon="K",
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
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# BARRA LATERAL (SIDEBAR)
# -------------------------------------------------------------
st.sidebar.markdown("## ⚡ KRONUS ERP")
st.sidebar.markdown("---")

# Seção de Navegação Principal
st.sidebar.markdown("### Navegação Principal")
modulo_selecionado = st.sidebar.selectbox(
    "Selecione o Módulo:",
    ["Módulo eSocial", "Cadastros", "Módulo Contábil"]
)

st.sidebar.markdown("---")

# -------------------------------------------------------------
# CONTEÚDO PRINCIPAL DE ACORDO COM A SEÇÃO SELECIONADA
# -------------------------------------------------------------

if modulo_selecionado == "Cadastros":
    st.title("🗂️ Central de Cadastros")
    st.markdown("Gerencie as informações estruturais do sistema.")
    
    # Sub-seções de Cadastros solicitadas
    tipo_cadastro = st.radio("Selecione o Cadastro:", ["Empresas", "Plano de Contas"])
    
    if tipo_cadastro == "Empresas":
        st.subheader("🏢 Gestão de Empresas")
        st.info("Painel de gerenciamento das empresas cadastradas no sistema.")
        # Aqui entram os campos de cadastro de empresas futuramente
        
    elif tipo_cadastro == "Plano de Contas":
        st.subheader("📑 Plano de Contas")
        st.warning("Área reservada. Aguardando o envio da estrutura completa do plano de contas para importação.")

elif modulo_selecionado == "Módulo eSocial":
    st.title("🏛️ Módulo eSocial")
    st.markdown("Geração e validação de pacotes XML para envio integrado.")
    
    # Seleção de eventos de teste do eSocial
    evento = st.selectbox(
        "Selecione o Evento do eSocial:",
        ["S-1000 - Informações do Empregador", "S-2230 - Afastamento Temporário", "S-1299 - Fechamento de Eventos Periódicos"]
    )
    
    if evento == "S-2230 - Afastamento Temporário":
        st.write("### Parâmetros para o Evento S-2230")
        st.text_input("CPF do Trabalhador")
        st.date_input("Data de Início do Afastamento")
    elif evento == "S-1299 - Fechamento de Eventos Periódicos":
        st.write("### Parâmetros para o Evento S-1299")
        st.text_input("Período de Apuração (MMAAAA)")
    else:
        st.write("Selecione S-2230 ou S-1299 para interagir com a geração dos XMLs de teste.")

elif modulo_selecionado == "Módulo Contábil":
    st.title("📊 Módulo Contábil & DVA")
    st.markdown("Consolidação de demonstrações financeiras e estruturação contábil.")
    st.info("Ambiente corporativo ativo com persistência em CSV.")
    
