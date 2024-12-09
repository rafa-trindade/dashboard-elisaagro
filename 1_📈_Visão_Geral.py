import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go 
import numpy as np
from datetime import datetime
import datetime as dt

import utils.data_utils as data_utils
import utils.string_utils as string_utils
import utils.style_utils as style_utils

# ---------------------------------------------------------------------
# Configurações iniciais da página e estilo
# ---------------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="B2B Refeições | Elisa Agro", 
    initial_sidebar_state="expanded", 
    page_icon="📊")

# Chamar a função para aplicar o estilo no início do script
style_utils.aplicar_estilo()

sidebar_logo = "https://i.postimg.cc/j5mwCcfV/logo-elisa.png"
main_body_logo = "https://i.postimg.cc/3xkGPmC6/streamlit02.png"
st.logo(sidebar_logo, icon_image=main_body_logo)

# Define a data de início do contrato
data_inicio = pd.Timestamp('2024-03-01')

# ---------------------------------------------------------------------
# CARREGAMENTO DOS DADOS
# ---------------------------------------------------------------------
# Carrega o DataFrame a partir do CSV com as colunas especificadas
csv_url = "data/databaseElisa.csv"
df_elisa = pd.read_csv(csv_url, sep=";", decimal=",", thousands=".", 
                       usecols=['data', 'fazenda', 'almoco', 'janta', 'cafe', 'lanche', 'vlrCafe', 'vlrAlmoco', 'total'], 
                       index_col=None)

# Convertendo a coluna 'data' para o tipo datetime após carregar o dataframe
df_elisa['data'] = pd.to_datetime(df_elisa['data'], format='%d/%m/%Y', errors='coerce')
df_elisa['fazenda'] = df_elisa['fazenda'].astype('category')

# Opção de seleção no Streamlit (Todas as datas ou Contrato Vigente)
opcao = st.sidebar.selectbox(
    "Selecione:",
    ("Todas as datas", "Contrato Vigente")
)

# Filtrar o DataFrame conforme a opção selecionada
if opcao == "Todas as datas":
    df = df_elisa
    data_menu = df['data'].min()
else:
    df = df_elisa[df_elisa['data'] >= data_inicio]
    data_menu = df['data'].min()

col1_side, col2_side = st.sidebar.columns([2,1])

# Apresenta datas apuradas e última atualização na sidebar
col1_side.markdown('<h5 style="margin-bottom: -25px;">Início Apurado:</h5>', unsafe_allow_html=True)
col2_side.markdown(f'<h5 style="text-align: end; margin-bottom: -25px;">{data_menu.strftime("%d/%m/%Y")}</h5>', unsafe_allow_html=True)

col1_side.markdown('<h5 style="margin-bottom: 15px; color: #053061;">Última Atualização:</h5>', unsafe_allow_html=True)
col2_side.markdown('<h5 style="margin-bottom: 15px; text-align: end; color: #053061;">' + str(df['data'].max().strftime('%d/%m/%Y'))+ '</h5>', unsafe_allow_html=True)

# Criação das abas
tab1, tab2 = st.tabs(["📅 Fechamentos Diários", "\t"])

# Função auxiliar para validar se a data selecionada está disponível no DataFrame
def validate_date(selected_date, available_dates):
    """
    Verifica se a data selecionada está presente no conjunto de datas disponíveis.
    Se não estiver, exibe um erro no Streamlit.
    """
    if selected_date in available_dates:
        return True
    else:
        st.error(f"A data {selected_date.strftime('%d/%m/%Y')} não está disponível. Por favor, selecione uma data válida.")
        return False

########################################################################################
####### ABA FECHAMENTOS DIÁRIOS #########################################################
########################################################################################
with tab1:

    # Esses containers servem para organizar os elementos na tela
    with st.container(border=True):
        col_data_ini, col_data_fim = st.columns(2)
        # Aqui criamos colunas para colocar a seleção de data inicial e final
        col1, col2, col3  = st.columns([1.775,1.7,1])   
        with col1:
            ct1 = st.container()
            ct2 = st.container(border=True )
        with col2:
            ct3 = st.container(border=True )
        with col3:
            ct4 = st.container(border=True )
    with st.container(border=True):
        colradios, col4, col5= st.columns([0.65,1.3,3])
        # Containers para filtros adicionais (fazenda, tipo de refeição)
        with colradios:
            colradio1 = st.container(border=True) 
            colradio2 = st.container(border=True)
        with col4:
            ct5 = st.container(border=True )
        with col5:
            ct6 = st.container(border=True )

    # Captura do mês e ano atual
    mes_atual = dt.datetime.today().month
    ano_atual = dt.datetime.today().year

    # Lógica para definir uma data inicial padrão dependendo do dia do mês
    if df['data'].max().day < 20:
        mes_inicial_padrão = dt.date(ano_atual, mes_atual, 1)
    else:
        mes_inicial_padrão = dt.date(ano_atual, mes_atual, 20)

    # Converter novamente a coluna data para datetime (garantia)
    df['data'] = pd.to_datetime(df['data'])

    # Criação de um conjunto de datas disponíveis
    available_dates = set(df['data'].dt.date)
    min_date = df['data'].min().date()
    max_date = df['data'].max().date()

    # Seleção da data inicial
    data_inicial = col_data_ini.date_input(
        'Data Início:', 
        max_date, 
        min_value=min_date, 
        max_value=max_date, 
        format="DD/MM/YYYY",  
        key="data_inicio_key"
    )

    # Validar a data inicial selecionada
    if validate_date(data_inicial, available_dates):
        # Seleção da data final
        data_fim = col_data_fim.date_input(
            'Data Fim:', 
            None,
            min_value=data_inicial, 
            max_value=max_date, 
            format="DD/MM/YYYY", 
            key="data_fim_key",
        )
        
    # Converter as datas selecionadas para Timestamp
    if data_inicial:
        data_inicial = pd.Timestamp(data_inicial)
    if data_fim:
        data_fim = pd.Timestamp(data_fim)

    # Filtragem do DataFrame com base na seleção de datas
    if data_inicial and data_fim:
        if data_inicial > data_fim:
            # Se a data inicial for maior que a final, mostra um aviso
            st.warning('Data de início é maior que data de término!')
            filtered_df = df[(df['data'] == data_inicial)]
        else:
            filtered_df = df[(df['data'] >= data_inicial) & (df['data'] <= data_fim)]
    elif data_inicial and not data_fim:
        # Caso o usuário selecione somente data inicial (um único dia)
        filtered_df = df[df['data'] == data_inicial]
    elif data_fim and not data_inicial:
        # Caso o usuário selecione somente data final (um único dia)
        filtered_df = df[df['data'] == data_fim]
    else:
        filtered_df = df

    # Definição do período (string) para exibir no título dos gráficos e tabelas
    if data_inicial and data_fim and data_inicial != data_fim:
        dia_start = str(data_inicial.day).zfill(2)
        mes_start = str(data_inicial.month).zfill(2)
        ano_start = str(data_inicial.year)
        dia_end = str(data_fim.day).zfill(2)
        mes_end = str(data_fim.month).zfill(2)
        ano_end = str(data_fim.year)
        periodo = dia_start + "/" + mes_start + "/" + ano_start + " A " + dia_end + "/" + mes_end + "/" + ano_end
    elif data_inicial and data_fim and data_inicial == data_fim:
        periodo = data_inicial.strftime("%d/%m/%Y")
    elif data_inicial and not data_fim:
        periodo = data_inicial.strftime("%d/%m/%Y")
    elif data_fim and not data_inicial:
        periodo = data_fim.strftime("%d/%m/%Y")
    else:
        periodo = "Período não definido"

    # Obter a lista de fazendas
    lista_fazenda = df['fazenda'].unique().tolist()

    ########################################################################################
    ####### TABELA FECHAMENTO DIÁRIO #######################################################
    ########################################################################################
    # Agrupar dados para as refeições
    qtd_almoco = filtered_df.groupby("fazenda")[["almoco"]].sum(numeric_only=True).reindex(lista_fazenda)
    qtd_janta = filtered_df.groupby("fazenda")[["janta"]].sum(numeric_only=True).reindex(lista_fazenda)
    qtd_cafe = filtered_df.groupby("fazenda")[["cafe"]].sum(numeric_only=True).reindex(lista_fazenda)
    qtd_lanche = filtered_df.groupby("fazenda")[["lanche"]].sum(numeric_only=True).reindex(lista_fazenda)

    # Convertendo as séries em listas para exibição
    lista_almoco = qtd_almoco["almoco"].tolist()
    lista_janta = qtd_janta["janta"].tolist()
    lista_cafe = qtd_cafe["cafe"].tolist()
    lista_lanche = qtd_lanche["lanche"].tolist()

    # Substituir 0 por "-" para exibição
    lista_almoco_display = ['-' if v == 0 else v for v in lista_almoco]
    lista_janta_display = ['-' if v == 0 else v for v in lista_janta]
    lista_cafe_display = ['-' if v == 0 else v for v in lista_cafe]
    lista_lanche_display = ['-' if v == 0 else v for v in lista_lanche]

    data_dict = {
        "Fazenda": lista_fazenda,
        "Café": lista_cafe_display,
        "Almoço": lista_almoco_display,
        "Lanche": lista_lanche_display,
        "Janta": lista_janta_display
    }

    data_frame = pd.DataFrame(data_dict)
    # Remover linhas completamente vazias (caso existam)
    data_frame = data_frame.dropna(subset=["Café", "Almoço", "Lanche", "Janta"], how='all')

    # Calcular total das colunas
    soma_colunas = {
        "Fazenda": "<b>TOTAL</b>",
        "Café": f"<b>{int(qtd_cafe.sum(numeric_only=True).iloc[0]):,}".replace(',', '.') + "</b>",
        "Almoço": f"<b>{int(qtd_almoco.sum(numeric_only=True).iloc[0]):,}".replace(',', '.') + "</b>",
        "Lanche": f"<b>{int(qtd_lanche.sum(numeric_only=True).iloc[0]):,}".replace(',', '.') + "</b>",
        "Janta": f"<b>{int(qtd_janta.sum(numeric_only=True).iloc[0]):,}".replace(',', '.') + "</b>"
    }

    soma_colunas_df = pd.DataFrame([soma_colunas])
    # Adicionar linha de total ao final do DataFrame
    data_frame = pd.concat([data_frame, soma_colunas_df], ignore_index=True)

    # Estilização da tabela (cores de fundo e fonte)
    fill_colors = [
        ['#176f87'] * len(data_frame), 
        ['white'] * len(data_frame), 
        ['#e2e7ed'] * len(data_frame), 
        ['white'] * len(data_frame), 
        ['#e2e7ed'] * len(data_frame),
    ]
    font_colors = [
        ['white'] * len(data_frame),
        ['black'] * len(data_frame),
        ['black'] * len(data_frame),
        ['black'] * len(data_frame),
        ['black'] * len(data_frame)
    ]

    # Destacar a linha de total (com <b>)
    for i, col in enumerate(data_frame.columns):
        for j, cell_value in enumerate(data_frame[col]):
            if '<b>' in str(cell_value):
                fill_colors[i][j] = '#2d5480'
                font_colors[i][j] = 'white'

    # Criação da tabela usando Plotly
    fig_tabela_dia = go.Figure(data=[go.Table(
        header=dict(
            values=list(data_frame.columns),
            fill_color='#244366',
            line_color="lightgrey",
            font_color="white",
            font=dict(size=14.5),
            align='center',
            height=28  # Ajuste da altura do cabeçalho
        ),
        cells=dict(
            values=[data_frame[col] for col in data_frame.columns],
            fill=dict(color=fill_colors),
            line_color="lightgrey",
            font=dict(color=font_colors, size=13),
            align='center',
            height=29  # Ajuste da altura das células
        ))
    ])

    fig_tabela_dia.update_layout(
        yaxis=dict(domain=[0.3, 1]),
        height=139,
        margin=dict(r=0, t=20,b=0)
    )

    # Converter colunas relevantes para tipo numérico (se necessário para cálculos adicionais)
    data_frame['Café'] = pd.to_numeric(data_frame['Café'], errors='coerce')
    data_frame['Almoço'] = pd.to_numeric(data_frame['Almoço'], errors='coerce')
    data_frame['Lanche'] = pd.to_numeric(data_frame['Lanche'], errors='coerce')
    data_frame['Janta'] = pd.to_numeric(data_frame['Janta'], errors='coerce')

    ########################################################################################
    ####### GRÁFICO BARRAS TOTAL DE REFEIÇÕES NO PERÍODO SELECIONADO #######################
    ########################################################################################
    categorias = ['Café', 'Almoço', 'Lanche', 'Janta']
    valores = [
        data_frame['Café'].sum(numeric_only=True),
        data_frame['Almoço'].sum(numeric_only=True),
        data_frame['Lanche'].sum(numeric_only=True),
        data_frame['Janta'].sum(numeric_only=True)
    ]

    fig_barras = go.Figure(data=go.Bar(
        x=categorias,
        y=valores,
        text=valores,
        textposition='auto',
        texttemplate='%{y:.0f}',
        marker_color=["#2d5480", "#176f87", "#2d5480", "#176f87"],
        textangle=0
    ))

    fig_barras.update_layout(
        height=301,
        margin=dict(l=0, r=0, t=23, b=0),
        yaxis=dict(showticklabels=False),
        title_text=f'-QUANTIDADE TOTAL DE REFEIÇÕES ({periodo})',
        title_x=0,
        title_y=0.98,
        title_font_color="rgb(98,83,119)",
        title_font_size=15,
    )
    fig_barras.update_yaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey')
    fig_barras.update_xaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey')

    # Apresentar a tabela e o gráfico de barras
    ct1.plotly_chart(fig_tabela_dia, use_container_width=True, automargin=True)
    ct3.plotly_chart(fig_barras, use_container_width=True)

    ########################################################################################
    ####### GRÁFICO PIZZA (DISTRIBUIÇÃO POR FAZENDA) ######################################
    ########################################################################################
    fazenda_total = filtered_df.groupby("fazenda")[["total"]].sum(numeric_only=True).reset_index()
    fazenda_total = fazenda_total[fazenda_total['total'] > 0]
    total_geral = fazenda_total['total'].sum(numeric_only=True)
    fazenda_total['porcentagem'] = fazenda_total['total'] / total_geral * 100
    fazenda_total['porcentagem_formatada'] = fazenda_total['porcentagem'].apply(lambda x: f"{x:.2f}%")

    # Cria o gráfico de rosca/pizza da distribuição
    fig_venda_fazenda = px.pie(fazenda_total, names='fazenda', values='porcentagem', 
                               color='fazenda', 
                               color_discrete_sequence=[style_utils.barra_vermelha, style_utils.barra_azul, style_utils.barra_verde_escuro],
                               hover_data=['porcentagem_formatada'])

    fig_venda_fazenda.update_traces(
        texttemplate='%{label}<br>%{value:.2f}%', 
        textposition='inside'
    )

    fig_venda_fazenda.update_layout(
        height=301, 
        margin=dict(l=0, t=35, b=0, r=0),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0,
            xanchor="center",
            x=0.5,
            font=dict(size=12),
            itemsizing='constant',
            itemwidth=30,
            entrywidthmode='pixels'
        ),
        title={
            'text': f"-DISTRIBUIÇÃO ({periodo})",
            'y': 0.965,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'color': "rgb(98,83,119)",
                'size': 15
            }
        },
    )
    # Apresentar o gráfico de pizza
    ct4.plotly_chart(fig_venda_fazenda, use_container_width=True)

    ########################################################################################
    ####### BOX PLOT MENSAL PARA ANÁLISE DETALHADA #########################################
    ########################################################################################
    # Filtra para o mês e ano da data_inicial selecionada
    df_filtrado_mes = df[(pd.to_datetime(df['data']).dt.month == data_inicial.month) &
                         (pd.to_datetime(df['data']).dt.year == data_inicial.year)]

    # Agrupar e somar valores por data e fazenda
    df_agrupado = df_filtrado_mes.groupby(['data', 'fazenda']).sum(numeric_only=True).reset_index()
    df_agrupado = df_agrupado.rename(columns={'cafe': 'Café', 'almoco': 'Almoço', 'lanche': 'Lanche', 'janta': 'Janta'})  

    # Transformar o DataFrame para o formato longo
    df_long = df_agrupado.melt(id_vars=['data', 'fazenda'], value_vars=['Café', 'Almoço', 'Lanche', 'Janta'], 
                               var_name='Refeição', value_name='Valor')

    # Filtrando apenas fazendas com valor > 0
    fazendas_com_valor = df_long[df_long['Valor'] > 0]['fazenda'].unique()
    opcoes_fazenda = np.append(['Todas'], fazendas_com_valor)

    # Seleção da fazenda pelo radio
    with colradio1:
        fazenda_selecionada = st.radio("FAZENDA:", options=opcoes_fazenda, index=0, key="fazenda_selecionada")

    if fazenda_selecionada != 'Todas':
        df_filtrado_fazenda = df_long[(df_long['fazenda'] == fazenda_selecionada) & (df_long['Valor'] >= 0)]
    else:
        df_filtrado_fazenda = df_long[df_long['Valor'] >= 0]

    df_filtrado_valor_radio = df_filtrado_fazenda[df_filtrado_fazenda['Valor'] > 0]
    tipos_com_valor = df_filtrado_valor_radio['Refeição'].unique()

    # Seleção do tipo de refeição (Café, Almoço, Lanche, Janta)
    with colradio2:
        tipo_refeicao = st.radio("TIPO REFEIÇÃO:", options=tipos_com_valor, 
                                 index=list(tipos_com_valor).index("Almoço") if "Almoço" in tipos_com_valor else 0, 
                                 key="tipo_selecionado")

    df_selecionado = df_filtrado_fazenda[df_filtrado_fazenda['Refeição'] == tipo_refeicao]

    if fazenda_selecionada == 'Todas':
        # Se "Todas" foi selecionado, agrupa a soma de todas as fazendas por data
        df_selecionado = df_selecionado.groupby('data').sum(numeric_only=True).reset_index()

    # Criação do Box Plot
    fig_box = go.Figure()
    colors = {"Café": "#2d5480", "Almoço": "#2d5480", "Lanche": "#2d5480", "Janta": "#2d5480"}
    color = colors.get(tipo_refeicao, "#b3112e")  # Cor padrão se não encontrado

    fig_box.add_trace(go.Box(
        y=df_selecionado['Valor'],
        name=tipo_refeicao,
        marker=dict(color="#2d5480"),
        line=dict(color=color),
        boxpoints="all",
        hovertext=df_selecionado['data'].dt.strftime('%d/%m/%y')   
    ))

    fig_box.update_layout(
        height=284,
        margin=dict(l=0, r=0, t=30, b=0),
        title_text=f'-BOX PLOT QTD. DE REFEIÇÕES ({data_utils.mapa_meses[data_inicial.month].upper()}/{data_inicial.year})',
        title_font_color="rgb(98,83,119)",
        title_font_size=15,
        showlegend=False,
        title_x=0,
        title_y=1,
    )

    fig_box.update_yaxes(
        zerolinecolor='lightgrey',
        autorange=True,
        dtick=5,
        showline=False, 
        linecolor="Grey", 
        linewidth=0.1, 
        gridcolor='lightgrey', 
        showticklabels=True, 
        title_text='Quantidade',
    )

    fig_box.update_xaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey', title_text=f'{fazenda_selecionada}')
    fig_box.update_traces(marker=dict(size=4.5), boxmean='sd',)
    ct5.plotly_chart(fig_box, use_container_width=True)

    ########################################################################################
    ####### HISTOGRAMA MENSAL QUANTIDADES POR DIA ##########################################
    ########################################################################################
    # Criar colunas auxiliares
    df["Almoço | Janta"] = df["almoco"] + df["janta"]
    df["Café | Lanche"] = df["cafe"] + df["lanche"]
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["dia"] = df["data"].dt.day

    # Filtrar para o mês/ano selecionado
    data_selecionada = data_inicial
    df_filtrado_hist = df[(df["ano"] == data_selecionada.year) & (df["mes"] == data_selecionada.month)]
    if fazenda_selecionada != 'Todas':
        df_filtrado_hist = df_filtrado_hist[df_filtrado_hist['fazenda'] == fazenda_selecionada]

    df_grouped = df_filtrado_hist.groupby(["ano", "mes", "dia"]).sum(numeric_only=True).reset_index()
    df_grouped["Dia/Mês"] = df_grouped.apply(lambda row: f"{str(int(row['dia'])).zfill(2)}/{str(int(row['mes'])).zfill(2)}", axis=1)

    dia_selecionado = data_selecionada.day
    linhas_verticais = []
    # Adicionar linhas verticais a cada 7 dias
    for day in range(dia_selecionado, df_grouped['dia'].min() - 1, -7):
        if day in df_grouped['dia'].values:
            day_label = df_grouped[df_grouped['dia'] == day]["Dia/Mês"].values[0]
            linhas_verticais.append(day_label)
    for day in range(dia_selecionado + 7, df_grouped['dia'].max() + 1, 7):
        if day in df_grouped['dia'].values:
            day_label = df_grouped[df_grouped['dia'] == day]["Dia/Mês"].values[0]
            linhas_verticais.append(day_label)

    fig_hist = go.Figure()
    fig_hist.add_trace(go.Bar(
        x=df_grouped["Dia/Mês"],
        y=df_grouped["Almoço | Janta"],
        name="Almoço | Janta",
        marker_color="#81a8b4",
        text=df_grouped.apply(lambda row: f"<b>{int(row['Almoço | Janta'])}</b>" if row["Dia/Mês"] in linhas_verticais else "", axis=1),
        textposition='outside',
        textangle=-45,
        textfont=dict(color=style_utils.barra_verde_escuro,)
    ))

    fig_hist.add_trace(go.Bar(
        x=df_grouped["Dia/Mês"],
        y=df_grouped["Café | Lanche"],
        name="Café | Lanche",
        marker_color="#6882a0",
        text=df_grouped.apply(lambda row: f"<b>{int(row['Café | Lanche'])}</b>" if row["Dia/Mês"] in linhas_verticais else "", axis=1),
        textposition='outside',
        textangle=-45,
        textfont=dict(color=style_utils.barra_azul_escuro,)
    ))

    # Adicionar linhas verticais e horizontais no histograma
    for day_label in linhas_verticais:
        fig_hist.add_shape(
            type="line",
            x0=day_label,
            x1=day_label,
            y0=0,
            y1=df_grouped[["Almoço | Janta", "Café | Lanche"]].max().max(),
            line=dict(color="#b3112e", width=1, dash="dot")
        )

    ultimo_dia_almoco_janta = df_grouped["Almoço | Janta"].iloc[-1]
    ultimo_dia_cafe_lanche = df_grouped["Café | Lanche"].iloc[-1]

    fig_hist.add_shape(
        type="line",
        x0=df_grouped["Dia/Mês"].iloc[0],
        x1=df_grouped["Dia/Mês"].iloc[-1],
        y0=ultimo_dia_almoco_janta,
        y1=ultimo_dia_almoco_janta,
        line=dict(color="#176f87", width=1.5, dash="dashdot") 
    )

    fig_hist.add_shape(
        type="line",
        x0=df_grouped["Dia/Mês"].iloc[0],
        x1=df_grouped["Dia/Mês"].iloc[-1],
        y0=ultimo_dia_cafe_lanche,
        y1=ultimo_dia_cafe_lanche,
        line=dict(color="#2d5480", width=1.5, dash="dashdot")
    )

    # Ajuste dos ticks no eixo x
    if len(df_grouped) < 21:
        tickvals = df_grouped["Dia/Mês"].tolist()
    else:
        tickvals = linhas_verticais

    fig_hist.update_yaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey', dtick=10, 
                          range=[0, df_grouped["Almoço | Janta"].max() + 40])
    fig_hist.update_xaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey', tickmode='array', tickvals=tickvals)
    fig_hist.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        height=284,
        title_text=f'-HISTOGRAMA QUANTIDADE REFEIÇÕES AGRUPADAS ({data_utils.mapa_meses[data_inicial.month].upper()}/{data_inicial.year})',
        title_x=0,
        title_y=1,
        title_font_color="rgb(98,83,119)",
        title_font_size=15,
        barmode='group',
        yaxis=dict(showticklabels=False),
        xaxis_title="Período",
        legend=dict(x=0.7315, y=1.115, orientation='h')
    )

    # Apresentar o histograma
    ct6.plotly_chart(fig_hist, use_container_width=True, automargin=True)

    ########################################################################################
    ####### GRÁFICO ÁREA HISTÓRICO QUANTIDADES (LONGO PRAZO) ###############################
    ########################################################################################
    # Criar colunas auxiliares (já criadas acima, mas repetimos se necessário)
    df["Almoço | Janta"] = df["almoco"] + df["janta"]
    df["Café | Lanche"] = df["cafe"] + df["lanche"]
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month

    df_grouped_area = df.groupby(["ano", "mes"]).sum(numeric_only=True).reset_index()
    df_grouped_area["Mês/Ano"] = df_grouped_area.apply(lambda row: f"{data_utils.mapa_meses[int(row['mes'])]}/{int(row['ano'])}", axis=1)

    data_inicial_area = pd.Timestamp(df['data'].min())
    data_fim_area = pd.Timestamp(df['data'].max())
    periodo_area = f"{data_utils.mapa_meses[data_inicial_area.month].upper()}/{data_inicial_area.year} A {data_utils.mapa_meses[data_fim_area.month].upper()}/{data_fim_area.year}"

    current_month = pd.Timestamp.now().month
    current_year = pd.Timestamp.now().year
    previous_month = current_month - 1 if current_month != 1 else 12
    previous_year = current_year if current_month != 1 else current_year - 1

    previous_almoco_janta_value = df_grouped_area[(df_grouped_area["ano"] == previous_year) & (df_grouped_area["mes"] == previous_month)]["Almoço | Janta"].values[0]
    previous_cafe_lanche_value = df_grouped_area[(df_grouped_area["ano"] == previous_year) & (df_grouped_area["mes"] == previous_month)]["Café | Lanche"].values[0]

    fig_area = go.Figure()

    fig_area.add_trace(go.Scatter(
        x=df_grouped_area["Mês/Ano"],
        y=df_grouped_area["Almoço | Janta"],
        mode='lines+markers+text',
        name="Almoço | Janta",
        fill='tozeroy',
        marker_color=style_utils.barra_verde,
    ))

    fig_area.add_trace(go.Scatter(
        x=df_grouped_area["Mês/Ano"],
        y=df_grouped_area["Café | Lanche"],
        mode='lines+markers+text',
        name="Café | Lanche",
        fill='tozeroy',
        marker_color=style_utils.barra_azul,
        fillcolor="#6c87a6"
    ))

    # Linhas horizontais indicando valores do mês anterior
    fig_area.add_shape(
        type="line",
        x0=df_grouped_area["Mês/Ano"].iloc[0],
        x1=df_grouped_area["Mês/Ano"].iloc[-1],
        y0=previous_almoco_janta_value,
        y1=previous_almoco_janta_value,
        line=dict(color="#0e7089", width=1.5, dash="dashdot")
    )

    fig_area.add_shape(
        type="line",
        x0=df_grouped_area["Mês/Ano"].iloc[0],
        x1=df_grouped_area["Mês/Ano"].iloc[-1],
        y0=previous_cafe_lanche_value,
        y1=previous_cafe_lanche_value,
        line=dict(color="#145073", width=1.5, dash="dashdot")
    )

    previous_month_years = df_grouped_area[df_grouped_area["mes"] == previous_month]["ano"].values
    linhas_verticais = []
    for year in previous_month_years:
        month_year_label = f"{data_utils.mapa_meses[previous_month]}/{year}"
        linhas_verticais.append(month_year_label)
        fig_area.add_shape(
            type="line",
            x0=month_year_label,
            x1=month_year_label,
            y0=0,
            y1=df_grouped_area["Almoço | Janta"].max(),
            line=dict(color="#b3112e", width=1, dash="dot")
        )

    tickvals = linhas_verticais

    fig_area.update_yaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey', dtick=2000)
    fig_area.update_xaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey', tickmode='array', tickvals=tickvals)
    fig_area.update_layout(
        margin=dict(l=5, r=0, t=28, b=0),
        height=145.5,
        title=f"-HISTÓRICO REFEIÇÕES AGRUPADAS ({periodo_area})",
        title_font_color="rgb(98,83,119)",
        title_font_size=15,
        legend=dict(x=0.722, y=1.09, orientation='h'),
        title_x=0,
        title_y=1,
        yaxis=dict(showticklabels=False),
        showlegend=False
    )

    # Apresentar o gráfico de área histórico
    ct2.plotly_chart(fig_area, use_container_width=True, automargin=True)

