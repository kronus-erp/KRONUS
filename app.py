import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="KRONUS ERP - Contabilidade & eSocial",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------------------
# CSS CUSTOMIZADO: PALETA PRETO, BRANCO E AZUL CLARO (FUTURISTA / CORPORATIVO)
# -------------------------------------------------------------------------
custom_css = """
<style>
    /* Importação da fonte Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fundo da Aplicação */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }

    /* Ocultar elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Cabeçalho Futurista */
    .kronus-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #38bdf840;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(56, 189, 248, 0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .kronus-title {
        color: #ffffff;
        font-weight: 900;
        font-size: 2rem;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }
    
    .kronus-subtitle {
        color: #38bdf8;
        font-size: 0.95rem;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Métricas / Cards Futuristas no Topo */
    .metric-card {
        background: rgba(15, 23, 42, 0.85);
        border-left: 4px solid #38bdf8;
        border-top: 1px solid rgba(56, 189, 248, 0.2);
        border-right: 1px solid rgba(56, 189, 248, 0.2);
        border-bottom: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 16px;
        text-align: left;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 12px;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.15);
    }

    .metric-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    .metric-value {
        font-size: 1.5rem;
        color: #ffffff;
        font-weight: 700;
        margin-top: 4px;
    }
    
    .metric-sub {
        font-size: 0.75rem;
        color: #38bdf8;
        margin-top: 2px;
    }

    /* Estilização das Abas Principal (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0f172a;
        padding: 8px;
        border-radius: 14px;
        border: 1px solid #1e293b;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        border: none;
        background-color: transparent;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #38bdf8;
        background-color: rgba(56, 189, 248, 0.05);
    }

    .stTabs [aria-selected="true"] {
        background-color: #38bdf8 !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3);
    }

    /* Formulários e Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3) !important;
    }

    /* Estilização de Botões */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.25) !important;
        width: 100%;
    }

    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #7dd3fc 0%, #38bdf8 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.4) !important;
    }

    /* Expanders / Caixas Expansíveis */
    .streamlit-expanderHeader {
        background-color: #0f172a !important;
        color: #38bdf8 !important;
        border-radius: 8px !important;
        border: 1px solid #1e293b !important;
    }

    /* Tabelas e Dataframes */
    [data-testid="stDataFrame"] {
        border: 1px solid #1e293b;
        border-radius: 12px;
        overflow: hidden;
    }

    /* Ajustes para telas pequenas (Mobile Optimization) */
    @media (max-width: 768px) {
        .kronus-title {
            font-size: 1.4rem;
        }
        .kronus-header {
            padding: 16px;
        }
        .metric-value {
            font-size: 1.2rem;
        }
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------------------------------------------------------
# PERSISTÊNCIA DE DADOS E ARQUIVOS
# -------------------------------------------------------------------------
ARQUIVO_RAZAO = "razao_analitico_caixa.csv"
ARQUIVO_EMPRESA = "cadastro_empresa.csv"
ARQUIVO_PLANO = "plano_de_contas.csv"

plano_inicial_dict = {
    "--- ATIVO CIRCULANTE ---": [
        "1.1.1.01 - Caixa Geral",
        "1.1.1.02 - Bancos Conta Movimento",
        "1.1.1.03 - Aplicações Financeiras de Liquidez Imediata",
        "1.1.2.01 - Clientes Nacionais / Duplicatas a Receber",
        "1.1.2.99 - (-) Provisão para Créditos de Liquidação Duvidosa",
        "1.1.3.01 - Mercadorias para Revenda",
        "1.1.3.02 - Matérias-Primas",
        "1.1.3.03 - Produtos em Elaboração / Acabados",
    ],
    "--- ATIVO NÃO CIRCULANTE ---": [
        "1.2.1.01 - Móveis e Utensílios",
        "1.2.1.02 - Máquinas e Equipamentos",
        "1.2.1.03 - Equipamentos de Informática",
        "1.2.1.09 - (-) Depreciação Acumulada",
        "1.2.2.01 - Softwares e Licenças de Uso",
    ],
    "--- PASSIVO CIRCULANTE ---": [
        "2.1.1.01 - Fornecedores Nacionais",
        "2.1.2.01 - Salários a Pagar",
        "2.1.2.02 - Férias e 13º Salário a Pagar",
        "2.1.2.03 - FGTS a Recolher",
        "2.1.3.01 - Simples Nacional (DAS) a Recolher",
        "2.1.3.02 - Retenções de ISS / IRRF / INSS sobre Serviços",
    ],
    "--- PASSIVO NÃO CIRCULANTE ---": [
        "2.2.1.01 - Empréstimos e Financiamentos de Longo Prazo",
    ],
    "--- PATRIMÔNIO LÍQUIDO ---": [
        "2.3.1.01 - Capital Subscrito / Realizado",
        "2.3.1.02 - Capital Subscrito a Realizar",
        "2.3.2.01 - Lucros Acumulados / Reserva de Lucros",
    ],
    "--- RECEITAS ---": [
        "4.1.1.01 - Receita de Vendas de Mercadorias (Comércio)",
        "4.1.2.01 - Receita de Prestação de Serviços (Serviços)",
        "4.1.3.01 - Receita de Venda de Produtos (Indústria)",
        "4.2.1.01 - (-) Devoluções de Vendas",
        "4.2.2.01 - (-) Abatimentos e Descontos Concedidos",
    ],
    "--- CUSTOS E DESPESAS ---": [
        "5.1.1.01 - Custo das Mercadorias Vendidas (CMV)",
        "5.1.2.01 - Custo dos Serviços Prestados (CSP)",
        "5.1.3.01 - Custo dos Produtos Vendidos (CPV)",
        "5.2.1.01 - Salários e Ordenados",
        "5.2.1.02 - Encargos Sociais (INSS / FGTS)",
        "5.2.1.03 - Benefícios (Vale Transporte, Vale Alimentação)",
        "5.2.2.01 - Aluguel e Condomínio",
        "5.2.2.02 - Energia Elétrica, Água, Internet e Telefone",
        "5.2.2.03 - Honorários Contábeis",
        "5.2.2.04 - Material de Escritório",
        "5.2.2.05 - Despesas com Alimentação",
        "5.2.3.01 - Simples Nacional (DAS) - Despesa Tributária",
        "5.2.3.02 - Taxas e Licenças Diversas",
    ],
}

if "plano_de_contas" not in st.session_state:
    if os.path.exists(ARQUIVO_PLANO):
        try:
            df_p = pd.read_csv(ARQUIVO_PLANO, sep=";")
            p_dict = {}
            for grp in df_p["Grupo"].unique():
                p_dict[grp] = df_p[df_p["Grupo"] == grp]["Conta"].tolist()
            st.session_state.plano_de_contas = p_dict
        except Exception:
            st.session_state.plano_de_contas = plano_inicial_dict
    else:
        st.session_state.plano_de_contas = plano_inicial_dict

plano_de_contas = st.session_state.plano_de_contas

opcoes_selectbox = []
for grupo, contas in plano_de_contas.items():
    opcoes_selectbox.append(grupo)
    for c in contas:
        opcoes_selectbox.append(c)

dados_iniciais = [
    {
        "ID": 1,
        "Data": "2026-01-02",
        "Historico": "Subscrição de Capital Social Inicial",
        "Débito": "2.3.1.02 - Capital Subscrito a Realizar",
        "Crédito": "2.3.1.01 - Capital Subscrito / Realizado",
        "Valor": 1500.00,
    },
    {
        "ID": 2,
        "Data": "2026-01-02",
        "Historico": "Integralização de Capital Social em Bancos/Caixa",
        "Débito": "1.1.1.02 - Bancos Conta Movimento",
        "Crédito": "2.3.1.02 - Capital Subscrito a Realizar",
        "Valor": 1500.00,
    },
    {
        "ID": 3,
        "Data": "2026-01-02",
        "Historico": "Recebimento de Prestação de Serviços",
        "Débito": "1.1.1.02 - Bancos Conta Movimento",
        "Crédito": "4.1.2.01 - Receita de Prestação de Serviços (Serviços)",
        "Valor": 2400.00,
    }
]

if "df_lancamentos" not in st.session_state:
    if os.path.exists(ARQUIVO_RAZAO):
        try:
            df_lido = pd.read_csv(ARQUIVO_RAZAO, sep=";")
            if "Débito" not in df_lido.columns or "Crédito" not in df_lido.columns:
                st.session_state.df_lancamentos = pd.DataFrame(dados_iniciais)
            else:
                st.session_state.df_lancamentos = df_lido
        except Exception:
            st.session_state.df_lancamentos = pd.DataFrame(dados_iniciais)
    else:
        st.session_state.df_lancamentos = pd.DataFrame(dados_iniciais)

df_lanc = st.session_state.df_lancamentos

# -------------------------------------------------------------------------
# CÁLCULOS CONTÁBEIS RÁPIDOS PARA AS MÉTRICAS DO TOPO
# -------------------------------------------------------------------------
total_rec = df_lanc[
    df_lanc["Crédito"].isin(plano_de_contas.get("--- RECEITAS ---", []))
]["Valor"].sum()

total_desp_custo = df_lanc[
    df_lanc["Débito"].isin(plano_de_contas.get("--- CUSTOS E DESPESAS ---", []))
]["Valor"].sum()

lucro_liq_calc = total_rec - total_desp_custo

caixa_bancos = (
    df_lanc[df_lanc["Débito"].str.contains("Caixa|Bancos", na=False)]["Valor"].sum() -
    df_lanc[df_lanc["Crédito"].str.contains("Caixa|Bancos", na=False)]["Valor"].sum()
)

def calcular_secao(nome_grupo, tipo="ativo"):
    contas_grupo = plano_de_contas.get(nome_grupo, [])
    dados = []
    tot = 0.0
    for conta in contas_grupo:
        deb = df_lanc[df_lanc["Débito"] == conta]["Valor"].sum()
        cred = df_lanc[df_lanc["Crédito"] == conta]["Valor"].sum()
        saldo = (deb - cred) if tipo == "ativo" else (cred - deb)
        if "Lucros Acumulados" in conta:
            saldo += lucro_liq_calc
        dados.append({"Conta": conta, "Saldo (R$)": saldo})
        tot += saldo
    return pd.DataFrame(dados), tot

_, tot_ac_calc = calcular_secao("--- ATIVO CIRCULANTE ---", "ativo")
_, tot_anc_calc = calcular_secao("--- ATIVO NÃO CIRCULANTE ---", "ativo")
total_ativo_calc = tot_ac_calc + tot_anc_calc

# -------------------------------------------------------------------------
# CABEÇALHO FUTURISTA DA KRONUS ERP
# -------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="kronus-header">
        <div>
            <div class="kronus-title">⚡ KRONUS ERP</div>
            <div class="kronus-subtitle">Sistema Contábil Corporativo & Módulo eSocial</div>
        </div>
        <div style="text-align: right; font-size: 0.85rem; color: #94a3b8;">
            <div><strong style="color: #38bdf8;">Status:</strong> Operacional</div>
            <div><strong style="color: #ffffff;">Versão:</strong> 2.5 Pro</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------------------
# METRIC CARDS NO TOPO DA TELA
# -------------------------------------------------------------------------
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total do Ativo</div>
            <div class="metric-value">R$ {total_ativo_calc:,.2f}</div>
            <div class="metric-sub">Patrimônio Líquido Acumulado</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Disponibilidades</div>
            <div class="metric-value">R$ {caixa_bancos:,.2f}</div>
            <div class="metric-sub">Caixa + Bancos Conta Movimento</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_m3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Receita Operacional</div>
            <div class="metric-value">R$ {total_rec:,.2f}</div>
            <div class="metric-sub">Faturamento Bruto</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_m4:
    color_l = "#38bdf8" if lucro_liq_calc >= 0 else "#ef4444"
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: {color_l};">
            <div class="metric-label">Lucro Líquido</div>
            <div class="metric-value" style="color: {color_l};">R$ {lucro_liq_calc:,.2f}</div>
            <div class="metric-sub">Resultado do Exercício (DRE)</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# ABAS PRINCIPAIS DO SISTEMA
# -------------------------------------------------------------------------
aba_empresa, aba_lancamentos, aba_demonstracoes, aba_esocial = st.tabs([
    "🏢 Empresa",
    "📝 Partidas Dobradas",
    "📊 Demonstrações",
    "🛡️ eSocial"
])

# -------------------------------------------------------------------------
# ABA 1: CADASTRO DA EMPRESA
# -------------------------------------------------------------------------
with aba_empresa:
    st.markdown("### 🏢 Dados Cadastrais e Societários")
    
    dados_empresa_padrao = pd.DataFrame([{
        "Razao_Social": "KRONUS S.A. - Gestão e Participações",
        "CNPJ": "00.000.000/0001-00",
        "Inscricao_Estadual": "Isento",
        "Regime_Tributario": "Simples Nacional",
        "Endereco": "Curitiba / São José dos Pinhais - PR",
        "Contador_Responsavel": "Marcelo Denardi da Silva (CRC/PR)",
        "Email": "contato@kronuserp.com.br",
    }])

    if "df_empresa" not in st.session_state:
        st.session_state.df_empresa = dados_empresa_padrao

    with st.form("form_empresa_estilizado"):
        col_c1, col_c2 = st.columns(2)
        emp_atual = st.session_state.df_empresa.iloc[0]
        
        with col_c1:
            razao = st.text_input("Razão Social", value=str(emp_atual["Razao_Social"]))
            cnpj = st.text_input("CNPJ", value=str(emp_atual["CNPJ"]))
            ie = st.text_input("Inscrição Estadual", value=str(emp_atual["Inscricao_Estadual"]))
            regime = st.selectbox("Regime Tributário", ["Simples Nacional", "Lucro Presumido", "Lucro Real"])
        with col_c2:
            end = st.text_input("Endereço / Sede", value=str(emp_atual["Endereco"]))
            contador = st.text_input("Contador Responsável / CRC", value=str(emp_atual["Contador_Responsavel"]))
            email = st.text_input("E-mail de Contato", value=str(emp_atual["Email"]))

        btn_atualizar_empresa = st.form_submit_button("Atualizar Informações Societárias")
        if btn_atualizar_empresa:
            st.session_state.df_empresa = pd.DataFrame([{
                "Razao_Social": razao,
                "CNPJ": cnpj,
                "Inscricao_Estadual": ie,
                "Regime_Tributario": regime,
                "Endereco": end,
                "Contador_Responsavel": contador,
                "Email": email,
            }])
            st.success("✅ Cadastro da empresa atualizado com sucesso!")
            st.rerun()

    st.markdown("---")
    st.dataframe(st.session_state.df_empresa, use_container_width=True)

# -------------------------------------------------------------------------
# ABA 2: LANÇAMENTOS E DIÁRIO (PARTIDAS DOBRADAS SIMPLES E MÚLTIPLAS)
# -------------------------------------------------------------------------
with aba_lancamentos:
    st.markdown("### 📝 Motor de Lançamentos Contábeis")
    
    tipo_l = st.radio(
        "Formato da Operação:",
        ["Lançamento Simples (1D / 1C)", "Lançamento Composto/Múltiplo"],
        horizontal=True
    )

    if tipo_l == "Lançamento Simples (1D / 1C)":
        with st.form("form_simples_futurista"):
            st.markdown("##### ➕ Nova Partida Dobrada Simples")
            col1, col2 = st.columns(2)
            with col1:
                dt_l = st.date_input("Data do Lançamento")
                deb_c = st.selectbox("Conta a DEBITAR", opcoes_selectbox, key="s_deb")
            with col2:
                val_l = st.number_input("Valor (R$)", min_value=0.0, step=50.0, format="%.2f")
                cred_c = st.selectbox("Conta a CREDITAR", opcoes_selectbox, key="s_cred")
            hist_l = st.text_input("Histórico Operacional")
            
            if st.form_submit_button("Efetuar Lançamento Simples"):
                if deb_c.startswith("---") or cred_c.startswith("---"):
                    st.error("⚠️ Escolha contas analíticas válidas!")
                elif deb_c == cred_c:
                    st.error("⚠️ Débito e Crédito não podem ser idênticos!")
                else:
                    novo_id = len(st.session_state.df_lancamentos) + 1
                    novo_reg = pd.DataFrame([{
                        "ID": novo_id,
                        "Data": str(dt_l),
                        "Historico": hist_l,
                        "Débito": deb_c,
                        "Crédito": cred_c,
                        "Valor": val_l
                    }])
                    st.session_state.df_lancamentos = pd.concat([st.session_state.df_lancamentos, novo_reg], ignore_index=True)
                    st.session_state.df_lancamentos.to_csv(ARQUIVO_RAZAO, index=False, sep=";")
                    st.success("✅ Lançamento simples registrado com sucesso!")
                    st.rerun()

    else:
        with st.form("form_multiplo_futurista"):
            st.markdown("##### ➕ Nova Partida Múltipla / Composta")
            dt_lm = st.date_input("Data da Operação")
            hist_lm = st.text_input("Histórico Geral do Lançamento Composto")
            
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                st.markdown("<strong style='color:#38bdf8;'>🟢 Débitos:</strong>", unsafe_allow_html=True)
                d1_c = st.selectbox("1º Débito - Conta", opcoes_selectbox, key="m_d1")
                d1_v = st.number_input("1º Débito - Valor (R$)", min_value=0.0, format="%.2f", key="m_d1_v")
                d2_c = st.selectbox("2º Débito - Conta (Opcional)", ["Nenhum"] + opcoes_selectbox, key="m_d2")
                d2_v = st.number_input("2º Débito - Valor (R$)", min_value=0.0, format="%.2f", key="m_d2_v")
                
            with c_m2:
                st.markdown("<strong style='color:#7dd3fc;'>🔴 Créditos:</strong>", unsafe_allow_html=True)
                c1_c = st.selectbox("1º Crédito - Conta", opcoes_selectbox, key="m_c1")
                c1_v = st.number_input("1º Crédito - Valor (R$)", min_value=0.0, format="%.2f", key="m_c1_v")
                c2_c = st.selectbox("2º Crédito - Conta (Opcional)", ["Nenhum"] + opcoes_selectbox, key="m_c2")
                c2_v = st.number_input("2º Crédito - Valor (R$)", min_value=0.0, format="%.2f", key="m_c2_v")

            if st.form_submit_button("Efetuar Partida Múltipla"):
                tot_deb = d1_v + (d2_v if d2_c != "Nenhum" else 0.0)
                tot_cred = c1_v + (c2_v if c2_c != "Nenhum" else 0.0)
                
                if abs(tot_deb - tot_cred) > 0.01:
                    st.error(f"❌ Desequilíbrio Contábil! Débitos (R$ {tot_deb:.2f}) != Créditos (R$ {tot_cred:.2f})")
                else:
                    novas_linhas = []
                    id_base = len(st.session_state.df_lancamentos) + 1
                    if d1_v > 0 and not d1_c.startswith("---"):
                        novas_linhas.append({"ID": id_base, "Data": str(dt_lm), "Historico": hist_lm, "Débito": d1_c, "Crédito": c1_c, "Valor": d1_v})
                    if d2_c != "Nenhum" and d2_v > 0 and not d2_c.startswith("---"):
                        novas_linhas.append({"ID": id_base+1, "Data": str(dt_lm), "Historico": hist_lm + " (Desdobro)", "Débito": d2_c, "Crédito": c2_c if c2_c != "Nenhum" else c1_c, "Valor": d2_v})

                    if novas_linhas:
                        st.session_state.df_lancamentos = pd.concat([st.session_state.df_lancamentos, pd.DataFrame(novas_linhas)], ignore_index=True)
                        st.session_state.df_lancamentos.to_csv(ARQUIVO_RAZAO, index=False, sep=";")
                        st.success("✅ Partidas múltiplas registradas com equilíbrio absoluto!")
                        st.rerun()

    st.markdown("---")
    st.markdown("##### 📜 Livro Diário Geral")
    st.dataframe(st.session_state.df_lancamentos, use_container_width=True)

# -------------------------------------------------------------------------
# ABA 3: DEMONSTRAÇÕES CONTÁBEIS (RESPONSIVIDADE E VISUALIZAÇÃO LIMPA)
# -------------------------------------------------------------------------
with aba_demonstracoes:
    st.markdown("### 📊 Demonstrações Contábeis Societárias")
    
    opcao_demo = st.selectbox(
        "Selecione o Relatório para Exibição:",
        [
            "⚖️ Balanço Patrimonial & DRE",
            "📋 Balancete de Verificação",
            "💵 DFC - Fluxo de Caixa",
            "📈 DMPL - Mutações do PL",
            "🌐 DVA - Valor Adicionado"
        ]
    )

    st.markdown("---")

    if opcao_demo == "⚖️ Balanço Patrimonial & DRE":
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown("#### 🔹 BALANÇO PATRIMONIAL")
            df_ac, tot_ac = calcular_secao("--- ATIVO CIRCULANTE ---", "ativo")
            st.markdown("**Ativo Circulante**")
            st.dataframe(df_ac, use_container_width=True)
            
            df_anc, tot_anc = calcular_secao("--- ATIVO NÃO CIRCULANTE ---", "ativo")
            st.markdown("**Ativo Não Circulante**")
            st.dataframe(df_anc, use_container_width=True)
            st.markdown(f"### **TOTAL ATIVO: R$ {tot_ac + tot_anc:,.2f}**")

        with col_b2:
            st.markdown("#### 🔹 DRE - DEMONSTRAÇÃO DO RESULTADO")
            df_rec, _ = calcular_secao("--- RECEITAS ---", "passivo")
            st.markdown("**Receitas Brutas**")
            st.dataframe(df_rec, use_container_width=True)
            
            df_desp, _ = calcular_secao("--- CUSTOS E DESPESAS ---", "ativo")
            st.markdown("**Custos e Despesas**")
            st.dataframe(df_desp, use_container_width=True)
            st.markdown(f"### **LUCRO LÍQUIDO: R$ {lucro_liq_calc:,.2f}**")

    elif opcao_demo == "📋 Balancete de Verificação":
        st.markdown("#### 📋 Balancete Analítico de Verificação")
        dados_bal = []
        for g, contas in plano_de_contas.items():
            for c in contas:
                deb = df_lanc[df_lanc["Débito"] == c]["Valor"].sum()
                cred = df_lanc[df_lanc["Crédito"] == c]["Valor"].sum()
                if deb > 0 or cred > 0:
                    dados_bal.append({"Grupo": g, "Conta": c, "Débitos (R$)": deb, "Créditos (R$)": cred})
        st.dataframe(pd.DataFrame(dados_bal), use_container_width=True)

    elif opcao_demo == "💵 DFC - Fluxo de Caixa":
        st.markdown("#### 💵 Demonstração do Fluxo de Caixa (Método Direto)")
        st.info(f"💡 **Saldo Líquido de Caixa/Bancos Gerado:** R$ {caixa_bancos:,.2f}")

    elif opcao_demo == "📈 DMPL - Mutações do PL":
        st.markdown("#### 📈 Demonstração das Mutações do Patrimônio Líquido")
        st.success(f"📈 **Patrimônio Líquido Ajustado ao Fim do Exercício:** R$ {total_ativo_calc:,.2f}")

    elif opcao_demo == "🌐 DVA - Valor Adicionado":
        st.markdown("#### 🌐 Demonstração do Valor Adicionado")
        st.write(f"- **Riqueza Gerada (Receita):** R$ {total_rec:,.2f}")
        st.write(f"- **Insumos Adquiridos:** R$ {total_desp_custo:,.2f}")
        st.markdown(f"### **Valor Adicionado Líquido: R$ {max(0, total_rec - total_desp_custo):,.2f}**")

# -------------------------------------------------------------------------
# ABA 4: MÓDULO eSOCIAL (S-1000, S-1010, S-2200, S-1200, S-2230, S-1299)
# -------------------------------------------------------------------------
with aba_esocial:
    st.markdown("### 🛡️ Módulo de Integração eSocial XML")
    
    es_opcao = st.selectbox(
        "Selecione o Evento do eSocial para Gerar:",
        [
            "S-1000 (Informações do Empregador)",
            "S-1010 (Tabela de Rubricas)",
            "S-2200 (Admissão de Trabalhador)",
            "S-1200 (Remuneração de Trabalhador)",
            "S-2230 (Afastamento Temporário)",
            "S-1299 (Fechamento dos Eventos Periódicos)"
        ]
    )

    st.markdown("---")

    if "S-1000" in es_opcao:
        st.markdown("##### Evento S-1000 - Informações do Empregador")
        with st.form("form_xml_s1000"):
            c1, c2 = st.columns(2)
            with c1: cnpj_e = st.text_input("CNPJ Empregador", "00000000000100")
            with c2: class_t = st.selectbox("Classificação Tributária", ["01 - Simples Nacional", "99 - Geral"])
            if st.form_submit_button("Gerar XML S-1000"):
                esocial = ET.Element("eSocial", xmlns="http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_03_00")
                evt = ET.SubElement(esocial, "evtInfoEmpregador", Id=f"ID1{cnpj_e.zfill(14)}2026110412000000001")
                ide = ET.SubElement(evt, "ideEvento")
                ET.SubElement(ide, "tpAmb").text = "2"
                ET.SubElement(ide, "procEmi").text = "1"
                ET.SubElement(ide, "verProc").text = "KRONUS_ERP_v2.5"
                emp = ET.SubElement(evt, "ideEmpregador")
                ET.SubElement(emp, "tpInsc").text = "1"
                ET.SubElement(emp, "nrInsc").text = cnpj_e
                xml_str = minidom.parseString(ET.tostring(esocial)).toprettyxml(indent="  ")
                st.code(xml_str, language="xml")

    elif "S-2230" in es_opcao:
        st.markdown("##### Evento S-2230 - Afastamento Temporário")
        with st.form("form_xml_s2230"):
            c1, c2 = st.columns(2)
            with c1:
                cpf_af = st.text_input("CPF do Trabalhador", "00000000000")
                mat_af = st.text_input("Matrícula", "001")
            with c2:
                dt_af = st.date_input("Data de Início")
                motivo_af = st.selectbox("Motivo", ["01 - Acidente/Doença do Trabalho", "15 - Férias", "35 - Licença Maternidade"])
            if st.form_submit_button("Gerar XML S-2230"):
                esocial = ET.Element("eSocial", xmlns="http://www.esocial.gov.br/schema/evt/evtAfastTemp/v_S_01_03_00")
                evt = ET.SubElement(esocial, "evtAfastTemp", Id="ID1000000002026110412000000001")
                afast = ET.SubElement(evt, "iniAfastamento")
                ET.SubElement(afast, "dtIniAfast").text = str(dt_af)
                ET.SubElement(afast, "codMotAfast").text = motivo_af.split(" - ")[0]
                xml_str = minidom.parseString(ET.tostring(esocial)).toprettyxml(indent="  ")
                st.code(xml_str, language="xml")

    elif "S-1299" in es_opcao:
        st.markdown("##### Evento S-1299 - Fechamento dos Eventos Periódicos")
        with st.form("form_xml_s1299"):
            per_ap = st.text_input("Período de Apuração (AAAA-MM)", "2026-11")
            if st.form_submit_button("Gerar XML S-1299"):
                esocial = ET.Element("eSocial", xmlns="http://www.esocial.gov.br/schema/evt/evtFechEvPer/v_S_01_03_00")
                evt = ET.SubElement(esocial, "evtFechEvPer", Id="ID1000000002026110412000000001")
                info = ET.SubElement(evt, "infoFech")
                ET.SubElement(info, "evtRemun").text = "S"
                ET.SubElement(info, "evtPgtos").text = "S"
                xml_str = minidom.parseString(ET.tostring(esocial)).toprettyxml(indent="  ")
                st.code(xml_str, language="xml")

    else:
        st.info("💡 Selecione o evento desejado no menu acima para estruturar e validar o código XML.")

```
