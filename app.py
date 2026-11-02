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

# Garantir que a base de lançamentos fica guardada na sessão para não sumir ao interagir
if "df_lancamentos" not in st.session_state:
  try:
    st.session_state.df_lancamentos = pd.read_csv(
        "razao_analitico_caixa.csv", sep=";"
    )
    # Assegurar colunas padrão caso o CSV seja antigo
    if "Débito" not in st.session_state.df_lancamentos.columns:
      st.session_state.df_lancamentos["Débito"] = (
          "Ativo Circulante - Disponível / Banco"
      )
    if "Crédito" not in st.session_state.df_lancamentos.columns:
      st.session_state.df_lancamentos["Crédito"] = (
          "Resultado - Receitas Operacionais"
      )
  except:
    st.session_state.df_lancamentos = pd.DataFrame(
        columns=["Data", "Historico", "Débito", "Crédito", "Valor"]
    )

st.subheader(
    "Registo de Movimentos (Podes editar células ou apagar linhas usando o"
    " caixote do lixo)"
)

# Editor de dados interativo com suporte completo a exclusão e edição
df_editado = st.data_editor(
    st.session_state.df_lancamentos,
    use_container_width=True,
    num_rows="dynamic",
    key="editor_movimentos",
)

# Atualiza a sessão automaticamente com as alterações feitas na tabela (incluindo exclusões)
st.session_state.df_lancamentos = df_editado

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
      st.success("Lançamento efetuado e acumulado com sucesso! 🚀")
      st.rerun()
