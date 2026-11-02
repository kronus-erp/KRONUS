import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="KRONUS ERP - Contabilidade", page_icon="📊", layout="wide"
)

st.title("📊 KRONUS S.A. - Sistema Integrado de Gestão Contábil")
st.markdown(
    "Módulo Financeiro e Contábil em Nuvem | *Utilizador: Contador*"
)

# 1. Carregar Balanço Patrimonial
st.header("1. Balanço Patrimonial")
try:
  with open("balanco_patrimonial_kronus.txt", "r", encoding="utf-8") as f:
    linhas = f.readlines()

  dados_bp = []
  for linha in linhas:
    partes = linha.strip().split(";")
    if len(partes) == 3:
      dados_bp.append(
          {"Grupo": partes[0], "Conta": partes[1], "Saldo (R$)": float(partes[2])}
      )

  df_bp = pd.DataFrame(dados_bp)
  st.dataframe(df_bp, use_container_width=True)
except Exception as e:
  st.warning(
      "Ficheiro do balanço patrimonial não encontrado ou com formato a"
      f" ajustar: {e}"
  )

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

# 2. Livro Razão e Lançamentos com Partidas Dobradas
st.header("2. Livro Razão e Lançamentos Contábeis")

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

# Carregar dados e garantir compatibilidade de colunas
if "df_lancamentos" not in st.session_state:
  if os.path.exists(ARQUIVO_CSV):
    try:
      df_lido = pd.read_csv(ARQUIVO_CSV, sep=";")
      if "Débito" not in df_lido.columns or "Crédito" not in df_lido.columns:
        st.session_state.df_lancamentos = pd.DataFrame(dados_iniciais)
        st.session_state.df_lancamentos.to_csv(ARQUIVO_CSV, index=False, sep=";")
      else:
        st.session_state.df_lancamentos = df_lido
    except:
      st.session_state.df_lancamentos = pd.DataFrame(dados_iniciais)
  else:
    st.session_state.df_lancamentos = pd.DataFrame(dados_iniciais)
    st.session_state.df_lancamentos.to_csv(ARQUIVO_CSV, index=False, sep=";")

st.subheader("Registo de Movimentos e Gestão por Linha")

# Exibir os lançamentos linha a linha com o botão de excluir dedicado
for idx, row in st.session_state.df_lancamentos.iterrows():
  col_info, col_btn = st.columns([5, 1])
  with col_info:
    deb = row.get("Débito", "N/A")
    cred = row.get("Crédito", "N/A")
    st.markdown(
        f"**[{idx}] Data:** {row['Data']} | **Hist:** {row['Historico']} |"
        f" **Débito:** {deb} | **Crédito:** {cred} | **Valor:** R$"
        f" {row['Valor']:.2f}"
    )
  with col_btn:
    if st.button("🗑️ Excluir", key=f"btn_excluir_{idx}"):
      st.session_state.df_lancamentos = (
          st.session_state.df_lancamentos.drop(idx).reset_index(drop=True)
      )
      st.session_state.df_lancamentos.to_csv(ARQUIVO_CSV, index=False, sep=";")
      st.success(f"Lançamento {idx} excluído com sucesso!")
      st.rerun()
  st.markdown("---")

st.subheader("Novo Lançamento (Partidas Dobradas - Débito e Crédito)")
with st.form("form_partidas_dobradas", clear_on_submit=True):
  col1, col2 = st.columns(2)
  with col1:
    data_lanc = st.date_input("Data do Lançamento")
    conta_debito = st.selectbox("Conta a DEBITAR", lista_contas)
  with col2:
    valor_mov = st.number_input(
        "Valor (R$)", min_value=0.0, format="%.2f", step=10.0
    )
    conta_credito = st.selectbox("Conta a CREDITAR", lista_contas)

  historico = st.text_input(
      "Histórico / Descrição",
      placeholder="Ex: Recebimento de comissão de terceiro",
  )

  submitted = st.form_submit_button("Lançar Partida Dobrada")
  if submitted:
    if conta_debito == conta_credito:
      st.error(
          "A conta a debitar não pode ser igual à conta a creditar numa"
          " partida dobrada!"
      )
    else:
      novo_registo = pd.DataFrame(
          [{
              "Data": str(data_lanc),
              "Historico": historico,
              "Débito": conta_debito,
              "Crédito": conta_credito,
              "Valor": valor_mov,
          }]
      )
      st.session_state.df_lancamentos = pd.concat(
          [st.session_state.df_lancamentos, novo_registo], ignore_index=True
      )
      st.session_state.df_lancamentos.to_csv(ARQUIVO_CSV, index=False, sep=";")
      st.success("Lançamento efetuado e gravado com sucesso! 🚀")
      st.rerun()
