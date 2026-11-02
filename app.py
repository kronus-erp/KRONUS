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

df_lanc = st.session_state.df_lancamentos

# -------------------------------------------------------------
# 1. BALANÇO PATRIMONIAL DINÂMICO
# -------------------------------------------------------------
st.header("1. Balanço Patrimonial")
contas_patrimoniais = [
    ("Ativo Circulante", "Disponível / Banco"),
    ("Ativo Circulante", "Clientes"),
    ("Ativo Não Circulante", "Imobilizado"),
    ("Passivo Circulante", "Fornecedores"),
    ("Passivo Circulante", "Obrigações Trabalhistas"),
    ("Patrimônio Líquido", "Capital Social"),
    ("Patrimônio Líquido", "Lucros Acumulados"),
]

total_receitas = df_lanc[
    df_lanc["Crédito"] == "Resultado - Receitas Operacionais"
]["Valor"].sum()
total_despesas = df_lanc[
    df_lanc["Débito"] == "Resultado - Despesas Administrativas"
]["Valor"].sum()
lucro_liquido = total_receitas - total_despesas

dados_bp = []
for grupo, nome_conta in contas_patrimoniais:
  conta_completa = f"{grupo} - {nome_conta}"
  deb = df_lanc[df_lanc["Débito"] == conta_completa]["Valor"].sum()
  cred = df_lanc[df_lanc["Crédito"] == conta_completa]["Valor"].sum()

  if grupo.startswith("Ativo"):
    saldo = deb - cred
  else:
    saldo = cred - deb

  if nome_conta == "Lucros Acumulados":
    saldo += lucro_liquido

  dados_bp.append({"Grupo": grupo, "Conta": nome_conta, "Saldo (R$)": saldo})

st.dataframe(pd.DataFrame(dados_bp), use_container_width=True)

# -------------------------------------------------------------
# 2. DRE (DEMONSTRAÇÃO DO RESULTADO DO EXERCÍCIO)
# -------------------------------------------------------------
st.header("2. DRE - Demonstração do Resultado do Exercício")
dados_dre = [
    {"Demonstração": "Receitas Operacionais Brutas / Comissões", "Valor (R$)": total_receitas},
    {"Demonstração": "(-) Despesas Administrativas", "Valor (R$)": -total_despesas},
    {"Demonstração": "(=) Resultado Líquido do Exercício", "Valor (R$)": lucro_liquido},
]
st.dataframe(pd.DataFrame(dados_dre), use_container_width=True)

# -------------------------------------------------------------
# 3. DFC (DEMONSTRAÇÃO DOS FLUXOS DE CAIXA)
# -------------------------------------------------------------
st.header("3. DFC - Demonstração dos Fluxos de Caixa (Método Direto)")
# Entradas e Saídas na conta Disponível / Banco
entradas_caixa = df_lanc[df_lanc["Débito"] == "Ativo Circulante - Disponível / Banco"]["Valor"].sum()
saidas_caixa = df_lanc[df_lanc["Crédito"] == "Ativo Circulante - Disponível / Banco"]["Valor"].sum()
variacao_caixa = entradas_caixa - saidas_caixa

dados_dfc = [
    {"Fluxo de Caixa": "Entradas de Caixa (Débitos em Banco)", "Valor (R$)": entradas_caixa},
    {"Fluxo de Caixa": "Saídas de Caixa (Créditos em Banco)", "Valor (R$)": -saidas_caixa},
    {"Fluxo de Caixa": "(=) Variação Líquida de Caixa", "Valor (R$)": variacao_caixa},
]
st.dataframe(pd.DataFrame(dados_dfc), use_container_width=True)

# -------------------------------------------------------------
# 4. DVA (DEMONSTRAÇÃO DO VALOR ADICIONADO)
# -------------------------------------------------------------
st.header("4. DVA - Demonstração do Valor Adicionado")
dados_dva = [
    {"Especificação": "Receitas (Geração de Valor)", "Valor (R$)": total_receitas},
    {"Especificação": "Insumos Adquiridos de Terceiros", "Valor (R$)": -total_despesas},
    {"Especificação": "(=) Valor Adicionado Líquido Produzido", "Valor (R$)": lucro_liquido},
    {"Especificação": "Distribuição do Valor Adicionado (Lucros Retidos)", "Valor (R$)": lucro_liquido},
]
st.dataframe(pd.DataFrame(dados_dva), use_container_width=True)

# -------------------------------------------------------------
# 5. DMPL (DEMONSTRAÇÃO DAS MUTAÇÕES DO PATRIMÔNIO LÍQUIDO)
# -------------------------------------------------------------
st.header("5. DMPL - Demonstração das Mutações do Patrimônio Líquido")
capital_social_inicial = df_lanc[
    (df_lanc["Crédito"] == "Patrimônio Líquido - Capital Social") & 
    (df_lanc["Historico"] == "Saldo Inicial")
]["Valor"].sum()

dados_dmpl = [
    {
        "Conta do PL": "Capital Social",
        "Saldo Inicial (R$)": capital_social_inicial,
        "Aumentos / Adições (R$)": 0.0,
        "Resultado do Período (R$)": 0.0,
        "Saldo Final (R$)": capital_social_inicial
    },
    {
        "Conta do PL": "Lucros Acumulados",
        "Saldo Inicial (R$)": 0.0,
        "Aumentos / Adições (R$)": 0.0,
        "Resultado do Período (R$)": lucro_liquido,
        "Saldo Final (R$)": lucro_liquido
    }
]
st.dataframe(pd.DataFrame(dados_dmpl), use_container_width=True)


# -------------------------------------------------------------
# 6. LIVRO RAZÃO E LANÇAMENTOS CONTÁBEIS
# -------------------------------------------------------------
st.header("6. Livro Razão e Gestão de Lançamentos")

if "editando_idx" not in st.session_state:
  st.session_state.editando_idx = None

st.subheader("Registo de Movimentos e Gestão por Linha")

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

# Painel de Edição
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
