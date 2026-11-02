import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="KRONUS ERP - Contabilidade Completa", page_icon="📊", layout="wide"
)

# -------------------------------------------------------------------------
# CABEÇALHO CORPORATIVO COM LOGO REDIMENSIONADA À ESQUERDA E SLOGAN AO LADO
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
    # width=150 controla exatamente o tamanho compacto da logo
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

# Restante do código e abas...
aba_empresa, aba_lancamentos, aba_demonstracoes = st.tabs([
    "🏢 Cadastro da Empresa",
    "📝 Lançamentos & Diário",
    "📊 Demonstrações Contábeis",
])
