import numpy as np
import plotly.express as px
import streamlit as st

barra_azul = "#2d5480" 
barra_azul_escuro = "#2d5c80"
barra_verde = "#176f87"
barra_verde_claro = px.colors.sequential.Darkmint[3]
barra_verde_escuro = "#176f87"
barra_vermelha = "#a22938"
barra_cinza_claro = "#c6d0d2"
barra_cinza_escuro = "#c6d0d2"

#Cria um dicionário de meses por extenso
mapa_meses = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

# Mapeamento dos meses para índices numéricos
meses_mapa = {
    "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4, "Maio": 5, "Junho": 6,
    "Julho": 7, "Agosto": 8, "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
}

lista_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

# Define a função para estilizar o DataFrame
def table_highlight_rows(data):
    # Cores de fundo
    header_bg_color = '#176f87'
    total_row_bg_color = '#244366'  # Cor para a linha inteira com "TOTAL" na coluna Data
    total_column_bg_color = "#2d5480"  # Cor para a coluna TOTAL
    column_colors = ['#eeeeee', '#dddddd']

    # Cores de fonte
    header_font_color = 'white'
    total_font_color = 'white'
    default_font_color = 'black'

    # Lista de estilos
    styles = []
    for idx, row in data.iterrows():
        row_style = []
        for col_idx, item in enumerate(row):
            # Estilização para a linha inteira que tem "TOTAL" na coluna Data
            if row['Data'] == 'TOTAL' and data.columns[col_idx] != 'TOTAL':
                row_style.append(f'background-color: {total_row_bg_color}; color: {total_font_color}')
            # Estilização para a coluna Data
            elif data.columns[col_idx] == 'Data' or data.columns[col_idx] == 'APT':
                row_style.append(f'background-color: {header_bg_color}; color: {header_font_color}')
            # Estilização para a coluna TOTAL
            elif data.columns[col_idx] == 'TOTAL':
                # Estilização especial para a célula "TOTAL" na coluna "TOTAL"
                if row['Data'] == 'TOTAL':
                    row_style.append(f'background-color: {total_row_bg_color}; color: {total_font_color}')
                else:
                    row_style.append(f'background-color: {total_column_bg_color}; color: {total_font_color}')
            else:
                row_style.append(f'background-color: {column_colors[col_idx % 2]}; color: {default_font_color}')
        styles.append(row_style)

    return np.array(styles)

# Retorna uma lista de anos disponíveis (valores únicos) em uma coluna data no DataFrame
def anos_disponiveis(df):
    return sorted(df['data'].dt.year.unique())

#Retorna uma lista de meses disponíveis para um determinado ano no DataFrame
def atualiza_meses_disponiveis(ano, df):
    meses_numeros = df[df['data'].dt.year == ano]['data'].dt.month.unique()
    meses_nomes = [mapa_meses[num] for num in sorted(meses_numeros)]
    return meses_nomes

# Formata um número para o formato de moeda brasileira (R$)
def formata_para_brl(valor):
    try:
        valor = float(valor)
    except ValueError:
        return valor
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

#Converte um valor formatado em string como moeda brasileira para float
def brl_para_float(valor):
    try:
        valor = str(valor)
    except ValueError:
        return valor
    return float(valor.replace('R$', '').replace('.', '').replace(',', '.'))

# Defina a função para aplicar estilo CSS Streamlit
def aplicar_estilo():
    st.markdown(
        """
        <style> 

            #MainMenu {visibility: hidden;}    
            footer {visibility: hidden;}
            header {visibility: hidden;} 

            [data-testid="baseButton-headerNoPadding"] {
                color: #2d4f72;
            }
            [data-testid="stSidebarCollapseButton"] {
                display: unset;
            }
            
            .st-emotion-cache-1jicfl2 {
                padding: 0rem 5rem 1rem;        

            /* Estilo para o container principal das notificações */
            [data-testid="stNotification"][role="alert"] {
                border-radius: 10px !important; /* Mantém a borda arredondada */
            }

            /* Estilo para o conteúdo específico das notificações */
            [data-testid="stNotificationContentInfo"] {
                background-color: #bac2d0 !important; /* Cor de fundo para st.info */
                color: #34527e !important; /* Cor do texto para st.info */
            }
            [data-testid="stNotificationContentSuccess"] {
                background-color: #b5cbd1 !important; /* Cor de fundo para st.success */
                color: #1d6e85 !important; /* Cor do texto para st.success */
            }
            [data-testid="stNotificationContentError"] {
                background-color: #dcb5bb !important; /* Cor de fundo para st.error */
                color: #a32639 !important; /* Cor do texto para st.error */
            }

            /* Estilo para garantir que o container principal também tenha o mesmo fundo */
            [data-testid="stNotification"][role="alert"]:has([data-testid="stNotificationContentInfo"]) {
                background-color: #bac2d0 !important; /* Cor de fundo para o container principal de st.info */
                color: #34527e !important; /* Cor do texto para o container principal de st.info */
            }
            [data-testid="stNotification"][role="alert"]:has([data-testid="stNotificationContentSuccess"]) {
                background-color: #b5cbd1 !important; /* Cor de fundo para o container principal de st.success */
                color: #1d6e85 !important; /* Cor do texto para o container principal de st.success */
            }
            [data-testid="stNotification"][role="alert"]:has([data-testid="stNotificationContentError"]) {
                background-color: #dcb5bb !important; /* Cor de fundo para o container principal de st.error */
                color: #a32639 !important; /* Cor do texto para o container principal de st.error */
            }

        </style>
        """,
        unsafe_allow_html=True
    )