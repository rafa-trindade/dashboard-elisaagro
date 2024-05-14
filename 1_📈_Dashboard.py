import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime as dt
from datetime import datetime




st.set_page_config(layout="wide", page_title="B2B Refeições | Elisa Agro", initial_sidebar_state="expanded", page_icon="📊")

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}    
                footer {visibility: hidden;}
                header {visibility: hidden;} 
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            background-image: url(https://i.postimg.cc/52vw7RW6/streamlit-Logo2.png);
            background-repeat: no-repeat;
            padding-top: 37px;
            background-position: 18px 55px;
            position: relative;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

df = pd.read_csv("databaseElisa.csv", sep=";", decimal=",", thousands=".", usecols=['data','fazenda', 'almoco', 'janta', 'cafe','lanche', 'vlrCafe', 'vlrAlmoco', 'total'], index_col=None) 

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

link_url = "https://drive.google.com/drive/folders/1N4V0ZJLiGAHxRrBpVPHv0hqkFJ3CwFsM"
st.sidebar.markdown(f'''
    <h4 style="text-align: center;">
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



tab1, tab2, tab3, tab4 = st.tabs(["📅 Fechamentos Diários", "📊 Visão Mensal", "📊 Visão Anual", "📈 Análise Quanti-Qualitativa"])

with tab1:
    col_data_ini, col_data_fim = st.columns(2)
    col1, col2 = st.columns([2,1])
    st.write("---")
    c1 = st.container()
with tab2:
    col_filtro_mes, col_filtro_ano = st.columns(2)  
    col5, col6 = st.columns([2,1])
with tab3:
    col3, col4 = st.columns([1,3])
with tab4:
    col_data_ini_quali, col_data_fim_quali = st.columns(2)
    c4 = st.container()




# Dicionário para mapear número do mês ao nome em português com a primeira letra maiúscula
meses = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

colors = px.colors.diverging.RdBu



#################### Tabela Demostrativo Período ########################

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

        data = {
            "Fazenda": lista_fazenda,
            "Café": lista_cafe,
            "Almoço": lista_almoco,
            "Lanche": lista_lanche,
            "Janta": lista_janta
        }

        data_frame = pd.DataFrame(data)

        # Filtrar o data_frame para incluir apenas linhas onde algum dos valores não é NaN
        data_frame = data_frame.dropna(subset=["Café", "Almoço", "Lanche", "Janta"], how='all')

        soma_colunas = {
            "Fazenda": "<b>TOTAL</b>",
            "Café": "<b>" + str('{0:,}'.format(int(data_frame["Café"].sum())).replace(',','.')) + "</b>",
            "Almoço": "<b>" + str('{0:,}'.format(int(data_frame["Almoço"].sum())).replace(',','.')) + "</b>",
            "Lanche": "<b>" + str('{0:,}'.format(int(data_frame["Lanche"].sum())).replace(',','.')) + "</b>",
            "Janta": "<b>" + str('{0:,}'.format(int(data_frame["Janta"].sum())).replace(',','.')) + "</b>"
        }

        data_frame = data_frame.append(soma_colunas, ignore_index=True)

        fig_tabela_dia = go.Figure(data=[go.Table(
                        header=dict(
                            values=list(data_frame.columns),
                            fill_color='#004d72',
                            line_color="lightgrey",
                            font_color="white",
                            align='center',
                            height=25  # Ajusta a altura do cabeçalho
                        ),
                        cells=dict(
                            values=[data_frame.Fazenda, data_frame.Café, data_frame.Almoço, data_frame.Lanche, data_frame.Janta],
                            fill=dict(color=['#DEE6EF', 'white','#f7f7f7','white','#f7f7f7']),
                            line_color="lightgrey",
                            font_color="black",
                            align='center',
                            height=25  # Ajusta a altura das células
                        ))
                    ])

        fig_tabela_dia.update_layout(
                                    yaxis=dict(
                                        domain=[0.3, 1]  # Ajuste os valores conforme necessário
                                    ),
                                    title={ 'text': "-FECHAMENTO DE " + periodo, 'y':0.92, 'x':0.0, 'xanchor': 'left', 'yanchor': 'top'},
                                    height=282,
                                    margin=dict(r=10, t=50,b=0)
        )
        
        col1.plotly_chart(fig_tabela_dia, use_container_width=True, automargin=True)



#################### Gráfico Fazenda Período ########################


        # Cálculo dos totais
        fazenda_total = filtered_df.groupby("fazenda")[["total"]].sum().reset_index()

        # Adicionando uma coluna com os valores formatados em R$
        fazenda_total['total_formatado'] = fazenda_total['total'].apply(lambda x: f"R$ {x:,.2f}".replace('.', '@').replace(',', '.').replace('@', ','))

        # Criando o gráfico
        fig_venda_fazenda = px.pie(fazenda_total, names="fazenda", values="total", color_discrete_sequence=px.colors.sequential.RdBu,
                                hover_data=['total_formatado'], hover_name='fazenda')

        # Configurações adicionais
        fig_venda_fazenda.update_traces(textposition='inside', textinfo='percent+label')
        fig_venda_fazenda.update_layout(width=600, height=282, margin=dict(l=10., t=50,b=0))
        col2.plotly_chart(fig_venda_fazenda, use_container_width=True)



#################### Comparativo Mensal entre Almoço | Janta e Café | Lanche ########################
 
        # Definindo cores

        df["data"] = pd.to_datetime(df["data"], errors='coerce')

        df["Almoço | Janta"] = df["almoco"] + df["janta"]
        df["Café | Lanche"] = df["cafe"] + df["lanche"]

        df["ano"] = df["data"].dt.year
        df["mes"] = df["data"].dt.month

        # Agrupar os dados por ano e mês
        df_grouped = df.groupby(["ano", "mes"]).sum().reset_index()

        # Criar uma nova coluna com o formato "Mês/Ano"
        df_grouped["Mês/Ano"] = df_grouped.apply(lambda row: f"{meses[row['mes']]}/{int(row['ano'])}", axis=1)

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
            line=dict(color="red", width=1.5, dash="dashdot")
        )

        # Adicionar a linha horizontal ao gráfico
        fig.add_shape(
            type="line",
            x0=df_grouped["Mês/Ano"].iloc[0],  # Começa no primeiro ponto do eixo x
            x1=df_grouped["Mês/Ano"].iloc[-1],  # Termina no último ponto do eixo x
            y0=previous_cafe_lanche_value,
            y1=previous_cafe_lanche_value,
            line=dict(color="blue", width=1.5, dash="dashdot")
        )


        # Identificar o mês anterior ao atual
        current_month = pd.Timestamp.now().month
        previous_month = current_month - 1 if current_month != 1 else 12

        # Buscar os anos para os quais temos dados do mês anterior
        previous_month_years = df_grouped[df_grouped["mes"] == previous_month]["ano"].values

        # Adicionar linhas verticais para cada "Mês/Ano" do mês anterior em todos os anos disponíveis
        for year in previous_month_years:
            month_year_label = f"{meses[previous_month]}/{year}"
            fig.add_shape(
                type="line",
                x0=month_year_label,
                x1=month_year_label,
                y0=0,
                y1=df_grouped["Almoço | Janta"].max(),  # Assumindo que isso cobre o máximo valor do gráfico
                line=dict(color="grey", width=1, dash="dot")
            )



        # Adicionar a área para Almoço | Janta
        fig.add_trace(go.Scatter(
            x=df_grouped["Mês/Ano"],
            y=df_grouped["Almoço | Janta"],
            mode='lines+markers',  # Corrigido
            name="Almoço | Janta",
            fill='tozeroy',
            marker_color=colors[1],
            fillcolor=colors[3]
        ))

        # Adicionar a área para Café | Lanche
        fig.add_trace(go.Scatter(
            x=df_grouped["Mês/Ano"],
            y=df_grouped["Café | Lanche"],
            mode='lines+markers',  # Corrigido
            name="Café | Lanche",
            fill='tozeroy',
            marker_color=colors[-1],
            fillcolor=colors[-3]
        ))
        

        # Ajustar o layout
        fig.update_layout(
            margin=dict(t=50),
            title="-COMPARATIVO MENSAL REFEIÇÕES AO LONGO DO TEMPO",
            xaxis_title="Meses",
            yaxis_title="Quantidade"
        )        

        fig.update_yaxes(
            showline=True,
            linecolor="Grey",
            linewidth=0.5
        )


        # Exibir o gráfico no Streamlit
        c1.plotly_chart(fig, use_container_width=True, automargin=True)





#################### Gráfico Visão Geral Mensal ########################


        # Convertendo a coluna 'data' para o tipo datetime
        df['data'] = pd.to_datetime(df['data'], errors='coerce')
     
        # Determinando o mês e ano atuais
        mes_atual = meses[dt.datetime.now().month]
        ano_atual = dt.datetime.now().year

        # Criação dos selectbox para o mês e ano, com valores padrão sendo o mês e ano atuais
        mes_selecionado = col_filtro_mes.selectbox("Mês", list(meses.values()), index=list(meses.values()).index(mes_atual), key="mes_selecionado")
        ano_selecionado = col_filtro_ano.selectbox("Ano", sorted(df['data'].dt.year.unique(), reverse=True), index=0,  key="ano_selecionado")

        # Convertendo a seleção de mês de volta para o número do mês
        mes_selecionado = [key for key, value in meses.items() if value == mes_selecionado][0]

        # Filtrando o dataframe com base no mês e ano selecionados
        df_mes_filtrado = df[(df['data'].dt.month == mes_selecionado) & (df['data'].dt.year == ano_selecionado)]

        if df_mes_filtrado.empty:
            col5.warning(f"Não há dados disponíveis para {mes_selecionado}/{ano_selecionado}.")
        else:
            # Agregando os dados por dia
            venda_total = df_mes_filtrado.groupby("data")[["total"]].sum().reset_index()
            
            # Adicionando coluna com valores formatados em R$
            venda_total['total_formatado'] = venda_total['total'].apply(lambda x: f"R$ {x:,.2f}".replace('.', '@').replace(',', '.').replace('@', ','))

            # Formatando a coluna 'data' para o padrão dd/mm/aa
            venda_total['data_formatada'] = venda_total['data'].dt.strftime('%d/%m/%y')

            mes_nome = meses[int(mes_selecionado)]
            # Criando o gráfico e usando 'total_formatado' para os valores das barras e 'data_formatada' para o eixo x
            title = f"-EXERCIDO NO MÊS DE {mes_nome.upper()} DE {ano_selecionado}"
            fig_venda_mes = px.bar(venda_total, x="data_formatada", y="total", color_discrete_sequence=[px.colors.diverging.RdBu[1]], title=title, text='total_formatado')
            
            # Configurações de layout e formatação
            fig_venda_mes.update_layout(
                margin=dict(t=50, b=0),
                #yaxis_tickprefix="R$ ",
                yaxis_tickformat=",.0s",
                yaxis_showgrid=True,
                yaxis_title="Faturamento",
                xaxis_title=f"{mes_nome} de {ano_selecionado}" 
            )

            # Configurações adicionais do eixo y
            fig_venda_mes.update_yaxes(
                showline=True,
                linecolor = "Grey",
                linewidth=0.5
            )

            col5.plotly_chart(fig_venda_mes, use_container_width=True)



#################### Gráfico Visão Geral Anual ########################


        # Convertendo a coluna 'data' para o tipo datetime
        df['data'] = pd.to_datetime(df['data'], errors='coerce')

        # Extraindo mês e ano como números
        df['mes_num'] = df['data'].dt.month
        df['ano'] = df['data'].dt.year

        # Usando o ano_selecionado para filtrar o dataframe
        df_filtrado = df[df['ano'] == ano_selecionado]

        # Agregando os dados por mês
        venda_total_mensal = df_filtrado.groupby(['mes_num', 'ano'])[['total']].sum().reset_index()

        # Ordenando pelo mês
        venda_total_mensal = venda_total_mensal.sort_values(by='mes_num')

        # Mapeando os números de volta para os nomes de meses e combinando com o ano
        venda_total_mensal['mes'] = venda_total_mensal['mes_num'].map(meses)
        venda_total_mensal['mes_ano'] = venda_total_mensal['mes'] + '/' + venda_total_mensal['ano'].astype(str)

        # Adicionando uma coluna com os valores formatados em reais
        venda_total_mensal['total_formatado'] = venda_total_mensal['total'].apply(lambda x: f"R$ {x:,.2f}".replace('.', '@').replace(',', '.').replace('@', ','))

        # Criando o gráfico e outras configurações
        title = f"-EXERCIDO NO ANO DE {ano_selecionado}"
        
        fig_venda_mes = px.bar(
            venda_total_mensal, 
            x="mes_ano",
            y="total", 
            color_discrete_sequence=[px.colors.diverging.RdBu[9]], 
            title=title, 
            text='total_formatado'
        )

        # Atualizando layout e formatação dos eixos
        fig_venda_mes.update_layout(
            margin=dict(t=50),
            height=517,
            #yaxis_tickprefix="R$ ",
            yaxis_showgrid=True,
            yaxis_title="Faturamento",
            xaxis_title=f"{ano_selecionado}"  # Atualizando o título do eixo x para "Meses"
        )

        # Configurações adicionais do eixo y
        fig_venda_mes.update_yaxes(
            showline=True,
            linecolor = "Grey",
            linewidth=0.5
        )

        col6.plotly_chart(fig_venda_mes, use_container_width=True)



#################### Gráfico Visão Geral Total por ano ########################


        # Convertendo a coluna 'data' para o tipo datetime
        df['data'] = pd.to_datetime(df['data'], errors='coerce')

        # Extraindo o ano como string
        df['ano'] = df['data'].dt.year.astype(str)

        # Agregando os dados por ano
        venda_total_anual = df.groupby('ano')[['total']].sum().reset_index()

        # Adicionando uma coluna com os valores formatados em reais
        venda_total_anual['total_formatado'] = venda_total_anual['total'].apply(lambda x: f"R$ {x:,.2f}".replace('.', '@').replace(',', '.').replace('@', ','))

        # Criando o gráfico e outras configurações
        title = "-EXERCIDO ANUAL"
        fig_venda_ano = px.bar(venda_total_anual, x="ano", y="total", color_discrete_sequence=[px.colors.diverging.RdBu[1]], title=title, text='total_formatado')

        # Atualizando layout e formatação dos eixos
        fig_venda_ano.update_layout(
            margin=dict(t=50),
            #yaxis_tickprefix="R$ ",
            yaxis_showgrid=True,
            yaxis_title="Faturamento",
            xaxis_title="Anos"  # Atualizando o título do eixo x para "Ano"
        )

        # Configurações adicionais do eixo y
        fig_venda_ano.update_yaxes(
            showline=True,
            linecolor = "Grey",
            linewidth=0.5
        )

        # Considerando que "c3" seja o novo container:
        col3.plotly_chart(fig_venda_ano, use_container_width=True)

#################### Gráfico de Barras Agrupadas por mês ########################


        # Primeiro, garanta que a coluna 'data' é do tipo datetime
        df['data'] = pd.to_datetime(df['data'], errors='coerce')

        # Extraindo ano e mês
        df['ano_mes'] = df['data'].dt.to_period('M')

        # Determinar o mês atual
        current_month = pd.Timestamp.now().to_period('M')

        # Filtrar o DataFrame para excluir o mês atual
        df_filtered = df[df['ano_mes'] != current_month]

        # Agregando os dados por ano e mês
        venda_total_mensal = df_filtered.groupby('ano_mes')[['total']].sum().reset_index()

        # Criando colunas separadas para o mês e o ano
        venda_total_mensal['year'] = venda_total_mensal['ano_mes'].dt.year.astype(str)
        venda_total_mensal['month'] = venda_total_mensal['ano_mes'].dt.month.astype(int)

        venda_total_mensal['month_name'] = venda_total_mensal['month'].map(meses)

        venda_total_mensal['total_formatado'] = venda_total_mensal['total'].apply(lambda x: f"R$ {x:,.2f}".replace('.', '@').replace(',', '.').replace('@', ','))

        # Sequência de cores da paleta RdBu
        colors = px.colors.diverging.RdBu

        # Mapeamento de cada ano para uma cor específica da paleta (como exemplo)
        # Ajuste conforme necessário
        color_map = {
            '2021': px.colors.diverging.RdBu[8],
            '2022': px.colors.diverging.RdBu[7],
            '2023': px.colors.diverging.RdBu[1],
            '2024': px.colors.diverging.RdBu[2]

        }

        # Criando o Gráfico de Barras Agrupadas
        fig_barras = px.bar(
            venda_total_mensal, 
            x="month_name", 
            y="total", 
            color="year",  
            barmode='group',
            labels={"total": "Faturamento", "month_name": "Mês", "year": "Ano"},
            title="-COMPARATIVO ANUAL",
            color_discrete_map=color_map  # Aplicando o mapeamento de cores
        )

        fig_barras.update_layout(
            margin=dict(t=50),
            #yaxis_tickprefix="R$ ",
            yaxis_showgrid=True,
            yaxis_title="Faturamento",
            xaxis_title=""  # Atualizando o título do eixo x para "Meses"
        )

        # Configurações adicionais do eixo y
        fig_barras.update_yaxes(
            showline=True,
            linecolor = "Grey",
            linewidth=0.5
        )        

        # Considerando que "c2" seja o novo container (ajuste o nome do container conforme necessário):
        col4.plotly_chart(fig_barras, use_container_width=True)



    else:
        st.warning('A coluna "data" não foi encontrada na base fornecida.')

#################### Gráfico Qualitativo ########################


incio_data = dt.date(ano_atual, 1, 1)
fim_data = df['data'].max()



data_inicial_quali = col_data_ini_quali.date_input('DATA INÍCIO:', incio_data, None, format="DD/MM/YYYY")
data_fim_quali = col_data_fim_quali.date_input('DATA FIM:', fim_data, None, format="DD/MM/YYYY")

if data_inicial_quali:
    data_inicial_quali = pd.Timestamp(data_inicial_quali)
if data_fim_quali:
    data_fim_quali = pd.Timestamp(data_fim_quali)

if data_inicial_quali or data_fim_quali:

    if 'data' in df.columns:
        
        if data_inicial_quali is not None:
            dia_start2 = str(data_inicial_quali.day).zfill(2)
            mes_start2 = str(data_inicial_quali.month).zfill(2)
            ano_start2 = str(data_inicial_quali.year)

        if data_fim_quali is not None:
            
            dia_end2 = str(data_fim_quali.day).zfill(2)
            mes_end2 = str(data_fim_quali.month).zfill(2)
            ano_end2 = str(data_fim_quali.year)
        
        if data_inicial_quali and data_fim_quali:

            if data_inicial_quali > data_fim_quali:
                st.warning('Data de início é maior que data de término!')
            else:
                date_difference = data_inicial_quali - data_fim_quali
                filtrado_df = df[(df['data'] >= data_inicial_quali) & (df['data'] <= data_fim_quali)] 

                if data_inicial_quali == data_fim_quali:
                    periodo2 = dia_start2 + "/" + mes_start2 + "/" + ano_start2                
                else:
                    periodo2 = dia_start2 + "/" + mes_start2 + "/" + ano_start2 + " A " + dia_end2 + "/" + mes_end2 + "/" + ano_end2
        
        elif data_inicial_quali:
            periodo2 = dia_start2 + "/" + mes_start2 + "/" + ano_start2
            filtrado_df = df[(df['data'] == data_inicial_quali)]
        elif data_fim_quali:
            periodo2 = dia_end2 + "/" + mes_end + "/" + ano_end2
            filtrado_df = df[(df['data'] == data_fim_quali)]

        # 1. Convertendo a coluna 'data' para datetime
        filtrado_df['data'] = pd.to_datetime(filtrado_df['data'], errors='coerce')

        # Verificar valores nulos
        if filtrado_df['data'].isnull().any():
            st.warning('Existem valores inválidos na coluna data!')

        # Agregando os dados
        filtrado_df['Refeições'] = filtrado_df['almoco'] + filtrado_df['janta']
        filtrado_df['Lanches'] = filtrado_df['cafe'] + filtrado_df['lanche']
        df_agregado = filtrado_df.groupby('data').sum()[['Refeições', 'Lanches', 'total']].reset_index()
        df_agregado['data'] = df_agregado['data'].dt.strftime('%d/%m/%y')

        # Definindo cores
        colors = px.colors.diverging.RdBu

        # Criando traços
        bar_refeicoes = go.Bar(
            x=df_agregado['data'],
            y=df_agregado['Refeições'],
            name='Almoço | Janta',
            text=df_agregado['Refeições'],
            textposition='inside',
            marker=dict(color=colors[-4])
        )

        bar_lanches = go.Bar(
            x=df_agregado['data'],
            y=df_agregado['Lanches'],
            name='Café | Lanche',
            text=df_agregado['Lanches'],
            textposition='inside',
            marker=dict(color=colors[-3])
        )


        line_total = go.Scatter(
            x=df_agregado['data'],
            y=df_agregado['total'],
            mode='lines',
            name='Qualitativo',
            line=dict(color='red', shape='linear'),
            yaxis='y2'
        )
        traces = [bar_refeicoes, bar_lanches, line_total]


        # Filtrar a linha "Qualitativo" a partir de 01/09/2023
        mask = (pd.to_datetime(df_agregado['data'], format='%d/%m/%y') >= '2023-09-01')
        qualitativo_post_2023 = df_agregado[mask]

        # Encontrar o valor máximo da linha "Qualitativo" APENAS após 01/09/2023
        max_value_qualitativo_post_2023 = qualitativo_post_2023['total'].max()

        # Obter o valor da coluna 'total' do último dia disponível
        last_day_total_value = df_agregado['total'].iloc[-1]

        # Criando a figura
        fig_quantidade_dia = go.Figure(data=traces)


        # Adicionar a linha horizontal no gráfico baseada no valor máximo pós 01/09/2023
        fig_quantidade_dia.add_shape(
            go.layout.Shape(
                type="line",
                xref="x",
                yref="y2",
                x0=df_agregado['data'].iloc[0],  # Início do eixo x
                x1=df_agregado['data'].iloc[-1],  # Final do eixo x
                y0=max_value_qualitativo_post_2023,
                y1=max_value_qualitativo_post_2023,
                line=dict(
                    color="white",
                    width=1.5,
                    dash="dashdot",
                )
            )
        )
            
        # Adicionar a linha horizontal baseada no valor do último dia disponível
        fig_quantidade_dia.add_shape(
            go.layout.Shape(
                type="line",
                xref="x",
                yref="y2",
                x0=df_agregado['data'].iloc[0],  # Início do eixo x
                x1=df_agregado['data'].iloc[-1],  # Final do eixo x
                y0=last_day_total_value,
                y1=last_day_total_value,
                line=dict(
                    color="white",
                    width=1.5,
                    dash="dashdot",
                )
            )
        )

        # Atualizar layout e exibir gráfico
        fig_quantidade_dia.update_layout(
            margin=dict(t=50,b=0),
            title= "-ANÁLISE QUANTI-QUALITATIVA NO " + periodo2,
            barmode='group',
            xaxis_title='Dias',
            yaxis_title='Quantidade',
            yaxis2=dict(
                overlaying='y',
                side='right',
                showgrid=False,
                title='Total'
            )
        )

        fig_quantidade_dia.update_yaxes(
            showline=True,
            linecolor="Grey",
            linewidth=0.5
        )

        # Exibindo o gráfico
        c4.plotly_chart(fig_quantidade_dia, use_container_width=True, automargin=True)

    else:
        st.warning('A coluna "data" não foi encontrada na base fornecida.')




