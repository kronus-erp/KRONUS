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

# Carregar dados persistentes do ficheiro CSV do servidor
if "df_lancamentos" not in st.session_state:
  if os.path.exists(ARQUIVO_CSV):
    try:
      st.session_state.df_lancamentos = pd.read_csv(ARQUIVO_CSV, sep=";")
    except:
      st.session_state.df_lancamentos = pd.DataFrame(
          columns=["Data", "Historico", "Débito", "Crédito", "Valor"]
      )
  else:
    st.session_state.df_lancamentos = pd.DataFrame(
        columns=["Data", "Historico", "Débito", "Crédito", "Valor"]
    )

st.subheader("Registo de Movimentos e Gestão de Lançamentos")

# Exibir tabela para visualização limpa
st.dataframe(st.session_state.df_lancamentos, use_container_width=True)

# Secção Dedicada para Exclusão de Lançamentos de forma Segura
if not st.session_state.df_lancamentos.empty:
  st.markdown("### 🗑️ Excluir Lançamento Incorreto")
  col_excluir_1, col_excluir_2 = st.columns([3, 1])

  with col_excluir_1:
    # Criar uma lista descritiva de cada linha para o contador selecionar facilmente
    opcoes_linhas = []
    for idx, row in st.session_state.df_lancamentos.iterrows():
      desc = f"[{idx}] Data: {row['Data']} | Histórico: {row['Historico']} | Valor: R$ {row['Valor']}"
      opcoes_linhas.append((idx, desc))

    linha_selecionada_desc = st.selectbox(
        "Selecione o lançamento que deseja excluir:",
        options=[item[1] for item in opcoes_linhas],
    )

    # Descobrir o índice real da linha selecionada
    idx_para_excluir = None
    for item in opcoes_linhas:
      if item[1] == linha_selecionada_desc:
        idx_para_excluir = item[0]

  with col_excluir_2:
    st.write("")  # Espaçamento vertical para alinhar com o selectbox
    st.write("")
    if st.button("Excluir Registo"):
      if idx_para_excluir is not None:
        st.session_state.df_lancamentos = (
            st.session_state.df_lancamentos.drop(idx_para_excluir)
            .reset_index(drop=True)
        )
        # Salvar imediatamente a alteração no servidor
        st.session_state.df_lancamentos.to_csv(
            ARQUIVO_CSV, index=False, sep=";"
        )
        st.success("Lançamento excluído com sucesso! 🚀")
        st.rerun()

st.subheader("Novo Lançamento (Partidas Dobradas - Débito e Crédito)")
with st.form("form_partidas_dobradas", clear_on_submit=True):
  col1, col2 = st.columns(2)
  with col1:
    data_lanc = st.date_input("Data do Lançamento")
    conta_debito = st.selectbox("Conta a DEBITAR", lista_contas)
  with col2:
    valor_mov = st.number_input(
        "Valor (R$)", min_value=0.0, format="%.2f", step=100.0
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
      # Gravação automática imediata no ficheiro do servidor
      st.session_state.df_lancamentos.to_csv(ARQUIVO_CSV, index=False, sep=";")
      st.success("Lançamento efetuado e gravado com sucesso! 🚀")
      st.rerun()
