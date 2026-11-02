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

# 2. Razão Analítico de Caixa e Lançamentos Editáveis
st.header("2. Razão Analítico de Caixa e Lançamentos")
try:
  df_caixa = pd.read_csv("razao_analitico_caixa.csv", sep=";")
  st.subheader("Registo Atual de Movimentos")
  st.dataframe(df_caixa, use_container_width=True)

  st.subheader("Novo Lançamento Contábil (Partidas Dobradas)")
  with st.form("form_lancamento"):
    col1, col2, col3 = st.columns(3)
    with col1:
      data_lanc = st.date_input("Data do Lançamento")
    with col2:
      historico = st.text_input(
          "Histórico", placeholder="Ex: Pagamento de despesa"
      )
    with col3:
      tipo_mov = st.selectbox("Tipo", ["Entrada", "Saida"])

    valor_mov = st.number_input(
        "Valor (R$)", min_value=0.0, format="%.2f", step=100.0
    )

    submitted = st.form_submit_button("Registar Lançamento")
    if submitted:
      novo_registo = pd.DataFrame(
          [{
              "Data": str(data_lanc),
              "Historico": historico,
              "Tipo": tipo_mov,
              "Valor": valor_mov,
          }]
      )
      df_caixa = pd.concat([df_caixa, novo_registo], ignore_index=True)
      st.success(
          "Lançamento efetuado com sucesso! (Podes exportar ou atualizar a"
          " base)"
      )
      st.dataframe(df_caixa, use_container_width=True)

except Exception as e:
  st.warning(f"Erro ao carregar o razão de caixa: {e}")
