import numpy as np
import plotly.express as px # type: ignore
import streamlit as st

barra_azul = "#2d5480" 
barra_azul2 = "#42658d" 
barra_azul_escuro = "#2d5c80"
barra_verde = "#176f87"
barra_vermelha = "#a22938"



barra_verde_claro = px.colors.sequential.Darkmint[3]
barra_verde_escuro = "#176f87"

barra_cinza_claro = "#c6d0d2"
barra_cinza_escuro = "#c6d0d2"


conjunto_cores = px.colors.diverging.RdBu




def table_highlight_rows(data):
    # Cores de fundo
    header_bg_color = '#2166ac'
    total_row_bg_color = '#053061'  # Cor para a linha inteira com "TOTAL" na coluna Data
    total_column_bg_color = '#4393c3'  # Cor para a coluna TOTAL
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
            elif data.columns[col_idx] == 'Data':
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


# Defina a função para aplicar estilo CSS
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
                padding: 0rem 5rem 7rem;        

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
