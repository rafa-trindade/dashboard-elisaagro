import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
import locale
import calendar

st.set_page_config(layout="wide", page_title="Restaurante Dona Nize", initial_sidebar_state="expanded", page_icon="📊")

st.sidebar.markdown('<h2 style="color: #b2182b; margin-bottom: -40px; text-align: center;">Dona Nize | Elisa Agro</h2>', unsafe_allow_html=True)
st.sidebar.markdown('<h4 style="margin-bottom: -200px; text-align: center;">(Fornecimento Alimentação)</h4>', unsafe_allow_html=True)

st.sidebar.write("____")

col1_side, col2_side = st.sidebar.columns([2,1])

col1_side.markdown('<h5 style="margin-bottom: -25px;">Início Apurado:', unsafe_allow_html=True)
col1_side.markdown('<h5 style="margin-bottom: 15px;">Contrato Vigente:</h5>', unsafe_allow_html=True)

col2_side.markdown('<h5 style="margin-bottom: -25px;">01/01/2021</h5>', unsafe_allow_html=True)
col2_side.markdown('<h5 style="margin-bottom: 15px;">31/08/2026</h5>', unsafe_allow_html=True)

st.sidebar.write("____")

link_url = "https://drive.google.com/drive/folders/1N4V0ZJLiGAHxRrBpVPHv0hqkFJ3CwFsM"
st.sidebar.markdown(f'''
    <h4>
        <a href="{link_url}" target="_blank" style="color: #b2182b; text-decoration: none;" 
           onmouseover="this.style.textDecoration='none';" onmouseout="this.style.textDecoration='none';">
           📂 Drive Fechamentos Diários
        </a>
    </h4>
    <style>
        a:hover {{
            text-decoration: none !important;
        }}
        a:visited {{
            color: #b2182b;
        }}
    </style>
''', unsafe_allow_html=True)


df = pd.read_csv("databaseElisa.csv", sep=";", decimal=",", thousands=".", usecols=['data','fazenda', 'almoco', 'janta', 'cafe','lanche', 'total'], index_col=None) 

# Convertendo a coluna 'data' para o tipo datetime após carregar o dataframe
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
df['data'] = df['data'].dt.date

col1_side.markdown('<h5 style="color: #b2182b;">Última Atualização:</h5>', unsafe_allow_html=True)
col2_side.markdown('<h5 style="color: #b2182b;">' + str(df['data'].max().strftime('%d/%m/%Y'))+ '</h5>', unsafe_allow_html=True)


mes_atual = dt.datetime.today().month
ano_atual = dt.datetime.today().year

mes_inicial_padrão = dt.date(ano_atual, mes_atual, 1)

tab1, tab2, tab3 = st.tabs(["📅 Fechametos Diários", "📊 Visão Mensal", "📊 Visão Anual"])

with tab1:
    col_data_ini, col_data_fim = st.columns(2)
    col1, col2 = st.columns([2,1])
    st.write("_____")
    c3 = st.container()
with tab2:
    col1_filtro1, col2_filtro1 = st.columns(2)  
    c1 = st.container()
    c5 = st.container()
with tab3:
    cfiltro2 = st.container()
    col3, col4 = st.columns([1,3])
    st.write("_____")
    c2 = st.container()
    c4 = st.container()

data_inicial = col_data_ini.date_input('DATA INÍCIO:', mes_inicial_padrão, None, format="DD/MM/YYYY")
data_fim = col_data_fim.date_input('DATA FIM:', None, format="DD/MM/YYYY")



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
                periodo = dia_start + "/" + mes_start + "/" + ano_start + " a " + dia_end + "/" + mes_end + "/" + ano_end
                filtered_df = df[(df['data'] >= data_inicial) & (df['data'] <= data_fim)]
        elif data_inicial:
            periodo = dia_start + "/" + mes_start + "/" + ano_start
            filtered_df = df[(df['data'] == data_inicial)]
        elif data_fim:
            periodo = dia_end + "/" + mes_end + "/" + ano_end
            filtered_df = df[(df['data'] == data_fim)]



        #################### Tabela Demostrativo Período ########################
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
                            fill_color='#b2182b',
                            line_color="lightgrey",
                            font_color="white",
                            align='center',
                            height=25  # Ajusta a altura do cabeçalho
                        ),
                        cells=dict(
                            values=[data_frame.Fazenda, data_frame.Café, data_frame.Almoço, data_frame.Lanche, data_frame.Janta],
                            fill=dict(color=['linen', 'white','#f7f7f7','white','#f7f7f7']),
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
                                    title={ 'text': "-Fechamento de " + periodo, 'y':0.92, 'x':0.0, 'xanchor': 'left', 'yanchor': 'top'},
                                    height=282,
                                    margin=dict(r=10, t=50,b=0)
)
        col1.plotly_chart(fig_tabela_dia, use_container_width=True, automargin=True)


        #################### Gráfico Fazenda Período ########################

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


        

        #################### Gráfico Quantidade Refeições e lanches por dia ########################

        # 1. Certificando-se de que a coluna 'data' é do tipo datetime
        filtered_df['data'] = pd.to_datetime(filtered_df['data'], errors='coerce')

        # Se houver valores nulos após a conversão, isso pode indicar problemas nos dados
        if filtered_df['data'].isnull().any():
            st.warning('Existem valores inválidos na coluna data!')

        # 2. Agregando os dados por data usando o método .sum()
        filtered_df['Refeições'] = filtered_df['almoco'] + filtered_df['janta']
        filtered_df['Lanches'] = filtered_df['cafe'] + filtered_df['lanche']

        # Agregar por data e somar as colunas de interesse
        df_agregado = filtered_df.groupby('data').sum()[['Refeições', 'Lanches', 'total']].reset_index()

        # Transformando a coluna data para o formato desejado
        df_agregado['data'] = df_agregado['data'].dt.strftime('%d/%m/%y')

        # Criando as barras separadamente para 'Refeições' e 'Lanches'
        bar_refeicoes = go.Bar(
            x=df_agregado['data'],
            y=df_agregado['Refeições'],
            name='Refeições',
            text=df_agregado['Refeições'],
            textposition='inside'
        )

        bar_lanches = go.Bar(
            x=df_agregado['data'],
            y=df_agregado['Lanches'],
            name='Lanches',
            text=df_agregado['Lanches'],
            textposition='inside'
        )

        # Criando o trace para a linha que representa o 'total'
        line_total = go.Scatter(
            x=df_agregado['data'],
            y=df_agregado['total'],
            mode='lines',
            name='Qualitativo',
            line=dict(
                color='red',
                shape='linear'  
            ),
            yaxis='y2'  # Associando a linha ao segundo eixo y
        )

        # Verificando a diferença entre a maior e a menor data
        min_date = pd.to_datetime(df_agregado['data'].min(), format='%d/%m/%y')
        max_date = pd.to_datetime(df_agregado['data'].max(), format='%d/%m/%y')
        date_difference = max_date - min_date

        # Se a diferença for maior ou igual a seis meses, incluir a linha total
        if date_difference >= pd.Timedelta(days=5*30):  # Considerando uma média de 30 dias por mês
            traces = [bar_refeicoes, bar_lanches, line_total]
        else:
            traces = [bar_refeicoes, bar_lanches]

        # Sequência de cores da paleta RdBu
        colors = px.colors.diverging.RdBu

        # Traço para Refeições
        bar_refeicoes = go.Bar(
            x=df_agregado['data'],
            y=df_agregado['Refeições'],
            name='Refeições',
            marker=dict(color=colors[7])  # Especificando a cor para Refeições
        )

        # Traço para Lanches
        bar_lanches = go.Bar(
            x=df_agregado['data'],
            y=df_agregado['Lanches'],
            name='Lanches',
            marker=dict(color=colors[8])  # Especificando a cor para Lanches
        )

        # Combine os traços em uma lista
        traces = [bar_refeicoes, bar_lanches] 

        # Combinando as barras e (possivelmente) a linha em uma única figura
        fig_quantidade_dia = go.Figure(data=traces)

        # Ajustes gerais do gráfico
        fig_quantidade_dia.update_layout(
            margin=dict(t=50),
            title='-Quantidade de Refeições e Lanches por Dia',
            barmode='group',
            xaxis_title='Data',
            yaxis_title='Quantidade',
            yaxis2=dict(
                overlaying='y',
                side='right',
                showgrid=False,
                title='Total'
            )
        )

        # Configurações adicionais do eixo y
        fig_quantidade_dia.update_yaxes(
            showline=True,
            linecolor="Grey",
            linewidth=0.5
        )

        c3.plotly_chart(fig_quantidade_dia, use_container_width=True, automargin=True)














        #################### Gráfico Visão Geral Mensal ########################
        # Convertendo a coluna 'data' para o tipo datetime
        df['data'] = pd.to_datetime(df['data'], errors='coerce')


        # #######st.sidebar.markdown('<h3 style="text-align:center; margin-bottom:-30px;">Filtro Visão Geral</h3>', unsafe_allow_html=True)
        
        # Determinando o mês e ano atuais
        mes_atual = meses[dt.datetime.now().month]
        ano_atual = dt.datetime.now().year

        # Criação dos selectbox para o mês e ano, com valores padrão sendo o mês e ano atuais
        mes_selecionado = col1_filtro1.selectbox("Mês", list(meses.values()), index=list(meses.values()).index(mes_atual))
        ano_selecionado = col2_filtro1.selectbox("Ano", sorted(df['data'].dt.year.unique(), reverse=True), index=0)

        # Convertendo a seleção de mês de volta para o número do mês
        mes_selecionado = [key for key, value in meses.items() if value == mes_selecionado][0]

        # Filtrando o dataframe com base no mês e ano selecionados
        df_mes_filtrado = df[(df['data'].dt.month == mes_selecionado) & (df['data'].dt.year == ano_selecionado)]


        if df_mes_filtrado.empty:
            c1.warning(f"Não há dados disponíveis para {mes_selecionado}/{ano_selecionado}.")
        else:
            # Agregando os dados por dia
            venda_total = df_mes_filtrado.groupby("data")[["total"]].sum().reset_index()
            
            # Adicionando coluna com valores formatados em R$
            venda_total['total_formatado'] = venda_total['total'].apply(lambda x: f"R$ {x:,.2f}".replace('.', '@').replace(',', '.').replace('@', ','))

            # Formatando a coluna 'data' para o padrão dd/mm/aa
            venda_total['data_formatada'] = venda_total['data'].dt.strftime('%d/%m/%y')


            mes_nome = meses[int(mes_selecionado)]
            # Criando o gráfico e usando 'total_formatado' para os valores das barras e 'data_formatada' para o eixo x
            title = f"-Exercido no mês de {mes_nome} de {ano_selecionado}"
            fig_venda_mes = px.bar(venda_total, x="data_formatada", y="total", color_discrete_sequence=[px.colors.diverging.RdBu[1]], title=title, text='total_formatado')
            
            # Configurações de layout e formatação
            fig_venda_mes.update_layout(
                margin=dict(t=50, b=0),
                #yaxis_tickprefix="R$ ",
                yaxis_tickformat=",.0s",
                yaxis_showgrid=True,
                yaxis_title="Faturamento",
                xaxis_title="Dias" 
            )

            # Configurações adicionais do eixo y
            fig_venda_mes.update_yaxes(
                showline=True,
                linecolor = "Grey",
                linewidth=0.5
            )

            c1.plotly_chart(fig_venda_mes, use_container_width=True)



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
        title = f"-Exercido no ano de {ano_selecionado}"
        fig_venda_mes = px.bar(venda_total_mensal, x="mes_ano", y="total", color_discrete_sequence=[px.colors.diverging.RdBu[9]], title=title, text='total_formatado')

        # Atualizando layout e formatação dos eixos
        fig_venda_mes.update_layout(
            margin=dict(t=50),
            #yaxis_tickprefix="R$ ",
            yaxis_showgrid=True,
            yaxis_title="Faturamento",
            xaxis_title="Meses"  # Atualizando o título do eixo x para "Meses"
        )

        # Configurações adicionais do eixo y
        fig_venda_mes.update_yaxes(
            showline=True,
            linecolor = "Grey",
            linewidth=0.5
        )

        c5.plotly_chart(fig_venda_mes, use_container_width=True)



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
        title = "-Exercido Anual"
        fig_venda_ano = px.bar(venda_total_anual, x="ano", y="total", color_discrete_sequence=[px.colors.diverging.RdBu[1]], title=title, text='total_formatado')

        # Atualizando layout e formatação dos eixos
        fig_venda_ano.update_layout(
            margin=dict(t=50,b=0),
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
            '2021': px.colors.diverging.RdBu[1],
            '2022': px.colors.diverging.RdBu[7],
            '2023': px.colors.diverging.RdBu[8]
        }

        # Criando o Gráfico de Barras Agrupadas
        fig_barras = px.bar(
            venda_total_mensal, 
            x="month_name", 
            y="total", 
            color="year",  
            barmode='group',
            labels={"total": "Faturamento", "month_name": "Mês", "year": "Ano"},
            title="-Comparativo Anual",
            color_discrete_map=color_map  # Aplicando o mapeamento de cores
        )

        fig_barras.update_layout(
            margin=dict(t=50,b=0),
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
        c2.plotly_chart(fig_barras, use_container_width=True)



        #################### Gráfico Comparativo Faturamento/Quantidade ########################

        # Convertendo a coluna 'data' para o tipo datetime
        df['data'] = pd.to_datetime(df['data'], errors='coerce')

        # Extraindo o ano como string
        df['ano'] = df['data'].dt.year.astype(str)

        # Agregando os dados por ano e somando as colunas de interesse
        df['Refeições'] = df['almoco'] + df['janta']
        df['Lanches'] = df['cafe'] + df['lanche']

        venda_total_anual = df.groupby('ano')[['total', 'Refeições', 'Lanches']].sum().reset_index()


        colors = px.colors.diverging.RdBu

        # Criando as barras para 'Total', 'Refeições' e 'Lanches'
        bar_total = go.Bar(
            x=venda_total_anual['ano'],
            y=venda_total_anual['total'],
            name='Faturamento',
            text=venda_total_anual['total'].apply(lambda x: f"R$ {x:,.2f}".replace('.', '@').replace(',', '.').replace('@', ',')),
            textposition='inside',
            marker=dict(color=colors[1])
        )

        bar_refeicoes = go.Bar(
            x=venda_total_anual['ano'],
            y=venda_total_anual['Refeições'],
            name='Refeições',
            yaxis='y2',
            marker=dict(color=colors[7])
        )

        bar_lanches = go.Bar(
            x=venda_total_anual['ano'],
            y=venda_total_anual['Lanches'],
            name='Lanches',
            yaxis='y2',
            marker=dict(color=colors[8])
        )

        # Combinando as barras em uma única figura
        fig_venda_ano = go.Figure(data=[bar_total, bar_refeicoes, bar_lanches])

        # Atualizando layout e formatação dos eixos
        fig_venda_ano.update_layout(
            title="-Relação Qualitativa",
            margin=dict(t=50,b=0),
            yaxis_showgrid=True,
            yaxis_title="Faturamento",
            xaxis_title="Anos",
            barmode='group',  # Para agrupar as barras por ano
            yaxis2=dict(
                overlaying='y',
                side='right',
                showgrid=False,
                title='Quantidade'
            )
        )

        # Configurações adicionais do eixo y
        fig_venda_ano.update_yaxes(
            showline=True,
            linecolor="Grey",
            linewidth=0.5
        )

        # Considerando que "col4" seja o novo container:
        col4.plotly_chart(fig_venda_ano, use_container_width=True)

    else:

        st.warning('A coluna "data" não foi encontrada na base fornecida.')
