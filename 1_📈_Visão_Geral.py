import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt

import utils.data_utils as data_utils
import utils.string_utils as string_utils
import utils.style_utils as style_utils

st.set_page_config(layout="wide", page_title="B2B Refeições | Elisa Agro", initial_sidebar_state="expanded", page_icon="📊")

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}    
                footer {visibility: hidden;}
                header {visibility: hidden;} 
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)


sidebar_logo = "https://i.postimg.cc/j5mwCcfV/logo-elisa.png"
main_body_logo = "https://i.postimg.cc/3xkGPmC6/streamlit02.png"
st.logo(sidebar_logo, icon_image=main_body_logo)

df = pd.read_csv("data/databaseElisa.csv", sep=";", decimal=",", thousands=".", usecols=['data','fazenda', 'almoco', 'janta', 'cafe','lanche', 'vlrCafe', 'vlrAlmoco', 'total'], index_col=None) 

# Convertendo a coluna 'data' para o tipo datetime após carregar o dataframe
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
df['data'] = df['data'].dt.date

#st.sidebar.markdown('<h2 style="color: #053061; margin-bottom: -40px; text-align: center;">B2B Refeições | Elisa Agro</h2>', unsafe_allow_html=True)
#st.sidebar.markdown('<h4 style="margin-bottom: -200px; text-align: center;">(Fornecimento Alimentação)</h4>', unsafe_allow_html=True)

#st.sidebar.write("____")

col1_side, col2_side = st.sidebar.columns([2,1])

col1_side.markdown('<h5 style="margin-bottom: -25px;">Início Apurado:', unsafe_allow_html=True)
col2_side.markdown('<h5 style="text-align: end; margin-bottom: -25px;">01/01/2021</h5>', unsafe_allow_html=True)

col1_side.markdown('<h5 style="margin-bottom: 15px; color: #053061;">Última Atualização:</h5>', unsafe_allow_html=True)
col2_side.markdown('<h5 style="margin-bottom: 15px; text-align: end; color: #053061;">' + str(df['data'].max().strftime('%d/%m/%Y'))+ '</h5>', unsafe_allow_html=True)


col1_side.markdown('<h5 style="margin-bottom: -25px;">Contrato Vigente:</h5>', unsafe_allow_html=True)
col2_side.markdown('<h5 style="text-align: end; margin-bottom: -25px;">02/2027</h5>', unsafe_allow_html=True)

# Ordenar o DataFrame com base na coluna 'data' para obter a data mais recente e pegar a última linha
linha_mais_recente = df.sort_values(by='data', ascending=False).iloc[0]

# Atribuir os valores às variáveis
valor_refeicao = "R$ {:,.2f}".format(linha_mais_recente['vlrAlmoco']).replace(".", "@").replace(",", ".").replace("@", ",")
valor_lanche = "R$ {:,.2f}".format(linha_mais_recente['vlrCafe']).replace(".", "@").replace(",", ".").replace("@", ",")

col1_side.markdown('<h5 style="margin-bottom: -25px;">Refeição:</h5>', unsafe_allow_html=True)
col2_side.markdown(f'<h5 style="text-align: end; margin-bottom: -25px;">{valor_refeicao}</h5>', unsafe_allow_html=True)
col1_side.markdown('<h5 style="margin-bottom: -25px;">Lanche:</h5>', unsafe_allow_html=True)
col2_side.markdown(f'<h5 style="text-align: end; margin-bottom: -25px;">{valor_lanche}</h5>', unsafe_allow_html=True)

st.sidebar.write("____")


tab1, tab2 = st.tabs(["📅 Fechamentos Diários", "\t"])

with tab1:
    with st.container(border=True):
        col_data_ini, col_data_fim = st.columns(2)
        col1, col2, col3 = st.columns([2,2,1])     
    with st.container(border=True):
        col4 ,  col5= st.columns([2,3])

########################################################################################
####### ABA FECHAMENTOS DIÁRIOS ########################################################
########################################################################################

########################################################################################
####### TABELA FECHAMENTO DIÁRIO #######################################################
########################################################################################

mes_atual = dt.datetime.today().month
ano_atual = dt.datetime.today().year

if df['data'].max().day < 20:
    mes_inicial_padrão = dt.date(ano_atual, mes_atual, 1)
else:
    mes_inicial_padrão = dt.date(ano_atual, mes_atual, 20)

data_inicial = col_data_ini.date_input('DATA INÍCIO:', mes_inicial_padrão, None, format="DD/MM/YYYY",  key="data_inicio_key")
data_fim = col_data_fim.date_input('DATA FIM:', None, format="DD/MM/YYYY", key="data_fim_key")

if data_inicial:
    data_inicial = pd.Timestamp(data_inicial)
if data_fim:
    data_fim = pd.Timestamp(data_fim)

df['data'] = pd.to_datetime(df['data'])

if data_inicial or data_fim:
    if 'data' in df.columns:  
        if data_inicial is not None:
            dia_start = str(data_inicial.day).zfill(2)
            mes_start = str(data_inicial.month).zfill(2)
            ano_start = str(data_inicial.year)
        if data_fim is not None:
            dia_end = str(data_fim.day).zfill(2)
            mes_end = str(data_fim.month).zfill(2)
            ano_end = str(data_fim.year)
        if data_inicial and data_fim:
            if data_inicial > data_fim:
                st.warning('Data de início é maior que data de término!')
            else:
                filtered_df = df[(df['data'] >= data_inicial) & (df['data'] <= data_fim)] 

                if data_inicial == data_fim:
                    periodo = dia_start + "/" + mes_start + "/" + ano_start                
                else:
                    periodo = dia_start + "/" + mes_start + "/" + ano_start + " A " + dia_end + "/" + mes_end + "/" + ano_end
        elif data_inicial:
            periodo = dia_start + "/" + mes_start + "/" + ano_start
            filtered_df = df[(df['data'] == data_inicial)]
        elif data_fim:
            periodo = dia_end + "/" + mes_end + "/" + ano_end
            filtered_df = df[(df['data'] == data_fim)]

        lista_fazenda = df['fazenda'].unique().tolist()

        qtd_almoco = filtered_df.groupby("fazenda")[["almoco"]].sum()
        qtd_janta = filtered_df.groupby("fazenda")[["janta"]].sum()
        qtd_cafe = filtered_df.groupby("fazenda")[["cafe"]].sum()
        qtd_lanche = filtered_df.groupby("fazenda")[["lanche"]].sum()

        qtd_almoco = qtd_almoco.reindex(lista_fazenda)
        qtd_janta = qtd_janta.reindex(lista_fazenda)
        qtd_cafe = qtd_cafe.reindex(lista_fazenda)
        qtd_lanche = qtd_lanche.reindex(lista_fazenda)

        lista_almoco = qtd_almoco["almoco"].tolist()
        lista_janta = qtd_janta["janta"].tolist()
        lista_cafe = qtd_cafe["cafe"].tolist()
        lista_lanche = qtd_lanche["lanche"].tolist()

        # Cria cópias das listas para exibição com "-" no lugar de 0
        lista_almoco_display = ['-' if v == 0 else v for v in lista_almoco]
        lista_janta_display = ['-' if v == 0 else v for v in lista_janta]
        lista_cafe_display = ['-' if v == 0 else v for v in lista_cafe]
        lista_lanche_display = ['-' if v == 0 else v for v in lista_lanche]

        data = {
            "Fazenda": lista_fazenda,
            "Café": lista_cafe_display,
            "Almoço": lista_almoco_display,
            "Lanche": lista_lanche_display,
            "Janta": lista_janta_display
        }

        data_frame = pd.DataFrame(data)

        # Filtrar o data_frame para incluir apenas linhas onde algum dos valores não é NaN
        data_frame = data_frame.dropna(subset=["Café", "Almoço", "Lanche", "Janta"], how='all')

        soma_colunas = {
            "Fazenda": "<b>TOTAL</b>",
            "Café": f"<b>{int(qtd_cafe.sum(numeric_only=True).iloc[0]):,}".replace(',', '.') + "</b>",
            "Almoço": f"<b>{int(qtd_almoco.sum(numeric_only=True).iloc[0]):,}".replace(',', '.') + "</b>",
            "Lanche": f"<b>{int(qtd_lanche.sum(numeric_only=True).iloc[0]):,}".replace(',', '.') + "</b>",
            "Janta": f"<b>{int(qtd_janta.sum(numeric_only=True).iloc[0]):,}".replace(',', '.') + "</b>"
        }

        # Convertendo o dicionário para um DataFrame
        soma_colunas_df = pd.DataFrame([soma_colunas])

        data_frame = pd.concat([data_frame, soma_colunas_df], ignore_index=True)
        
        # Inicializar listas de cores para as células com as cores padrões
        fill_colors = [
            ['#0e7089'] * len(data_frame), 
            ['white'] * len(data_frame), 
            ['#e8ecec'] * len(data_frame), 
            ['white'] * len(data_frame), 
            ['#e8ecec'] * len(data_frame),
        ]
        font_colors = [
            ['white'] * len(data_frame),
            ['black'] * len(data_frame),
            ['black'] * len(data_frame),
            ['black'] * len(data_frame),
            ['black'] * len(data_frame)
        ]

        # Iterar sobre todas as células e aplicar estilo se contiver <b>
        for i, col in enumerate(data_frame.columns):
            for j, cell_value in enumerate(data_frame[col]):
                if '<b>' in str(cell_value):  # Verificar se a string <b> está presente no valor da célula
                    fill_colors[i][j] = '#006494'  # Cor de fundo
                    font_colors[i][j] = 'white'  # Cor da fonte

        # Criar a tabela
        fig_tabela_dia = go.Figure(data=[go.Table(
            header=dict(
                values=list(data_frame.columns),
                fill_color='#124b70',
                line_color="lightgrey",
                font_color="white",
                align='center',
                height=32  # Ajusta a altura do cabeçalho
            ),
            cells=dict(
                values=[data_frame[col] for col in data_frame.columns],
                fill=dict(color=fill_colors),
                line_color="lightgrey",
                font=dict(color=font_colors),
                align='center',
                height=32  # Ajusta a altura das células
            ))
        ])

        fig_tabela_dia.update_layout(
                                    yaxis=dict(
                                        domain=[0.3, 1]  # Ajuste os valores conforme necessário
                                    ),
                                    #title={ 'text': "-FECHAMENTO DE " + periodo, 'y':0.92, 'x':0.0, 'xanchor': 'left', 'yanchor': 'top'},
                                    height=310,
                                    margin=dict(r=0, t=20,b=0)
        )


        # Convertendo colunas relevantes para tipo numérico (se necessário)
        data_frame['Café'] = pd.to_numeric(data_frame['Café'], errors='coerce')
        data_frame['Almoço'] = pd.to_numeric(data_frame['Almoço'], errors='coerce')
        data_frame['Lanche'] = pd.to_numeric(data_frame['Lanche'], errors='coerce')
        data_frame['Janta'] = pd.to_numeric(data_frame['Janta'], errors='coerce')

        # Dados para o gráfico de barras
        categorias = ['Café', 'Almoço', 'Lanche', 'Janta']
        valores = [
            data_frame['Café'].sum(),
            data_frame['Almoço'].sum(),
            data_frame['Lanche'].sum(),
            data_frame['Janta'].sum()
        ]

        # Criando o gráfico de barras
        fig_barras = go.Figure(data=go.Bar(
            x=categorias,
            y=valores,
            text=valores,
            textposition='auto',
            texttemplate='%{y:.0f}',  # Formato do texto (inteiro sem casas decimais)
            marker_color=px.colors.sequential.Bluyl_r[0:2] + px.colors.sequential.Bluyl_r[0:2],  # Cor das barras
            textangle = 0

        ))

        fig_barras.update_layout(
            #title='Consumo Diário por Refeição',
            height=332,
            margin=dict(l=0, r=0, t=40, b=0),
            yaxis=dict(showticklabels=False),
            title_text='-QUANTIDADE TOTAL DE REFEIÇÕES NO PERÍODO SELECIONADO',
            title_x=0.01,
            title_y=0.94,
            title_font_color="rgb(98,83,119)"

        )
        fig_barras.update_yaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey')
        fig_barras.update_xaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey')

        # Mostrando a tabela ao lado do gráfico de barras
        col1.plotly_chart(fig_tabela_dia, use_container_width=True, automargin=True)
        col2.plotly_chart(fig_barras, use_container_width=True)

        


########################################################################################
####### GRÁFICO PIZZA FECHAMENTO DIÁRIO ################################################
########################################################################################
        # Cálculo dos totais
        fazenda_total = filtered_df.groupby("fazenda")[["total"]].sum(numeric_only=True).reset_index()

        # Filtrar as fazendas com valor maior que 0
        fazenda_total = fazenda_total[fazenda_total['total'] > 0]

        # Calcular a porcentagem relativa ao total
        total_geral = fazenda_total['total'].sum()
        fazenda_total['porcentagem'] = fazenda_total['total'] / total_geral * 100

        # Adicionando uma coluna com os valores formatados em porcentagem
        fazenda_total['porcentagem_formatada'] = fazenda_total['porcentagem'].apply(lambda x: f"{x:.2f}%")

        # Criando o gráfico de rosca
        fig_venda_fazenda = px.pie(fazenda_total, names='fazenda', values='porcentagem', 
                                color='fazenda', 
                                color_discrete_sequence=  px.colors.sequential.RdBu[1:2] + px.colors.sequential.Teal_r + px.colors.sequential.Teal_r[3:], 
                                hover_data=['porcentagem_formatada'])

        # Configurações adicionais
        fig_venda_fazenda.update_traces(
            texttemplate='%{label}<br>%{value:.2f}%', 
            textposition='inside'
        )
        
        fig_venda_fazenda.update_layout(
            #width=200, 
            height=310, 
            margin=dict(l=0, t=50, b=0, r=0), 
            showlegend=False,
            title_text='-DISTRIBUIÇÃO POR FAZENDA',
            title_x=0.1,
            title_y=0.94,
            title_font_color="rgb(98,83,119)"
        )

        col3.plotly_chart(fig_venda_fazenda, use_container_width=True)


########################################################################################
####### GRAFICO BOX PLOT MENSAL ########################################################
########################################################################################

        # Filtrar os dados para incluir apenas o mês da data mais antiga
        df_filtrado = df[(pd.to_datetime(df['data']).dt.month == data_inicial.month) &
                         (pd.to_datetime(df['data']).dt.year == data_inicial.year)]
        
        # Agrupar e somar os valores por data
        df_agrupado = df_filtrado.groupby('data').sum().reset_index()

        df_long = df_agrupado.rename(columns={'cafe': 'Café', 'almoco': 'Almoço','lanche': 'Lanche', 'janta': 'Janta'})  

        # Transformar o DataFrame para o formato longo
        df_long = df_long.melt(id_vars=['data'], value_vars=['Café', 'Almoço', 'Lanche', 'Janta'], 
                                var_name='Refeição', value_name='Valor')

        # Criar o gráfico de box
        fig_box = px.box(df_long,
                         x='Refeição',
                         y='Valor',
                        color='Refeição',
                        points="all",
                        color_discrete_sequence=  px.colors.sequential.Bluyl_r[0:1]  + px.colors.sequential.RdBu[1:2] + px.colors.sequential.RdBu_r[1:1],
                        )

        fig_box.update_layout(
            #title='Consumo Diário por Refeição',
            height=359,
            margin=dict(l=0, r=0, t=24, b=0),
            title_text=f'-BOX PLOT QUANTIDADE DE REFEIÇÕES EM {data_utils.mapa_meses[data_inicial.month].upper()}/{data_inicial.year}',
            title_x=0.00,
            title_y=0.964,
            title_font_color="rgb(98,83,119)",
            showlegend=False,

        )

        fig_box.update_yaxes(showline=False, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey', showticklabels=True, title_text='', range=[-10, df_agrupado['cafe'].max() + 30])
        fig_box.update_xaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey', title_text='REFEIÇÕES')
        fig_box.update_traces(marker=dict(size=3))


        col4.plotly_chart(fig_box, use_container_width=True)


########################################################################################
####### GRAFICO AREA HISTORICO QUANTIDADES #############################################
########################################################################################

        df["data"] = pd.to_datetime(df["data"], errors='coerce')

        df["Almoço | Janta"] = df["almoco"] + df["janta"]
        df["Café | Lanche"] = df["cafe"] + df["lanche"]

        df["ano"] = df["data"].dt.year
        df["mes"] = df["data"].dt.month

        # Agrupar os dados por ano e mês
        df_grouped = df.groupby(["ano", "mes"]).sum(numeric_only=True).reset_index()

        # Criar uma nova coluna com o formato "Mês/Ano"
        df_grouped["Mês/Ano"] = df_grouped.apply(lambda row: f"{data_utils.mapa_meses[row['mes']]}/{int(row['ano'])}", axis=1)

        # Criar o gráfico de área
        fig = go.Figure()


        # Identificar o mês e ano atual
        current_month = pd.Timestamp.now().month
        current_year = pd.Timestamp.now().year

        # Calculando o mês anterior
        previous_month = current_month - 1 if current_month != 1 else 12
        previous_year = current_year if current_month != 1 else current_year - 1

        # Identificar o valor de 'Almoço | Janta' para o mês anterior
        previous_almoco_janta_value = df_grouped[(df_grouped["ano"] == previous_year) & (df_grouped["mes"] == previous_month)]["Almoço | Janta"].values[0]
        previous_cafe_lanche_value = df_grouped[(df_grouped["ano"] == previous_year) & (df_grouped["mes"] == previous_month)]["Café | Lanche"].values[0]


        # Adicionar a linha horizontal ao gráfico
        fig.add_shape(
            type="line",
            x0=df_grouped["Mês/Ano"].iloc[0],  # Começa no primeiro ponto do eixo x
            x1=df_grouped["Mês/Ano"].iloc[-1],  # Termina no último ponto do eixo x
            y0=previous_almoco_janta_value,
            y1=previous_almoco_janta_value,
            line=dict(color="#0e7089", width=1.5, dash="dashdot")
        )

        # Adicionar a linha horizontal ao gráfico
        fig.add_shape(
            type="line",
            x0=df_grouped["Mês/Ano"].iloc[0],  # Começa no primeiro ponto do eixo x
            x1=df_grouped["Mês/Ano"].iloc[-1],  # Termina no último ponto do eixo x
            y0=previous_cafe_lanche_value,
            y1=previous_cafe_lanche_value,
            line=dict(color="#145073", width=1.5, dash="dashdot")
        )

        # Identificar o mês anterior ao atual
        current_month = pd.Timestamp.now().month
        previous_month = current_month - 1 if current_month != 1 else 12

        # Buscar os anos para os quais temos dados do mês anterior
        previous_month_years = df_grouped[df_grouped["mes"] == previous_month]["ano"].values

        # Adicionar linhas verticais para cada "Mês/Ano" do mês anterior em todos os anos disponíveis
        for year in previous_month_years:
            month_year_label = f"{data_utils.mapa_meses[previous_month]}/{year}"
            fig.add_shape(
                type="line",
                x0=month_year_label,
                x1=month_year_label,
                y0=0,
                y1=df_grouped["Almoço | Janta"].max(),  # Assumindo que isso cobre o máximo valor do gráfico
                line=dict(color="#b3112e", width=1, dash="dot")
            )

        # Adicionar a área para Almoço | Janta
        fig.add_trace(go.Scatter(
            x=df_grouped["Mês/Ano"],
            y=df_grouped["Almoço | Janta"],
            mode='lines+markers+text',  
            name="Almoço | Janta",
            fill='tozeroy',
            marker_color="#0e7089",
            #fillcolor="#b3112e"
        ))

        # Adicionar a área para Café | Lanche
        fig.add_trace(go.Scatter(
            x=df_grouped["Mês/Ano"],
            y=df_grouped["Café | Lanche"],
            mode='lines+markers+text',  # Corrigido
            name="Café | Lanche",
            fill='tozeroy',
            marker_color="#145073",
            fillcolor="#7e96a8"
        ))
               

        # Configuração do gráfico
        fig.update_yaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey')
        fig.update_xaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey')
        fig.update_layout(margin=dict(t=50), height=400, title="-HISTÓRICO QUANTIDADE DE REFEIÇÕES AGRUPADAS", title_font_color="rgb(98,83,119)", yaxis_title="Quantidade")

        # Exibir o gráfico no Streamlit
        col5.plotly_chart(fig, use_container_width=True, automargin=True)
