import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="KRONUS ERP - Contabilidade Completa", page_icon="📊", layout="wide"
)

st.title("📊 KRONUS S.A. - Sistema Integrado de Gestão Contábil")
st.markdown(
    "Módulo Financeiro e Contábil em Nuvem | *Utilizador: Contador*"
)

# Criar Abas Principais para organizar o ERP
aba_contabilidade, aba_empresa = st.tabs([
    "📊 Contabilidade & Demonstrações",
    "🏢 Cadastro da Empresa",
])

# -------------------------------------------------------------------------
# ABA 1: CONTABILIDADE & DEMONSTRAÇÕES
# -------------------------------------------------------------------------
with aba_contabilidade:
  # Lista de Contas para Partidas Dobradas
  lista_contas = [
      "Ativo Circulante - Disponível / Banco",
      "Ativo Circulante - Clientes",
      "Ativo Não Circulante - Imobilizado",
      "Passivo Circulante - Fornecedores",
      "Passivo Circulante - Obrigações Trabalhistas",
      "Patrimônio Líquido - Capital Social",
      "Patrimônio Líquido - Lucros Acumulados",
      "Resultado - Receitas Operacionais",
      "Resultado - Despesas Administrativas",
  ]

  ARQUIVO_CSV = "razao_analitico_caixa.csv"

  dados_iniciais = [
      {
          "Data": "2026-11-01",
          "Historico": "Saldo Inicial",
          "Débito": "Ativo Circulante - Disponível / Banco",
          "Crédito": "Patrimônio Líquido - Capital Social",
          "Valor": 150000.0,
      },
      {
          "Data": "2026-11-02",
          "Historico": "Recebimento de Cliente",
          "Débito": "Ativo Circulante - Disponível / Banco",
          "Crédito": "Ativo Circulante - Clientes",
          "Valor": 15000.0,
      },
      {
          "Data": "2026-11-03",
          "Historico": "Pagamento de Fornecedor",
          "Débito": "Passivo Circulante - Fornecedores",
          "Crédito": "Ativo Circulante - Disponível / Banco",
          "Valor": 8000.0,
      },
      {
          "Data": "2026-11-04",
          "Historico": "Despesas Administrativas",
          "Débito": "Resultado - Despesas Administrativas",
          "Crédito": "Ativo Circulante - Disponível / Banco",
          "Valor": 2500.0,
      },
      {
          "Data": "2026-11-02",
          "Historico": "Ref. Comissão 9bet",
          "Débito": "Ativo Circulante - Disponível / Banco",
          "Crédito": "Resultado - Receitas Operacionais",
          "Valor": 14.0,
      },
      {
          "Data": "2026-11-02",
          "Historico": "Ref. Comissão D16",
          "Débito": "Ativo Circulante - Disponível / Banco",
          "Crédito": "Resultado - Receitas Operacionais",
          "Valor": 10.0,
      },
  ]

  # Carregar lançamentos e garantir compatibilidade
  if "df_lancamentos" not in st.session_state:
    if os.path.exists(ARQUIVO_CSV):
      try:
        df_lido = pd.read_csv(ARQUIVO_CSV, sep=";")
        if "Débito" not in df_lido.columns or "Crédito" not in df_lido.columns:
          st.session_state.df_lancamentos = pd.DataFrame(dados_iniciais)
          st.session_state.df_lanc
