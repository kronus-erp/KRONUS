import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="KRONUS ERP - Contabilidade Completa", page_icon="📊", layout="wide"
)

# -------------------------------------------------------------------------
# CABEÇALHO CORPORATIVO COM LOGO À ESQUERDA E SLOGAN AO LADO
# -------------------------------------------------------------------------
col_logo, col_texto = st.columns([1, 4])

with col_logo:
  ficheiro_logo = None
  for nome_possivel in [
      "logo_kronus.png",
      "logo.png",
      "logotipo.png",
      "kronus_logo.png",
  ]:
    if os.path.exists(nome_possivel):
      ficheiro_logo = nome_possivel
      break

  if ficheiro_logo:
    st.image(ficheiro_logo, width=150)
  else:
    st.markdown("### KRONUS S.A.")

with col_texto:
  st.markdown(
      "<h2 style='margin-bottom: 0px; color: #111;'>KRONUS S.A.</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<h4 style='margin-top: 5px; color: #555; font-weight: 400;'>KRONUS: Valor"
      " em cada segundo</h4>",
      unsafe_allow_html=True,
  )

st.markdown("---")

# -------------------------------------------------------------------------
# CRIAÇÃO DAS TRÊS ABAS PRINCIPAIS
# -------------------------------------------------------------------------
aba_empresa, aba_lancamentos, aba_demonstracoes = st.tabs([
    "🏢 Cadastro da Empresa",
    "📝 Lançamentos & Diário",
    "📊 Demonstrações Contábeis",
])

# Ficheiros de Persistência
ARQUIVO_RAZAO = "razao_analitico_caixa.csv"
ARQUIVO_EMPRESA = "cadastro_empresa.csv"
ARQUIVO_PLANO = "plano_de_contas.csv"

# Plano de Contas Inicial Padrão (ITG 1000)
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

# Gestão do Plano de Contas em Session State / CSV
if "plano_de_contas" not in st.session_state:
  if os.path.exists(ARQUIVO_PLANO):
    try:
      df_p = pd.read_csv(ARQUIVO_PLANO, sep=";")
      p_dict = {}
      for grp in df_p["Grupo"].unique():
        p_dict[grp] = df_p[df_p["Grupo"] == grp]["Conta"].tolist()
      st.session_state.plano_de_contas = p_dict
    except:
      st.session_state.plano_de_contas = plano_inicial_dict
  else:
    st.session_state.plano_de_contas = plano_inicial_dict
    registos_plano = []
    for g, contas in st.session_state.plano_de_contas.items():
      for c in contas:
        registos_plano.append({"Grupo": g, "Conta": c})
    pd.DataFrame(registos_plano).to_csv(ARQUIVO_PLANO, index=False, sep=";")

plano_de_contas = st.session_state.plano_de_contas

# Listas auxiliares para selects
lista_contas_analiticas = []
for grupo, contas in plano_de_contas.items():
  for c in contas:
    lista_contas_analiticas.append(c)

opcoes_selectbox = []
for grupo, contas in plano_de_contas.items():
  opcoes_selectbox.append(grupo)
  for c in contas:
    opcoes_selectbox.append(c)

lancamentos_iniciais = [
    {
        "id": 1,
        "historico": "Subscrição de Capital Social Inicial",
        "conta_debito": "2.3.1.02 - Capital Subscrito a Realizar",
        "conta_credito": "2.3.1.01 - Capital Subscrito / Realizado",
        "valor": 1500.00,
    },
    {
        "id": 2,
        "historico": "Integralização de Capital Social em Bancos/Caixa",
        "conta_debito": "1.1.1.02 - Bancos Conta Movimento",  # Ou 1.1.1.01 - Caixa Geral
        "conta_credito": "2.3.1.02 - Capital Subscrito a Realizar",
        "valor": 1500.00,
    },
    {
        "Data": "2026-11-02",
        "Historico": "Recebimento de Prestação de Serviços"
        "Debito": "1.1.1.02 - Bancos Conta Movimento",
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
    df_lanc["Crédito"].isin(
        plano_de_contas.get("--- RECEITAS ---", [])
    )
    & df_lanc["Crédito"].str.contains("4.1", na=False)
]["Valor"].sum()
deducoes_receita = df_lanc[
    df_lanc["Débito"].isin(
        plano_de_contas.get("--- RECEITAS ---", [])
    )
    & df_lanc["Débito"].str.contains("4.2", na=False)
]["Valor"].sum()
receita_liquida = total_receitas - deducoes_receita

total_custos = df_lanc[
    df_lanc["Débito"].isin(
        plano_de_contas.get("--- CUSTOS E DESPESAS ---", [])
    )
    & df_lanc["Débito"].str.contains("5.1", na=False)
]["Valor"].sum()
lucro_bruto = receita_liquida - total_custos

total_despesas = df_lanc[
    df_lanc["Débito"].isin(
        plano_de_contas.get("--- CUSTOS E DESPESAS ---", [])
    )
    & df_lanc["Débito"].str.contains("5.2", na=False)
]["Valor"].sum()
lucro_liquido = lucro_bruto - total_despesas


# Função auxiliar de cálculo global blindada contra erros
def calcular_secao(nome_grupo, tipo="ativo"):
  contas_grupo = plano_de_contas.get(nome_grupo, [])
  dados = []
  tot = 0.0
  for conta in contas_grupo:
    try:
      deb = df_lanc[df_lanc["Débito"] == conta]["Valor"].sum()
      cred = df_lanc[df_lanc["Crédito"] == conta]["Valor"].sum()
      saldo = (deb - cred) if tipo == "ativo" else (cred - deb)
      if "Lucros Acumulados" in conta:
        saldo += lucro_liquido
      dados.append({"Conta": conta, "Saldo (R$)": saldo})
      tot += saldo
    except Exception:
      dados.append({"Conta": conta, "Saldo (R$)": 0.0})
  return pd.DataFrame(dados), tot


# -------------------------------------------------------------------------
# ABA 1: CADASTRO DA EMPRESA
# -------------------------------------------------------------------------
with aba_empresa:
  st.header("Cadastro e Dados Cadastrais da Empresa")
  st.markdown("Gira as informações oficiais da sociedade.")

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

  modo_empresa = st.radio(
      "Ação:", ["Editar Empresa Atual", "Cadastrar Nova Empresa"], horizontal=True
  )

  regimes_disponiveis = ["Lucro Real", "Lucro Presumido", "Simples Nacional"]

  if modo_empresa == "Cadastrar Nova Empresa":
    st.markdown("### Registo de Nova Empresa")
    with st.form("form_nova_empresa"):
      col_nc1, col_nc2 = st.columns(2)
      with col_nc1:
        nova_razao = st.text_input("Razão Social")
        novo_cnpj = st.text_input("CNPJ")
        nova_ie = st.text_input("Inscrição Estadual", value="Isento")
        novo_regime = st.selectbox("Regime Tributário", regimes_disponiveis)
      with col_nc2:
        novo_endereco = st.text_input("Endereço / Sede")
        novo_contador = st.text_input(
            "Contador Responsável / CRC",
            value="Marcelo Denardi da Silva (CRC/PR)",
        )
        novo_email = st.text_input("E-mail Profissional")

      salvar_nova = st.form_submit_button("Adicionar Nova Empresa")
      if salvar_nova:
        nova_linha = pd.DataFrame([{
            "Razao_Social": nova_razao,
            "CNPJ": novo_cnpj,
            "Inscricao_Estadual": nova_ie,
            "Regime_Tributario": novo_regime,
            "Endereco": novo_endereco,
            "Contador_Responsavel": novo_contador,
            "Email": novo_email,
        }])
        st.session_state.df_empresa = pd.concat(
            [st.session_state.df_empresa, nova_linha], ignore_index=True
        )
        st.session_state.df_empresa.to_csv(ARQUIVO_EMPRESA, index=False, sep=";")
        st.success("Nova empresa cadastrada com sucesso!")
        st.rerun()

  else:
    if not st.session_state.df_empresa.empty:
      empresas_disponiveis = st.session_state.df_empresa[
          "Razao_Social"
      ].tolist()
      empresa_selecionada = st.selectbox(
          "Selecione a Empresa para Gerir/Editar:", empresas_disponiveis
      )

      idx_emp = st.session_state.df_empresa[
          st.session_state.df_empresa["Razao_Social"] == empresa_selecionada
      ].index[0]
      empresa_atual = st.session_state.df_empresa.loc[idx_emp]

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

        salvar_empresa = st.form_submit_button("Atualizar Dados da Empresa")
        if salvar_empresa:
          st.session_state.df_empresa.loc[idx_emp, "Razao_Social"] = razao_social
          st.session_state.df_empresa.loc[idx_emp, "CNPJ"] = cnpj
          st.session_state.df_empresa.loc[
              idx_emp, "Inscricao_Estadual"
          ] = inscricao_estadual
          st.session_state.df_empresa.loc[
              idx_emp, "Regime_Tributario"
          ] = regime_tributario
          st.session_state.df_empresa.loc[idx_emp, "Endereco"] = endereco
          st.session_state.df_empresa.loc[
              idx_emp, "Contador_Responsavel"
          ] = contador_resp
          st.session_state.df_empresa.loc[idx_emp, "Email"] = email_empresa

          st.session_state.df_empresa.to_csv(
              ARQUIVO_EMPRESA, index=False, sep=";"
          )
          st.success("Dados atualizados com sucesso!")
          st.rerun()

  st.markdown("---")
  st.subheader("Resumo do Cadastro Atual de Empresas")
  st.dataframe(st.session_state.df_empresa, use_container_width=True)


# -------------------------------------------------------------------------
# ABA 2: LANÇAMENTOS & DIÁRIO
# -------------------------------------------------------------------------
with aba_lancamentos:
  st.header("Módulo de Lançamentos (Partidas Dobradas)")

  with st.expander("Adicionar Nova Conta Analítica ao Plano de Contas"):
    with st.form("form_nova_conta"):
      grupo_escolhido = st.selectbox(
          "Selecione o Grupo / Cabeçalho", list(plano_de_contas.keys())
      )
      nova_conta_str = st.text_input(
          "Nome/Código da Conta (ex: 5.2.2.05 - Despesas com Alimentação)"
      )
      btn_salvar_conta = st.form_submit_button("Guardar Nova Conta")

      if btn_salvar_conta:
        if nova_conta_str and nova_conta_str not in plano_de_contas[grupo_escolhido]:
          plano_de_contas[grupo_escolhido].append(nova_conta_str)
          st.session_state.plano_de_contas = plano_de_contas

          registos_plano = []
          for g, contas in plano_de_contas.items():
            for c in contas:
              registos_plano.append({"Grupo": g, "Conta": c})
          pd.DataFrame(registos_plano).to_csv(ARQUIVO_PLANO, index=False, sep=";")

          st.success(f"Conta '{nova_conta_str}' adicionada com sucesso!")
          st.rerun()
        else:
          st.error(
              "Preencha o nome da conta ou verifique se ela já existe no grupo."
          )

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
    historico = st.text_input("Histórico / Descrição")
    submitted = st.form_submit_button("Lançar Partida Dobrada")
    if submitted:
      if conta_debito.startswith("---") or conta_credito.startswith("---"):
        st.error("Selecione uma conta analítica válida!")
      elif conta_debito == conta_credito:
        st.error("Débito e Crédito não podem ser iguais!")
      else:
        novo_registo = pd.DataFrame([{
            "Data": str(data_lanc),
            "Historico": historico,
            "Débito": conta_debito,
            "Crédito": conta_credito,
            "Valor": valor_mov,
        }])
        st.session_state.df_lancamentos = pd.concat(
            [st.session_state.df_lancamentos, novo_registo], ignore_index=True
        )
        st.session_state.df_lancamentos.to_csv(ARQUIVO_RAZAO, index=False, sep=";")
        st.success("Lançamento efetuado!")
        st.rerun()

  st.markdown("---")
  st.subheader("Gestão e Listagem de Lançamentos")
  for idx, row in st.session_state.df_lancamentos.iterrows():
    col_info, col_edit, col_del = st.columns([4, 1, 1])
    with col_info:
      st.markdown(
          f"**[{idx}] {row['Data']}** | {row['Historico']} | **D:**"
          f" {row.get('Débito')} | **C:** {row.get('Crédito')} | **R$"
          f" {row['Valor']:.2f}**"
      )
    with col_edit:
      if st.button("✏️", key=f"btn_edit_{idx}"):
        st.session_state.editando_idx = idx
    with col_del:
      if st.button("🗑️", key=f"btn_del_{idx}"):
        if st.session_state.editando_idx == idx:
          st.session_state.editando_idx = None
        st.session_state.df_lancamentos = (
            st.session_state.df_lancamentos.drop(idx).reset_index(drop=True)
        )
        st.session_state.df_lancamentos.to_csv(ARQUIVO_RAZAO, index=False, sep=";")
        st.rerun()

  if st.session_state.editando_idx is not None:
    idx_edit = st.session_state.editando_idx
    if idx_edit in st.session_state.df_lancamentos.index:
      row_atual = st.session_state.df_lancamentos.loc[idx_edit]
      st.markdown(f"### A Editar o Lançamento [{idx_edit}]")
      with st.form(f"form_editar_{idx_edit}"):
        col_e1, col_e2 = st.columns(2)
        with col_e1:
          nova_data = st.text_input("Data (AAAA-MM-DD)", value=str(row_atual["Data"]))
          deb_atual = str(row_atual.get("Débito", lista_contas_analiticas[0]))
          idx_deb = opcoes_selectbox.index(deb_atual) if deb_atual in opcoes_selectbox else 0
          novo_debito = st.selectbox("Conta a DEBITAR", opcoes_selectbox, index=idx_deb)
        with col_e2:
          novo_valor = st.number_input("Valor (R$)", min_value=0.0, value=float(row_atual["Valor"]), format="%.2f", step=10.0)
          cred_atual = str(row_atual.get("Crédito", lista_contas_analiticas[0]))
          idx_cred = opcoes_selectbox.index(cred_atual) if cred_atual in opcoes_selectbox else 0
          novo_credito = st.selectbox("Conta a CREDITAR", opcoes_selectbox, index=idx_cred)

        novo_hist = st.text_input("Histórico / Descrição", value=str(row_atual["Historico"]))
        col_salv, col_canc = st.columns(2)
        with col_salv:
          salvar_edicao = st.form_submit_button("Guardar")
        with col_canc:
          cancelar_edicao = st.form_submit_button("Cancelar")

        if salvar_edicao:
          if novo_debito.startswith("---") or novo_credito.startswith("---"):
            st.error("Selecione uma conta analítica válida!")
          elif novo_debito == novo_credito:
            st.error("Débito e Crédito não podem ser iguais!")
          else:
            st.session_state.df_lancamentos.loc[idx_edit, "Data"] = nova_data
            st.session_state.df_lancamentos.loc[idx_edit, "Historico"] = novo_hist
            st.session_state.df_lancamentos.loc[idx_edit, "Débito"] = novo_debito
            st.session_state.df_lancamentos.loc[idx_edit, "Crédito"] = novo_credito
            st.session_state.df_lancamentos.loc[idx_edit, "Valor"] = novo_valor
            st.session_state.df_lancamentos.to_csv(ARQUIVO_RAZAO, index=False, sep=";")
            st.session_state.editando_idx = None
            st.success("Atualizado com sucesso!")
            st.rerun()
        if cancelar_edicao:
          st.session_state.editando_idx = None
          st.rerun()


# -------------------------------------------------------------------------
# ABA 3: DEMONSTRAÇÕES CONTÁBEIS & LIVROS OFICIAIS
# -------------------------------------------------------------------------
with aba_demonstracoes:
  st.header("Demonstrações Contábeis Oficiais")
  st.markdown("Relatórios financeiros gerados em conformidade com a legislação e ITG 1000.")

  # 1. Balanço Patrimonial
  st.subheader("1. Balanço Patrimonial")
  st.markdown("##### ATIVO")

  st.markdown("###### Ativo Circulante")
  df_ac, tot_ac = calcular_secao("--- ATIVO CIRCULANTE ---", "ativo")
  st.dataframe(df_ac, use_container_width=True)
  st.markdown(f"**Total Ativo Circulante: R$ {tot_ac:.2f}**")

  st.markdown("###### Ativo Não Circulante")
  df_anc, tot_anc = calcular_secao("--- ATIVO NÃO CIRCULANTE ---", "ativo")
  st.dataframe(df_anc, use_container_width=True)
  st.markdown(f"**Total Ativo Não Circulante: R$ {tot_anc:.2f}**")

  st.markdown(f"### **TOTAL DO ATIVO: R$ {tot_ac + tot_anc:.2f}**")
  st.markdown("---")

  st.markdown("##### PASSIVO E PATRIMÔNIO LÍQUIDO")
  st.markdown("###### Passivo Circulante")
  df_pc, tot_pc = calcular_secao("--- PASSIVO CIRCULANTE ---", "passivo")
  st.dataframe(df_pc, use_container_width=True)
  st.markdown(f"**Total Passivo Circulante: R$ {tot_pc:.2f}**")

  st.markdown("###### Passivo Não Circulante")
  df_pnc, tot_pnc = calcular_secao("--- PASSIVO NÃO CIRCULANTE ---", "passivo")
  st.dataframe(df_pnc, use_container_width=True)
  st.markdown(f"**Total Passivo Não Circulante: R$ {tot_pnc:.2f}**")

  st.markdown("###### Patrimônio Líquido")
  df_pl, tot_pl = calcular_secao("--- PATRIMÔNIO LÍQUIDO ---", "passivo")
  st.dataframe(df_pl, use_container_width=True)
  st.markdown(f"**Total Patrimônio Líquido: R$ {tot_pl:.2f}**")

  st.markdown(
      f"### **TOTAL DO PASSIVO + PL: R$ {tot_pc + tot_pnc + tot_pl:.2f}**"
  )
  st.markdown("---")

  # 2. DRE
  st.subheader("2. DRE - Demonstração do Resultado do Exercício")
  st.markdown("###### Receitas")
  df_rec, _ = calcular_secao("--- RECEITAS ---", "passivo")
  st.dataframe(df_rec, use_container_width=True)
  st.markdown(f"**Receita Líquida: R$ {receita_liquida:.2f}**")

  st.markdown("###### Custos e Despesas")
  df_desp, _ = calcular_secao("--- CUSTOS E DESPESAS ---", "ativo")
  st.dataframe(df_desp, use_container_width=True)
  st.markdown(
      f"### **Resultado Líquido do Exercício: R$ {lucro_liquido:.2f}**"
  )
  st.markdown("---")

  # 3. DFC
  st.subheader("3. DFC - Demonstração dos Fluxos de Caixa (Método Direto)")
  entradas_caixa = df_lanc[
      df_lanc["Débito"].str.contains("Caixa|Bancos", na=False)
  ]["Valor"].sum()
  saidas_caixa = df_lanc[
      df_lanc["Crédito"].str.contains("Caixa|Bancos", na=False)
  ]["Valor"].sum()
  variacao_caixa = entradas_caixa - saidas_caixa

  dados_dfc = [
      {
          "Fluxo de Caixa": "Entradas de Caixa (Disponibilidades)",
          "Valor (R$)": entradas_caixa,
      },
      {
          "Fluxo de Caixa": "Saídas de Caixa (Disponibilidades)",
          "Valor (R$)": -saidas_caixa,
      },
      {
          "Fluxo de Caixa": "(=) Variação Líquida de Caixa",
          "Valor (R$)": variacao_caixa,
      },
  ]
  st.dataframe(pd.DataFrame(dados_dfc), use_container_width=True)
  st.markdown("---")

  # 4. DVA
  st.subheader("4. DVA - Demonstração do Valor Adicionado")
  dados_dva = [
      {
          "Especificação": "Receitas (Geração de Valor)",
          "Valor (R$)": total_receitas,
      },
      {
          "Especificação": "Insumos Adquiridos de Terceiros / Despesas",
          "Valor (R$)": -total_despesas,
      },
      {
          "Especificação": "(=) Valor Adicionado Líquido Produzido",
          "Valor (R$)": lucro_liquido,
      },
      {
          "Especificação": "Distribuição do Valor Adicionado (Lucros Retidos)",
          "Valor (R$)": lucro_liquido,
      },
  ]
  st.dataframe(pd.DataFrame(dados_dva), use_container_width=True)
  st.markdown("---")

  # 5. DMPL
  st.subheader("5. DMPL - Demonstração das Mutações do Patrimônio Líquido")
  capital_social_inicial = df_lanc[
      (df_lanc["Crédito"].str.contains("2.3.1", na=False))
      & (df_lanc["Historico"].str.contains("Capital", na=False))
  ]["Valor"].sum()

  dados_dmpl = [
      {
          "Conta do PL": "Capital Subscrito / Realizado",
          "Saldo Inicial (R$)": capital_social_inicial,
          "Aumentos / Adições (R$)": 0.0,
          "Resultado do Período (R$)": 0.0,
          "Saldo Final (R$)": capital_social_inicial,
      },
      {
          "Conta do PL": "Lucros Acumulados",
          "Saldo Inicial (R$)": 0.0,
          "Aumentos / Adições (R$)": 0.0,
          "Resultado do Período (R$)": lucro_liquido,
          "Saldo Final (R$)": lucro_liquido,
      },
  ]
  st.dataframe(pd.DataFrame(dados_dmpl), use_container_width=True)
  st.markdown("---")

  # -------------------------------------------------------------------------
  # LIVROS FISCAIS E CONTÁBEIS OBRIGATÓRIOS
  # -------------------------------------------------------------------------
  st.header("Livros Fiscais e Contábeis Obrigatórios")

  # 1. Livro Diário
  st.subheader("1. Livro Diário (Registo Cronológico)")
  st.dataframe(df_lanc, use_container_width=True)
  st.markdown("---")

  # 2. Livro Caixa
  st.subheader("2. Livro Caixa (Movimentação de Caixa e Bancos)")
  df_caixa = df_lanc[
      df_lanc["Débito"].str.contains("Caixa|Bancos", na=False)
      | df_lanc["Crédito"].str.contains("Caixa|Bancos", na=False)
  ].copy()
  if not df_caixa.empty:
    st.dataframe(df_caixa, use_container_width=True)
  else:
    st.info("Nenhum lançamento registado nas contas de Caixa ou Bancos.")
  st.markdown("---")

  # 3. Livro Razão Analítico
  st.subheader("3. Livro Razão Analítico por Conta")
  conta_selecionada_razao = st.selectbox(
      "Selecione a Conta Analítica para ver o Razão:", lista_contas_analiticas
  )

  df_razao_conta = df_lanc[
      (df_lanc["Débito"] == conta_selecionada_razao)
      | (df_lanc["Crédito"] == conta_selecionada_razao)
  ].copy()

  if not df_razao_conta.empty:
    st.dataframe(df_razao_conta, use_container_width=True)
    total_debitos_conta = df_lanc[df_lanc["Débito"] == conta_selecionada_razao][
        "Valor"
    ].sum()
    total_creditos_conta = df_lanc[df_lanc["Crédito"] == conta_selecionada_razao][
        "Valor"
    ].sum()
    st.markdown(
        f"Totais na conta -- Débitos: R$ {total_debitos_conta:.2f} | Créditos:"
        f" R$ {total_creditos_conta:.2f}"
    )
  else:
    st.info(
        f"Não existem movimentos registados para a conta"
        f" {conta_selecionada_razao}."
    )
