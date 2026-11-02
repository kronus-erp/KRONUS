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
        st.session_state.df_lancamentos.to_csv(ARQUIVO_CSV, index=False, sep=";")
      else:
        st.session_state.df_lancamentos = df_lido
    except:
      st.session_state.df_lancamentos = pd.DataFrame(dados_iniciais)
  else:
    st.session_state.df_lancamentos = pd.DataFrame(dados_iniciais)
    st.session_state.df_lancamentos.to_csv(ARQUIVO_CSV, index=False, sep=";")

# 1. Balanço Patrimonial Dinâmico Baseado nos Lançamentos
st.header("1. Balanço Patrimonial (Atualizado em Tempo Real)")

# Saldos base iniciais extraídos do ficheiro ou definidos estruturalmente
saldos_base = {
    "Ativo Circulante - Disponível / Banco": 150000.0,
    "Ativo Circulante - Clientes": 35000.0,
    "Ativo Não Circulante - Imobilizado": 330000.0,
    "Passivo Circulante - Fornecedores": 45000.0,
    "Passivo Circulante - Obrigações Trabalhistas": 25000.0,
    "Patrimônio Líquido - Capital Social": 400000.0,
    "Patrimônio Líquido - Lucros Acumulados": 15000.0,
}

df_lanc = st.session_state.df_lancamentos

# Calcular saldos dinâmicos para o Balanço
dados_bp_dinamico = []

for conta_completa, saldo_inicial in saldos_base.items():
  # Calcular total de débitos e créditos para esta conta nos lançamentos
  deb = df_lanc[df_lanc["Débito"] == conta_completa]["Valor"].sum()
  cred = df_lanc[df_lanc["Crédito"] == conta_completa]["Valor"].sum()

  # Contas de Ativo aumentam com Débito e diminuem com Crédito
  if "Ativo" in conta_completa:
    saldo_atual = saldo_inicial + deb - cred
    grupo = conta_completa.split(" - ")[0]
    nome_conta = conta_completa.split(" - ")[1]
  # Contas de Passivo e PL aumentam com Crédito e diminuem com Débito
  else:
    saldo_atual = saldo_inicial + cred - deb
    grupo = conta_completa.split(" - ")[0]
    nome_conta = conta_completa.split(" - ")[1]

  dados_bp_dinamico.append(
      {"Grupo": grupo, "Conta": nome_conta, "Saldo (R$)": saldo_atual}
  )

# Adicionar o resultado líquido do exercício (Receitas - Despesas) acumulado em Lucros Acumulados
total_receitas = df_lanc[
    df_lanc["Crédito"] == "Resultado - Receitas Operacionais"
]["Valor"].sum()
total_despesas = df_lanc[
    df_lanc["Débito"] == "Resultado - Despesas Administrativas"
]["Valor"].sum()
resultado_liquido = total_receitas - total_despesas

# Ajustar o saldo de Lucros Acumulados com o resultado do período
for item in dados_bp_dinamico:
  if item["Conta"] == "Lucros Acumulados":
    item["Saldo (R$)"] += resultado_liquido

df_bp = pd.DataFrame(dados_bp_dinamico)
st.dataframe(df_bp, use_container_width=True)

# 2. Livro Razão e Lançamentos com Partidas Dobradas
st.header("2. Livro Razão e Lançamentos Contábeis")

# Controlo de edição na sessão
if "editando_idx" not in st.session_state:
  st.session_state.editando_idx = None

st.subheader("Registo de Movimentos e Gestão por Linha")

# Exibir os lançamentos com botões de Editar e Excluir lado a lado
for idx, row in st.session_state.df_lancamentos.iterrows():
  col_info, col_edit, col_del = st.columns([4, 1, 1])
  with col_info:
    deb = row.get("Débito", "N/A")
    cred = row.get("Crédito", "N/A")
    st.markdown(
        f"**[{idx}] {row['Data']}** | {row['Historico']} | **D:** {deb} |"
        f" **C:** {cred} | **R$ {row['Valor']:.2f}**"
    )
  with col_edit:
    if st.button("✏️ Editar", key=f"btn_edit_{idx}"):
      st.session_state.editando_idx = idx
  with col_del:
    if st.button("🗑️ Excluir", key=f"btn_del_{idx}"):
      if st.session_state.editando_idx == idx:
        st.session_state.editando_idx = None
      st.session_state.df_lancamentos = (
          st.session_state.df_lancamentos.drop(idx).reset_index(drop=True)
      )
      st.session_state.df_lancamentos.to_csv(ARQUIVO_CSV, index=False, sep=";")
      st.success(f"Lançamento {idx} excluído com sucesso!")
      st.rerun()
  st.markdown("---")

# Se o utilizador clicou em editar numa linha específica
if st.session_state.editando_idx is not None:
  idx_edit = st.session_state.editando_idx
  if idx_edit in st.session_state.df_lancamentos.index:
    row_atual = st.session_state.df_lancamentos.loc[idx_edit]

    st.markdown(f"### ✏️ A Editar o Lançamento [{idx_edit}]")
    with st.form(f"form_editar_{idx_edit}"):
      col_e1, col_e2 = st.columns(2)
      with col_e1:
        nova_data = st.text_input("Data (AAAA-MM-DD)", value=str(row_atual["Data"]))
        deb_atual = str(row_atual.get("Débito", lista_contas[0]))
        idx_deb = lista_contas.index(deb_atual) if deb_atual in lista_contas else 0
        novo_debito = st.selectbox("Conta a DEBITAR", lista_contas, index=idx_deb)
      with col_e2:
        novo_valor = st.number_input(
            "Valor (R$)", min_value=0.0, value=float(row_atual["Valor"]), format="%.2f", step=10.0
        )
        cred_atual = str(row_atual.get("Crédito", lista_contas[0]))
        idx_cred = lista_contas.index(cred_atual) if cred_atual in lista_contas else 0
        novo_credito = st.selectbox("Conta a CREDITAR", lista_contas, index=idx_cred)

      novo_hist = st.text_input("Histórico / Descrição", value=str(row_atual["Historico"]))

      col_salvar, col_cancelar = st.columns(2)
      with col_salvar:
        salvar_edicao = st.form_submit_button("💾 Guardar Alterações")
      with col_cancelar:
        cancelar_edicao = st.form_submit_button("❌ Cancelar")

      if salvar_edicao:
        if novo_debito == novo_credito:
          st.error("A conta a debitar não pode ser igual à conta a creditar!")
        else:
          st.session_state.df_lancamentos.loc[idx_edit, "Data"] = nova_data
          st.session_state.df_lancamentos.loc[idx_edit, "Historico"] = novo_hist
          st.session_state.df_lancamentos.loc[idx_edit, "Débito"] = novo_debito
          st.session_state.df_lancamentos.loc[idx_edit, "Crédito"] = novo_credito
          st.session_state.df_lancamentos.loc[idx_edit, "Valor"] = novo_valor

          st.session_state.df_lancamentos.to_csv(ARQUIVO_CSV, index=False, sep=";")
          st.session_state.editando_idx = None
          st.success("Lançamento atualizado e gravado com sucesso! 🚀")
          st.rerun()

      if cancelar_edicao:
        st.session_state.editando_idx = None
        st.rerun()

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
