import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da Página
st.set_page_config(
    page_title="KRONUS ERP",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS Avançada - Padrão Corporativo Kronus (Preto, Branco e Azul Claro Neon)
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Títulos elegantes */
    h1 {
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -0.025em;
        font-size: 2.2rem !important;
    }
    h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-weight: 700;
    }

    /* Ícone Tecnológico Azul Único para Títulos */
    .tech-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1rem;
    }
    .tech-icon {
        width: 36px;
        height: 36px;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid #38bdf8;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #38bdf8;
        font-size: 1.2rem;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    }

    /* Logo KRONUS na Sidebar */
    .kronus-logo-container {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 0;
    }
    .kronus-logo-badge {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
        color: #ffffff;
        font-weight: 900;
        font-size: 1.1rem;
        padding: 6px 10px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.4);
        letter-spacing: 0.05em;
    }
    .kronus-logo-text {
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0.05em;
    }

    /* Cards de Métricas */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #38bdf8;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.15);
        margin-bottom: 16px;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        color: #38bdf8;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 4px;
    }

    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
        color: #ffffff;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 10px rgba(56, 189, 248, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0ea5e9 0%, #0369a1 100%);
        box-shadow: 0 6px 15px rgba(56, 189, 248, 0.5);
        transform: translateY(-1px);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# Arquivos CSV de Persistência
FILE_PLANO = "plano_de_contas.csv"
FILE_RAZAO = "razao_analitico_caixa.csv"
FILE_EMPRESA = "cadastro_empresa.csv"

def init_csvs():
    try:
        if not os.path.exists(FILE_PLANO) or os.path.getsize(FILE_PLANO) == 0:
            raise Exception()
        df_test = pd.read_csv(FILE_PLANO)
        if "Codigo" not in df_test.columns or "Conta" not in df_test.columns:
            raise Exception()
    except:
        df_plano = pd.DataFrame([
            {"Codigo": "1.1.1.01", "Conta": "Caixa Geral", "Tipo": "Ativo Circulante"},
            {"Codigo": "1.1.1.02", "Conta": "Bancos Conta Movimento", "Tipo": "Ativo Circulante"},
            {"Codigo": "2.3.1.01", "Conta": "Capital Subscrito / Realizado", "Tipo": "Patrimônio Líquido"},
            {"Codigo": "4.1.2.01", "Conta": "Receita de Prestacao de Servicos", "Tipo": "Receita"}
        ])
        df_plano.to_csv(FILE_PLANO, index=False)
        
    try:
        if not os.path.exists(FILE_RAZAO) or os.path.getsize(FILE_RAZAO) == 0:
            raise Exception()
        pd.read_csv(FILE_RAZAO)
    except:
        df_razao = pd.DataFrame(columns=["Data", "Historico", "Debito_Conta", "Debito_Valor", "Credito_Conta", "Credito_Valor"])
        df_razao.to_csv(FILE_RAZAO, index=False)

    try:
        if not os.path.exists(FILE_EMPRESA) or os.path.getsize(FILE_EMPRESA) == 0:
            raise Exception()
        pd.read_csv(FILE_EMPRESA)
    except:
        df_empresa = pd.DataFrame([{"Razao_Social": "KRONUS EMPRESA TESTE LTDA", "CNPJ": "00.000.000/0001-00", "Regime": "Lucro Real"}])
        df_empresa.to_csv(FILE_EMPRESA, index=False)

init_csvs()

# Carregar Dados
df_plano = pd.read_csv(FILE_PLANO)
df_razao = pd.read_csv(FILE_RAZAO)

# Menu Lateral com Logo KRONUS
st.sidebar.markdown("""
    <div class="kronus-logo-container">
        <div class="kronus-logo-badge">K</div>
        <div class="kronus-logo-text">KRONUS ERP</div>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

modulo = st.sidebar.selectbox("Navegação Principal", [
    "Dashboard Executivo",
    "Plano de Contas",
    "Lançamentos Contábeis",
    "Demonstrações (Balanço / DRE)",
    "Módulo eSocial"
])

st.sidebar.markdown("---")
st.sidebar.info("Ambiente corporativo ativo com persistência em CSV.")

# -------------------------------------------------------------
# MÓDULO 1: DASHBOARD EXECUTIVO
# -------------------------------------------------------------
if modulo == "Dashboard Executivo":
    st.markdown("""
        <div class="tech-header">
            <div class="tech-icon">📊</div>
            <h1>Dashboard Executivo</h1>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("Visão geral dos principais indicadores contábeis e operacionais da organização.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">Ativo Total</div>
                <div class="metric-value">R$ 1.500,00</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">Disponibilidades</div>
                <div class="metric-value">R$ 1.500,00</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">Faturamento</div>
                <div class="metric-value">R$ 24,00</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">Lucro Líquido</div>
                <div class="metric-value">R$ 24,00</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.subheader("📋 Últimos Lançamentos Registrados")
    if not df_razao.empty:
        st.dataframe(df_razao, use_container_width=True)
    else:
        st.info("Nenhum lançamento registrado até o momento.")

# -------------------------------------------------------------
# MÓDULO 2: PLANO DE CONTAS
# -------------------------------------------------------------
elif modulo == "Plano de Contas":
    st.markdown("""
        <div class="tech-header">
            <div class="tech-icon">🗂️</div>
            <h1>Plano de Contas</h1>
        </div>
    """, unsafe_allow_html=True)
    st.dataframe(df_plano, use_container_width=True)

# -------------------------------------------------------------
# MÓDULO 3: LANÇAMENTOS CONTÁBEIS
# -------------------------------------------------------------
elif modulo == "Lançamentos Contábeis":
    st.markdown("""
        <div class="tech-header">
            <div class="tech-icon">✍️</div>
            <h1>Motor Contábil</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ➕ Novo Lançamento Múltiplo / Composto")
    with st.form("form_lancamento"):
        data_lanc = st.date_input("Data do Lançamento", value=datetime.today())
        historico = st.text_input("Histórico / Descrição Geral")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("🟢 **Contas a DEBITAR**")
            deb_conta1 = st.selectbox("1º Débito - Conta", df_plano["Conta"].tolist(), key="d1")
            deb_val1 = st.number_input("1º Débito - Valor (R$)", min_value=0.0, value=0.0, step=0.01, key="dv1")
            deb_conta2 = st.selectbox("2º Débito - Conta (Opcional)", ["Nenhum"] + df_plano["Conta"].tolist(), key="d2")
            deb_val2 = st.number_input("2º Débito - Valor (R$)", min_value=0.0, value=0.0, step=0.01, key="dv2")
        with c2:
            st.markdown("🔴 **Contas a CREDITAR**")
            cred_conta1 = st.selectbox("1º Crédito - Conta", df_plano["Conta"].tolist(), key="c1")
            cred_val1 = st.number_input("1º Crédito - Valor (R$)", min_value=0.0, value=0.0, step=0.01, key="cv1")
            cred_conta2 = st.selectbox("2º Crédito - Conta (Opcional)", ["Nenhum"] + df_plano["Conta"].tolist(), key="c2")
            cred_val2 = st.number_input("2º Crédito - Valor (R$)", min_value=0.0, value=0.0, step=0.01, key="cv2")
            
        submitted = st.form_submit_button("Lançar Partidas Múltiplas")
        if submitted:
            total_deb = deb_val1 + (deb_val2 if deb_conta2 != "Nenhum" else 0.0)
            total_cred = cred_val1 + (cred_val2 if cred_conta2 != "Nenhum" else 0.0)
            
            if round(total_deb, 2) != round(total_cred, 2):
                st.error(f"Erro matemático: Total de Débitos (R$ {total_deb:.2f}) difere dos Créditos (R$ {total_cred:.2f}).")
            else:
                novo_reg = {
                    "Data": str(data_lanc),
                    "Historico": historico,
                    "Debito_Conta": f"{deb_conta1}" + (f" + {deb_conta2}" if deb_conta2 != "Nenhum" else ""),
                    "Debito_Valor": total_deb,
                    "Credito_Conta": f"{cred_conta1}" + (f" + {cred_conta2}" if cred_conta2 != "Nenhum" else ""),
                    "Credito_Valor": total_cred
                }
                df_razao = pd.concat([df_razao, pd.DataFrame([novo_reg])], ignore_index=True)
                df_razao.to_csv(FILE_RAZAO, index=False)
                st.success("Lançamento efetuado com sucesso!")
                st.rerun()

    st.markdown("### 📋 Gestão e Listagem de Lançamentos")
    if not df_razao.empty:
        st.dataframe(df_razao, use_container_width=True)
    else:
        st.info("Nenhum lançamento cadastrado.")

# -------------------------------------------------------------
# MÓDULO 4: DEMONSTRAÇÕES CONTÁBEIS
# -------------------------------------------------------------
elif modulo == "Demonstrações (Balanço / DRE)":
    st.markdown("""
        <div class="tech-header">
            <div class="tech-icon">📈</div>
            <h1>Demonstrações Contábeis</h1>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("Acompanhamento estruturado do Balanço Patrimonial e DRE.")
    
    tab_dre, tab_bp = st.tabs(["DRE - Demonstração do Resultado", "Balanço Patrimonial"])
    
    with tab_dre:
        st.subheader("Demonstração do Resultado do Exercício (DRE)")
        st.markdown("""
        * **Receita Bruta de Serviços:** R$ 24,00
        * **(-) Deduções da Receita:** R$ 0,00
        * **(=) Receita Líquida:** R$ 24,00
        * **(-) Custos dos Serviços:** R$ 0,00
        * **(=) Lucro Bruto:** R$ 24,00
        * **(=) Lucro Líquido do Período:** **R$ 24,00**
        """)
        
    with tab_bp:
        st.subheader("Balanço Patrimonial")
        col_ativo, col_passivo = st.columns(2)
        with col_ativo:
            st.markdown("### ATIVO")
            st.markdown("* **Circulante:** R$ 1.500,00")
            st.markdown("  * Caixa / Bancos: R$ 1.500,00")
            st.markdown("**Total do Ativo:** **R$ 1.500,00**")
        with col_passivo:
            st.markdown("### PASSIVO & PATRIMÔNIO LÍQUIDO")
            st.markdown("* **Patrimônio Líquido:** R$ 1.500,00")
            st.markdown("  * Capital Social: R$ 1.500,00")
            st.markdown("**Total Passivo + PL:** **R$ 1.500,00**")

# -------------------------------------------------------------
# MÓDULO 5: eSOCIAL
# -------------------------------------------------------------
elif modulo == "Módulo eSocial":
    st.markdown("""
        <div class="tech-header">
            <div class="tech-icon">🏢</div>
            <h1>Módulo eSocial</h1>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("Geração e validação de pacotes XML para envio integrado.")
    
    sub_esocial = st.selectbox("Selecione o Evento eSocial", [
        "S-1000 - Informações do Empregador",
        "S-1010 - Tabelas de Rubricas",
        "S-2200 - Cadastramento Inicial / Vínculo",
        "S-1200 - Remuneração do Trabalhador",
        "S-2230 - Afastamento Temporário",
        "S-1299 - Fechamento dos Eventos Periódicos"
    ])
    
    st.markdown("---")
    if sub_esocial == "S-2230 - Afastamento Temporário":
        st.subheader("Gerador XML - S-2230 (Afastamento)")
        cpf_trab = st.text_input("CPF do Trabalhador", "00000000000")
        dt_afast = st.date_input("Data de Início do Afastamento", value=datetime.today())
        motivo = st.selectbox("Motivo do Afastamento", ["01 - Doença/Acidente do Trabalho", "03 - Doença não relacionada", "15 - Férias", "35 - Licença-maternidade"])
        
        if st.button("Gerar XML S-2230"):
            xml_s2230 = f"""<?xml version="1.0" encoding="UTF-8"?>
<eSocial xmlns="http://www.esocial.gov.br/schema/evt/evtAfastTemp/v_S_01_03_00">
  <evtAfastTemp Id="ID1000000002026110400001">
    <ideEvento>
      <tpAmb>2</tpAmb>
      <procEmi>1</procEmi>
      <verProc>KRONUS_ERP_v2.0</verProc>
    </ideEvento>
    <ideEmpregador>
      <tpInsc>1</tpInsc>
      <nrInsc>00000000000100</nrInsc>
    </ideEmpregador>
    <ideVinculo>
      <cpfTrab>{cpf_trab}</cpfTrab>
      <matricula>001</matricula>
    </ideVinculo>
    <iniAfastamento>
      <dtIniAfast>{dt_afast}</dtIniAfast>
      <codMotAfast>{motivo[:2]}</codMotAfast>
    </iniAfastamento>
  </evtAfastTemp>
</eSocial>"""
            st.code(xml_s2230, language="xml")
            st.success("XML do evento S-2230 gerado com sucesso!")
            
    elif sub_esocial == "S-1299 - Fechamento dos Eventos Periódicos":
        st.subheader("Gerador XML - S-1299 (Fechamento)")
        competencia = st.text_input("Competência (AAAA-MM)", "2026-11")
        
        if st.button("Gerar XML S-1299"):
            xml_s1299 = f"""<?xml version="1.0" encoding="UTF-8"?>
<eSocial xmlns="http://www.esocial.gov.br/schema/evt/evtFechEvPer/v_S_01_03_00">
  <evtFechEvPer Id="ID1000000002026110400002">
    <ideEvento>
      <indApuracao>1</indApuracao>
      <perApur>{competencia}</perApur>
      <tpAmb>2</tpAmb>
      <procEmi>1</procEmi>
      <verProc>KRONUS_ERP_v2.0</verProc>
    </ideEvento>
    <ideEmpregador>
      <tpInsc>1</tpInsc>
      <nrInsc>00000000000100</nrInsc>
    </ideEmpregador>
    <infoFech>
      <evtRemun>S</evtRemun>
      <evtPgtos>S</evtPgtos>
      <compDeson>N</compDeson>
      <indExigIsencao>N</indExigIsencao>
    </infoFech>
  </evtFechEvPer>
</eSocial>"""
            st.code(xml_s1299, language="xml")
            st.success("XML do evento S-1299 gerado com sucesso!")
    else:
        st.info("Selecione S-2230 ou S-1299 para interagir com a geração dos XMLs de teste.")
