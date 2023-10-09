import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt

st.set_page_config(layout="wide", page_title="Restaurante Dona Nize", initial_sidebar_state="expanded", page_icon="📊")

df = pd.read_csv("databaseElisa.csv", sep=";", decimal=",", thousands=".", usecols=['data','fazenda', 'almoco', 'janta', 'cafe','lanche', 'vlrCafe', 'vlrAlmoco', 'total'], index_col=None) 

# Convertendo a coluna 'data' para o tipo datetime após carregar o dataframe
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
df['data'] = df['data'].dt.date

st.sidebar.markdown('<h2 style="color: #b2182b; margin-bottom: -40px; text-align: center;">Dona Nize | Elisa Agro</h2>', unsafe_allow_html=True)
st.sidebar.markdown('<h4 style="margin-bottom: -200px; text-align: center;">(Fornecimento Alimentação)</h4>', unsafe_allow_html=True)

st.sidebar.write("____")

col1_side, col2_side = st.sidebar.columns([2,1])

col1_side.markdown('<h5 style="margin-bottom: -25px;">Início Apurado:', unsafe_allow_html=True)
col2_side.markdown('<h5 style="text-align: end; margin-bottom: -25px;">01/01/2021</h5>', unsafe_allow_html=True)

col1_side.markdown('<h5 style="margin-bottom: 15px; color: #b2182b;">Última Atualização:</h5>', unsafe_allow_html=True)
col2_side.markdown('<h5 style="margin-bottom: 15px; text-align: end; color: #b2182b;">' + str(df['data'].max().strftime('%d/%m/%Y'))+ '</h5>', unsafe_allow_html=True)


col1_side.markdown('<h5 style="margin-bottom: -25px;">Contrato Vigente:</h5>', unsafe_allow_html=True)
col2_side.markdown('<h5 style="text-align: end; margin-bottom: -25px;">31/08/2026</h5>', unsafe_allow_html=True)

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
        <a href="{link_url}" target="_blank" style="text-align: center; color: #b2182b; text-decoration: none;" 
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



tab1, tab2, tab3 = st.tabs(["📅 Fechametos Diários", "📊 Visão Mensal", "📊 Visão Anual"])

with tab1:
    col_data_ini, col_data_fim = st.columns(2)
    col1, col2 = st.columns([2,1])
    c1 = st.container()
with tab2:
    col_filtro_mes, col_filtro_ano = st.columns(2)  
    c2 = st.container()
    c3 = st.container()
with tab3:
    col3, col4 = st.columns([1,3])



#################### Tabela Demostrativo Período ########################


mes_atual = dt.datetime.today().month
ano_atual = dt.datetime.today().year

mes_inicial_padrão = dt.date(ano_atual, mes_atual, 1)

data_inicial = col_data_ini.date_input('DATA INÍCIO:', mes_inicial_padrão, None, format="DD/MM/YYYY")
data_fim = col_data_fim.date_input('DATA FIM:', None, format="DD/MM/YYYY")
date_difference = pd.Timedelta(0)

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
                date_difference = data_fim - data_inicial
                periodo = dia_start + "/" + mes_start + "/" + ano_start + " A " + dia_end + "/" + mes_end + "/" + ano_end
                filtered_df = df[(df['data'] >= data_inicial) & (df['data'] <= data_fim)]     
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


        
#################### Gráfico Qualitativo ########################

        # 1. Convertendo a coluna 'data' para datetime
        filtered_df['data'] = pd.to_datetime(filtered_df['data'], errors='coerce')

        # Verificar valores nulos
        if filtered_df['data'].isnull().any():
            st.warning('Existem valores inválidos na coluna data!')

        # Agregando os dados
        filtered_df['Refeições'] = filtered_df['almoco'] + filtered_df['janta']
        filtered_df['Lanches'] = filtered_df['cafe'] + filtered_df['lanche']
        df_agregado = filtered_df.groupby('data').sum()[['Refeições', 'Lanches', 'total']].reset_index()
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
            marker=dict(color=colors[7])
        )

        bar_lanches = go.Bar(
            x=df_agregado['data'],
            y=df_agregado['Lanches'],
            name='Café | Lanche',
            text=df_agregado['Lanches'],
            textposition='inside',
            marker=dict(color=colors[8])
        )

        # Condicionando a criação do traço da linha "Qualitativo"
        if date_difference >= pd.Timedelta(days=6*30):  # Aproximando 6 meses
            line_total = go.Scatter(
                x=df_agregado['data'],
                y=df_agregado['total'],
                mode='lines',
                name='Qualitativo',
                line=dict(color='red', shape='linear'),
                yaxis='y2'
            )
            traces = [bar_refeicoes, bar_lanches, line_total]
        else:
            traces = [bar_refeicoes, bar_lanches]

        # Construindo a figura
        fig_quantidade_dia = go.Figure(data=traces)
        fig_quantidade_dia.update_layout(
            margin=dict(t=50),
            title= "-TOTAL REFEIÇÕES DE " + periodo + " (representação quanti-qualitativa a partir de 6 meses)",
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
        c1.plotly_chart(fig_quantidade_dia, use_container_width=True, automargin=True)



#################### Gráfico Visão Geral Mensal ########################


        # Convertendo a coluna 'data' para o tipo datetime
        df['data'] = pd.to_datetime(df['data'], errors='coerce')

        # Dicionário para mapear número do mês ao nome em português com a primeira letra maiúscula
        meses = {
            1: "JANEIRO",
            2: "FEVEREIRO",
            3: "MARÇO",
            4: "ABRIL",
            5: "MAIO",
            6: "JUNHO",
            7: "JULHO",
            8: "AGOSTO",
            9: "SETEMBRO",
            10: "OUTUBRO",
            11: "NOVEMBRO",
            12: "DEZEMBRO"
        }        
        # Determinando o mês e ano atuais
        mes_atual = meses[dt.datetime.now().month]
        ano_atual = dt.datetime.now().year

        # Criação dos selectbox para o mês e ano, com valores padrão sendo o mês e ano atuais
        mes_selecionado = col_filtro_mes.selectbox("Mês", list(meses.values()), index=list(meses.values()).index(mes_atual))
        ano_selecionado = col_filtro_ano.selectbox("Ano", sorted(df['data'].dt.year.unique(), reverse=True), index=0)

        # Convertendo a seleção de mês de volta para o número do mês
        mes_selecionado = [key for key, value in meses.items() if value == mes_selecionado][0]

        # Filtrando o dataframe com base no mês e ano selecionados
        df_mes_filtrado = df[(df['data'].dt.month == mes_selecionado) & (df['data'].dt.year == ano_selecionado)]

        if df_mes_filtrado.empty:
            c2.warning(f"Não há dados disponíveis para {mes_selecionado}/{ano_selecionado}.")
        else:
            # Agregando os dados por dia
            venda_total = df_mes_filtrado.groupby("data")[["total"]].sum().reset_index()
            
            # Adicionando coluna com valores formatados em R$
            venda_total['total_formatado'] = venda_total['total'].apply(lambda x: f"R$ {x:,.2f}".replace('.', '@').replace(',', '.').replace('@', ','))

            # Formatando a coluna 'data' para o padrão dd/mm/aa
            venda_total['data_formatada'] = venda_total['data'].dt.strftime('%d/%m/%y')

            mes_nome = meses[int(mes_selecionado)]
            # Criando o gráfico e usando 'total_formatado' para os valores das barras e 'data_formatada' para o eixo x
            title = f"-EXERCIDO NO MÊS DE {mes_nome} DE {ano_selecionado}"
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

            c2.plotly_chart(fig_venda_mes, use_container_width=True)



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

        c3.plotly_chart(fig_venda_mes, use_container_width=True)



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
            '2023': px.colors.diverging.RdBu[1]
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
