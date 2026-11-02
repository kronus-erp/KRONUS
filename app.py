import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="KRONUS ERP - Contabilidade Completa", page_icon="📊", layout="wide"
)

# -------------------------------------------------------------------------
# CABEÇALHO COM LOGOTIPO E SLOGAN OFICIAL
# -------------------------------------------------------------------------
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
  ficheiro_logo = None
  for nome_possivel in ["logo_kronus.png", "logo.png", "logotipo.png", "kronus_logo.png"]:
    if os.path.exists(nome_possivel):
      ficheiro_logo = nome_possivel
      break
  
  if ficheiro_logo:
    st.image(ficheiro_logo, use_container_width=True)
  else:
    st.markdown("<h2 style='text-align: center;'>KRONUS S.A.</h2>", unsafe_allow_html=True)

st.markdown(
    "<h3 style='text-align: center; color: #555;'>KRONUS: Valor em cada segundo</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Criar Abas Principais (Cadastro da Empresa em primeiro)
aba_empresa, aba_contabilidade = st.tabs([
    "🏢 Cadastro da Empresa",
    "📊 Contabilidade & Demonstrações",
])

# Ficheiros de Persistência
ARQUIVO_RAZAO = "razao_analitico_caixa.csv"
ARQUIVO_EMPRESA = "cadastro_empresa.csv"

# -------------------------------------------------------------------------
# ABA 1: CADASTRO DA EMPRESA
# -------------------------------------------------------------------------
with aba_empresa:
  st.header("🏢 Cadastro e Dados Cadastrais da Empresa")
  st.markdown(
      "Gira as informações oficiais da sociedade para emissão de relatórios e conformidade legal."
  )

  dados_empresa_padrao = pd.DataFrame([{
      "Razao_Social": "KRONUS S.A. - Gestão e Participações",
      "CNPJ": "00.000.000/0001-00",
      "Inscricao_Estadual": "Isento",
      "Regime_Tributario": "Simples Nacional",
      "Endereco": "Curitiba / São José dos Pinhais - PR",
      "Contador_Responsavel": "Marcelo Denardi da Silva (CRC/PR)",
      "Email": "contato@contabilions.com.br",
  }])

  if "df_empresa" not in st.session_state:
    if os.path.exists(ARQUIVO_EMPRESA):
      try:
        st.session_state.df_empresa = pd.read_csv(ARQUIVO_EMPRESA, sep=";")
      except:
        st.session_state.df_empresa = dados_empresa_padrao
    else:
      st.session_state.df_empresa = dados_empresa_padrao
      st.session_state.df_empresa.to_csv(ARQUIVO_EMPRESA, index=False, sep=";")

  empresa_atual = st.session_state.df_empresa.iloc[0]

  regimes_disponiveis = ["Lucro Real", "Lucro Presumido", "Simples Nacional"]
  regime_atual = str(empresa_atual["Regime_Tributario"])
  idx_regime = (
      regimes_disponiveis.index(regime_atual)
      if regime_atual in regimes_disponiveis
      else 2
  )

  with st.form("form_cadastro_empresa"):
    col_c1, col_c2 = st.columns(2)
    with col_c1:
      razao_social = st.text_input(
          "Razão Social", value=str(empresa_atual["Razao_Social"])
      )
      cnpj = st.text_input("CNPJ", value=str(empresa_atual["CNPJ"]))
      inscricao_estadual = st.text_input(
          "Inscrição Estadual",
          value=str(empresa_atual["Inscricao_Estadual"]),
      )
      regime_tributario = st.selectbox(
          "Regime Tributário", regimes_disponiveis, index=idx_regime
      )

    with col_c2:
      endereco = st.text_input(
          "Endereço / Sede", value=str(empresa_atual["Endereco"])
      )
      contador_resp = st.text_input(
          "Contador Responsável / CRC",
          value=str(empresa_atual["Contador_Responsavel"]),
      )
      email_empresa = st.text_input(
          "E-mail Profissional", value=str(empresa_atual["Email"])
      )

    salvar_empresa = st.form_submit_button("💾 Salvar Dados da Empresa")

    if salvar_empresa:
      st.session_state.df_empresa = pd.DataFrame([{
          "Razao_Social": razao_social,
          "CNPJ": cnpj,
          "Inscricao_Estadual": inscricao_estadual,
          "Regime_Tributario": regime_tributario,
          "Endereco": endereco,
          "Contador_Responsavel": contador_resp,
          "Email": email_empresa,
      }])
      st.session_state.df_empresa.to_csv(ARQUIVO_EMPRESA, index=False, sep=";")
      st.success("Dados cadastrais da empresa salvos com sucesso! 🚀")
      st.rerun()

  st.markdown("---")
  st.subheader("📋 Resumo do Cadastro Atual")
  st.dataframe(st.session_state.df_empresa, use_container_width=True)

# -------------------------------------------------------------------------
# ABA 2: CONTABILIDADE & DEMONSTRAÇÕES
# -------------------------------------------------------------------------
with aba_contabilidade:
  plano_de_contas = {
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
          "5.2.3.01 - Simples Nacional (DAS) - Despesa Tributária",
          "5.2.3.02 - Taxas e Licenças Diversas",
      ],
  }

  lista_contas_analiticas = []
  for grupo, contas in plano_de_contas.items():
    for c in contas:
      lista_contas_analiticas.append(c)

  opcoes_selectbox = []
  for grupo, contas in plano_de_contas.items():
    opcoes_selectbox.append(grupo)
    for c in contas:
      opcoes_selectbox.append(c)

  dados_iniciais = [
      {
          "Data": "2026-11-01",
          "Historico": "Saldo Inicial Capital",
          "Débito": "1.1.1.02 - Bancos Conta Movimento",
          "Crédito": "2.3.1.01 - Capital Subscrito / Realizado",
          "Valor": 150000.0,
      },
      {
          "Data": "2026-11-02",
          "Historico": "Recebimento de Prestação de Serviços",
          "Débito": "1.1.1.02 - Bancos Conta Movimento",
          "Crédito": "4.1.2.01 - Receita de Prestação de Serviços (Serviços)",
          "Valor": 24.0,
      },
  ]

  if "df_lancamentos" not in st.session_state:
    if os.path.exists(ARQUIVO_RAZAO):
      try:
        df_lido = pd.read_csv(ARQUIVO_RAZAO, sep=";")
        if "Débito" not in df_lido.columns or "Crédito" not in df_lido.columns:
          st.session_state.df_lancamentos = pd.DataFrame(dados_iniciais)
          st.session_state.df_lancamentos.to_csv(ARQUIVO_RAZAO, index=False, sep=";")
        else:
          st.session_state.df_lancamentos = df_lido
      except:
        st.session_state.df_lancamentos = pd.DataFrame(dados_iniciais)
    else:
      st.session_state.df_lancamentos = pd.DataFrame(dados_iniciais)
      st.session_state.df_lancamentos.to_csv(ARQUIVO_RAZAO, index=False, sep=";")

  df_lanc = st.session_state.df_lancamentos

  total_receitas = df_lanc[
      df_lanc["Crédito"].isin(plano_de_contas["--- RECEITAS ---"])
      & df_lanc["Crédito"].str.contains("4.1", na=False)
  ]["Valor"].sum()
  deducoes_receita = df_lanc[
      df_lanc["Débito"].isin(plano_de_contas["--- RECEITAS ---"])
      & df_lanc["Débito"].str.contains("4.2", na=False)
  ]["Valor"].sum()
  receita_liquida = total_receitas - deducoes_receita

  total_custos = df_lanc[
      df_lanc["Débito"].isin(plano_de_contas["--- CUSTOS E DESPESAS ---"])
      & df_lanc["Débito"].str.contains("5.1", na=False)
  ]["Valor"].sum()
  lucro_bruto = receita_liquida - total_custos

  total_despesas = df_lanc[
      df_lanc["Débito"].isin(plano_de_contas["--- CUSTOS E DESPESAS ---"])
      & df_lanc["Débito"].str.contains("5.2", na=False)
  ]["Valor"].sum()
  lucro_liquido = lucro_bruto - total_despesas

  # -------------------------------------------------------------------------
  # 1. MÓDULO DE LANÇAMENTOS (TOPO)
  # -------------------------------------------------------------------------
  st.header("1. Módulo de Lançamentos (Partidas Dobradas)")
  st.markdown("Registe novas operações contábeis com débito e crédito cruzados.")

  if "editando_idx" not in st.session_state:
    st.session_state.editando_idx = None

  with st.form("form_partidas_dobradas", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      data_lanc = st.date_input("Data do Lançamento")
      conta_debito = st.selectbox("Conta a DEBITAR", opcoes_selectbox)
    with col2:
      valor_mov = st.number_input("Valor (R$)", min_value=0.0, format="%.2f", step=10.0)
      conta_credito = st.selectbox("Conta a CREDITAR", opcoes_selectbox)

    historico = st.text_input("Histórico / Descrição", placeholder="Ex: Recebimento de cliente ou pagamento despesa")

    submitted = st.form_submit_button("Lançar Partida Dobrada")
    if submitted:
      if conta_debito.startswith("---") or conta_credito.startswith("---"):
        st.error("Por favor, selecione uma conta analítica válida (os títulos com '---' servem apenas como divisão).")
      elif conta_debito == conta_credito:
        st.error("A conta a debitar não pode ser igual à conta a creditar numa partida dobrada!")
      else:
        novo_registo = pd.DataFrame([{
            "Data": str(data_lanc),
            "Historico": historico,
            "Débito": conta_debito,
            "Crédito": conta_credito,
            "Valor": valor_mov,
        }])
        st.session_state.df_lancamentos = pd.concat([st.session_state.df_lancamentos, novo_registo], ignore_index=True)
        st.session_state.df_lancamentos.to_csv(ARQUIVO_RAZAO, index=False, sep=";")
        st.success("Lançamento efetuado e gravado com sucesso! 🚀")
        st.rerun()

  st.markdown("---")
  st.subheader("📋 Gestão e Listagem de Lançamentos")

  for idx, row in st.session_state.df_lancamentos.iterrows():
    col_info, col_edit, col_del = st.columns([4, 1, 1])
    with col_info:
      deb = row.get("Débito", "N/A")
