import pandas as pd
import streamlit as st

# Configuração da Página - Estilo Clean / Sebrae Markup
st.set_page_config(
    page_title="Chronos S.A. - Sistema Contábil & Societário",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏛️ CHRONOS S.A. — Ecossistema Contábil e Financeiro")
st.markdown(
    "*Módulo Integrado de Demonstrações Contábeis Oficiais e Notas Explicativas*"
)
st.divider()

# ==========================================
# 1. BASE DE DADOS SIMULADA (MOCK DE SALDOS)
# ==========================================
# Em um ambiente de produção, estes dados vêm do motor de partidas dobradas / razão.
@st.cache_data
def carregar_saldos_contabeis():
  contas = {
      "1.1.1.01": {
          "nome": "Caixa e Equivalentes de Caixa",
          "grupo": "Ativo Circulante",
          "saldo": 150000.0,
      },
      "1.1.2.01": {
          "nome": "Clientes / Duplicatas a Receber",
          "grupo": "Ativo Circulante",
          "saldo": 85000.0,
      },
      "1.1.3.01": {
          "nome": "Estoques de Mercadorias",
          "grupo": "Ativo Circulante",
          "saldo": 140000.0,
      },  # Já líquido da eliminação de lucros!
      "1.2.1.01": {
          "nome": "Imobilizado (Máquinas e Equipamentos)",
          "grupo": "Ativo Não Circulante",
          "saldo": 250000.0,
      },
      "2.1.1.01": {
          "nome": "Fornecedores Nacionais",
          "grupo": "Passivo Circulante",
          "saldo": 60000.0,
      },
      "2.1.2.01": {
          "nome": "Obrigações Fiscais e Trabalhistas",
          "grupo": "Passivo Circulante",
          "saldo": 45000.0,
      },
      "2.2.1.01": {
          "nome": "Financiamentos de Longo Prazo",
          "grupo": "Passivo Não Circulante",
          "saldo": 120000.0,
      },
      "2.3.1.01": {
          "nome": "Capital Social Realizado",
          "grupo": "Patrimônio Líquido",
          "saldo": 250000.0,
      },
      "2.3.2.01": {
          "nome": "Reservas de Lucros",
          "grupo": "Patrimônio Líquido",
          "saldo": 50000.0,
      },
      "3.1.1.01": {
          "nome": "Receita Bruta de Vendas",
          "grupo": "DRE - Receitas",
          "saldo": 500000.0,
      },
      "3.1.2.01": {
            "nome": "Deduções da Receita Bruta (Tributos)",
            "grupo": "DRE - Deduções",
            "saldo": -75000.0,
      },
      "3.2.1.01": {
          "nome": "Custo das Mercadorias Vendidas (CMV)",
          "grupo": "DRE - Custos",
          "saldo": -200000.0,
      },
      "3.3.1.01": {
            "nome": "Despesas Operacionais / Administrativas",
            "grupo": "DRE - Despesas",
            "saldo": -125000.0,
      },
  }
  return pd.DataFrame.from_dict(contas, orient="index")


df_saldos = carregar_saldos_contabeis()

# ==========================================
# 2. MENU LATERAL DE NAVEGAÇÃO
# ==========================================
st.sidebar.header("Módulos de Relatórios")
menu = st.sidebar.selectbox(
    "Selecione a Demonstração:",
    [
        "Balancete de Verificação",
        "Balanço Patrimonial (BP)",
        "DRE",
        "DRA",
        "DMPL / DLPA",
        "DFC (Fluxo de Caixa)",
        "DVA",
        "Notas Explicativas (Completa)",
        "Relatório Societário & Custos",
    ],
)

# ==========================================
# 3. RENDERIZAÇÃO DOS MÓDULOS
# ==========================================

if menu == "Balancete de Verificação":
  st.subheader("📊 Balancete de Verificação Analítico/Sintético")
  st.dataframe(df_saldos, use_container_width=True)
  total_saldos = df_saldos["saldo"].sum()
  st.metric(
      label="Batimento Geral (Ativo - Passivo/PL/Resultado)",
      value=f"R$ {total_saldos:,.2f}",
  )

elif menu == "Balanço Patrimonial (BP)":
  st.subheader("🏛️ Balanço Patrimonial - Visão Consolidada")

  col1, col2 = st.columns(2)
  with col1:
    st.markdown("### ATIVO")
    ativo_circ = df_saldos[
        df_saldos["grupo"].isin(["Ativo Circulante"])
    ]["saldo"].sum()
    ativo_nao_circ = df_saldos[
        df_saldos["grupo"].isin(["Ativo Não Circulante"])
    ]["saldo"].sum()

    st.write(
        f"**Ativo Circulante:** R$ {ativo_circ:,.2f}"
    )  # Já com estoque ajustado (140k)
    st.write(f"**Ativo Não Circulante:** R$ {ativo_nao_circ:,.2f}")
    st.metric(
        "**TOTAL DO ATIVO**", f"R$ {ativo_circ + ativo_nao_circ:,.2f}"
    )

  with col2:
    st.markdown("### PASSIVO & PATRIMÔNIO LÍQUIDO")
    pass_circ = df_saldos[
        df_saldos["grupo"].isin(["Passivo Circulante"])
    ]["saldo"].sum()
    pass_nao_circ = df_saldos[
        df_saldos["grupo"].isin(["Passivo Não Circulante"])
    ]["saldo"].sum()
    pl = df_saldos[df_saldos["grupo"].isin(["Patrimônio Líquido"])][
        "saldo"
    ].sum()
    # Adicionando o resultado do exercício ao PL provisoriamente para fechamento
    lucro_liq = (
        df_saldos[df_saldos["grupo"].str.startswith("DRE")]["saldo"].sum()
    )

    st.write(f"**Passivo Circulante:** R$ {pass_circ:,.2f}")
    st.write(f"**Passivo Não Circulante:** R$ {pass_nao_circ:,.2f}")
    st.write(f"**Patrimônio Líquido Base:** R$ {pl:,.2f}")
    st.write(f"**Lucro Líquido do Exercício:** R$ {lucro_liq:,.2f}")
    st.metric(
        "**TOTAL PASSIVO + PL**",
        f"R$ {pass_circ + pass_nao_circ + pl + lucro_liq:,.2f}",
    )

elif menu == "DRE":
  st.subheader("📈 Demonstração do Resultado do Exercício (DRE)")
  receita_bruta = df_saldos.loc["3.1.1.01", "saldo"]
  deducoes = df_saldos.loc["3.1.2.01", "saldo"]
  receita_liq = receita_bruta + deducoes
  cmv = df_saldos.loc["3.2.1.01", "saldo"]
  lucro_bruto = receita_liq + cmv
  despesas = df_saldos.loc["3.3.1.01", "saldo"]
  lair = lucro_bruto + despesas

  st.write(f"Receita Bruta de Vendas: R$ {receita_bruta:,.2f}")
  st.write(f"(-) Deduções da Receita Bruta: R$ {deducoes:,.2f}")
  st.markdown(f"**(=) Receita Líquida:** R$ {receita_liq:,.2f}")
  st.write(f"(-) Custo das Mercadorias Vendidas (CMV): R$ {cmv:,.2f}")
  st.markdown(f"**(=) Lucro Bruto:** R$ {lucro_bruto:,.2f}")
  st.write(f"(-) Despesas Operacionais: R$ {despesas:,.2f}")
  st.metric("**(=) Resultado Líquido do Período (LAIR):**", f"R$ {lair:,.2f}")

elif menu == "DRA":
  st.subheader("🌐 Demonstração do Resultado Abrangente (DRA)")
  st.info(
      "Apresenta os ganhos e perdas não reconhecidos no resultado (ex: ajustes"
      " de avaliação patrimonial)."
  )
  st.write("Lucro Líquido do Período: R$ 100.000,00")
  st.write(
      "Outros Resultados Abrangentes (Ajustes de conversão / Mark-to-Market):"
      " R$ 0,00"
  )
  st.metric(
      "**Resultado Abrangente Total do Período:**", "R$ 100.000,00"
  )

elif menu == "DMPL / DLPA":
  st.subheader(
      "🔄 Demonstração das Mutações do Patrimônio Líquido (DMPL) & DLPA"
  )
  st.table(
      pd.DataFrame({
          "Conta do PL": [
              "Capital Social",
              "Reservas de Lucros",
              "Lucros Acumulados",
          ],
          "Saldo Inicial": ["R$ 250.000,00", "R$ 50.000,00", "R$ 0,00"],
          "Aumentos / Lucro": ["R$ 0,00", "R$ 0,00", "R$ 100.000,00"],
          "Destinações / Baixas": ["R$ 0,00", "R$ 0,00", "R$ 0,00"],
          "Saldo Final": ["R$ 250.000,00", "R$ 50.000,00", "R$ 100.000,00"],
      })
  )

elif menu == "DFC (Fluxo de Caixa)":
  st.subheader("💵 Demonstração dos Fluxos de Caixa (DFC - Método Indireto)")
  st.write("Lucro Líquido Ajustado: R$ 100.000,00")
  st.write("(+) Depreciação e Amortização: R$ 15.000,00")
  st.write("(-) Aumento em Duplicatas a Receber: (R$ 10.000,00)")
  st.write("(+) Aumento em Fornecedores: R$ 8.000,00")
  st.metric(
      "**Geração Líquida de Caixa pelas Atividades Operacionais:**",
      "R$ 113.000,00",
  )

elif menu == "DVA":
  st.subheader("⚖️ Demonstração do Valor Adicionado (DVA)")
  st.write(
      "1. Receitas (Vendas de Mercadorias e Serviços): R$ 500.000,00"
  )
  st.write("2. Insumos Adquiridos de Terceiros (CMV + Despesas): (R$ 325.000,00)")
  st.markdown("**3. Valor Adicionado Bruto: R$ 175.000,00**")
  st.write("4. Retenções (Depreciação): (R$ 15.000,00)")
  st.markdown("**5. Valor Adicionado Líquido Produzido: R$ 160.000,00**")

elif menu == "Notas Explicativas (Completa)":
  st.subheader("📝 Notas Explicativas às Demonstrações Contábeis")
  st.markdown(
      "*Em conformidade com os CPCs e a Lei das S.A. (Lei nº 6.404/76)*"
  )

  with st.expander("Nota 1: Contexto Operacional", expanded=True):
    st.write(
        "A **Chronos S.A.** é uma sociedade anônima de capital fechado,"
        " com sede em Curitiba-PR, tendo por objeto social o desenvolvimento de"
        " soluções corporativas, contábeis e participações societárias."
    )

  with st.expander("Nota 2: Apresentação e Normas Contábeis"):
    st.write(
        "As demonstrações contábeis foram elaboradas de acordo com as práticas"
        " contábeis adotadas no Brasil, incluindo os Pronunciamentos Técnicos"
        " do CPC e as Normas Brasileiras de Contabilidade (NBC TG)."
    )

  with st.expander("Nota 3: Critérios de Avaliação de Estoques (Eliminação MEP)"):
    st.write(
        "Os estoques são avaliados ao custo de aquisição ou valor líquido"
        " de realização, dos dois o menor. Foram integralmente eliminados os"
        " lucros não realizados decorrentes de transações intercompanhias"
        " (matriz e controladas), totalizando o ajuste de R$ 20.000,00 no saldo"
        " consolidado do exercício."
    )

  with st.expander("Nota 4: Instrumentos Financeiros e Gestão de Riscos"):
    st.write(
        "A Companhia adota políticas prudentes de gestão de capital de giro,"
        " abstendo-se de operações de crédito onerosas de longo prazo que"
        " comprometam a liquidez e a estrutura de solvência patrimonial."
    )

elif menu == "Relatório Societário & Custos":
  st.subheader("🏢 Relatório Societário, Equivalência Patrimonial e Custos")
  st.info(
      "Painel de controle com parâmetros de coligadas, controle de estoques"
      " intercompany e margens."
  )
  st.write(
      "- **Participação Societária (MEP):** Monitoramento ativo de controladas"
      " com eliminação de lucros não realizados."
  )
  st.write(
      "- **Margem de Contribuição Operacional:** Alinhada ao ponto de"
      " equilíbrio estrutural da companhia."
  )

st.divider()
st.caption(
    "Chronos S.A. Engine — Arquitetura de Alta Performance | Desenvolvido com"
    " foco em Governança e Transparência."
)
