import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
from datetime import datetime
import locale
import calendar

#try:
#    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
#except locale.Error:
#    st.warning("pt_BR locale não está instalado no sistema. Mostrando nomes de meses em inglês.")


st.set_page_config(layout="wide", page_title="Restaurante Dona Nize", initial_sidebar_state="expanded", page_icon="🧊")

st.sidebar.markdown('<h2 style="text-align: center; text-decoration: underline;">Restaurante Dona Nize | Elisa Agro</h2>', unsafe_allow_html=True)


df = pd.read_csv("databaseElisa.csv", sep=";", decimal=",", thousands=".",
                 usecols=['data','fazenda', 'almoco', 'janta', 'cafe','lanche', 'total'],
                 index_col=None
                 ) 

st.markdown("""
        <style>
               .block-container {
                    padding-top: 20px;
                }
        </style>
            
            
        """, unsafe_allow_html=True)

df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
df['data'] = df['data'].dt.date

mes_atual = dt.datetime.today().month
ano_atual = dt.datetime.today().year

default_start_date = dt.date(ano_atual, mes_atual, 1)

st.sidebar.markdown('<h3 style="text-align:center; margin-bottom:-30px;">Filtro Demostrativo</h3>', unsafe_allow_html=True)


start_date = st.sidebar.date_input('DATA INÍCIO:', default_start_date, None, format="DD/MM/YYYY")
end_date = st.sidebar.date_input('DATA FIM:', None, format="DD/MM/YYYY")

st.sidebar.write("____")

if start_date:
    start_date = pd.Timestamp(start_date)
if end_date:
    end_date = pd.Timestamp(end_date)

col1, col2 = st.columns([2,1])
c1 = st.container()
col3, col4 = st.columns([2,1])

if start_date or end_date:

    if 'data' in df.columns:
        
        if start_date is not None:
            dia_start = str(start_date.day)
            mes_start = str(start_date.month)
            ano_start = str(start_date.year)

        if end_date is not None:
            
            dia_end = str(end_date.day)
            mes_end = str(end_date.month)
            ano_end = str(end_date.year)
        
        if start_date and end_date:

            if start_date > end_date:
                st.warning('Data de início é maior que data de término!')
            else:
                periodo = dia_start + "/" + mes_start + "/" + ano_start + " - " + dia_end + "/" + mes_end + "/" + ano_end
                filtered_df = df[(df['data'] >= start_date) & (df['data'] <= end_date)]
        elif start_date:
            periodo = dia_start + "/" + mes_start + "/" + ano_start
            filtered_df = df[(df['data'] == start_date)]
        elif end_date:
            periodo = dia_end + "/" + mes_end + "/" + ano_end
            filtered_df = df[(df['data'] == end_date)]

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
                    
        #del(lista_fazenda[7])
        #del(lista_almoco[7])
        #del(lista_janta[7])
        #del(lista_cafe[7])
        #del(lista_lanche[7])  

        data = {
            "Fazenda": lista_fazenda,
            "Café": lista_cafe,
            "Almoço": lista_almoco,
            "Lanche": lista_lanche,
            "Janta": lista_janta
        }

        data_frame = pd.DataFrame(data)

        sums = {
            "Fazenda": "<b>TOTAL</b>",
            "Café": "<b>" + str('{0:,}'.format(int(data_frame["Café"].sum())).replace(',','.')) + "</b>",
            "Almoço": "<b>" + str('{0:,}'.format(int(data_frame["Almoço"].sum())).replace(',','.')) + "</b>",
            "Lanche": "<b>" + str('{0:,}'.format(int(data_frame["Lanche"].sum())).replace(',','.')) + "</b>",
            "Janta": "<b>" + str('{0:,}'.format(int(data_frame["Janta"].sum())).replace(',','.')) + "</b>"
                }

        data_frame = data_frame.append(sums, ignore_index=True)

        fig = go.Figure(data=[go.Table(
                    header=dict(
                        values=list(data_frame.columns),
                        fill_color='firebrick',
                        line_color="lightgrey",
                        font_color="white",
                        align='center',
                        height=25  # Ajusta a altura do cabeçalho
                    ),
                    cells=dict(
                        values=[data_frame.Fazenda, data_frame.Café, data_frame.Almoço, data_frame.Lanche, data_frame.Janta],
                        fill=dict(color=['linen', 'white','whitesmoke','white','whitesmoke']),
                        line_color="lightgrey",
                        font_color="black",
                        align='center',
                        height=25  # Ajusta a altura das células
                    ))
                ])

        fig.update_layout(title={ 'text': "Demostrativo: " + periodo, 'y':0.76, 'x':0.0, 'xanchor': 'left', 'yanchor': 'top'})
        fig.update_layout(height = 460, margin=dict(r=10,t=140))
        col1.plotly_chart(fig, use_container_width=True, automargin=True)

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
        fig_venda_fazenda.update_layout(width=600, height=460, margin=dict(l=10, b=50, t=130))
        col2.plotly_chart(fig_venda_fazenda, use_container_width=True)

        #################### Gráfico Visão Geral Mensal ########################
        # Convertendo a coluna 'data' para o tipo datetime
        df['data'] = pd.to_datetime(df['data'], errors='coerce')

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

        st.sidebar.markdown('<h3 style="text-align:center; margin-bottom:-30px;">Filtro Visão Geral</h3>', unsafe_allow_html=True)
        
        # Determinando o mês e ano atuais
        mes_atual = meses[dt.datetime.now().month]
        ano_atual = dt.datetime.now().year

        # Criação dos selectbox para o mês e ano, com valores padrão sendo o mês e ano atuais
        selected_mes = st.sidebar.selectbox("Mês", list(meses.values()), index=list(meses.values()).index(mes_atual))
        selected_ano = st.sidebar.selectbox("Ano", sorted(df['data'].dt.year.unique(), reverse=True), index=0)

        # Convertendo a seleção de mês de volta para o número do mês
        mes_selecionado = [key for key, value in meses.items() if value == selected_mes][0]

        # Filtrando o dataframe com base no mês e ano selecionados
        df_mes_filtrado = df[(df['data'].dt.month == mes_selecionado) & (df['data'].dt.year == selected_ano)]


        if df_mes_filtrado.empty:
            st.warning(f"Não há dados disponíveis para {selected_mes}/{selected_ano}.")
        else:
            # Agregando os dados por dia
            venda_total = df_mes_filtrado.groupby("data")[["total"]].sum().reset_index()
            
            # Adicionando coluna com valores formatados em R$
            venda_total['total_formatado'] = venda_total['total'].apply(lambda x: f"R$ {x:,.2f}".replace('.', '@').replace(',', '.').replace('@', ','))

            # Formatando a coluna 'data' para o padrão dd/mm/aa
            venda_total['data_formatada'] = venda_total['data'].dt.strftime('%d/%m/%y')

            # Criando o gráfico e usando 'total_formatado' para os valores das barras e 'data_formatada' para o eixo x
            title = f"Visão Diária: {selected_mes}/{selected_ano}"
            fig_venda_mes = px.bar(venda_total, x="data_formatada", y="total", color_discrete_sequence=[px.colors.diverging.RdBu[0]], title=title, text='total_formatado')
            
            # Configurações de layout e formatação
            fig_venda_mes.update_layout(
                margin=dict(t=50),
                yaxis_tickprefix="R$ ",
                yaxis_showgrid=True,
                yaxis_title="Faturamento",
                xaxis_title="Dias"
            )

            # Formatação do eixo y
            fig_venda_mes.update_yaxes(tickprefix="R$", tickformat=',.2f', showline=True, linewidth=1, linecolor='black', mirror=True)

            c1.plotly_chart(fig_venda_mes, use_container_width=True)
         
        #################### Gráfico Visão Geral Anual ########################

        # Convertendo a coluna 'data' para o tipo datetime
        df['data'] = pd.to_datetime(df['data'], errors='coerce')

        # Extraindo mês e ano como números
        df['mes_num'] = df['data'].dt.month
        df['ano'] = df['data'].dt.year

        # Usando o selected_ano para filtrar o dataframe
        df_filtrado = df[df['ano'] == selected_ano]

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
        title = f"Visão Mensal: {selected_ano}"
        fig_venda_mes = px.bar(venda_total_mensal, x="mes_ano", y="total", color_discrete_sequence=[px.colors.diverging.RdBu[1]], title=title, text='total_formatado')

        # Atualizando layout e formatação dos eixos
        fig_venda_mes.update_layout(
            margin=dict(t=50),
            yaxis_tickprefix="R$ ",
            yaxis_showgrid=True,
            yaxis_title="Faturamento",
            xaxis_title="Meses"  # Atualizando o título do eixo x
        )

        # Configurações adicionais do eixo y
        fig_venda_mes.update_yaxes(
            tickformat=',.2f',
            separatethousands=True,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True
        )

        col3.plotly_chart(fig_venda_mes, use_container_width=True)

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
        title = "Visão Geral Anual"
        fig_venda_ano = px.bar(venda_total_anual, x="ano", y="total", color_discrete_sequence=[px.colors.diverging.RdGy_r[1]], title=title, text='total_formatado')

        # Atualizando layout e formatação dos eixos
        fig_venda_ano.update_layout(
            margin=dict(t=50),
            yaxis_tickprefix="R$ ",
            yaxis_showgrid=True,
            yaxis_title="Faturamento",
            xaxis_title="Anos"  # Atualizando o título do eixo x para "Ano"
        )

        # Configurações adicionais do eixo y
        fig_venda_ano.update_yaxes(
            tickformat=',.2f',
            separatethousands=True,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True
        )

        # Considerando que "c3" seja o novo container:
        col4.plotly_chart(fig_venda_ano, use_container_width=True)

    else:

        st.warning('A coluna "data" não foi encontrada na base fornecida.')
