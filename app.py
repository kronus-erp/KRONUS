import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="KRONUS ERP - Contabilidade Completa", page_icon="📊", layout="wide"
)

# -------------------------------------------------------------------------
# CABEÇALHO CORPORATIVO COM LOGO À ESQUERDA
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
      
st.markdown("---")

# -------------------------------------------------------------------------
# CRIAÇÃO DAS ABAS PRINCIPAIS (INCLUINDO O eSOCIAL)
# -------------------------------------------------------------------------
aba_empresa, aba_lancamentos, aba_demonstracoes, aba_esocial = st.tabs([
    "🏢 Cadastro da Empresa",
    "📝 Lançamentos & Diário",
    "📊 Demonstrações Contábeis",
    "🛡️ Módulo eSocial (S-1000)"
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

dados_iniciais = [
    {
        "ID": 1,
        "Data": "2026-01-02",
        "Historico": "Subscricao de Capital Social Inicial",
        "Débito": "2.3.1.02 - Capital Subscrito a Realizar",
        "Crédito": "2.3.1.01 - Capital Subscrito / Realizado",
        "Valor": 1500.00,
    },
    {
        "ID": 2,
        "Data": "2026-01-02",
        "Historico": "Integralizacao de Capital Social em Bancos/Caixa",
        "Débito": "1.1.1.02 - Bancos Conta Movimento",
        "Crédito": "2.3.1.02 - Capital Subscrito a Realizar",
        "Valor": 1500.00,
    },
    {
        "ID": 3,
        "Data": "2026-01-02",
        "Historico": "Recebimento de Prestacao de Servicos",
        "Débito": "1.1.1.02 - Bancos Conta Movimento",
        "Crédito": "4.1.2.01 - Receita de Prestacao de Servicos",
        "Valor": 24.00,
    }
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

if "ID" not in st.session_state.df_lancamentos.columns:
    st.session_state.df_lancamentos.insert(0, "ID", range(1, len(st.session_state.df_lancamentos) + 1))

df_lanc = st.session_state.df_lancamentos

total_receitas = df_lanc[
    df_lanc["Crédito"].isin(plano_de_contas.get("--- RECEITAS ---", []))
    & df_lanc["Crédito"].str.contains("4.1", na=False)
]["Valor"].sum()
deducoes_receita = df_lanc[
    df_lanc["Débito"].isin(plano_de_contas.get("--- RECEITAS ---", []))
    & df_lanc["Débito"].str.contains("4.2", na=False)
]["Valor"].sum()
receita_liquida = total_receitas - deducoes_receita

total_custos = df_lanc[
    df_lanc["Débito"].isin(plano_de_contas.get("--- CUSTOS E DESPESAS ---", []))
    & df_lanc["Débito"].str.contains("5.1", na=False)
]["Valor"].sum()
lucro_bruto = receita_liquida - total_custos

total_despesas = df_lanc[
    df_lanc["Débito"].isin(plano_de_contas.get("--- CUSTOS E DESPESAS ---", []))
    & df_lanc["Débito"].str.contains("5.2", na=False)
]["Valor"].sum()
lucro_liquido = lucro_bruto - total_despesas

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
      empresas_disponiveis = st.session_state.df_empresa["Razao_Social"].tolist()
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
          st.session_state.df_empresa.loc[idx_emp, "Inscricao_Estadual"] = inscricao_estadual
          st.session_state.df_empresa.loc[idx_emp, "Regime_Tributario"] = regime_tributario
          st.session_state.df_empresa.loc[idx_emp, "Endereco"] = endereco
          st.session_state.df_empresa.loc[idx_emp, "Contador_Responsavel"] = contador_resp
          st.session_state.df_empresa.loc[idx_emp, "Email"] = email_empresa

          st.session_state.df_empresa.to_csv(ARQUIVO_EMPRESA, index=False, sep=";")
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
          st.error("Preencha o nome da conta ou verifique se ela já existe no grupo.")

  st.markdown("---")
  st.subheader("📋 Gestão do Plano de Contas")
  
  grupo_gestao = st.selectbox("Selecione o Grupo para Gerir", list(plano_de_contas.keys()), key="select_grupo_gestao")
  contas_grupo_atual = plano_de_contas.get(grupo_gestao, [])
  
  if contas_grupo_atual:
      for idx_c, conta_str in enumerate(contas_grupo_atual):
          col_gc1, col_gc2, col_gc3 = st.columns([5, 1, 1])
          with col_gc1:
              st.write(f"• {conta_str}")
          with col_gc2:
              if st.button("✏️", key=f"edit_c_{grupo_gestao}_{idx_c}"):
                  st.session_state["editando_conta_grupo"] = grupo_gestao
                  st.session_state["editando_conta_idx"] = idx_c
                  st.rerun()
          with col_gc3:
              if st.button("🗑️", key=f"del_c_{grupo_gestao}_{idx_c}"):
                  plano_de_contas[grupo_gestao].pop(idx_c)
                  st.session_state.plano_de_contas = plano_de_contas
                  
                  registos_plano = []
                  for g, contas in plano_de_contas.items():
                      for c in contas:
                          registos_plano.append({"Grupo": g, "Conta": c})
                  pd.DataFrame(registos_plano).to_csv(ARQUIVO_PLANO, index=False, sep=";")
                  st.success("Conta excluída com sucesso!")
                  st.rerun()
  else:
      st.info("Nenhuma conta cadastrada neste grupo.")

  if "editando_conta_grupo" in st.session_state and st.session_state["editando_conta_grupo"] == grupo_gestao:
      g_edit = st.session_state["editando_conta_grupo"]
      i_edit = st.session_state["editando_conta_idx"]
      if i_edit < len(plano_de_contas[g_edit]):
          conta_antiga = plano_de_contas[g_edit][i_edit]
          st.warning(f"A editar a conta: {conta_antiga}")
          novo_nome_conta = st.text_input("Novo Nome/Código da Conta", value=conta_antiga, key="input_edicao_conta_str")
          
          col_se, col_ce = st.columns(2)
          with col_se:
              if st.button("Salvar Alteração da Conta"):
                  plano_de_contas[g_edit][i_edit] = novo_nome_conta
                  st.session_state.plano_de_contas = plano_de_contas
                  
                  registos_plano = []
                  for g, contas in plano_de_contas.items():
                      for c in contas:
                          registos_plano.append({"Grupo": g, "Conta": c})
                  pd.DataFrame(registos_plano).to_csv(ARQUIVO_PLANO, index=False, sep=";")
                  
                  if "df_lancamentos" in st.session_state and not st.session_state.df_lancamentos.empty:
                      df_l = st.session_state.df_lancamentos
                      df_l["Débito"] = df_l["Débito"].replace(conta_antiga, novo_nome_conta)
                      df_l["Crédito"] = df_l["Crédito"].replace(conta_antiga, novo_nome_conta)
                      st.session_state.df_lancamentos = df_l
                      df_l.to_csv(ARQUIVO_RAZAO, index=False, sep=";")
                  
                  del st.session_state["editando_conta_grupo"]
                  del st.session_state["editando_conta_idx"]
                  st.success("Conta e histórico atualizados em cascata!")
                  st.rerun()
          with col_ce:
              if st.button("Cancelar Edição da Conta"):
                  del st.session_state["editando_conta_grupo"]
                  del st.session_state["editando_conta_idx"]
                  st.rerun()

  st.markdown("---")

  if "editando_idx" not in st.session_state:
    st.session_state.editando_idx = None

  if st.session_state.editando_idx is not None:
    idx_edit = st.session_state.editando_idx
    if idx_edit in st.session_state.df_lancamentos.index:
      row_edit = st.session_state.df_lancamentos.loc[idx_edit]
      st.warning(f"✏️ **Editando o Lançamento ID/Índice #{idx_edit}**")
      
      with st.form("form_edicao_lancamento"):
        col1_e, col2_e = st.columns(2)
        with col1_e:
          try:
            data_val = pd.to_datetime(row_edit["Data"]).date()
          except:
            data_val = pd.to_datetime("today").date()
          data_lanc_e = st.date_input("Data do Lançamento", value=data_val, key="edit_data")
          
          idx_deb = opcoes_selectbox.index(row_edit["Débito"]) if row_edit["Débito"] in opcoes_selectbox else 0
          conta_debito_e = st.selectbox("Conta a DEBITAR", opcoes_selectbox, index=idx_deb, key="edit_deb")
        
        with col2_e:
          valor_mov_e = st.number_input("Valor (R$)", min_value=0.0, value=float(row_edit["Valor"]), format="%.2f", step=10.0, key="edit_val")
          idx_cred = opcoes_selectbox.index(row_edit["Crédito"]) if row_edit["Crédito"] in opcoes_selectbox else 0
          conta_credito_e = st.selectbox("Conta a CREDITAR", opcoes_selectbox, index=idx_cred, key="edit_cred")
        
        historico_e = st.text_input("Histórico / Descrição", value=str(row_edit["Historico"]), key="edit_hist")
        
        col_btn_salvar, col_btn_cancelar = st.columns(2)
        with col_btn_salvar:
          sub_salvar = st.form_submit_button("💾 Salvar Alterações")
        with col_btn_cancelar:
          sub_cancelar = st.form_submit_button("❌ Cancelar Edição")
          
        if sub_salvar:
          if conta_debito_e.startswith("---") or conta_credito_e.startswith("---"):
            st.error("Selecione uma conta analítica válida!")
          elif conta_debito_e == conta_credito_e:
            st.error("Débito e Crédito não podem ser iguais!")
          else:
            st.session_state.df_lancamentos.loc[idx_edit, "Data"] = str(data_lanc_e)
            st.session_state.df_lancamentos.loc[idx_edit, "Historico"] = historico_e
            st.session_state.df_lancamentos.loc[idx_edit, "Débito"] = conta_debito_e
            st.session_state.df_lancamentos.loc[idx_edit, "Crédito"] = conta_credito_e
            st.session_state.df_lancamentos.loc[idx_edit, "Valor"] = valor_mov_e
            
            st.session_state.df_lancamentos.to_csv(ARQUIVO_RAZAO, index=False, sep=";")
            st.session_state.editando_idx = None
            st.success("Lançamento atualizado com sucesso!")
            st.rerun()
            
        if sub_cancelar:
          st.session_state.editando_idx = None
          st.rerun()

  st.subheader("➕ Novo Lançamento de Partida Dobrada")
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
        novo_id = int(st.session_state.df_lancamentos["ID"].max() + 1) if not st.session_state.df_lancamentos.empty and "ID" in st.session_state.df_lancamentos.columns else 1
        novo_registo = pd.DataFrame([{
            "ID": novo_id,
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
        st.rerun()
    with col_del:
      if st.button("🗑️", key=f"btn_del_{idx}"):
        st.session_state.df_lancamentos = st.session_state.df_lancamentos.drop(idx).reset_index(drop=True)
        st.session_state.df_lancamentos.to_csv(ARQUIVO_RAZAO, index=False, sep=";")
        if st.session_state.editando_idx == idx:
            st.session_state.editando_idx = None
        st.success("Lançamento excluído com sucesso!")
        st.rerun()


# -------------------------------------------------------------------------
# ABA 3: DEMONSTRAÇÕES CONTÁBEIS & LIVROS OFICIAIS
# -------------------------------------------------------------------------
with aba_demonstracoes:
  st.header("Demonstrações Contábeis Oficiais")
  st.markdown("Relatórios financeiros gerados em conformidade com a legislação e ITG 1000.")

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

  st.subheader("2. DRE - Demonstração do Resultado do Exercício")
  df_rec, _ = calcular_secao("--- RECEITAS ---", "passivo")
  st.dataframe(df_rec, use_container_width=True)
  st.markdown(f"**Receita Líquida: R$ {receita_liquida:.2f}**")
  
  df_desp, _ = calcular_secao("--- CUSTOS E DESPESAS ---", "ativo")
  st.dataframe(df_desp, use_container_width=True)
  st.markdown(f"### **Resultado Líquido do Exercício: R$ {lucro_liquido:.2f}**")
  st.markdown("---")

  st.header("Livros Contábeis Obrigatórios")
  st.subheader("Livro Diário")
  st.dataframe(df_lanc, use_container_width=True)


# -------------------------------------------------------------------------
# ABA 4: MÓDULO eSOCIAL (S-1000)
# -------------------------------------------------------------------------
with aba_esocial:
  st.header("🛡️ eSocial - Evento S-1000 (Informações do Empregador)")
  st.markdown("Gere o arquivo XML oficial para transmissão e validação dos dados da empresa no ambiente do eSocial.")

  def gerar_xml_s1000(
      tp_amb, proc_emi, ver_proc, tp_insc, nr_insc,
      class_trib, ind_coop, ind_constr, ind_desoneracao,
      nm_ctt, cpf_ctt, fone_fixo, email_ctt
  ):
    esocial = ET.Element(
        "eSocial", xmlns="http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_03_00"
    )
    id_evt = f"ID{tp_insc}{nr_insc.zfill(14)}2026110312000000001"
    evt = ET.SubElement(esocial, "evtInfoEmpregador", Id=id_evt)

    ide_evento = ET.SubElement(evt, "ideEvento")
    ET.SubElement(ide_evento, "tpAmb").text = str(tp_amb)
    ET.SubElement(ide_evento, "procEmi").text = str(proc_emi)
    ET.SubElement(ide_evento, "verProc").text = str(ver_proc)

    ide_empregador = ET.SubElement(evt, "ideEmpregador")
    ET.SubElement(ide_empregador, "tpInsc").text = str(tp_insc)
    ET.SubElement(ide_empregador, "nrInsc").text = str(nr_insc)

    info_empregador = ET.SubElement(evt, "infoEmpregador")
    inclusao = ET.SubElement(info_empregador, "inclusao")

    ide_periodo = ET.SubElement(inclusao, "idePeriodo")
    ET.SubElement(ide_periodo, "iniValid").text = "2026-01"

    info_cadastro = ET.SubElement(inclusao, "infoCadastro")
    ET.SubElement(info_cadastro, "classTrib").text = str(class_trib)
    ET.SubElement(info_cadastro, "indCoop").text = str(ind_coop)
    ET.SubElement(info_cadastro, "indConstr").text = str(ind_constr)
    ET.SubElement(info_cadastro, "indDesoneracao").text = str(ind_desoneracao)
    ET.SubElement(info_cadastro, "indOptRegEletron").text = "1"

    contato = ET.SubElement(info_cadastro, "contato")
    ET.SubElement(contato, "nmCtt").text = nm_ctt
    ET.SubElement(contato, "cpfCtt").text = cpf_ctt
    if fone_fixo:
      ET.SubElement(contato, "foneFijo").text = fone_fixo
    ET.SubElement(contato, "email").text = email_ctt

    xml_str = minidom.parseString(ET.tostring(esocial)).toprettyxml(indent="  ")
    return xml_str

  with st.form("form_s1000_kronus"):
    st.markdown("### 1. Parâmetros de Transmissão")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
      tp_amb = st.selectbox("Ambiente", ["2 - Produção Restrita (Testes)", "1 - Produção Real"], index=0)
      tp_amb_val = 2 if "2" in tp_amb else 1
    with col_p2:
      tp_insc = st.selectbox("Tipo de Inscrição", ["1 - CNPJ", "2 - CPF"], index=0)
      tp_insc_val = 1 if "1" in tp_insc else 2
    with col_p3:
      nr_insc = st.text_input("Número do CNPJ/CPF (somente números)", "00000000000100")

    st.markdown("---")
    st.markdown("### 2. Classificação Tributária e Regimes")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
      class_trib_opcoes = {
          "01": "01 - Simples Nacional (Sem Substituição Previdenciária)",
          "02": "02 - Simples Nacional (Com Substituição Previdenciária)",
          "03": "03 - Simples Nacional (Atividades Mistas)",
          "99": "99 - Pessoas Jurídicas em Geral (Lucro Presumido / Lucro Real)",
      }
      class_trib_sel = st.selectbox("Classificação Tributária", list(class_trib_opcoes.values()), index=0)
      class_trib_val = class_trib_sel.split(" - ")[0]

      ind_coop = st.selectbox("Indicativo de Cooperativa", [
          "0 - Não é cooperativa", "1 - Cooperativa de Trabalho",
          "2 - Cooperativa de Produção", "3 - Outras Cooperativas"
      ])
      ind_coop_val = ind_coop.split(" - ")[0]

    with col_t2:
      ind_desoneracao = st.selectbox("Desoneração da Folha (CPRB)", ["0 - Não Aplicável", "1 - Empresa Enquadrada na Desoneração"])
      ind_desoneracao_val = ind_desoneracao.split(" - ")[0]

      ind_constr = st.selectbox("Indicativo de Construtora", ["0 - Não é Construtora", "1 - Empresa Construtora"])
      ind_constr_val = ind_constr.split(" - ")[0]

    st.markdown("---")
    st.markdown("### 3. Dados do Responsável de Contato")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
      nm_ctt = st.text_input("Nome do Contato", value="Marcelo Arildo Francisco Denardi da Silva")
      cpf_ctt = st.text_input("CPF do Contato (somente números)", "00000000000")
    with col_c2:
      fone_fixo = st.text_input("Telefone de Contato", "(41) 99999-9999")
      email_ctt = st.text_input("E-mail do Responsável", "contato@contabilions.com.br")

    btn_gerar_s1000 = st.form_submit_button("⚙️ Gerar e Validar XML do S-1000")

  if btn_gerar_s1000:
    xml_resultado = gerar_xml_s1000(
        tp_amb=tp_amb_val, proc_emi=1, ver_proc="KRONUS_ERP_v1.0",
        tp_insc=tp_insc_val, nr_insc=nr_insc, class_trib=class_trib_val,
        ind_coop=ind_coop_val, ind_constr=ind_constr_val,
        ind_desoneracao=ind_desoneracao_val, nm_ctt=nm_ctt,
        cpf_ctt=cpf_ctt, fone_fixo=fone_fixo, email_ctt=email_ctt
    )

    st.success("✅ Evento S-1000 gerado com sucesso!")
    st.markdown("#### Visualização do XML Gerado:")
    st.code(xml_resultado, language="xml")

    st.download_button(
        label="📥 Baixar Arquivo XML (evtInfoEmpregador.xml)",
        data=xml_resultado,
        file_name=f"S1000_{nr_insc}.xml",
        mime="application/xml",
    )
