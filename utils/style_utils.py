import numpy as np
import plotly.express as px # type: ignore

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
