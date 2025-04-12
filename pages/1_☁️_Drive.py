import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide", page_title="B2B Refeições | Elisa Agro", initial_sidebar_state="expanded", page_icon="📊")


hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}    
                footer {visibility: hidden;}
                header {visibility: hidden;} 

                .st-emotion-cache-1jicfl2 {
                    padding: 4rem 4rem 7rem;
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

sidebar_logo = "https://i.postimg.cc/Hk26YfrK/logo-elisa.png"
main_body_logo = "https://i.postimg.cc/3xkGPmC6/streamlit02.png"
st.logo(sidebar_logo, icon_image=main_body_logo)


df = pd.read_csv("data/databaseElisa.csv", sep=";", decimal=",", thousands=".", usecols=['data','fazenda', 'almoco', 'janta', 'cafe','lanche', 'vlrCafe', 'vlrAlmoco', 'total'], index_col=None) 

# Convertendo a coluna 'data' para o tipo datetime após carregar o dataframe
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
df['data'] = df['data'].dt.date

col1_side, col2_side = st.sidebar.columns([2,1])

col1_side.markdown('<h5 style="margin-bottom: -25px;">Início Apurado:', unsafe_allow_html=True)
col2_side.markdown('<h5 style="text-align: end; margin-bottom: -25px;">01/01/2021</h5>', unsafe_allow_html=True)

col1_side.markdown('<h5 style="margin-bottom: 15px; color: #053061;">Última Atualização:</h5>', unsafe_allow_html=True)
col2_side.markdown('<h5 style="margin-bottom: 15px; text-align: end; color: #053061;">' + str(df['data'].max().strftime('%d/%m/%Y'))+ '</h5>', unsafe_allow_html=True)


# Ordenar o DataFrame com base na coluna 'data' para obter a data mais recente e pegar a última linha
linha_mais_recente = df.sort_values(by='data', ascending=False).iloc[0]

# Atribuir os valores às variáveis
valor_refeicao = "R$ {:,.2f}".format(linha_mais_recente['vlrAlmoco']).replace(".", "@").replace(",", ".").replace("@", ",")
valor_lanche = "R$ {:,.2f}".format(linha_mais_recente['vlrCafe']).replace(".", "@").replace(",", ".").replace("@", ",")

link_url = "https://drive.google.com/drive/folders/1LQS1tEYiy3xGVXaUMb_77jQcngjZOgXA?usp=drive_link"

with st.container(border=True, height=80):
    st.markdown(f'''
        <h4 style="text-align: center; vertical-align: middle;">
            <a href="{link_url}" target="_blank" style="text-align: center; color: #053061; text-decoration: none;" 
            onmouseover="this.style.textDecoration='none';" onmouseout="this.style.textDecoration='none';">
            ☁️ Drive Fechamentos Diários
            </a>
        </h4>
        <style>
            a:hover {{
                text-decoration: none !important;
            }}
            a:visited {{
                color: #053061;
            }}
        </style>
    ''', unsafe_allow_html=True)
 
