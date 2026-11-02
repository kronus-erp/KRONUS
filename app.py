# =====================================================================
# KRONUS S.A. - SISTEMA ERP CONTÁBIL, FISCAL E CRM (STREAMLIT APP)
# =====================================================================

import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(
    page_title="KRONUS S.A. - ERP Contábil e Fiscal",
    page_icon="🏛️",
    layout="wide"
)

# Estilização visual limpa
st.title("🏛️ KRONUS S.A. - Executive Dashboard & ERP")
st.markdown("Plataforma de Gestão Integrada, Inteligência Contábil e Módulo Fiscal Automático.")
st.markdown("---")

# Inicialização da Base de Dados na Sessão (Estado da Aplicação)
if "clientes" not in st.session_state:
    st.session_state.clientes = {}
if "fornecedores" not in st.session_state:
    st.session_state.fornecedores = {}
if "lancamentos_diario" not in st.session_state:
    st.session_state.lancamentos_diario = []

# Abas Principais do Sistema
aba1, aba2, aba3 = st.tabs(["📊 Balanço & DRE", "📥 Módulo Fiscal & CRM", "📈 Motor de Indicadores"])

# =====================================================================
# ABA 1: BALANÇO E DRE
# =====================================================================
with aba1:
    st.subheader("Demonstrações Contábeis e Financeiras")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Balanço Patrimonial Simplificado")
        balanco_data = {
            "Conta Contábil": [
                "Ativo Circulante", "Realizável Longo Prazo", "Ativo Imobilizado", "Ativo Total", 
                "Passivo Circulante", "Passivo Não Circulante", "Patrimônio Líquido", "Passivo Total + PL"
            ],
            "Valor (R$)": [
                550000.00, 150000.00, 400000.00, 1100000.00, 
                200000.00, 300000.00, 600000.00, 1100000.00
            ]
        }
        df_balanco = pd.DataFrame(balanco_data)
        st.dataframe(df_balanco, use_container_width=True, hide_index=True)
        
    with col2:
        st.markdown("### 📈 Demonstração do Resultado (DRE)")
        dre_data = {
            "Conta Contábil": [
                "Receita Bruta / Líquida", "(-) CMV (Custo das Mercadorias)", "(=) Lucro Bruto", 
                "(-) Despesas Operacionais", "(=) EBITDA", "(=) Lucro Líquido do Exercício"
            ],
            "Valor (R$)": [
                1500000.00, -600000.00, 900000.00, -550000.00, 420000.00, 240000.00
            ]
        }
        df_dre = pd.DataFrame(dre_data)
        st.dataframe(df_dre, use_container_width=True, hide_index=True)

# =====================================================================
# ABA 2: MÓDULO FISCAL & CRM (CADASTRO AUTOMÁTICO)
# =====================================================================
with aba2:
    st.subheader("Processamento de Notas Fiscais & Cadastro Automático (CRM)")
    st.markdown("Simule a importação de XMLs da Receita, SEFAZ ou Prefeituras. O sistema reconhece a entidade, cadastra automaticamente e gera as **Partidas Dobradas**.")
    
    col_f, col_v = st.columns(2)
    
    # Processamento de Compra
    with col_f:
        st.markdown("#### 📥 Nota Fiscal de Compra (Entrada)")
        with st.form("form_compra"):
            cnpj_f = st.text_input("CNPJ do Fornecedor", value="45.789.123/0001-99")
            nome_f = st.text_input("Nome do Fornecedor", value="Distribuidora de Insumos SJP Ltda")
            val_tot = st.number_input("Valor Total da Nota (R$)", value=12500.00, format="%.2f")
            icms_rec = st.number_input("ICMS a Recuperar (R$)", value=2250.00, format="%.2f")
            submitted_compra = st.form_submit_button("Processar NF de Compra")
            
            if submitted_compra:
                # CRM Automático
                if cnpj_f not in st.session_state.fornecedores:
                    st.session_state.fornecedores[cnpj_f] = {"nome": nome_f, "status": "Ativo"}
                    st.success(f"🏢 [CRM] Fornecedor cadastrado automaticamente: {nome_f}")
                else:
                    st.info(f"🏢 [CRM] Fornecedor já registado na base: {nome_f}")
                
                ativo_est = val_tot - icms_rec
                lancamento = {
                    "tipo": "COMPRA DE ENTRADA (XML)",
                    "entidade": nome_f,
                    "debitos": [
                        f"1.1.3.01 - Estoque de Mercadorias: R$ {ativo_est:,.2f}",
                        f"1.1.4.02 - ICMS a Recuperar: R$ {icms_rec:,.2f}"
                    ],
                    "creditos": [
                        f"2.1.1.01 - Fornecedores Nacionais: R$ {val_tot:,.2f}"
                    ]
                }
                st.session_state.lancamentos_diario.append(lancamento)
                st.success("⚖️ Lançamento contábil gerado com sucesso!")

    # Processamento de Venda
    with col_v:
        st.markdown("#### 📤 Nota Fiscal de Venda (Saída)")
        with st.form("form_venda"):
            doc_c = st.text_input("CPF/CNPJ do Cliente", value="123.456.789-00")
            nome_c = st.text_input("Nome do Cliente", value="Comércio e Varejo Curitibano S.A.")
            val_venda = st.number_input("Valor da Venda (R$)", value=20000.00, format="%.2f")
            cmv_val = st.number_input("CMV - Baixa de Estoque (R$)", value=9000.00, format="%.2f")
            submitted_venda = st.form_submit_button("Processar NF de Venda")
            
            if submitted_venda:
                # CRM Automático
                if doc_c not in st.session_state.clientes:
                    st.session_state.clientes[doc_c] = {"nome": nome_c, "status": "Ativo"}
                    st.success(f"👤 [CRM] Cliente cadastrado automaticamente: {nome_c}")
                else:
                    st.info(f"👤 [CRM] Cliente já registado na base: {nome_c}")
                    
                lanc_venda = {
                    "tipo": "VENDA DE MERCADORIA (NF-e)",
                    "entidade": nome_c,
                    "debitos": [
                        f"1.1.1.02 - Clientes a Receber / Duplicatas: R$ {val_venda:,.2f}"
                    ],
                    "creditos": [
                        f"3.1.1.01 - Receita Bruta de Vendas: R$ {val_venda:,.2f}"
                    ]
                }
                lanc_cmv = {
                    "tipo": "BAIXA DE CMV",
                    "entidade": nome_c,
                    "debitos": [
                        f"3.1.2.01 - CMV (Custo das Mercadorias): R$ {cmv_val:,.2f}"
                    ],
                    "creditos": [
                        f"1.1.3.01 - Estoque de Mercadorias: R$ {cmv_val:,.2f}"
                    ]
                }
                st.session_state.lancamentos_diario.extend([lanc_venda, lanc_cmv])
                st.success("⚖️ Lançamentos de Venda e CMV gerados com sucesso!")

    st.markdown("---")
    st.subheader("📜 Diário Contábil (Partidas Dobradas Recentes)")
    
    if st.session_state.lancamentos_diario:
        for idx, l in enumerate(reversed(st.session_state.lancamentos_diario), 1):
            with st.expander(f"Lançamento #{idx} | [{l['tipo']}] — Referência: {l['entidade']}", expanded=True):
                col_d, col_c = st.columns(2)
                with col_d:
                    st.markdown("**Débitos:**")
                    for deb in l["debitos"]:
                        st.write(f"• {deb}")
                with col_c:
                    st.markdown("**Créditos:**")
                    for cred in l["creditos"]:
                        st.write(f"• {cred}")
    else:
        st.info("Ainda não existem lançamentos fiscais processados nesta sessão. Utilize os formulários acima para testar.")

# =====================================================================
# ABA 3: MOTOR DE INDICADORES
# =====================================================================
with aba3:
    st.subheader("Motor Master de Indicadores Contábeis e Fundamentalistas")
    st.markdown("Análise automatizada da saúde financeira da empresa com base nos dados correntes.")
    
    # Dados base para cálculo
    ac, pc, est, rlp, elp, at, pl, rec_liq, luc_liq = 550000.0, 200000.0, 120000.0, 150000.0, 300000.0, 1100000.0, 600000.0, 1500000.0, 240000.0
    
    liq_corrente = ac / pc
    liq_seca = (ac - est) / pc
    liq_geral = (ac + rlp) / (pc + elp)
    margem_liq = (luc_liq / rec_liq) * 100
    roe = (luc_liq / pl) * 100
    roa = (luc_liq / at) * 100
    
    st.markdown("### 💧 Índices de Liquidez")
    col_l1, col_l2, col_l3 = st.columns(3)
    col_l1.metric(label="Liquidez Corrente", value=f"{liq_corrente:.2f}", delta="Ideal > 1.0")
    col_l2.metric(label="Liquidez Seca", value=f"{liq_seca:.2f}")
    col_l3.metric(label="Liquidez Geral", value=f"{liq_geral:.2f}")
    
    st.markdown("### 💰 Índices de Rentabilidade & Retorno")
    col_r1, col_r2, col_r3 = st.columns(3)
    col_r1.metric(label="Margem Líquida", value=f"{margem_liq:.2f}%")
    col_r2.metric(label="ROE (Retorno sobre o PL)", value=f"{roe:.2f}%")
    col_r3.metric(label="ROA (Retorno sobre o Ativo)", value=f"{roa:.2f}%")
