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
      "Gira as informações oficiais da sociedade para emissão de relatórios e"
      " conformidade legal."
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
  lista_contas = [
      # ATIVO CIRCULANTE
      "1.1.1.01 - Caixa Geral",
      "1.1.1.02 - Bancos Conta Movimento",
      "1.1.1.03 - Aplicações Financeiras de Liquidez Imediata",
      "1.1.2.01 - Clientes Nacionais / Duplicatas a Receber",
      "1.1.2.99 - (-) Provisão para Créditos de Liquidação Duvidosa",
      "1.1.3.01 - Mercadorias para Revenda",
      "1.1.3.02 - Matérias-Primas",
      "1.1.3.03 - Produtos em Elaboração / Acabados",
      # ATIVO NÃO CIRCULANTE
      "1.2.1.01 - Móveis e Utensílios",
      "1.2.1.02 - Máquinas e Equipamentos",
      "1.2.1.03 - Equipamentos de Informática",
      "1.2.1.09 - (-) Depreciação Acumulada",
      "1.2.2.01 - Softwares e Licenças de Uso",
      # PASSIVO CIRCULANTE
      "2.1.1.01 - Fornecedores Nacionais",
      "2.1.2.01 - Salários a Pagar",
      "2.1.2.02 - Férias e 13º Salário a Pagar",
      "2.1.2.03 - FGTS a Recolher",
      "2.1.3.01 - Simples Nacional (DAS) a Recolher",
      "2.1.3.02 - Retenções de ISS / IRRF / INSS sobre Serviços",
      # PASSIVO NÃO CIRCULANTE & PL
      "2.2.1.01 - Empréstimos e Financiamentos de Longo Prazo",
      "2.3.1.01 - Capital Subscrito / Realizado",
      "2.3.2.01 - Lucros Acumulados / Reserva de Lucros",
      # RECEITAS
      "4.1.1.01 - Receita de Vendas de Mercadorias (Comércio)",
      "4.1.2.01 - Receita de Prestação de Serviços (Serviços)",
      "4.1.3.01 - Receita de Venda de Produtos (Indústria)",
      "4.2.1.01 - (-) Devoluções de Vendas",
      "4.2.2.01 - (-) Abatimentos e Descontos Concedidos",
      # CUSTOS E DESPESAS
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
  ]

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

  # Gestão de Estado dos Lançamentos
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

  # Apurações
  total_receitas = df_lanc[df_lanc["Crédito"].str.startswith("4.1")]["Valor"].sum()
  deducoes_receita = df_lanc[df_lanc["Débito"].str.startswith("4.2")]["Valor"].sum()
  receita_liquida = total_receitas - deducoes_receita

  total_custos = df_lanc[df_lanc["Débito"].str.startswith("5.1")]["Valor"].sum()
  lucro_bruto = receita_liquida - total_custos

  total_despesas = df_lanc[df_lanc["Débito"].str.startswith("5.2")]["Valor"].sum()
  lucro_liquido = lucro_bruto - total_despesas

  # -------------------------------------------------------------------------
  # 1. BALANÇO PATRIMONIAL POR SEÇÕES
  # -------------------------------------------------------------------------
  st.header("1. Balanço Patrimonial")

  def calcular_secao(contas_lista, tipo="ativo"):
    dados = []
    total_secao = 0.0
    for conta in contas_lista:
      deb = df_lanc[df_lanc["Débito"] == conta]["Valor"].sum()
      cred = df_lanc[df_lanc["Crédito"] == conta]["Valor"].sum()
      
      if tipo == "ativo":
        saldo = deb - cred
      else: # passivo ou pl
        saldo = cred - deb

      if "Lucros Acumulados" in conta:
        saldo += lucro_liquido

      if saldo != 0.0 or True: # Mostrar mesmo com saldo zero para visual completo
        dados.append({"Conta": conta, "Saldo (R$)": saldo})
        total_secao += saldo
    return pd.DataFrame(dados), total_secao

  ativo_circulante_contas = [c for c in lista_contas if c.startswith("1.1")]
  ativo_nao_circulante_contas = [c for c in lista_contas if c.startswith("1.2")]
  passivo_circulante_contas = [c for c in lista_contas if c.startswith("2.1")]
  passivo_nao_circulante_contas = [c for c in lista_contas if c.startswith("2.2")]
  pl_contas = [c for c in lista_contas if c.startswith("2.3")]

  st.subheader("🟢 ATIVO CIRCULANTE")
  df_ac, tot_ac = calcular_secao(ativo_circulante_contas, "ativo")
  st.dataframe(df_ac, use_container_width=True)
  st.markdown(f"**Total Ativo Circulante: R$ {tot_ac:.2f}**")

  st.subheader("🔵 ATIVO NÃO CIRCULANTE")
  df_anc, tot_anc = calcular_secao(ativo_nao_circulante_contas, "ativo")
  st.dataframe(df_anc, use_container_width=True)
  st.markdown(f"**Total Ativo Não Circulante: R$ {tot_anc:.2f}**")
  st.markdown(f"### 📊 **TOTAL DO ATIVO: R$ {tot_ac + tot_anc:.2f}**")

  st.markdown("---")

  st.subheader("🟠 PASSIVO CIRCULANTE")
  df_pc, tot_pc = calcular_secao(passivo_circulante_contas, "passivo")
  st.dataframe(df_pc, use_container_width=True)
  st.markdown(f"**Total Passivo Circulante: R$ {tot_pc:.2f}**")

  st.subheader("🟤 PASSIVO NÃO CIRCULANTE")
  df_pnc, tot_pnc = calcular_secao(passivo_nao_circulante_contas, "passivo")
  st.dataframe(df_pnc, use_container_width=True)
  st.markdown(f"**Total Passivo Não Circulante: R$ {tot_pnc:.2f}**")

  st.subheader("🟣 PATRIMÔNIO LÍQUIDO")
  df_pl, tot_pl = calcular_secao(pl_contas, "passivo")
  st.dataframe(df_pl, use_container_width=True)
  st.markdown(f"**Total Patrimônio Líquido: R$ {tot_pl:.2f}**")
  st.markdown(f"### 📊 **TOTAL DO PASSIVO + PL: R$ {tot_pc + tot_pnc + tot_pl:.2f}**")

  # -------------------------------------------------------------------------
  # 2. DRE POR SEÇÕES
  # -------------------------------------------------------------------------
  st.header("2. DRE - Demonstração do Resultado do Exercício")
  
  st.subheader("📈 Receitas Operacionais")
  receitas_contas = [c for c in lista_contas if c.startswith("4.1") or c.startswith("4.2")]
  df_rec, _ = calcular_secao(receitas_contas, "passivo")
  st.dataframe(df_rec, use_container_width=True)
  st.markdown(f"**Receita Líquida: R$ {receita_liquida:.2f}**")

  st.subheader("📉 Custos das Vendas e Serviços")
  custos_contas = [c for c in lista_contas if c.startswith("5.1")]
  df_custos, _ = calcular_secao(custos_contas, "ativo")
  st.dataframe(df_custos, use_container_width=True)
  st.markdown(f"**Lucro Bruto: R$ {lucro_bruto:.2f}**")

  st.subheader("📋 Despesas Operacionais e Administrativas (incluindo DAS)")
  despesas_contas = [c for c in lista_contas if c.startswith("5.2")]
  df_desp, _ = calcular_secao(despesas_contas, "ativo")
  st.dataframe(df_desp, use_container_width=True)
  st.markdown(f"### 🎯 **Resultado Líquido do Exercício: R$ {lucro_liquido:.2f}**")

  # 3. DFC
  st.header("3. DFC - Demonstração dos Fluxos de Caixa (Método Direto)")
  entradas_caixa = df_lanc[df_lanc["Débito"].str.contains("Caixa|Bancos", na=False)]["Valor"].sum()
  saidas_caixa = df_lanc[df_lanc["Crédito"].str.contains("Caixa|Bancos", na=False)]["Valor"].sum()
  variacao_caixa = entradas_caixa - saidas_caixa

  dados_dfc = [
      {"Fluxo de Caixa": "Entradas de Caixa (Disponibilidades)", "Valor (R$)": entradas_caixa},
      {"Fluxo de Caixa": "Saídas de Caixa (Disponibilidades)", "Valor (R$)": -saidas_caixa},
      {"Fluxo de Caixa": "(=) Variação Líquida de Caixa", "Valor (R$)": variacao_caixa},
  ]
  st.dataframe(pd.DataFrame(dados_dfc), use_container_width=True)

  # 4. DVA
  st.header("4. DVA - Demonstração do Valor Adicionado")
  dados_dva = [
      {"Especificação": "Receitas (Geração de Valor)", "Valor (R$)": total_receitas},
      {"Especificação": "Insumos Adquiridos de Terceiros / Despesas", "Valor (R$)": -total_despesas},
      {"Especificação": "(=) Valor Adicionado Líquido Produzido", "Valor (R$)": lucro_liquido},
      {"Especificação": "Distribuição do Valor Adicionado (Lucros Retidos)", "Valor (R$)": lucro_liquido},
  ]
  st.dataframe(pd.DataFrame(dados_dva), use_container_width=True)

  # 5. DMPL
  st.header("5. DMPL - Demonstração das Mutações do Patrimônio Líquido")
  capital_social_inicial = df_lanc[
      (df_lanc["Crédito"].str.startswith("2.3.1"))
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

  # 6. Livro Diário
  st.header("6. Livro Diário (Registo Cronológico)")
  st.dataframe(df_lanc, use_container_width=True)

  # 7. Livro Razão e Gestão de Lançamentos
  st.header("7. Livro Razão e Gestão de Lançamentos")

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
        st.session_state.df_lancamentos.to_csv(ARQUIVO_RAZAO, index=False, sep=";")
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
            st.session_state.df_lancamentos.loc
