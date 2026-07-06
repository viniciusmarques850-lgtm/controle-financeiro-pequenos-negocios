import streamlit as st
import sys 
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


from database import criar_tabelas
from models import adicionar_lancamento, listar_lancamentos, resumo_mes
from relatorios import grafico_por_categoria 
from datetime import datetime


criar_tabelas()

st.title("💰 Controle Financeiro")
st.subheader("Novo Lançamento")

with st.form("form_lancamento"):
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor, (R$)", min_value=0.01, step=0.01)
    tipo = st.selectbox("Tipo", ["entrada", "saida"])
    categoria = st.text_input("Categoria (Ex: Fixo, Vendas, Alimentação)")
    salvar = st.form_submit_button("Salvar")

    if salvar:
        if descricao and categoria:
            adicionar_lancamento(descricao, valor, tipo, categoria)
            st.success(f"Lançamento '{descricao}' adicionado com sucesso!")
        else:
                st.error("Por favor, preencha todos os campos obrigatórios.")

st.divider()
st.subheader("📊 Resumo do Mês")

mes_atual = datetime.now().month
ano_atual = datetime.now().year

resumo = resumo_mes(ano_atual, mes_atual)

col1, col2, col3 = st.columns(3)
col1.metric("Entradas", f"R$ {resumo['entrada']:.2f}")
col2.metric("Saídas", f"R$ {resumo['saida']:.2f}")
col3.metric("Saldo", f"R$ {resumo['saldo']:.2f}")

st.divider()
st.subheader("📋 Lançamentos do Mês")

lancamentos = listar_lancamentos()
if lancamentos:
    dados = [dict(l) for l in lancamentos]
    st.dataframe(dados, use_container_width=True)
else:
    st.info("Nenhum lançamento cadastrado ainda.")

    st.divider()
st.subheader("📈 Gastos por Categoria")

grafico_por_categoria(ano_atual, mes_atual)

caminho_grafico = f"docs/prints/gastos_{ano_atual}_{mes_atual:02d}.png"

if os.path.exists(caminho_grafico):
    st.image(caminho_grafico, use_container_width=True)
else:
    st.info("Nenhum dado suficiente para gerar o gráfico.")
